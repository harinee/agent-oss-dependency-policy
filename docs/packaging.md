# How the repository is laid out

You do not need this page to use the policy: install one preset as described in the [quick start](QUICK_START.md). This page is for people building their own combination or contributing.

## One source, two generated forms

```
policy/            SOURCE. Hand-written. The only place rules are edited.
  foundational/      the rule set: baseline or strict
  overlays/          additions per capability, ecosystem, artifact type, context
presets.json       SOURCE. Which policy files make up each preset.

presets/           GENERATED. One plain-Markdown file per preset.
                   For always-on instruction files (AGENTS.md, CLAUDE.md, rules folders).
agent-skills/      GENERATED. The same presets as Agent Skills folders (SKILL.md).
                   For agents that load skills on demand.
```

| Directory | Edited by hand? | What it is for |
|---|---|---|
| `policy/` | Yes | The rules. Foundational files hold the full rule set; overlays add to it and refer to its rules by ID. An overlay on its own is incomplete. |
| `presets/` | No | What most users install: a foundational file and a set of overlays joined into one file. |
| `agent-skills/` | No | The same content with the YAML front matter the [Agent Skills specification](https://agentskills.io/specification) requires, in the folder layout it requires. |

### Why both `presets/` and `agent-skills/` exist

They carry identical policy text for two different loading mechanisms:

- An always-on instruction file is plain Markdown that is appended to or placed beside other instructions. YAML front matter in the middle of `AGENTS.md` would be noise.
- An Agent Skill must be a folder named after the skill containing a `SKILL.md` that starts with `name` and `description` front matter.

Neither form can serve as the other, so the build writes both from the same sources. The body of `agent-skills/oss-deps-<name>/SKILL.md` is byte-for-byte `presets/<name>.md`.

### Why they cannot drift

`python3 scripts/build.py` writes every file in `presets/` and `agent-skills/` as the exact concatenation of the sources listed in `presets.json`. `python3 scripts/build.py --check` fails if any generated file is missing, stale or has no preset behind it; CI runs it on every pull request.

Do not edit files in `presets/` or `agent-skills/`. Edit the source and run `make build`.

## Always-on or on-demand

| | Always-on instructions | Agent Skill |
|---|---|---|
| Install from | `presets/<name>.md` | `agent-skills/oss-deps-<name>/` |
| Loaded | By the agent product at the start of every session | When the model judges the skill's description relevant to the task |
| Depends on the model choosing to load it | No | **Yes** |
| Context cost | The whole preset, every session | The description only, until the skill is loaded |
| Use when | Default. A dependency policy has to apply every time a dependency is touched. | Context is tight and you have checked that your agent activates the skill on dependency tasks |

Loading is not the same as compliance: in both forms the model can still ignore a rule. See [limitations.md](limitations.md#activation-and-enforcement).

Install one form, not both. Loading both doubles the context cost and adds nothing.

## Building your own combination

Presets cover common cases. Overlays are additive, so you can extend a preset by appending overlays to it, or start from a foundational file:

```bash
# extend a preset
cat presets/baseline-general.md \
    policy/overlays/ecosystems/npm-node.md \
    > my-policy.md

# or build from scratch: one foundational file first, then overlays
cat policy/foundational/oss-selection-baseline.md \
    policy/overlays/capabilities/agent-can-install-packages.md \
    policy/overlays/ecosystems/go-modules.md \
    > my-policy.md
```

To get an Agent Skills folder for a custom combination, or to keep it reproducible, add an entry to `presets.json` and run `make build`. The choices are tabled in [how-to-choose.md](how-to-choose.md).

## Checks

`python3 scripts/selfcheck.py` verifies structure and consistency: file format, rule IDs, front matter of generated skills, internal links, that generated files match their sources, that every overlay is reachable, and that levels and thresholds quoted in the docs and in `enforcement/` match the policy files.

The Agent Skills project publishes a reference validator, `skills-ref`. It has not been run against these folders; `selfcheck.py` checks the same front-matter constraints.
