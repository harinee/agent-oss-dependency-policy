# Limitations

Read this before relying on the policy. None of these is a reason not to use it; each is a reason not to use it alone.

## Activation and enforcement

What makes the policy apply, and what stands behind it if the agent does not comply.

| Layer | What decides whether it applies | Technically enforced? |
|---|---|---|
| Preset in an always-on file (`AGENTS.md`, `CLAUDE.md`, a rules folder) | The agent product loads it at session start. No model decision is involved in loading. | No. Following each rule is up to the model. |
| Preset as an Agent Skill | The model decides whether the skill's description matches the task | No. Loading and following are both up to the model. |
| `.dependency-policy/approved.txt` and `overrides.md` | The agent reads them because the policy says to | No |
| Package-manager config from [`enforcement/`](../enforcement/README.md) | The package manager, on every install, whoever runs it | **Yes**, for the version cooldown, install scripts and exact versions, on tool versions that support the setting |
| `check_pins.py` in CI | CI, on every pull request | **Yes**, for unpinned Actions, images without digests, missing lockfiles and unexpected registries, if the check is required to merge |
| Agent permission settings, sandboxing, branch protection | Your agent product and your repository host | **Yes**, and outside this repository |

Only four rule families have an enforced counterpart here: AGE-1, SCR-1 and the PIN and SRC-1 checks. Everything else (identity, lookalikes, publisher change, untrusted content, privileged artifacts, the unattended rules) exists only as text the model is asked to follow.

**Unattended agents.** With no human in the session, an ASK becomes "skip and log" (AUT-1) and the agent is told not to approve itself or edit the approved list or overrides. Nothing verifies that it did so. For unattended runs, treat the policy as the least reliable layer: enforce the cooldown and script settings in the package manager, run the agent in a sandbox with narrowly scoped credentials, and require human review of its pull requests.

**Exceptions.** The approved list, the security-patch fast path (FIX-1), the override (OVR-1) and the overrides file are honoured and recorded by the agent itself. There is no independent audit of them. A review step is what makes an exception accountable.

## It is advice, not a control

- **An agent can ignore it.** The files are text in the agent's context. Nothing stops an agent from skipping a rule, misreading it, or being argued out of it.
- **It has not been measured.** No agent has been run against these files in this repository. The eval harness exists so that you can measure it; until someone does, there is no evidence of how often any agent follows any rule.
- **It may not be loaded.** Agents differ in which instruction files they read, some cap their total size, and some have modes that skip them (for example `claude --bare`). In long sessions, earlier instructions can be summarised away unless the product re-injects them. Subagents may not receive them. The Agent Skills form is loaded only when the model decides it is relevant.
- **Prompt injection can defeat it.** The rule that content is data (TRU-1) depends on the model holding to it. A well-crafted injection may still succeed.
- **An unattended agent cannot be sure nobody is there.** The fail-closed rule tells it to assume so when unsure. That is a judgement by the agent.

## What the rules do not catch

- **A malicious version that outlives the cooldown.** If nobody detects a bad release within the cooldown period, the agent installs it and no rule objects. The cooldown works only because other people find problems first.
- **Anything already in the lockfile.** The first check exits early for versions that are already locked. A compromised version that got in earlier is never re-examined. Finding those is a scanner's job.
- **Transitive dependencies resolved fresh.** The cooldown applies to the version the agent chooses. A dependency of that dependency can still resolve to a brand-new release unless the package manager enforces the cooldown too (see `enforcement/`).
- **Code that runs on import or at start-up.** Blocking install scripts does not stop a payload that runs when the package is loaded, or from a Python `.pth` file. The Python overlay reports new `.pth` files after the fact; it does not prevent them.
- **Build-time code in some ecosystems.** Rust build scripts and procedural macros, NuGet build targets and Ruby native extensions run at build or install time and cannot be switched off. The overlays ask the agent to mention them, not to block them.
- **A convincing fake.** Checks rely on registry metadata. A squatted package that is older than the package-age threshold and links a plausible repository passes the identity checks. Repository links and author names are set by the publisher.
- **Takeover of an approved package.** The approved list skips identity and package-age checks. Only the cooldown and, where checkable, the publisher-change rule still stand in the way.
- **Publisher changes on most registries.** The publishing account per version is visible on npm and crates.io. On PyPI, NuGet and RubyGems the agent reports the check as not done. Where it is checkable, a legitimate change of maintainer also triggers a question.
- **Lookalike names in general.** Deciding that a name is "a near-miss of a more widely used package" is a judgement by the agent, with no fixed test.
- **Dependency confusion and private registries.** The rules say to use the project's configured registry and to ask before adding another. They do not check how your registries are configured.

## Costs

- **It can delay fixes.** A cooldown delays every new release, including fixes that are not tied to a published advisory. The fast path (FIX-1) covers only fixes for advisories rated high or critical, or known to be exploited.
- **It uses context.** A preset is roughly 160 to 330 lines (12 to 22 KB), loaded into every session.
- **It will sometimes ask when it should not.** The [response model](response-model.md) is designed to make that rare, and that claim is also unmeasured.
- **Missing evidence mostly fails open.** When a check cannot be done, the agent reports `not checked` and proceeds, except for package existence and version age (EVD-1). A registry that hides the publishing account, or an agent with no advisory database, leaves those checks undone.

## Thresholds

- The 3-day cooldown for packages and the 7-day cooldown for MCP servers and editor extensions are based on how quickly malicious releases were removed in the incidents surveyed, and on the defaults of Dependabot and Renovate. They are margins, not measurements.
- The 90-day package-age and 24-month staleness defaults are pragmatic starting points. Nobody has shown they are better than other values.

What each protects against and when to change it: [response-model.md](response-model.md#thresholds).

## Coverage

- **Depth is uneven.** npm and Python have the most specific guidance. Maven, Gradle and Go have no built-in cooldown, so the agent has to apply it by hand. PHP and other ecosystems have no overlay.
- **The evals are small.** Nine scenarios, npm only, one run each by default. Enough to see a direction, not to estimate a rate.
- **The incident table is a snapshot.** Twelve incidents, one source each, reviewed on 2026-11-24. None involved NuGet, RubyGems, Go or Cargo, so those overlays have not been checked against a real case.
- **Tool settings change.** Package-manager settings in the overlays and in `enforcement/` were checked against vendor documentation on 2026-11-24 and were not run, with the exception of the pin checker. Check your tool's version.

## The policy is itself a third-party input

A preset is a set of instructions you hand to an agent. Read it first, keep a copy at a known commit, and review changes when you update. The `agent-skills` overlay says this about every third-party skill, and it applies to this one.

## Status of each part

| Part | Status |
|---|---|
| Policy files | Advisory text. Structure and consistency checked by `scripts/selfcheck.py` in CI. |
| Install locations | Checked against each agent's documentation on 2026-11-24. Not run in each agent. |
| `enforcement/ci/check_pins.py` | Tested on passing and failing fixtures |
| Other `enforcement/` examples | Settings checked against vendor documentation on 2026-11-24; not run |
| `evals/` | Harness self-test passes with scripted stand-ins; no agent results |

## What to use with it

The policy complements these controls. It replaces none of them.

| Need | Why it is outside this repo | What to use alongside |
|---|---|---|
| Finding known vulnerabilities; automated updates | Needs a vulnerability database and a scanner, not instructions | Software composition analysis (for example OSV-Scanner, `npm audit`, `pip-audit`); Dependabot or Renovate with a cooldown |
| SBOMs and vulnerability management | An inventory and a process, not an agent decision | An SBOM generator (SPDX or CycloneDX) and a tracking process |
| Secret scanning and credential hygiene | Package malware steals credentials; limiting that is your environment's job | Secret scanning, short-lived and narrowly scoped tokens |
| Hardening your own CI/CD and releases | Only the publisher can fix publisher-side weaknesses | Workflow linting (for example zizmor), trusted publishing, protected branches |
| Private registries, proxies and install-time allowlists | Enforcement at the network or registry | A registry proxy or an install-time firewall (for example Socket Firewall) |
| Verifying signatures and provenance | Cryptographic verification is a tool's job; the policy only says how much weight to give the result | `npm audit signatures`, registry attestations |
| Agent sandboxing and least privilege | Limits what a bad install can reach; instructions cannot | Containers or VMs for agents, permission settings in your agent |
| Human code review | The policy asks the agent to stop; only review makes the stop binding | Required reviews and branch protection |
| Licence review | The policy flags licences; it does not judge them | Your legal process or a licence scanner |
| Incident response | Happens after the fact | A plan for rotating credentials and rebuilding |

How the rules relate to NIST SSDF, OWASP, CIS and SLSA: [mapping-to-standards.md](mapping-to-standards.md).
