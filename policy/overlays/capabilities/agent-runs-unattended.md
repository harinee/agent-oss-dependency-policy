# Agent Runs Unattended

> Fail-closed behaviour when no human is available to answer.

## When to use this

Apply when the agent runs with no human in the session: scheduled jobs, CI, background agents. Requires a foundational file.

## Instructions

- **UNA-1 (BLOCK)** Assume nobody can answer. Do not wait or prompt. Every ASK is handled by AUT-1: skip that dependency and log it. *Why:* an unanswered question must not become a yes.
- **UNA-2 (NOTE)** Log one line per skipped item: `ecosystem:name@version`, rule ID, reason. Put it in the PR description if you open one, otherwise in the job output. *Why:* a human needs to see what was not done.
- **UNA-3 (BLOCK)** Never use OVR-1. Never edit the approved list, the overrides file, a script allowlist, a threshold or this policy. *Why:* those are the human controls.
- **UNA-4 (BLOCK)** If skipping makes the task impossible, stop and report. Do not reach the same code another way: copying source in by hand, another registry, a fork, a different package with the same code. *Why:* a workaround defeats the rule it avoids.
- **UNA-5 (NOTE)** FIX-1 is allowed when all three of its conditions are confirmed. Record the advisory ID and where you verified it. If the package manager's own cooldown refuses the install, do not lift it: log the advisory, the fixed version and the one-off command so a human can apply the fix at once. *Why:* security fixes should not wait for a human, but an unattended agent must not switch off an enforced control.
- **UNA-6 (NOTE)** If a package needs an install script that is not allowlisted, install with scripts off and report whether it works. *Why:* SCR-1 without a human.
