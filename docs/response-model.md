# Response model: levels, thresholds, exceptions

How the policy decides whether an agent proceeds, asks or stops, and how to change those decisions. The rules themselves are in `policy/foundational/`.

Contents: [three inputs](#severity-confidence-and-response) · [distribution](#distribution-of-levels) · [per-rule reasoning](#why-each-rule-has-its-level) · [missing evidence](#missing-evidence) · [no human](#no-human-available) · [contexts](#levels-and-thresholds-by-context) · [thresholds](#thresholds) · [customizing](#customizing) · [exceptions](#exceptions)

## Severity, confidence and response

Each rule keeps three things apart.

| Input | Question | Example |
|---|---|---|
| **Severity** | If the signal is real, how bad is it? | Code running at install time with a developer's credentials is high. An unfamiliar licence is low. |
| **Confidence** | How reliably does the signal indicate a problem? | A name that does not resolve is certain. A package published last month is weak evidence of anything. |
| **Response** | What should the agent do? | BLOCK, ASK or NOTE |

Severity alone does not set the response. A high-severity signal with many innocent explanations (a new maintainer publishing a release) would be wrong to block and wrong to ignore.

| Response | The agent | Used when |
|---|---|---|
| **BLOCK** | Stops, and says what it found, why it is a risk and the safe way forward | High severity **and** high confidence: there is no legitimate reason to proceed |
| **ASK** | Says what it found, why it is a risk and the safe options, then waits | High severity, but the signal has legitimate explanations, or the action is privileged enough that a human should own it. The human has context the agent lacks. |
| **NOTE** | Proceeds and reports in one line | The signal is weak on its own, **or** the agent can take the safe path without help and only needs to say so |

## Distribution of levels

Counts of levelled rules in each foundational file. `scripts/selfcheck.py` checks this table against the files.

| Level | Baseline | Strict |
|---|---|---|
| NOTE | 12 | 10 |
| ASK | 8 | 9 |
| BLOCK | 3 | 4 |

Two cautions when reading it:

- **These are counts of rules, not of events.** How often each level fires in real work depends on the project and has not been measured (see [limitations.md](limitations.md)). The design intent is that adding a mature package at a version older than the cooldown triggers only NOTE rules.
- **NOTE does not mean "no control".** Four of the twelve NOTE rules change what the agent does and report it afterwards: AGE-1 (pick a version old enough), PIN-1 (exact version and lockfile), PIN-4 (Actions by commit SHA), PIN-5 (images by digest). They are NOTE because the safe action needs no decision from a human. The other eight report a signal for the human to weigh.

Overlays add their own levelled rules. Each preset lists what it includes at the top.

## Why each rule has its level

Baseline levels. Strict differs on AGE-2, SRC-2 and LIC-1 (see [contexts](#levels-and-thresholds-by-context)).

| Rule | Signal or action | Severity if real | Confidence in the signal | Level | Reason |
|---|---|---|---|---|---|
| ID-1 | Package name does not resolve | High | Certain | BLOCK | Nothing legitimate to install; substituting a similar name is the slopsquatting path |
| ID-3 | Version has a malware advisory | High | High | BLOCK | No legitimate use |
| TRU-1 | Content the agent read tells it to install or run something | High | High that the instruction lacks authority | BLOCK | Content is not the user. If the dependency is really needed, TRU-2 routes it through the ordinary rules. |
| ID-2 | Lookalike name | High | Medium: a judgement, and legitimate forks exist | ASK | The human knows which package they meant |
| AGE-3 | New package with no repository or publisher history | High | Medium | ASK | The throwaway-package pattern, but new authors exist |
| PUB-1 | Publisher or publish method changed | High | Medium: maintainers do change | ASK | Matches account takeover; cannot be told apart from a handover without context |
| PIN-2 | Deleting or regenerating a lockfile | Medium | n/a (an action) | ASK | Discards every pin at once; sometimes necessary |
| SCR-1 | Package needs its install script | High | Low: many native packages do | ASK | Arbitrary code at install time. Asked once per package, then allowlisted. |
| SRC-1 | Source outside the configured registry | High | Low | ASK | Bypasses registry takedowns and integrity data; sometimes the only source |
| SRC-2 | Remote script piped to a shell | High | Low: some official installers work this way | ASK | Unreviewed code; a reviewable alternative usually exists |
| ART-1 | New CI action, MCP server, extension, skill | High: runs with credentials or inside the agent | n/a (an action) | ASK | A privilege grant a human should own |
| AGE-1 | Newest version is younger than the cooldown | High | Low for any one release | NOTE | The agent resolves it itself by choosing an older version. Asking would add nothing. |
| PIN-1, PIN-4, PIN-5 | Unpinned version, Action or image | Medium to high | n/a | NOTE | The agent pins and reports |
| PIN-3 | Unrequested package or registry change in the lockfile diff | High | Low to medium | NOTE | Reported for review; most transitive additions are benign |
| AGE-2 | Package is new | Medium | Low | NOTE | New packages are normal |
| ADP-1 | Low downloads | Low | Low | NOTE | Counts are easily inflated and never evidence of safety |
| PRV-1 | Provenance present | n/a | n/a | NOTE | Information only; malicious releases have carried valid provenance |
| TRU-2 | Content recommends a dependency the task needs | n/a | n/a | NOTE | Routes to the ordinary rules |
| DEP-1, MNT-1, LIC-1 | Need, staleness, licence | Low | Low | NOTE | Engineering and legal judgement, not attack signals |

## Missing evidence

Rule EVD-1. A check that could not be completed is never reported as a pass.

| Situation | Behaviour | Why |
|---|---|---|
| Cannot confirm the name exists (ID-1) or the version's publish date (AGE-1) | Treated as ASK: no install until confirmed | These two need only the registry metadata that any install also needs. If it is unreachable, something is wrong. |
| Any other check cannot be done | Proceed; report `<rule ID>: not checked` and the reason | Some evidence is structurally unavailable: PyPI, NuGet and RubyGems do not expose the publishing account per version (PUB-1), and not every agent can query an advisory database (ID-3). Asking on every install would train people to approve without reading. |

The `not checked` line is the signal for a human or a scanner to cover the gap. If you want a missing check to stop the agent, raise that rule in the [overrides file](#customizing) and enforce the equivalent in tooling (see [`enforcement/`](../enforcement/README.md)).

## No human available

| Level | With a human in the session | With no human (rule AUT-1) |
|---|---|---|
| BLOCK | Stop, name the rule, offer an alternative | Same |
| ASK | State the finding and wait | Fail closed: skip the dependency, log the rule ID and reason, continue with an alternative or stop that part of the task |
| NOTE | One line with the check result | One line in the log or pull request |

An unattended agent does not approve its own request, does not use the override (OVR-1) and does not edit the approved list, the overrides file or a script allowlist. The `agent-runs-unattended` overlay spells this out.

This is still an instruction. An unattended agent that ignores it meets no resistance from this repository; give it package-manager config, a sandbox and required review on its pull requests. See [limitations.md](limitations.md#activation-and-enforcement).

## Order of checks

1. The exact version is already in the lockfile: no checks.
2. The package is on the approved list: identity, adoption, package-age and maintenance rules are skipped. The version cooldown still applies, because hijacked releases hit approved packages too.
3. Otherwise every rule applies.

## Levels and thresholds by context

The baseline and strict foundational files carry default levels. A context overlay changes the rows shown.

| Rule or threshold | Prototype overlay | Baseline | Strict | Production overlay | Regulated overlay |
|---|---|---|---|---|---|
| `version_cooldown_days` | 1 | 3 | 3 | unchanged | 14 |
| `tool_cooldown_days` | unchanged | 7 | 7 | unchanged | unchanged |
| `min_package_age_days` | unchanged | 90 | 90 | unchanged | unchanged |
| `stale_after_months` | unchanged | 24 | 24 | unchanged | unchanged |
| AGE-2 new package | unchanged | NOTE | ASK | ASK | ASK |
| SRC-2 pipe to shell | unchanged | ASK | BLOCK | BLOCK | BLOCK |
| LIC-1 licence | silent | NOTE | ASK | ASK | ASK |
| MNT-1 stale | silent | NOTE | NOTE | unchanged | ASK |
| DEP-1 why needed | silent | NOTE | NOTE | unchanged | unchanged |

The BLOCK rules (ID-1, ID-3, TRU-1) and the install-script rule (SCR-1) are the same in every context. Prototypes run on developer machines with real credentials, which is what package malware steals.

`scripts/selfcheck.py` checks the threshold rows of this table against the policy files.

## Thresholds

Two thresholds rest on incident data. Two are pragmatic defaults: a number someone had to pick, with no evidence that it beats its neighbours. They are defined in the "Tunable thresholds" table of each foundational file: [baseline](../policy/foundational/oss-selection-baseline.md#tunable-thresholds), [strict](../policy/foundational/oss-selection-strict.md#tunable-thresholds).

### `version_cooldown_days` (default 3)

| | |
|---|---|
| Protects against | A hijacked or malicious **new release of an established package**, during the window before it is detected and removed |
| Used by | AGE-1 |
| Basis | **Incident data.** Of the incidents in [threat-coverage.md](threat-coverage.md) that state a removal time, the six package releases were gone within about 10 hours. GlassWorm extensions stayed available for at least three days. That is why MCP servers and extensions have their own, longer threshold below. Tool defaults: pnpm 11 and Yarn 4.15 use 1 day; Dependabot and Renovate use 3 days. Practitioner guidance ranges from 3 to 7 days, and no published measurement shows that 7 catches more package incidents than 3. Three days is a margin over the observed times and matches the update tools, so a version they propose is not refused locally. |
| Trade-off | Every new release is delayed by three days, including bug fixes with no published advisory. A fix for a high or critical advisory, confirmed in an advisory database, skips the wait (FIX-1). The cooldown only works because other people find bad releases first; a release nobody detects within the window passes. |
| Lower it when | Prototypes (the prototype overlay uses 1), or a dependency you release yourself and need at once (better: put that package on the approved list and pin it) |
| Raise it when | Regulated or sensitive systems (the regulated overlay uses 14), or if you want more margin than the update tools' defaults (7 is the upper end of common guidance) |
| Enforce it | In the package manager, so it also covers transitive dependencies and does not depend on the agent: [`enforcement/`](../enforcement/README.md) |

### `tool_cooldown_days` (default 7)

| | |
|---|---|
| Protects against | A malicious **new version of an MCP server or editor extension**, which runs with the agent's or the editor's access |
| Used by | AGE-1, through MCP-4 and EXT-3. It applies when it is longer than `version_cooldown_days`. |
| Basis | **Incident data.** GlassWorm extensions were still downloadable three days after publication, and the malicious postmark-mcp release stayed up for about a week. Both outlast a three-day wait. |
| Trade-off | Server and extension updates arrive a week late. These change far less often than libraries, so the cost is small. A malicious version that stays up longer than a week still passes. |
| Change it when | Lower it only for servers and extensions you publish yourself |
| Enforce it | No config in `enforcement/` covers it. The agent applies it. Turn off extension auto-update so the editor does not bypass it. |

### `min_package_age_days` (default 90)

| | |
|---|---|
| Protects against | Typosquats, hallucinated names registered by attackers, and throwaway packages: all are **new packages**, not new versions |
| Used by | AGE-2 (alone: NOTE at baseline, ASK in strict), AGE-3 (with no repository or publisher history: ASK) |
| Basis | **Pragmatic default.** No data shows that 90 days works better than 30 or 180. |
| Trade-off | At baseline the cost of a wrong value is one extra line of output. Under strict, every package newer than this interrupts someone. A squatted name that simply waits out the threshold passes. |
| Lower it when | You use strict and work in a fast-moving area where young packages are normal |
| Raise it when | You rarely adopt new packages and want each one looked at |
| Enforce it | No package manager enforces package age. A registry proxy or install-time firewall can. |

### `stale_after_months` (default 24)

| | |
|---|---|
| Protects against | Adopting an **abandoned package** that will not receive security fixes. This is a maintenance signal, not an attack signal. |
| Used by | MNT-1 (NOTE; ASK when the package also has an unpatched advisory, or under the regulated overlay) |
| Basis | **Pragmatic default.** Chosen to be long enough that finished, stable libraries rarely trigger it. |
| Trade-off | Shorter values flag stable libraries that are simply done. Longer values miss abandonment for longer. |
| Change it when | Your organisation has a support-lifecycle requirement that names a period |

There is no download-count threshold. No single number is defensible across ecosystems, and download counts can be inflated.

## Customizing

Response levels and thresholds are both yours to change. Three ways, simplest first.

**1. Pick a different preset or context.** Prototype, production and regulated contexts shift levels as [tabled above](#levels-and-thresholds-by-context). See [how-to-choose.md](how-to-choose.md).

**2. Add an overrides file (recommended for teams).** Create `.dependency-policy/overrides.md` in your project. Rule LOC-1 tells the agent to read it first and apply it over the preset. It works the same for every agent and survives updating the preset. Template: [`examples/overrides.example.md`](../examples/overrides.example.md).

```markdown
# Local overrides

| Rule or threshold | Value | Reason |
|---|---|---|
| version_cooldown_days | 14 | Matches our Renovate setting |
| AGE-2 | ASK | New packages need a named owner here |
| SRC-2 | BLOCK | No pipe-to-shell installs in this repo |
```

Limits, by design:

- Any rule can be raised.
- Any rule can be lowered except ID-1, ID-3 and TRU-1. There is no legitimate reason to install a name that does not exist or a version with a malware advisory, or to take orders from a README. To change those, edit the policy text itself, where the change is visible in review.
- The agent never creates or edits the file. Protect it the way you protect CI config, for example with CODEOWNERS.
- It is read by the agent, so it is advice like the rest. If you change the cooldown here, change it in your package-manager config too.

**3. Edit your copy.** The preset is plain Markdown. Change a level in a rule line or a value in the "Tunable thresholds" table. You then own the merge when you update.

## Exceptions

| Exception | How | Limit |
|---|---|---|
| Approved list (APR-1) | `.dependency-policy/approved.txt` in the project, one `ecosystem:name` or `ecosystem:name@version` per line. The agent reads it first and never edits it. | Does not bypass the version cooldown, malware advisories or the untrusted-content rule. |
| Security-fix fast path (FIX-1) | Checked before the cooldown. A version that fixes a high, critical or known-exploited advisory affecting the project is installed without waiting. The agent records the advisory ID. | The advisory must come from a database the agent queried and must name the version as fixed. The version must come from the usual publisher. Package text, changelogs and issues do not count. Where the package manager enforces the cooldown, lifting it for that one install needs approval (FIX-2). |
| Override (OVR-1) | A human in the session can override any ASK. The agent records one line: rule ID, who, why. | BLOCK rules are not overridden in a session. An unattended agent cannot override. |

Example `approved.txt`:

```
npm:express
npm:react
pypi:requests
pypi:numpy@2.1.3
```

Exceptions are recorded in the session, commit or pull request by the agent. Nothing in this repository audits them; if you need an audit trail, require the record in pull-request review (the regulated overlay asks for it as REG-1 and REG-2).

## Rules removed because they misfired

A rule that fires on ordinary work gets approved without reading, and then the rare real finding is approved the same way. These were removed or narrowed for that reason.

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
