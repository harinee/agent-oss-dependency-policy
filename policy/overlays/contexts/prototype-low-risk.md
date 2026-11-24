# Prototype / Low Risk Context

> Lower friction for prototypes and experiments. The BLOCK rules and install-script rules do not relax.

## When to use this

Apply to proofs of concept, experiments and throwaway work. Use one context overlay at a time. Requires a foundational file.

Prototypes run on developer machines with real credentials, which is what recent package malware steals. That is why this overlay relaxes reporting, not the rules about what runs.

## Level shifts

| Rule | Level here |
|---|---|
| DEP-1 | silent |
| MNT-1 | silent |
| LIC-1 | silent |

## Tunable thresholds

| Threshold | Value here | Rationale |
|---|---|---|
| `version_cooldown_days` | 1 | Matches the shortest package-manager defaults. Covers releases pulled within hours. |

## Instructions

- **PROTO-1 (NOTE)** Keep a short list of dependencies that triggered AGE-2, AGE-3 or any ASK. Hand it over if the prototype moves toward production. *Why:* those decisions need a second look under stricter levels.
