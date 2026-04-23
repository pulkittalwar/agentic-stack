---
name: test-writer
version: 2026-04-23
description: Use whenever tests need to be written, added to, or audited — not just to hit coverage numbers but to catch real regressions. Produces tests at the right pyramid layer (unit / integration / e2e), each with assertions that would fail if the behavior regressed. Also audits existing test suites for coverage gaps in critical paths, over-mocking, and tests coupled to implementation details. Triggers on "write tests for this", "is the test coverage enough", "add regression tests", "audit the tests", or when a PR lacks tests for new behavior.
triggers: ["write tests for this", "test coverage", "add regression tests", "audit the tests", "is this tested enough"]
tools: [recall, git, bash]
sources:
  superpowers: pr-review-toolkit:pr-test-analyzer (behavioral coverage over line coverage)
  gstack: qa (framework detection + browser-based e2e)
preconditions: ["code to test exists, or a spec describing behavior to test exists"]
constraints:
  - every test has at least one assertion
  - behavioral coverage prioritized over line coverage
  - no tests coupled to implementation details (refactor-resilient)
  - tests at the right pyramid layer — unit-heavy, integration-moderate, e2e-thin
category: sdlc
---

# Test Writer

## Before acting — recall first

Run: `python3 .agent/tools/recall.py "tests for <feature or module>"`

Present surfaced lessons in a `Consulted lessons before acting:` block. If any lesson would be violated (e.g. a prior incident taught "never mock X"), STOP and explain.

## What a test-writer is

The test-writer's job is not to raise coverage; it is to buy confidence that future changes will not break current behavior. Every test answers a specific question: "would this test fail if the bug came back?" A test that cannot answer that question has no value — it passes because the code exists, not because the code works. Coverage tools tell you which lines were executed; tests tell you which behaviors are pinned. Those are different questions.

## Destinations — what a completed test set achieves

- **Every test has an assertion that would fail on regression.** Deletion test: remove the implementation; run the test; does it fail? If not, the test is decorative.
- **Tests are at the right pyramid layer.** Unit-heavy (many, fast, isolated). Integration-moderate (fewer, test real boundaries). E2E-thin (a handful, test critical happy paths end-to-end). Inverting the pyramid makes test suites slow and flaky.
- **Behavioral coverage, not line coverage.** Edge cases (empty, malformed, partial, concurrent, duplicate, out-of-order) are enumerated and tested per the architecture's edge-case matrix.
- **DAMP test names.** Descriptive And Meaningful Phrases. `test_count_unique_words_ignores_case` beats `test_counter_1`.
- **Refactor-resilient.** Tests exercise the public contract — inputs and observable outputs. They do not assert on private method calls, internal ordering, or data structures a refactor might legitimately change.
- **Explicit fixtures.** Test data is either inline-obvious or in a named fixture file. Magic numbers in assertions get a comment naming their provenance.

## Fences — what the test set must not contain

- **Assertion-less tests.** `pytest` will pass any function that does not throw. A test without `assert` is a decoy.
- **Framework tests.** Tests that verify the language, stdlib, or framework work as documented are noise. Test your code, not theirs.
- **Over-mocking.** Mocking everything but the code under test means the test passes even when the real integration fails. Mock only at architectural seams, not at every function boundary.
- **Implementation coupling.** Asserting "the private helper was called with these args in this order" breaks on refactor. Assert on input → output, not internals.
- **Single-layer over-investment.** 50 unit tests and zero integration tests means nothing is wired correctly. Or: 30 e2e tests and zero unit tests means the suite takes an hour.
- **Coverage-chasing tests.** Tests that exist to hit a line and nothing else. Line coverage without behavioral coverage is theater.

## The test pyramid (pr-review-toolkit + general best practice)

Thin → moderate → heavy, top to bottom:

- **E2E (few).** End-to-end through the real stack — browser click to database row. Slow, flaky, expensive. Reserve for critical happy paths; one or two per major feature.
- **Integration (moderate).** Test real architectural seams — two modules wired together, a real database, a real HTTP layer. Slower than unit, more confidence than unit. One per seam in the architecture.
- **Unit (many).** Test single functions / classes in isolation. Fast (ms), deterministic, abundant. Cover every edge case.

## The pr-test-analyzer coverage lens

For every new code path, ask:

1. **Would a regression here cause a user-visible failure?** If yes, test it.
2. **Is this an error-handling path that could fail silently?** Test the error path explicitly.
3. **Is this a boundary condition?** Empty, maximum, minimum, duplicate, malformed, concurrent. Each gets a test if it can actually occur.
4. **Is this a business-logic branch?** Every `if` that affects output deserves a test per branch.
5. **Could refactoring break this test?** If yes, the test is coupled — rewrite against the contract.

## Framework detection (from gstack /qa)

Before writing tests, detect the framework. Check for `jest.config.*`, `vitest.config.*`, `playwright.config.*`, `.rspec`, `pytest.ini`, `pyproject.toml` (with `[tool.pytest]`), `phpunit.xml`. Standard defaults by runtime:

| Runtime | Unit / integration | E2E |
|---|---|---|
| Python | pytest + pytest-cov | playwright (if web) |
| Node.js | vitest + @testing-library | playwright |
| Next.js | vitest + @testing-library/react | playwright |
| Go | stdlib testing + testify | — |
| Rust | cargo test + mockall | — |

If no framework exists, propose one (default: the table's first column for the runtime) and wait for user confirmation before writing tests against a framework that is not installed.

## Examples

**Good test (emulate):**

```python
def test_reconcile_emits_gap_csv_when_netsuite_deal_missing():
    """Deal in SFDC but absent from NetSuite period -> gap CSV row."""
    sfdc_deals = [Deal(id="D1", close_date="2026-06-30", amount=1000, touch="direct")]
    netsuite_period = NetSuitePeriod(period="2026-Q2", rows={})  # empty on purpose

    result = reconcile(sfdc_deals, netsuite_period)

    assert len(result.reconciled) == 0
    assert len(result.gaps) == 1
    assert result.gaps[0].deal_id == "D1"
    assert result.gaps[0].reason == "no_netsuite_match"
```

Why it is good: named for behavior (not `test_1`), inputs are minimal and explicit, assertions check observable outputs (not private helpers), would fail loudly if the gap-emission logic regressed.

**Bad test (avoid):**

```python
def test_reconciler():
    r = Reconciler()
    r._parse_internal = MagicMock()
    r._normalize_internal = MagicMock()
    r._join_internal = MagicMock()
    r.run()
    assert r._parse_internal.called
    assert r._normalize_internal.called
    assert r._join_internal.called
```

Fails on: vague name, over-mocking hides real failures, asserts on private methods (implementation coupling), no observable-output assertions, would not fail if the reconciler returned the wrong result.

**Failure to learn from:**

A test suite had 98% line coverage and green-on-every-CI for six months. A refactor split one function into two; the refactor passed all tests. In production, the two halves were wired in the wrong order and the reconciliation silently produced wrong numbers for three days. **Lesson:** high line coverage combined with no integration tests at the seam means the test suite is pinning structure, not behavior. Add one integration test per architectural seam, even if unit tests fully cover each side.

## Self-check before declaring tests done

For every test written, run the **deletion test**: temporarily delete (or comment out) one line of the implementation the test is supposed to cover. Re-run the test. If it still passes, the test is not actually testing that line — rewrite or add assertions until deletion breaks it. Undo the deletion when done.

## Save + handoff

Tests land alongside the code (e.g. `tests/test_*.py` mirroring `src/`), per the repo convention. After writing, run the full suite once and report: count passed, count failed, coverage delta if measured. Hand to `code-reviewer` for PR review.

## Self-rewrite hook

After every 5 test-writing sessions, or the first time high-line-coverage tests fail to catch a production regression, read the last 5 test-writer entries from episodic memory. Add fences for newly-discovered failure modes (e.g. "always add integration test at X-type seam"). Commit: `skill-update: test-writer, <one-line reason>`.
