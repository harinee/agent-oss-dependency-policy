# How the files are packaged

## Three layers

| Layer | Where | What it is |
|---|---|---|
| Foundational | `skills/foundational/` | The rule set. Pick `oss-selection-baseline` or `oss-selection-strict`. |
| Overlays | `skills/overlays/` | Additions for a capability, ecosystem, artifact type or context. Each one needs a foundational file. |
| Presets | `packaged/` | A foundational file and a set of overlays joined into one file, ready to copy. |

Overlays refer to foundational rules by ID (for example "apply AGE-1") and do not repeat them. An overlay on its own is incomplete.

## Presets are generated

`presets.json` lists each preset's source files. `python3 scripts/build.py` writes each preset as the exact concatenation of its sources, so a preset cannot drift from them. `python3 scripts/build.py --check` fails if a preset is out of date; CI runs it.

Do not edit files in `packaged/` or `agent-skills/`. Edit the source and rebuild.

To make your own combination, either join files by hand:

```bash
cat skills/foundational/oss-selection-baseline.skills.md \
    skills/overlays/capabilities/agent-can-install-packages.skills.md \
    skills/overlays/ecosystems/go-modules.skills.md \
    > my-policy.md
```

or add an entry to `presets.json` and run the build.

## Two ways to give a preset to an agent

**As always-on instructions (recommended).** Copy the preset into a file your agent reads on every session, such as `AGENTS.md`. A dependency policy has to apply every time a dependency is touched, and always-on files guarantee it is loaded. See [QUICK_START.md](QUICK_START.md) for locations per agent.

**As an Agent Skill.** Each preset is also built as a folder under `agent-skills/` in the [Agent Skills](https://agentskills.io/specification) layout:

```
agent-skills/
  oss-deps-baseline-general/
    SKILL.md        # YAML front matter (name, description) + the preset
```

The `name` matches the folder name and the `description` says when to use it, as the specification requires. Copy the folder into your agent's skills directory, for example `.claude/skills/` or `.agents/skills/`.

A skill is loaded when the agent decides its description matches the task. That saves context when no dependency work is happening, but the agent may not load it when it should. If you rely on the skill form, check that your agent activates it on a dependency task.

The `.skills.md` suffix on files in `skills/` and `packaged/` is this repository's own naming. It is not part of the Agent Skills format; those files are plain Markdown.

## Checks

`python3 scripts/selfcheck.py` verifies the structure: file format, rule IDs, front matter of generated skills, internal links, that presets match their sources, that every overlay is reachable, and that thresholds in the docs and in `enforcement/` match the policy tables.

The Agent Skills project publishes a reference validator, `skills-ref`. It has not been run against these folders; `selfcheck.py` checks the same front-matter constraints.
