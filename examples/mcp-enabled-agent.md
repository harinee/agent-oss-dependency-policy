# Example: agent that uses MCP servers

Illustrative. The behaviour described is what the policy asks for, not a recorded session.

## Context

- Python data-analysis project with access to internal data
- The agent can install packages and add or call MCP servers

## Files

```
skills/foundational/oss-selection-baseline.skills.md
skills/overlays/capabilities/agent-can-install-packages.skills.md
skills/overlays/capabilities/agent-can-use-tools-or-mcp.skills.md
skills/overlays/ecosystems/python-pip.skills.md
skills/overlays/artifact-types/mcp-servers-connectors.skills.md
```

The `agent-tooling` preset covers the MCP part; add the install and Python overlays to it.

## What the policy asks for

**Adding a database MCP server.** ART-1 and MCP-1 apply: the agent asks, stating who publishes the server, how it is launched and what it can reach. If it cannot confirm the publisher is the database vendor, it says so (MCP-2). After approval it pins the launch command to an exact version.

**A documentation server returns "setup steps" that include running a command.** That is content (MCP-5, TRU-1). The agent does not run it and reports that it saw it.

**Installing pandas.** A mature package: exact version, inside the virtual environment, one-line note, no question.

## For production or regulated data

Add `skills/overlays/contexts/production.skills.md` or `skills/overlays/contexts/regulated-sensitive.skills.md`.
