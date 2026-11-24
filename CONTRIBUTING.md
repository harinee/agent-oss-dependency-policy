# Contributing

Thanks for helping. This page is the short version; the [contribution guide](docs/contribution-guide.md) has the writing rules in full.

## Setup

You need Python 3 and `make`. There is nothing to install. The scripts use only the standard library and were tested with Python 3.13.

```bash
git clone https://github.com/YOUR-USERNAME/agent-oss-dependency-policy.git
cd agent-oss-dependency-policy
make check
```

`make check` runs what CI runs: the self-check, the pin check and the eval harness self-test.

## Where things live

| Path | What it is | Edit it? |
|---|---|---|
| `policy/foundational/` | The rule set, in a baseline and a strict version | Yes. Keep rule text identical in both; only levels differ. |
| `policy/overlays/` | Additions per capability, ecosystem, artifact type and context | Yes |
| `presets.json` | Which sources make up each preset | Yes |
| `presets/`, `agent-skills/` | Generated from the above | No. Run `make build`. |
| `enforcement/` | Config and scripts that back rules | Yes |
| `evals/` | Scenarios and the runner | Yes |
| `docs/` | Documentation | Yes |

## Common tasks

**Report a rule that misfired.** Open an issue with the "Rule misfired" template. False positives are the most useful feedback this project can get, because a policy that interrupts too often gets switched off.

**Change or add a rule.**
1. Edit the file under `policy/`. A rule line looks like `- **PREFIX-N (NOTE)** What to do. *Why:* one line.`, with the next free number for that file's prefix.
2. Default to `NOTE`. In the pull request, say why any `ASK` or `BLOCK` is worth the interruption.
3. For a foundational rule, make the same change in both foundational files.
4. `make build && make check`.

**Add an overlay.**
1. Copy an existing overlay in the same folder and choose an unused rule prefix.
2. Add it to a preset in `presets.json` and to the tables in `docs/how-to-choose.md`. The self-check fails until both are done.
3. `make build && make check`.

**Change a threshold default.** Edit the "Tunable thresholds" table in both foundational files, the table in `docs/response-model.md`, and the values in `enforcement/`. The self-check tells you which ones you missed. State your source, or say there is none.

**Add an incident to `docs/threat-coverage.md`.** Give one dated source, say whether it passes the scope test at the top of that page, and name the rule that addresses it or the gap.

**Add an eval scenario.** Copy a file in `evals/scenarios/`, include `dry_run` commands for both stand-ins, and run `make evals-selftest`. Use fictional package data.

**Share eval results.** Run the harness against an agent (see `evals/README.md`) and open an issue with the "Eval results" template. Include the agent name and version, the command, the preset, and the `results.json` summary. Results from more than one run are worth much more than one.

## Ground rules

- Do not state an incident, statistic, tool feature or standards mapping without a source you have read, and give its date.
- Name a tool or setting only after checking it exists and does what you say.
- These files are advice to an agent. Do not describe them as preventing, ensuring or enforcing anything.
- Keep pull requests to one theme.

## Pull requests

The pull request template lists what reviewers check. CI must pass. Contributions are licensed under the MIT License.
