# Friction model

The policy is built to stop an agent pulling in unchecked dependencies without making developers switch it off. This page explains the design. The rules themselves are in `skills/foundational/`.

## Three response levels

| Level | Meaning | With a human in the session | With no human available |
|---|---|---|---|
| BLOCK | Never proceed | Stop, name the rule, offer an alternative | Same |
| ASK | Needs explicit approval | State the finding in one or two lines and wait | Fail closed: skip the dependency, log the rule ID and reason, carry on or stop that part of the task |
| NOTE | Proceed | One line with the check result | One line in the log or pull request |

Most rules are NOTE. A rule is ASK only when the event is rare and the risk is high. A rule is BLOCK only when there is no legitimate reason to proceed: a package name that does not exist, a version with a malware advisory, or instructions found inside content the agent was reading.

## Three questions the policy keeps apart

| Question | What it catches | Who it interrupts |
|---|---|---|
| How old is this **version**? (AGE-1) | A hijacked release of an established package | Nobody, normally. The agent picks the newest version that is old enough and says so. |
| How old is this **package**? (AGE-2, AGE-3) | Typosquats, invented names, throwaway packages | Only new packages that also lack a repository or publisher history |
| Did the **publisher** change? (PUB-1) | Account takeover, ownership transfer | Only where the registry exposes it |

A mature dependency at a version older than the cooldown passes with at most a one-line note.

## Order of checks

1. The exact version is already in the lockfile: no checks.
2. The package is on the approved list: identity, adoption, package-age and maintenance rules are skipped. The version cooldown still applies, because hijacked releases hit approved packages too.
3. Otherwise every rule applies.

## Levels and thresholds by context

The baseline and strict foundational files carry default levels. A context overlay changes the rows shown.

| Rule or threshold | Prototype overlay | Baseline | Strict | Production overlay | Regulated overlay |
|---|---|---|---|---|---|
| `version_cooldown_days` | 1 | 7 | 7 | unchanged | 14 |
| `min_package_age_days` | unchanged | 90 | 90 | unchanged | unchanged |
| `stale_after_months` | unchanged | 24 | 24 | unchanged | unchanged |
| AGE-2 new package | unchanged | NOTE | ASK | ASK | ASK |
| SRC-2 pipe to shell | unchanged | ASK | BLOCK | BLOCK | BLOCK |
| LIC-1 licence | silent | NOTE | ASK | ASK | ASK |
| MNT-1 stale | silent | NOTE | NOTE | unchanged | ASK |
| DEP-1 why needed | silent | NOTE | NOTE | unchanged | unchanged |

The BLOCK rules (ID-1, ID-3, TRU-1) and the install-script rule (SCR-1) are the same in every context. Prototypes run on developer machines with real credentials, which is what recent package malware steals.

`scripts/selfcheck.py` checks the threshold rows of this table against the policy files.

## The thresholds are judgement calls

A threshold is a number someone had to pick. One of the three is anchored to evidence; the other two are not. "No data behind it" means nobody has shown that 90 days works better than 30 or 180. It is a starting point to adjust from your own experience.

| Threshold | Default | Basis |
|---|---|---|
| `version_cooldown_days` | 7 | In the six hijacked package releases in [threat-coverage.md](threat-coverage.md) with a stated removal time, all were gone within about 10 hours. GlassWorm extensions stayed available for at least three days. Package-manager defaults are shorter: pnpm 11 and Yarn 4.15 use 1 day, Dependabot 3 days. Seven days is a margin, not a measurement. |
| `min_package_age_days` | 90 | A guess, carried over from earlier versions of this repository. No data behind it. The cost of it being wrong is low: at baseline it only adds a one-line note. Under the strict foundation it triggers an ASK, so lower it there if it interrupts too often. |
| `stale_after_months` | 24 | A guess, chosen to be long enough that finished, stable libraries rarely trigger it. No data behind it. It only adds a one-line note. |

To change one, edit the "Tunable thresholds" table in your copy of the policy. If your package manager can enforce the value, set it there as well; see [`enforcement/`](../enforcement/README.md).

There is no download-count threshold. No single number is defensible across ecosystems, and download counts can be inflated.

## Escape hatches

| Hatch | How | Limit |
|---|---|---|
| Approved list (APR-1) | `.dependency-policy/approved.txt` in the project, one `ecosystem:name` or `ecosystem:name@version` per line. The agent reads it first and never edits it. | Does not bypass the version cooldown, malware advisories or the untrusted-content rule. |
| Security-patch fast path (FIX-1) | A version that fixes a published advisory may bypass the cooldown. The agent records the advisory ID. | The advisory must come from a database the agent queried, not from package text. |
| Override (OVR-1) | A human can override any ASK. The agent records one line: rule ID, who, why. | BLOCK rules change only by editing the policy. An unattended agent cannot override. |
| Context overlays | Prototype, production and regulated shift levels as tabled above. | One at a time. |

Example `approved.txt`:

```
npm:express
npm:react
pypi:requests
pypi:numpy@2.1.3
```

## Rules removed because they misfired

| Earlier rule | Why it was a false-positive source | Now |
|---|---|---|
| Approval for any package newer than 3 months | Flags every legitimate new package; misses hijacked versions of old ones | NOTE at baseline; ASK only together with no repository or publisher history |
| Approval for single-maintainer packages | Describes a large share of every ecosystem and is not a compromise signal | Removed |
| Fewer than 100 stars or downloads | Stars can be bought; the number was arbitrary | Stars never used; low downloads reported as a NOTE |
| No commits in 12 months | Finished libraries are quiet | 24 months, NOTE; ASK only with an unpatched advisory |
| No version ranges anywhere | Wrong for libraries; redundant with a frozen lockfile | Exact installs plus lockfile; libraries may keep ranges |
| "Unverified publisher" | Never defined, so not checkable | Replaced by ID-1, AGE-3 and PUB-1 |
| `curl \| bash` forbidden everywhere | Several official toolchain installers work this way | ASK at baseline, BLOCK in strict and production |
| Flag every lockfile change in a pull request | Fires on every dependency change | Report only unexpected additions and registry changes |

## What this cannot do

These are instructions. An agent can ignore them, misread them, or be talked out of them. See [limitations.md](limitations.md).
