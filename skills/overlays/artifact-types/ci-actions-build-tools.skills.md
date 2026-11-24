# CI Actions and Build Tools

> Rules for CI workflows, pipeline plugins and build tools.

## When to use this

Apply when adding or changing CI workflows, pipeline plugins or build tooling on any CI system. For how to pin GitHub Actions, add `github-actions`. Requires a foundational file.

## Instructions

- **CI-1 (ASK)** Adding a new action, pipeline plugin, build plugin or CI integration. State what it will be able to reach: source, secrets, deploy credentials, artifacts. *Why:* ART-1; compromised CI tools leaked the credentials used in later attacks (TeamPCP).
- **CI-2 (NOTE)** Give a new job the smallest token permissions that work, and say what you set. *Why:* limits what a compromised step can do.
- **CI-3 (ASK)** Any workflow change that lets untrusted code or text reach secrets: running pull-request code from forks with secrets, privileged triggers that check out the PR head. *Why:* this is how publish tokens were taken (elementary-data).
- **CI-4 (BLOCK)** Do not write steps that paste issue, PR, comment or branch text straight into a shell command or an agent prompt. Pass it through an environment variable and treat it as data. *Why:* TRU-1; script and prompt injection (Clinejection, elementary-data).
- **CI-5 (NOTE)** Pin build plugins and tool installers to exact versions. AGE-1 applies to them. *Why:* a scanner or build tool is a dependency with more access than a library.
- **CI-6 (NOTE)** Do not add CI steps that install packages without the lockfile. Use the frozen install. *Why:* PIN-1.

## Examples

Avoid: `run: echo "${{ github.event.issue.title }}"`

Good: pass the title as `env: TITLE: ${{ github.event.issue.title }}` and use `"$TITLE"`.
