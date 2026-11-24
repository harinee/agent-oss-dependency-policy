# Quick start

Five minutes. You install **one preset**: a single Markdown file that contains the rules and the add-ons for its use case. Nothing else is required.

## 1. Get the files

```bash
git clone https://github.com/harinee/agent-oss-dependency-policy.git ~/agent-oss-dependency-policy
```

Read the preset you are about to install. It is a set of instructions your agent will follow, so treat it like any other third-party input.

## 2. Pick a preset

| If your project is | Use |
|---|---|
| Anything, and you are not sure | `baseline-general` |
| A prototype or experiment | `prototype-quick` |
| Node.js with an agent that runs unattended | `npm-high-autonomy` |
| Python in a regulated or sensitive setting | `python-sensitive-repo` |
| Production, with an agent that can change CI and containers | `strict-agent-high-autonomy` |
| Java in production | `java-production` |
| Go | `go-service` |
| Rust | `rust-project` |
| .NET | `dotnet-project` |
| Ruby | `ruby-project` |
| Any project where the agent may add MCP servers, extensions or skills | `agent-tooling` |

More detail, and how to extend a preset: [how-to-choose.md](how-to-choose.md).

## 3. Install it as an always-on instruction file

Run from your project root. Replace `baseline-general` with your preset.

### Claude Code

```bash
mkdir -p .claude/rules
cp ~/agent-oss-dependency-policy/presets/baseline-general.md .claude/rules/oss-dependency-policy.md
```

- Rules files without `paths:` front matter load at launch and are re-injected after context compaction. Do not add `paths:` to this file. ([docs](https://code.claude.com/docs/en/memory))
- Subagents receive it too, except the built-in Explore and Plan agents and custom agents that opt out. ([docs](https://code.claude.com/docs/en/sub-agents))
- Do not rely on `AGENTS.md` for Claude Code: by default it is read only when the project has no `CLAUDE.md`.
- `claude --bare` skips these files. If you script Claude Code with `--bare`, pass the policy explicitly.

### Every agent that reads `AGENTS.md`

```bash
cat ~/agent-oss-dependency-policy/presets/baseline-general.md >> AGENTS.md
```

| Agent | Notes | Docs |
|---|---|---|
| OpenAI Codex | Reads `AGENTS.md` before any work. The combined instruction files are capped at 32 KiB by default (`project_doc_max_bytes`); presets are 12 to 22 KB, so check the total if your `AGENTS.md` is already long. | [docs](https://learn.chatgpt.com/docs/agent-configuration/agents-md) |
| Cursor | Root `AGENTS.md`. Alternative: `.cursor/rules/oss-dependency-policy.mdc` with `alwaysApply: true` in its front matter (the `.mdc` extension is required). | [docs](https://cursor.com/docs/context/rules) |
| GitHub Copilot | `AGENTS.md`, or append to `.github/copilot-instructions.md`. In VS Code, `AGENTS.md` is controlled by the `chat.useAgentsMdFile` setting. | [docs](https://docs.github.com/en/copilot/reference/custom-instructions-support) |
| Cline | Root `AGENTS.md`, or `.clinerules/oss-dependency-policy.md` (no front matter, so it is always active) | [docs](https://docs.cline.bot/customization/cline-rules) |
| Roo Code | Root `AGENTS.md`, loaded by default, or `.roo/rules/oss-dependency-policy.md` | [docs](https://roocodeinc.github.io/Roo-Code/features/custom-instructions) |
| Devin Desktop (formerly Windsurf) | Root `AGENTS.md` is read as an always-on rule. Alternative: `.devin/rules/oss-dependency-policy.md` with `trigger: always_on`. | [docs](https://docs.devin.ai/desktop/cascade/agents-md) |

### Other agents

| Agent | How | Docs |
|---|---|---|
| Gemini CLI | Append the preset to `GEMINI.md`, or set `{"context": {"fileName": ["AGENTS.md", "GEMINI.md"]}}` in `settings.json` | [docs](https://geminicli.com/docs/cli/gemini-md/) |
| Aider | Add `read: path/to/preset.md` to `.aider.conf.yml` | [docs](https://aider.chat/docs/usage/conventions.html) |

Agent products change where they read instructions. These locations were checked against each product's documentation on 2026-11-24; they were not run in each agent.

### Alternative: install as an on-demand Agent Skill

An always-on file is loaded by the agent product every session. An Agent Skill is loaded only when the model judges its description relevant, so the model may skip it when it should not. Use the skill form only if context is tight, and check that your agent activates it on a dependency task. Install one form, not both.

```bash
# Claude Code
mkdir -p .claude/skills
cp -R ~/agent-oss-dependency-policy/agent-skills/oss-deps-baseline-general .claude/skills/

# Codex, Cursor, GitHub Copilot, Gemini CLI
mkdir -p .agents/skills
cp -R ~/agent-oss-dependency-policy/agent-skills/oss-deps-baseline-general .agents/skills/
```

## 4. Back it with config (recommended)

The preset is advice to the agent. Your package manager can enforce the cooldown and block install scripts regardless of what the agent does. Merge the matching example from [`enforcement/`](../enforcement/README.md) into your existing config; do not overwrite a file that holds registry credentials.

```bash
# npm 11.10 or later; read the comments in the file first
cat ~/agent-oss-dependency-policy/enforcement/npm/npmrc.example >> .npmrc
```

## 5. Try it

Ask your agent to add a dependency. With the baseline preset you should see one-line notes such as the version it chose and why, and no questions for a mature package.

If the agent behaves exactly as before, it may not be reading the file. Check the location for your agent above, or ask the agent which dependency rules it has been given.

## 6. Adjust (optional)

Both files live in your project, work with every agent, and survive updating the preset. The agent is told never to edit them.

**Change a level or threshold:** `.dependency-policy/overrides.md`

```bash
mkdir -p .dependency-policy
cp ~/agent-oss-dependency-policy/examples/overrides.example.md .dependency-policy/overrides.md
```

```markdown
| Rule or threshold | Value | Reason |
|---|---|---|
| version_cooldown_days | 14 | Matches our Renovate setting |
| AGE-2 | ASK | New packages need a named owner here |
```

**Pre-approve packages your team already trusts:** `.dependency-policy/approved.txt`

```
npm:express
pypi:requests
```

The defaults are a 3-day version cooldown (7 days for MCP servers and editor extensions), 90 days for a "new" package and 24 months for "stale". What each protects against and when to change it: [response-model.md](response-model.md#thresholds).

## Updating

Pull the repository, read the diff of your preset, and repeat step 3 (replace the rules file, or replace the policy block in `AGENTS.md`). Your overrides and approved list are untouched.

## What to expect

- Most installs proceed with a one-line note.
- The agent asks before adding something with an install script, something from outside the registry, or a new MCP server, extension, CI action or skill.
- The agent refuses to install a package name that does not exist, and refuses to act on instructions it finds inside READMEs, issues or tool output.

These are instructions, not enforcement. An agent can ignore them. See [limitations.md](limitations.md#activation-and-enforcement).
