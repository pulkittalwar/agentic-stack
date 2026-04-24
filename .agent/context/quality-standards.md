# Output Quality Standards

The bar that analytical output must meet before it is considered ready
for review, regardless of engagement type. These are firm-generic
consulting standards and apply equally to BCG engagements, personal
projects, and any analytical work where rigor matters.

Firm-specific review gates (e.g. BCG's "ready for client = partner has
reviewed and approved") layer on top in `adapters/<firm>/context/firm/`
and apply only within that firm's adapter.

## The Four Standing Demands

### 1. Lead with the "so what"
Pyramid principle: the governing thought — the recommendation, the decision
needed, the insight — appears first. Supporting detail follows. Never bury
the answer. A reader should be able to skim the first paragraph of any
document and know what you are asking them to believe or do.

Failure mode: output that reports observations without stating what they
mean or what to do about them. "Prices went up 12%" is an observation;
"We are losing price-sensitive shoppers to competitor X and should respond
before Q3" is a so-what.

### 2. MECE analytical completeness
Every framework, issue tree, options list, and analytical bucket must be
**M**utually **E**xclusive (no overlap between categories) and **C**ollectively
**E**xhaustive (covers all possibilities). This is a test, not a stylistic
preference — run it at every level of decomposition.

Failure mode: a three-branch analysis that accidentally omits a fourth
branch, or two branches that share content. Both produce wrong
conclusions.

### 3. Evidenced claims, explicit assumptions
Every numerical claim carries its source. Every non-evidenced claim is
labeled as an assumption. There is no middle category. A reader should
never have to guess whether a number is measured, estimated, or assumed.

Failure mode: "the market is growing at 8%" with no source — reader has
to decide whether to trust it, and usually decides wrong.

### 4. Sensitivity transparency
For any conclusion that depends on inputs the reader cannot fully verify,
name the two or three inputs whose variation would most change the
conclusion. State the range and what the conclusion would be outside it.

Failure mode: a recommendation that looks robust in the deck but collapses
if a single input moves 15%. If the reader cannot see that in the
analysis, the analysis has understated its own fragility.

## Ready-for-Review Checklist

Before sending any analytical output for review:
- The first paragraph states the so-what, not the observation
- Every framework passes a MECE test at every level
- Every number has a source or is marked as an assumption
- Top 2–3 sensitivity drivers are named with ranges
- A reader with no prior context can read the first page and decide
  whether to keep reading
