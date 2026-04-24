#!/usr/bin/env python3
"""
Direct Confluence-to-local sync. No LLM intermediation.

Reads config.yaml for space/site info, .env for credentials.
Downloads pages under configured folder mappings and writes as markdown.

Uses v2 API to list pages in space + get page bodies,
and v1 API to resolve parent page titles (v2 hides some folder pages).

Usage:
    python3 scripts/sync-confluence.py          # interactive (confirms overwrites)
    python3 scripts/sync-confluence.py --yes    # auto-approve overwrites
"""

import base64
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent

# Confluence folder → local path mapping
# Keys are matched against the page's ancestor path (case-insensitive)
FOLDER_MAPPINGS = {
    "agents":          ROOT / ".claude" / "agents",
    "rules":           ROOT / ".claude" / "rules",
    "context/projects": ROOT / "context" / "project",
    "personas":        ROOT / "personas",
    "specs":           ROOT / "specs",
    "workflows":       ROOT / "workflows",
}


def load_env():
    """Load .env file into environment."""
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())


def load_config():
    """Load config.yaml and return confluence settings."""
    config_path = ROOT / "config.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)
    return config.get("confluence", {})


def get_auth():
    """Return (email, token) from environment."""
    email = os.environ.get("CONFLUENCE_USER_EMAIL", "")
    token = os.environ.get("CONFLUENCE_API_TOKEN", "")
    return email, token


def make_auth_header(email, token):
    """Create Basic auth header."""
    creds = base64.b64encode(f"{email}:{token}".encode()).decode()
    return {"Authorization": f"Basic {creds}", "Accept": "application/json"}


# ---------------------------------------------------------------------------
# Confluence API
# ---------------------------------------------------------------------------

def api_get(base_url, path, headers, params=None):
    """GET request to a Confluence API endpoint."""
    import urllib.request
    import urllib.parse
    import urllib.error

    url = f"{base_url}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"  ERROR {e.code}: {path} — {body[:200]}")
        return None


def get_space_id(site_url, space_key, headers):
    """Resolve space_key to numeric space_id and homepage_id."""
    data = api_get(site_url, "/wiki/api/v2/spaces", headers, {"keys": space_key, "limit": 1})
    if data and data.get("results"):
        space = data["results"][0]
        return str(space["id"]), str(space.get("homepageId", ""))
    return None, None


def get_all_pages_in_space(site_url, space_id, headers):
    """List ALL pages in a space via v2 API (handles pagination)."""
    all_pages = []
    params = {"limit": 250, "sort": "title"}
    path = f"/wiki/api/v2/spaces/{space_id}/pages"
    while True:
        data = api_get(site_url, path, headers, params)
        if not data:
            break
        all_pages.extend(data.get("results", []))
        next_link = data.get("_links", {}).get("next")
        if not next_link:
            break
        path = next_link.replace(site_url, "") if site_url in next_link else next_link
        params = None
    return all_pages


def get_page_ancestors_v1(site_url, page_id, headers):
    """Get a page's ancestor chain via v1 API (works for folder pages that v2 hides)."""
    data = api_get(site_url, f"/wiki/rest/api/content/{page_id}", headers, {"expand": "ancestors"})
    if data and "ancestors" in data:
        return [a["title"] for a in data["ancestors"]]
    return None


def get_page_title_v1(site_url, page_id, headers):
    """Get a single page's title via v1 API."""
    data = api_get(site_url, f"/wiki/rest/api/content/{page_id}", headers)
    if data:
        return data.get("title")
    return None


def get_page_body(site_url, page_id, headers):
    """Get page body in storage format via v2 API."""
    data = api_get(site_url, f"/wiki/api/v2/pages/{page_id}", headers, {"body-format": "storage"})
    if data and "body" in data:
        return data["body"].get("storage", {}).get("value", "")
    return None


def build_page_paths(pages, homepage_id, site_url, headers):
    """
    Build full path for each page by resolving ancestors via v1 API.
    Returns dict: page_id -> list of path parts (excluding homepage).
    """
    # Cache for parent title lookups
    title_cache = {}

    def resolve_parent_title(parent_id):
        if parent_id not in title_cache:
            title_cache[parent_id] = get_page_title_v1(site_url, parent_id, headers)
        return title_cache[parent_id]

    by_id = {str(p["id"]): p for p in pages}
    known_ids = set(by_id.keys())
    paths = {}

    for page in pages:
        page_id = str(page["id"])
        if page_id == str(homepage_id):
            continue

        parent_id = str(page.get("parentId", ""))

        # If parent is homepage, page is top-level
        if parent_id == str(homepage_id):
            paths[page_id] = [page["title"]]
            continue

        # If parent is in our known pages, build path from it
        if parent_id in known_ids:
            # Recursively get parent path (but this parent might also have unknown parents)
            pass  # Fall through to v1 approach

        # Use v1 API to get full ancestor chain
        ancestors = get_page_ancestors_v1(site_url, page["id"], headers)
        if ancestors is not None:
            # ancestors includes homepage as first element, skip it
            # Build path: ancestors (minus homepage) + page title
            path_parts = [a for a in ancestors[1:]] + [page["title"]]  # skip homepage
            paths[page_id] = path_parts
        else:
            # Fallback: just page title
            paths[page_id] = [page["title"]]

    return paths


def match_to_folder_mapping(path_parts):
    """
    Given a page's path (list of titles from homepage),
    check if it falls under one of the FOLDER_MAPPINGS.
    Returns (folder_key, local_base, relative_subfolder_parts) or None.
    """
    for folder_key, local_base in FOLDER_MAPPINGS.items():
        folder_parts = folder_key.split("/")
        depth = len(folder_parts)

        if len(path_parts) <= depth:
            continue

        # Check if the first N parts match the folder key (case-insensitive)
        page_prefix = [p.lower().strip() for p in path_parts[:depth]]
        folder_prefix = [f.lower().strip() for f in folder_parts]

        if page_prefix == folder_prefix:
            subfolder = path_parts[depth:-1]  # intermediate folders between mapping root and page
            return folder_key, local_base, subfolder

    return None


# ---------------------------------------------------------------------------
# Content conversion
# ---------------------------------------------------------------------------

def storage_to_markdown(html_content):
    """Convert Confluence storage format (HTML) to markdown using pandoc."""
    try:
        result = subprocess.run(
            ["pandoc", "--from=html", "--to=markdown", "--wrap=none"],
            input=html_content,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # Fallback: basic HTML tag stripping
    text = re.sub(r"<br\s*/?>", "\n", html_content)
    text = re.sub(r"</?p>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def title_to_filename(title):
    """Convert page title to a safe filename."""
    name = title.strip().lower()
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s]+", "-", name)
    return name + ".md"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    auto_approve = "--yes" in sys.argv

    load_env()
    conf = load_config()
    site_url = conf.get("site_url", "").rstrip("/")
    space_key = conf.get("space_key", "")

    if not space_key:
        print("ERROR: space_key is blank in config.yaml. Update it before syncing.")
        sys.exit(1)

    email, token = get_auth()
    if not email or not token:
        print("ERROR: Set CONFLUENCE_USER_EMAIL and CONFLUENCE_API_TOKEN in .env")
        print("  Generate a token at: https://id.atlassian.com/manage-profile/security/api-tokens")
        sys.exit(1)

    headers = make_auth_header(email, token)

    # Resolve space
    print(f"Resolving space '{space_key}' on {site_url}...")
    space_id, homepage_id = get_space_id(site_url, space_key, headers)
    if not space_id:
        print(f"ERROR: Could not find space '{space_key}'. Check your space_key and credentials.")
        sys.exit(1)
    print(f"  Space ID: {space_id}, Homepage ID: {homepage_id}")

    # Get ALL pages in space
    print(f"\nFetching all pages in space...")
    all_pages = get_all_pages_in_space(site_url, space_id, headers)
    print(f"  Found {len(all_pages)} total page(s)")

    # Build full paths using v1 ancestor API
    print(f"  Resolving page paths...")
    page_paths = build_page_paths(all_pages, homepage_id, site_url, headers)
    by_id = {str(p["id"]): p for p in all_pages}

    # Show discovered tree
    print(f"\n  Page tree:")
    for pid, parts in sorted(page_paths.items(), key=lambda x: "/".join(x[1]).lower()):
        print(f"    /{'/'.join(parts)}")

    # Match pages to folder mappings
    all_syncs = []

    for page_id, path_parts in page_paths.items():
        match = match_to_folder_mapping(path_parts)
        if not match:
            continue

        folder_key, local_base, subfolder = match
        page = by_id[page_id]
        title = page["title"]

        if subfolder:
            local_dir = local_base / Path(*subfolder)
        else:
            local_dir = local_base
        local_path = local_dir / title_to_filename(title)
        all_syncs.append((local_path, page_id, title, folder_key))

    if not all_syncs:
        print("\nNo pages matched the configured folder mappings.")
        print(f"  Expected folders: {list(FOLDER_MAPPINGS.keys())}")
        return

    # Sort by folder then title
    all_syncs.sort(key=lambda x: (x[3], x[2]))

    # Categorize new vs overwrite
    new_files = [(p, pid, t, f) for p, pid, t, f in all_syncs if not p.exists()]
    overwrite_files = [(p, pid, t, f) for p, pid, t, f in all_syncs if p.exists()]

    print(f"\n{'='*60}")
    print(f"Sync Summary")
    print(f"{'='*60}")

    if new_files:
        print(f"\nNew files ({len(new_files)}):")
        for p, _, t, f in new_files:
            print(f"  + {p.relative_to(ROOT)}")

    if overwrite_files:
        print(f"\nOverwrite ({len(overwrite_files)}):")
        for p, _, t, f in overwrite_files:
            print(f"  ~ {p.relative_to(ROOT)}")

    if not new_files and not overwrite_files:
        print("\nNothing to sync.")
        return

    # Confirm
    if not auto_approve:
        response = input(f"\nProceed with sync? [y/N] ").strip().lower()
        if response not in ("y", "yes"):
            print("Aborted.")
            return

    # Download and write
    print(f"\nSyncing {len(all_syncs)} page(s)...")
    success = 0
    errors = 0

    for local_path, page_id, title, _ in all_syncs:
        body = get_page_body(site_url, page_id, headers)
        if body is None:
            print(f"  FAIL: {title} — could not fetch content")
            errors += 1
            continue

        markdown = storage_to_markdown(body)

        local_path.parent.mkdir(parents=True, exist_ok=True)
        local_path.write_text(markdown + "\n", encoding="utf-8")
        print(f"  OK: {local_path.relative_to(ROOT)}")
        success += 1

    print(f"\nDone. {success} synced, {errors} errors.")


if __name__ == "__main__":
    main()
