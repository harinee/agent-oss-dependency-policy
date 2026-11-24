# Writing guide for policy files

How to write and structure rules and overlays. For setup, where things live and step-by-step tasks, start with [CONTRIBUTING.md](../CONTRIBUTING.md).

## What helps most

| Contribution | Why it matters |
|---|---|
| A report that a rule misfired | False positives decide whether the policy survives in a team |
| Eval results from a real agent | Nothing here has been measured yet |
| An overlay for an ecosystem not yet covered | PHP and others have none |
| A sourced incident and the gap it shows | Keeps the rules tied to real attacks |
| Clearer wording for a rule | Agents follow short, specific instructions better |

## File naming

Lowercase, hyphenated, ending in `.md`: `npm-node.md`, `rust-cargo.md`. One variable per file:

| Folder | Variable | Example |
|---|---|---|
| `capabilities/` | What the agent can do | `agent-can-install-packages` |
| `ecosystems/` | Language or package manager | `npm-node`, `python-pip` |
| `artifact-types/` | Kind of dependency | `github-actions`, `mcp-servers-connectors` |
| `contexts/` | Risk level | `production`, `regulated-sensitive` |

If a file covers two variables, split it.

## File structure

```markdown
# {Title}

> {One-line description}

## When to use this

{1-2 sentences. Overlays end with "Requires a foundational file."}

## Instructions

- **{PREFIX}-1 (NOTE)** {What to do}. *Why:* {one line}.
- **{PREFIX}-2 (ASK)** {Condition that needs approval}. *Why:* {one line}.

## Examples

Good: `{command or snippet}`

Avoid: `{command or snippet}`
```

Context overlays also have a "Level shifts" table and, if they change a number, a "Tunable thresholds" table.

## Rules for rules

- Every rule has an ID with a prefix unique to its file, one level (`BLOCK`, `ASK` or `NOTE`) and a one-line `*Why:*`.
- Default to `NOTE`. Use `ASK` only when the event is rare and the risk is high. Use `BLOCK` only when there is no legitimate reason to proceed. In the pull request, say how often the rule will fire on ordinary work and why that is worth it.
- Do not restate a foundational rule. Refer to it by ID: "apply AGE-1".
- Put numbers in a "Tunable thresholds" table, never in rule text, and say whether the default has evidence behind it.
- Name only tools and settings you have checked exist, and say where you checked.
- Where a check may be impossible, tell the agent to report `not checked` and not to guess (EVD-1).

## Language

Do:

- use the imperative: "install an exact version"
- be specific: "`name:tag@sha256:...`", not "pin images"
- give the agent something it can do or check

Do not:

- write vague guidance: "use secure dependencies"
- write an absolute without a reason
- recommend one vendor's product as the only way to meet a rule
- state an incident, statistic or standards mapping without a dated source
- say the policy prevents, ensures or enforces anything

## Testing

1. Run `make build && make check`.
2. Try it with at least one agent. Ask for something the rule should allow and something it should stop, and say in the pull request what happened.
3. Check for conflicts with existing rules and for duplication.
4. If the rule can be exercised mechanically, add an eval scenario.

## Review

Reviewers look for: a stated reason for any friction, sources for facts, no duplication of foundational rules, wording an agent can act on, and passing checks.

## Conduct

Be respectful, assume good intent, and give feedback on the work. Harassment, discrimination and personal attacks are not acceptable.

## Licence

Contributions are licensed under the MIT License.
