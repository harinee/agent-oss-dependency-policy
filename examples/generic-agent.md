# Example: general-purpose agent on a Node.js app

Illustrative. The behaviour described is what the policy asks for, not a recorded session.

## Context

- Node.js web application in development
- The agent can install packages and run shell commands
- A human is in the session

## Files

```
policy/foundational/oss-selection-baseline.md
policy/overlays/capabilities/agent-can-install-packages.md
policy/overlays/capabilities/agent-can-run-shell.md
policy/overlays/ecosystems/npm-node.md
```

The first three are the `baseline-general` preset; the npm overlay is added to it.

## What the policy asks for

**"Add express."** A mature package. The agent looks up the publish dates, installs the newest version older than 3 days with an exact version and scripts off, and reports one line. No question.

**"Add this package I found."** It was first published last week and has no linked repository. AGE-3 applies: the agent states that in two lines and waits.

**Adding a package with a native build step.** It needs its install script to work. SCR-1 applies: the agent asks once, and after approval adds it to the script allowlist so it does not ask again.

## Moving on

- Going to production: switch to the strict foundation or add `policy/overlays/contexts/production.md`.
- Adding CI: add `policy/overlays/artifact-types/github-actions.md`.
- The agent opens pull requests: add `policy/overlays/capabilities/agent-can-open-pr.md`.
