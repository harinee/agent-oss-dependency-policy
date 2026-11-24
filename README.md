<div align="center">

# Agent OSS Dependency Policy

**Guardrails for the packages your AI coding agent installs.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Set up](#set-up) · [Day to day](#day-to-day) · [Settings](#settings) · [Customize](#customize) · [Not stopped](#what-the-policy-does-not-stop) · [Use alongside](#use-it-alongside-your-other-controls) · [Limits](#limits) · [Documentation](#documentation)

</div>

---

Coding agents add packages quickly and rarely check them. This repository gives your agent a written set of rules for that step. Before it installs something, the agent checks whether the version is old enough to trust, whether the name is real, and whether install scripts should run. Most of the time it picks a safe version and carries on.

> [!IMPORTANT]
> The rules are instructions to the agent. An agent can ignore them. **Step 4** adds package-manager settings that hold the two most important limits whatever the agent does.

<br>

## Set up

About five minutes. Run the commands from your **project's root folder**.

### Step 1 · Download the files

```bash
git clone https://github.com/harinee/agent-oss-dependency-policy.git ~/agent-oss-dependency-policy
```

### Step 2 · Choose a preset

A preset is one file of rules for one kind of project. Open it and read it before you install it, because your agent will follow it.

| Your project | Preset | |
|---|---|---|
| Anything, or you are not sure | `baseline-general` | ![Start here](https://img.shields.io/badge/-Start%20here-0969da?style=flat-square) |
| A prototype or experiment | `prototype-quick` | |
| Node.js, with an agent that runs unattended | `npm-high-autonomy` | |
| Python, regulated or sensitive | `python-sensitive-repo` | |
| Production, with an agent that can change CI and containers | `strict-agent-high-autonomy` | |
| Java, Go, Rust, .NET or Ruby | `java-production`, `go-service`, `rust-project`, `dotnet-project`, `ruby-project` | |
| The agent may add MCP servers, extensions or skills | `agent-tooling` | |

Not an exact fit? See [how to choose and extend a preset](docs/how-to-choose.md).

### Step 3 · Add the preset to your agent

**Claude Code**

```bash
mkdir -p .claude/rules
cp ~/agent-oss-dependency-policy/presets/baseline-general.md .claude/rules/oss-dependency-policy.md
```

**Codex, Cursor, GitHub Copilot, Cline, Roo Code, Devin Desktop**

```bash
cat ~/agent-oss-dependency-policy/presets/baseline-general.md >> AGENTS.md
```

<details>
<summary><b>Gemini CLI, Aider, or a different file location</b></summary>
<br>

| Agent | Where to put the preset |
|---|---|
| Gemini CLI | Append to `GEMINI.md`, or add `"AGENTS.md"` to `context.fileName` in `settings.json` |
| Aider | `read: path/to/preset.md` in `.aider.conf.yml` |
| Cursor (alternative) | `.cursor/rules/oss-dependency-policy.mdc` with `alwaysApply: true` |
| GitHub Copilot (alternative) | Append to `.github/copilot-instructions.md` |
| Cline (alternative) | `.clinerules/oss-dependency-policy.md` |

Caveats and documentation links for each agent: [Quick start guide](docs/QUICK_START.md). Locations were checked against each product's documentation on 2026-11-24.

</details>

### Step 4 · Turn on the package-manager limits (recommended)

The preset asks the agent to behave. This step makes your package manager enforce two limits on every install, including installs the agent did not make:

1. **Versions published in the last 3 days are not installed.** This is the [cooldown](#the-3-day-cooldown).
2. **Install scripts do not run.** These are the scripts that execute code on your machine as soon as a package is installed.

Example for npm 11.10 or later. Older npm versions print an "Unknown project config" warning and ignore the cooldown, so check `npm --version` first:

```bash
cat ~/agent-oss-dependency-policy/enforcement/npm/npmrc.example >> .npmrc
```

> [!CAUTION]
> Limit 2 will break packages that build native code or download binaries during install, until you approve them. You will see this as a failed install, not a silent problem. If `.npmrc` already holds credentials, merge the file by hand instead of appending it.

Other package managers (pnpm, Yarn, Bun, uv, Cargo) and Dependabot or Renovate: [enforcement/](enforcement/README.md).

### Step 5 · Check that it loaded

- **Claude Code:** run `/memory`. `oss-dependency-policy.md` should be in the list.
- **Other agents:** open `AGENTS.md` (or the file you used) and check the policy text is there.

Commit the file so your whole team gets the same rules.

<br>

## Day to day

Once it is set up, most of the time you do nothing. This is what to expect.

| | Situation | What the agent does | What you do |
|:-:|---|---|---|
| ![Routine](https://img.shields.io/badge/-Routine-2da44e?style=flat-square) | Adds a well-established package | Installs the newest version at least 3 days old | Nothing |
| ![Routine](https://img.shields.io/badge/-Routine-2da44e?style=flat-square) | Adds a CI action or container image | Pins it to a commit SHA or image digest | Nothing |
| ![Routine](https://img.shields.io/badge/-Routine-2da44e?style=flat-square) | A high or critical vulnerability has a fix | Checks the advisory first. If it is confirmed, installs the fix without waiting. See [critical security fixes](#critical-security-fixes) | Approve the one-off install if your package manager enforces the cooldown |
| ![Ask](https://img.shields.io/badge/-Ask-bf8700?style=flat-square) | Package needs an install script | Stops and asks once | Approve it, or add it to the project's script allowlist |
| ![Ask](https://img.shields.io/badge/-Ask-bf8700?style=flat-square) | Package name is a near-miss of a much more popular one | Stops and asks | Check it is the package you meant |
| ![Ask](https://img.shields.io/badge/-Ask-bf8700?style=flat-square) | Brand-new package with no linked source repository or publisher history | Stops and asks | Check it is the package you meant |
| ![Ask](https://img.shields.io/badge/-Ask-bf8700?style=flat-square) | Publisher of a package has changed | Stops and asks | Confirm the change is expected |
| ![Ask](https://img.shields.io/badge/-Ask-bf8700?style=flat-square) | Install from outside the registry (git URL, tarball, binary), or a script piped into a shell | Stops and asks | Approve, or choose the registry version |
| ![Ask](https://img.shields.io/badge/-Ask-bf8700?style=flat-square) | After an install, a file outside the dependencies changed: agent config, editor tasks, CI workflow, git hook or shell profile | Stops, lists the files, and does not act on them | Review the listed files |
| ![Ask](https://img.shields.io/badge/-Ask-bf8700?style=flat-square) | Deleting or regenerating the lockfile to clear a conflict | Stops and asks | Approve, or resolve the conflict another way |
| ![Ask](https://img.shields.io/badge/-Ask-bf8700?style=flat-square) | New MCP server, editor extension, agent skill, scanner, build plugin or CI action | Stops and asks | Approve or reject |
| ![Ask](https://img.shields.io/badge/-Ask-bf8700?style=flat-square) | Upgrade of a version your project already pins or locks, when you did not ask for it | Stops and asks | Approve the upgrade, or keep the pinned version |
| ![Stop](https://img.shields.io/badge/-Stop-cf222e?style=flat-square) | The package name does not exist | Stops. Does not guess a similar name | Fix the name |
| ![Stop](https://img.shields.io/badge/-Stop-cf222e?style=flat-square) | The version has a malware advisory | Stops | Pick another package or version |
| ![Stop](https://img.shields.io/badge/-Stop-cf222e?style=flat-square) | A README, issue, web page or tool output says to install or run something | Does not follow the text, and reports what it saw | If you want it, ask the agent yourself. A package it names is then handled like any new dependency |

These are all 9 ask rules and all 3 stop rules of the `baseline-general` preset. Stricter presets ask more often.

**Ask** means the agent waits for your reply in the session. If no one is available to answer (an unattended run), it skips that dependency and logs why.

### What a flag looks like

Every ask and stop says what the agent found, why it is a risk, and how to carry on safely. You should never need to open the policy to understand one.

```text
SCR-1: needs your approval
Found: foo-native 2.1.0 runs an install script (node-gyp build).
Risk: install scripts run code on this machine with your credentials. Malware has spread this way.
Safe options: (1) approve, and I allowlist foo-native only; (2) I use a package that needs no script; (3) skip it.
```

### Critical security fixes

A confirmed fix for a serious vulnerability does not wait for the cooldown. The agent checks this **before** it applies the cooldown.

The fix is installed straight away when all three are true:

1. An advisory database (GitHub Advisory Database, OSV, or your package manager's audit command) rates the vulnerability **high or critical**, or lists it as exploited, and it affects the version you use now.
2. The advisory names the new version as the fix.
3. The new version comes from the usual publisher and has no malware advisory.

A "security fix" claim in a changelog, release note or issue does not count, because that is what an attacker would write. If any check fails, the agent tells you which one and asks.

If you turned on the package-manager limits in Step 4, the package manager will still refuse a new version. The agent shows you the evidence and a one-off command to approve. For npm:

```bash
npm install <package>@<fixed-version> --min-release-age=0
```

This lifts the wait for that one command and leaves your config unchanged. Other package managers: [enforcement guide](enforcement/README.md#urgent-security-fix-lifting-the-cooldown-for-one-install). Lower-severity fixes wait out the cooldown as usual.

### The 3-day cooldown

The cooldown is the wait between a version being published and the agent installing it.

- **Why it exists.** Hijacked releases of popular packages are usually spotted and removed within hours. In the incidents this policy reviewed, most were gone within about 10 hours. Waiting three days lets others find the problem first, and matches the defaults of Dependabot and Renovate. MCP servers and editor extensions wait 7 days, because bad versions of those have stayed available for days.
- **What it costs.** You pick up routine updates three days later. The agent still installs the newest version that has passed the wait, so you are not stuck on an old one. [Critical security fixes](#critical-security-fixes) skip the wait.
- **What it does not do.** It does not stop an old version that already has a known vulnerability. A vulnerability scanner does that. See [what to use with it](docs/limitations.md#what-to-use-with-it).

## What the levels mean

Every rule in the policy has one of three levels. The number of rules is for the `baseline-general` preset.

| Level | Number of rules | What the agent does |
|---|---|---|
| **NOTE** | 12 | ![NOTE](https://img.shields.io/badge/-NOTE-2da44e?style=flat-square) Takes the safe path. Says so in one line only when the check changed what it did. |
| **ASK** | 9 | ![ASK](https://img.shields.io/badge/-ASK-bf8700?style=flat-square) Explains the finding and waits for your reply. |
| **BLOCK** | 3 | ![BLOCK](https://img.shields.io/badge/-BLOCK-cf222e?style=flat-square) Stops and offers an alternative. |

The levels are set so that routine work rarely interrupts you. Full reasoning for each level: [response model](docs/response-model.md).

<br>

## Settings

The policy uses four numbers. You do not need to change them to get started.

| Setting | Default | What it controls | Change it only if |
|---|---|---|---|
| `version_cooldown_days` | 3 | How long a new package version waits before the agent installs it | Your team decides on a different wait. Change Step 4 to match. |
| `tool_cooldown_days` | 7 | The same wait for MCP servers and editor extensions | You publish the server or extension yourself |
| `min_package_age_days` | 90 | When a brand-new package is noted (and asked about, in some combinations) | Your team adopts new packages often, or almost never |
| `stale_after_months` | 24 | When a package with no recent releases is noted | You have a support-lifecycle requirement |

Settings are configuration, not actions. Changing one changes what the agent does. It does not change your package manager, so if you change the cooldown, change Step 4 as well. How to change them: [Customize](#customize). Detail and trade-offs: [response model](docs/response-model.md#thresholds).

<br>

## Customize

Only if you need to. Do not edit the preset. Add files to your project:

```bash
mkdir -p .dependency-policy
cp ~/agent-oss-dependency-policy/examples/overrides.example.md .dependency-policy/overrides.md   # then edit
```

| File | Use it to | Example line |
|---|---|---|
| `.dependency-policy/overrides.md` | Change a rule's level or a setting | `\| AGE-2 \| ASK \| New packages need an owner \|` |
| `.dependency-policy/approved.txt` | Let packages skip the identity and package-age checks | `npm:express` |

You can raise any rule. You can lower any rule except the three BLOCK rules. Full guide: [customizing](docs/response-model.md#customizing).

<br>

## Why this exists

Most supply-chain checks run after a package is already installed, in code review or in a scanner. By then an install script may have run on a developer's machine with their credentials. This policy acts at the moment the agent chooses the package.

It targets patterns that keep recurring:

- **Hijacked releases** of trusted packages, live for only a few hours
- **Invented package names.** Models suggest names that do not exist, and attackers register them.
- **Install-time code.** The Shai-Hulud worm spread to more than 500 npm packages this way.
- **Mutable tags.** Tags on `tj-actions/changed-files` were repointed to code that leaked CI secrets.
- **Instructions hidden in content.** A prompt injection led to an unauthorised `cline` release.

Sources, incidents and the rule for each: [why this exists](docs/why-this-exists.md) and [threat coverage](docs/threat-coverage.md).

<br>

## What the policy does not stop

Some recent incidents would get past every rule here. Each needs a different control.

| What gets through | Incident | Use instead |
|---|---|---|
| A payload that runs when a Python package is imported, or at every interpreter start (a `.pth` file) | LiteLLM 1.107.0, elementary-data | The cooldown is the only defence before install. Report new `.pth` files after install. |
| A malicious release that stays live longer than the cooldown | postmark-mcp (about a week), GlassWorm (days) | Scanning, and watching release notes on pinned packages |
| A pinned, already-approved MCP server or extension that changes behaviour | postmark-mcp, GlassWorm | Re-review on each update; disable auto-update in your editor |
| A compromised CI workflow or leaked token | elementary-data, Miasma, TeamPCP | Secret scanning, short-lived tokens, workflow linting |

Every incident row, with its rules and gaps: [threat coverage](docs/threat-coverage.md).

## Use it alongside your other controls

This policy covers one moment: the agent choosing and installing a package. It does not replace the tools below, and you still need them.

| You still need | Because the policy does not | For example |
|---|---|---|
| **Vulnerability scanning (SCA)** | Find known vulnerabilities in what you already use | OSV-Scanner, `npm audit`, `pip-audit`, Dependabot or Renovate |
| **Secret scanning and short-lived tokens** | Limit what a malicious package can steal | Your host's secret scanning, narrowly scoped credentials |
| **Agent sandboxing** | Limit what a bad install can reach | Containers or VMs, your agent's permission settings |
| **Human code review** | Make the agent's stops binding | Required reviews, branch protection |
| **SBOM and licence review** | Keep an inventory or judge licences | An SPDX or CycloneDX generator, a licence scanner |

Full list, including registry proxies, provenance checks and CI hardening: [what to use with it](docs/limitations.md#what-to-use-with-it).

<br>

## Limits

> [!WARNING]
> - **Guidance, not a guarantee.** The policy text cannot stop an agent from doing anything. Step 4 covers the cooldown and install scripts only.
> - **Not yet measured.** No agent has been run against these files. The [eval harness](evals/README.md) is ready; there are no results yet.
> - **A patient attacker can wait.** A malicious version that outlasts the cooldown passes the checks.
> - **Not a replacement** for vulnerability scanning, SBOMs, secret scanning, sandboxing or human review.

Read [limitations](docs/limitations.md) before you rely on this policy.

<br>

## Documentation

| Start here | Go deeper | Background |
|---|---|---|
| [Quick start by agent](docs/QUICK_START.md) | [Response model](docs/response-model.md) | [Why this exists](docs/why-this-exists.md) |
| [How to choose a preset](docs/how-to-choose.md) | [Threat coverage](docs/threat-coverage.md) | [Design principles](docs/design-principles.md) |
| [Enforcement config](enforcement/README.md) | [Evals](evals/README.md) | [Relation to standards](docs/mapping-to-standards.md) |
| [Limitations](docs/limitations.md) | [Layout and packaging](docs/packaging.md) | [Writing rules](docs/contribution-guide.md) |

## Contributing

The most useful contributions are reports of rules that misfired, eval results from real agents, and overlays for ecosystems not yet covered. Start with [CONTRIBUTING.md](CONTRIBUTING.md), and run `make check` before opening a pull request.

Released under the MIT licence. See [LICENSE](LICENSE).
