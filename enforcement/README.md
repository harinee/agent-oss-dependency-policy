# Enforcement

The policy files are instructions. An agent can ignore them. This directory holds machine-checkable counterparts for the rules that have one. Configuration is enforced by the package manager or by CI whether or not the agent follows the policy.

Use both. The policy covers decisions that no config can make, such as whether a package is the one you meant. The config covers rules that should not depend on an agent's judgment.

Everything here is an example to copy and adapt. File names end in `.example` so they are not picked up by accident. Settings and minimum versions were checked against each tool's documentation on 2026-11-24; check your tool version before relying on one.

## What each item does

| Rule | Item | What it does | What it does not catch |
|---|---|---|---|
| AGE-1, SCR-1, PIN-1 | [npm/npmrc.example](npm/npmrc.example) | Refuses versions younger than 3 days (npm 11.10.0+), skips lifecycle scripts, saves exact versions | A malicious version older than the cooldown. Payloads that run at import time, not install time. Older npm versions warn about `min-release-age` and do not apply it (seen with npm 11.4.2). |
| AGE-1, SCR-1 | [pnpm/pnpm-workspace.example.yaml](pnpm/pnpm-workspace.example.yaml) | Same cooldown in minutes (pnpm 10.16+); dependency build scripts run only if allowlisted | Same as above. |
| AGE-1, SCR-1 | [yarn/yarnrc.example.yml](yarn/yarnrc.example.yml) | Three-day age gate; third-party install scripts off | Same as above. |
| AGE-1 | [bun/bunfig.example.toml](bun/bunfig.example.toml) | Cooldown in seconds (Bun 1.3+) | Same as above. |
| AGE-1 | [python/uv.example.toml](python/uv.example.toml) | uv ignores distributions uploaded in the last 3 days | Code that runs at interpreter start from a `.pth` file. Source builds still run build code. |
| AGE-1 | [cargo/config.example.toml](cargo/config.example.toml) | Minimum publish age for crates (Rust 1.100+) | Build scripts and procedural macros still run at build time. |
| AGE-1 | [dependabot/dependabot.example.yml](dependabot/dependabot.example.yml) | Delays version-update pull requests by 3 days | Installs made outside Dependabot. Security updates are not delayed, by design. |
| AGE-1 | [renovate/renovate.example.json](renovate/renovate.example.json) | Delays update pull requests by 3 days | Installs made outside Renovate. Security updates bypass it, by design. |
| PIN-1, PIN-4, PIN-5, SRC-1 | [ci/check_pins.py](ci/check_pins.py) | Fails when workflow actions are not pinned to a commit SHA, Dockerfile images have no digest, `package.json` has no lockfile or points at git or URL sources, requirements entries lack `==`, or a lockfile resolves from an unexpected registry | Whether a pinned thing is safe or how old it is. Whether a SHA belongs to the action's own repository. Images in Compose or Kubernetes files. Ecosystems other than npm and pip requirements files. |
| same | [ci/github-workflow.example.yml](ci/github-workflow.example.yml) | Runs `check_pins.py` on pull requests | Same as the script. |
| same | [pre-commit/pre-commit-config.example.yaml](pre-commit/pre-commit-config.example.yaml) | Runs `check_pins.py` before each commit | Same as the script. Hooks can be skipped locally, so keep the CI check too. |

## Other tools with a built-in setting

No example file is shipped for these. The setting names are from each tool's documentation.

| Tool | Setting | Note |
|---|---|---|
| pip | `--uploaded-prior-to P3D` (pip 26.1+) | Only effective with indexes that provide upload times. |
| pip | `--only-binary :all:` and `--require-hashes` | Refuses source builds; requires a hash for every requirement. |
| Poetry | `poetry config solver.min-release-age 3` (Poetry 2.4.0+) | Days. |
| Bundler | `bundle config set cooldown 3` (Bundler 4.0.13+) | Days. Versions served without a creation time are not filtered. |
| NuGet | `minPublishAgeHours` on a package source (.NET SDK 11.0.100+) | Does not apply to ordinary package restore. |
| Go | none | The toolchain has no release-age setting. The agent applies AGE-1 itself (see the Go overlay). |
| Maven, Gradle | none found | Use the Dependabot or Renovate cooldown for update pull requests. |
| GitHub Actions | workflow lockfile, `.github/workflows/actions.lock` | Records commit SHAs for actions. Does not cover reusable-workflow calls. |

## Urgent security fix: lifting the cooldown for one install

The cooldown settings here do not know about advisories. A fix for a critical vulnerability published yesterday is refused like any other new version. The policy's fast path (FIX-1) covers this: the agent confirms the advisory and the publisher, then asks you to approve one install. It must not lift the setting itself (FIX-2).

Lift the cooldown for a single command and leave the config file alone:

```bash
npm install <package>@<fixed-version> --min-release-age=0
```

Run on npm 12.2.3 on 2026-11-25: with `min-release-age` set in `.npmrc` the install was refused, and with the flag it succeeded.

- The flag applies to everything that command resolves, including new transitive dependencies. Name one exact version and keep the lockfile in place so nothing else moves.
- For other package managers, use the tool's own per-command or per-package exception and check its documentation. None was run here. pnpm documents an exclude list for the release-age setting; name the exact version, because a bare package name exempts every future release too.
- Dependabot and Renovate security updates already bypass their cooldown.

## Making an ASK binding with agent permission settings

Some agent products can force a confirmation prompt before a command runs, whatever the model decides. This is the closest technical counterpart to an ASK. No example file is shipped; the snippet below is for Claude Code (`.claude/settings.json`), composed from its [permissions documentation](https://code.claude.com/docs/en/permissions) on 2026-11-24 and not run.

```json
{
  "permissions": {
    "ask": ["Bash(npm install *)", "Bash(npm i *)", "Bash(pip install *)", "Bash(npx *)"]
  }
}
```

- An `ask` rule prompts even when an `allow` rule also matches. In a non-interactive run (`claude -p`) with nothing to approve it, the call is denied and the run continues.
- It prompts on every matching command, including installs from the lockfile, so it costs more interruptions than the policy's ASK rules do.
- It matches the command text, so it is not a security boundary: another way of invoking the package manager is not matched. A sandbox is.

## Rules with no machine-checkable counterpart here

ID-1, ID-2, AGE-2, AGE-3, PUB-1, TRU-1, TRU-2, ART-1, DEP-1, MNT-1 and the unattended rules depend on judgment or on context a config file does not have. For those, the policy text is all there is in this repository. Tools that cover part of that ground are listed in the README under what to use alongside this repo.

## Keeping values in step

The cooldown value in these files matches `version_cooldown_days` in the baseline policy (3 days). The longer `tool_cooldown_days` (7 days) for MCP servers and editor extensions has no config counterpart here; the agent applies it. `scripts/selfcheck.py` fails if they differ. If you change the threshold in your copy of the policy, change it in your config too.

## Running the pin check

```bash
python3 enforcement/ci/check_pins.py /path/to/your/repo
python3 enforcement/ci/check_pins.py /path/to/your/repo --allow-registry npm.pkg.github.com
```

It prints one line per finding with the file, line and rule ID, and exits 1 if there are any. It uses only the Python standard library.
