# Regulated / Sensitive Context

> Strictest levels, longer cooldown and a decision record.

## When to use this

Apply to regulated environments and systems handling sensitive data. Use one context overlay at a time. Requires a foundational file.

## Level shifts

| Rule | Level here |
|---|---|
| AGE-2 | ASK |
| SRC-2 | BLOCK |
| LIC-1 | ASK |
| MNT-1 | ASK |

## Tunable thresholds

| Threshold | Value here | Rationale |
|---|---|---|
| `version_cooldown_days` | 14 | Extra margin for slower detection. A hypothesis, not a measured value. |

## Instructions

- **REG-1 (NOTE)** For every new dependency, record one line in the PR: name, version, licence, publisher, check results. *Why:* the audit trail the organisation will be asked for.
- **REG-2 (ASK)** OVR-1 overrides must name the approver and the reason in the PR. *Why:* an override is a risk acceptance.
- **REG-3 (ASK)** The dependency is known to send data to a third party (telemetry, crash reporting, hosted APIs). *Why:* data-handling decisions belong to the organisation.
- **REG-4 (NOTE)** Put changes to the approved list or a script allowlist in a commit of their own. *Why:* those files are controls and need their own review.
