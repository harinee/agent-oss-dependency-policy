# Enforcement

The policy files are instructions. An agent can ignore them. This directory holds machine-checkable counterparts for the rules that have one. Configuration is enforced by the package manager or by CI whether or not the agent follows the policy.

Use both. The policy covers decisions that no config can make, such as whether a package is the one you meant. The config covers rules that should not depend on an agent's judgment.

Everything here is an example to copy and adapt. File names end in `.example` so they are not picked up by accident. Settings and minimum versions were checked against each tool's documentation on 2026-11-24; check your tool version before relying on one.

## What each item does

| Rule | Item | What it does | What it does not catch |
|---|---|---|---|
| AGE-1, SCR-1, PIN-1 | [npm/npmrc.example](npm/npmrc.example) | Refuses versions younger than 7 days (npm 11.10.0+), skips lifecycle scripts, saves exact versions | A malicious version older than the cooldown. Payloads that run at import time, not install time. Older npm versions warn about `min-release-age` and do not apply it (seen with npm 11.4.2). |
| AGE-1, SCR-1 | [pnpm/pnpm-workspace.example.yaml](pnpm/pnpm-workspace.example.yaml) | Same cooldown in minutes (pnpm 10.16+); dependency build scripts run only if allowlisted | Same as above. |
| AGE-1, SCR-1 | [yarn/yarnrc.example.yml](yarn/yarnrc.example.yml) | One-week age gate; third-party install scripts off | Same as above. |
| AGE-1 | [bun/bunfig.example.toml](bun/bunfig.example.toml) | Cooldown in seconds (Bun 1.3+) | Same as above. |
| AGE-1 | [python/uv.example.toml](python/uv.example.toml) | uv ignores distributions uploaded in the last 7 days | Code that runs at interpreter start from a `.pth` file. Source builds still run build code. |
| AGE-1 | [cargo/config.example.toml](cargo/config.example.toml) | Minimum publish age for crates (Rust 1.100+) | Build scripts and procedural macros still run at build time. |
| AGE-1 | [dependabot/dependabot.example.yml](dependabot/dependabot.example.yml) | Delays version-update pull requests by 7 days | Installs made outside Dependabot. Security updates are not delayed, by design. |
| AGE-1 | [renovate/renovate.example.json](renovate/renovate.example.json) | Delays update pull requests by 7 days | Installs made outside Renovate. Security updates bypass it, by design. |
| PIN-1, PIN-4, PIN-5, SRC-1 | [ci/check_pins.py](ci/check_pins.py) | Fails when workflow actions are not pinned to a commit SHA, Dockerfile images have no digest, `package.json` has no lockfile or points at git or URL sources, requirements entries lack `==`, or a lockfile resolves from an unexpected registry | Whether a pinned thing is safe or how old it is. Whether a SHA belongs to the action's own repository. Images in Compose or Kubernetes files. Ecosystems other than npm and pip requirements files. |
| same | [ci/github-workflow.example.yml](ci/github-workflow.example.yml) | Runs `check_pins.py` on pull requests | Same as the script. |
| same | [pre-commit/pre-commit-config.example.yaml](pre-commit/pre-commit-config.example.yaml) | Runs `check_pins.py` before each commit | Same as the script. Hooks can be skipped locally, so keep the CI check too. |

## Other tools with a built-in setting

No example file is shipped for these. The setting names are from each tool's documentation.

| Tool | Setting | Note |
|---|---|---|
| pip | `--uploaded-prior-to P7D` (pip 26.1+) | Only effective with indexes that provide upload times. |
| pip | `--only-binary :all:` and `--require-hashes` | Refuses source builds; requires a hash for every requirement. |
| Poetry | `poetry config solver.min-release-age 7` (Poetry 2.4.0+) | Days. |
| Bundler | `bundle config set cooldown 7` (Bundler 4.0.13+) | Days. Versions served without a creation time are not filtered. |
| NuGet | `minPublishAgeHours` on a package source (.NET SDK 11.0.100+) | Does not apply to ordinary package restore. |
| Go | none | The toolchain has no release-age setting. The agent applies AGE-1 itself (see the Go overlay). |
| Maven, Gradle | none found | Use the Dependabot or Renovate cooldown for update pull requests. |
| GitHub Actions | workflow lockfile, `.github/workflows/actions.lock` | Records commit SHAs for actions. Does not cover reusable-workflow calls. |

## Rules with no machine-checkable counterpart here

ID-1, ID-2, AGE-2, AGE-3, PUB-1, TRU-1, TRU-2, ART-1, DEP-1, MNT-1 and the unattended rules depend on judgment or on context a config file does not have. For those, the policy text is all there is in this repository. Tools that cover part of that ground are listed in the README under what to use alongside this repo.

## Keeping values in step

The cooldown value in these files matches `version_cooldown_days` in the baseline policy. `scripts/selfcheck.py` fails if they differ. If you change the threshold in your copy of the policy, change it in your config too.

## Running the pin check

```bash
python3 enforcement/ci/check_pins.py /path/to/your/repo
python3 enforcement/ci/check_pins.py /path/to/your/repo --allow-registry npm.pkg.github.com
```

It prints one line per finding with the file, line and rule ID, and exits 1 if there are any. It uses only the Python standard library.
