# Security

## What counts as a security problem here

This repository contains instructions for AI agents and a few scripts. A security problem is, for example:

- a rule or example that tells an agent to do something unsafe
- text in a policy file that could be used to manipulate an agent
- a flaw in `enforcement/ci/check_pins.py` that makes it pass something it claims to catch
- an eval shim that can reach the network or install something

A rule that is merely too strict or too loose is not a security problem; use the "Rule misfired" issue template.

## Reporting

Use GitHub's private vulnerability reporting for this repository (Security tab, "Report a vulnerability") if it is available. Otherwise open an issue that says a security report is waiting, without the details, and a maintainer will arrange a private channel.

## If you use these files

Treat a preset like any other third-party input: read it before giving it to an agent, vendor a copy at a specific commit, and review the diff when you update it. The `agent-skills` overlay in this repository says the same thing about every third-party skill, including this one.
