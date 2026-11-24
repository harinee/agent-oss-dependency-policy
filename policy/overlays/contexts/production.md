# Production Context

> Stricter levels and change discipline for production systems.

## When to use this

Apply to production and customer-facing systems. Use one context overlay at a time. Requires a foundational file. On top of `oss-selection-strict` the level shifts below change nothing; on top of the baseline they raise three rules.

## Level shifts

| Rule | Level here |
|---|---|
| AGE-2 | ASK |
| SRC-2 | BLOCK |
| LIC-1 | ASK |

## Instructions

- **PROD-1 (ASK)** Pre-release versions: alpha, beta, release candidates, snapshots. *Why:* not intended for production by their own authors.
- **PROD-2 (NOTE)** Make each dependency change revertible on its own: one change, one commit or PR. *Why:* rollback is the fastest response to a bad release.
- **PROD-3 (NOTE)** For a major-version upgrade, link the changelog and name the breaking changes that affect this project. *Why:* reviewers need it to judge the change.
