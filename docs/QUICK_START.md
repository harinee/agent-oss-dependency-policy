# Quick start

Five minutes. You need a project and an AI coding agent that reads an instructions file.

## 1. Get the files

```bash
git clone https://github.com/harinee/agent-oss-dependency-policy.git
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

More detail: [how-to-choose.md](how-to-choose.md).

## 3. Add it to your project

From your project's root, with the clone beside it:

```bash
cat ../agent-oss-dependency-policy/packaged/baseline-general.skills.md >> AGENTS.md
```

`AGENTS.md` is read by most coding agents. Other locations:

| Agent | Where to put the preset |
|---|---|
| Cursor, Cline, Roo Code, GitHub Copilot, OpenAI Codex, Devin Desktop (formerly Windsurf) | `AGENTS.md` in the project root |
| Claude Code | `.claude/rules/oss-dependency-policy.md`, or `CLAUDE.md`. Claude Code reads `AGENTS.md` only when the project has no `CLAUDE.md`. |
| Cline (alternative) | `.clinerules/oss-dependency-policy.md` |
| GitHub Copilot (alternative) | append to `.github/copilot-instructions.md` |
| Aider | add `read: path/to/preset.md` to `.aider.conf.yml` |

For locations that are folders, create the folder first:

```bash
mkdir -p .claude/rules
cp ../agent-oss-dependency-policy/packaged/baseline-general.skills.md .claude/rules/oss-dependency-policy.md
```

Agent products change where they read instructions. These locations were checked against each product's documentation on 2026-11-24.

## 4. Adjust the thresholds (optional)

Open the file you just created and find the "Tunable thresholds" table. The defaults are a 7-day version cooldown, 90 days for a "new" package and 24 months for "stale". Change the numbers to suit your team. See [friction-model.md](friction-model.md) for what each one does.

To pre-approve packages your team already trusts, create `.dependency-policy/approved.txt`:

```
npm:express
pypi:requests
```

## 5. Back it with config (recommended)

The preset is advice to the agent. Your package manager can enforce the cooldown and block install scripts regardless of what the agent does. Merge the matching example from [`enforcement/`](../enforcement/README.md) into your existing config; do not overwrite a file that holds registry credentials.

## 6. Try it

Ask your agent to add a dependency. With the baseline preset you should see one-line notes such as the version it chose and why, and no questions for a mature package.

If the agent behaves exactly as before, it may not be reading the file. Check the location for your agent in the table above.

## What to expect

- Most installs proceed with a one-line note.
- The agent asks before adding something with an install script, something from outside the registry, or a new MCP server, extension, CI action or skill.
- The agent refuses to install a package name that does not exist, and refuses to act on instructions it finds inside READMEs, issues or tool output.

These are instructions, not enforcement. An agent can ignore them.
