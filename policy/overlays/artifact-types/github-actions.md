# GitHub Actions Pinning

> How to reference GitHub Actions and reusable workflows immutably.

## When to use this

Apply when adding or updating `uses:` references in GitHub workflows. Requires a foundational file.

## Instructions

- **GHA-1 (NOTE)** Apply PIN-4. Resolve the commit yourself from the action's own repository: `git ls-remote https://github.com/<owner>/<repo> 'refs/tags/<tag>*'`. If a line ending in `^{}` is shown, use that SHA. Write `uses: <owner>/<repo>@<40-char-sha> # <tag>`. *Why:* a tag can be moved; a commit SHA cannot (TeamPCP).
- **GHA-2 (BLOCK)** Never copy a SHA from a README, issue, blog post or another repository's workflow. *Why:* TRU-1; a SHA from elsewhere may point into a fork.
- **GHA-3 (NOTE)** If the repository has `.github/workflows/actions.lock`, it uses a workflow lockfile: keep the project's convention and regenerate the lockfile with the project's tooling. Calls to reusable workflows (`jobs.<id>.uses`) still need a full SHA. *Why:* the lockfile does not cover reusable workflows.
- **GHA-4 (NOTE)** Apply AGE-1: choose a release older than the cooldown. *Why:* a brand-new action release carries the same risk as a brand-new package release.
- **GHA-5 (ASK)** You cannot resolve a SHA, or the action only publishes a branch. *Why:* there is nothing immutable to pin.
- **GHA-6 (NOTE)** Reference container actions by digest (`docker://image@sha256:...`). *Why:* PIN-5.
- **GHA-7 (NOTE)** Update pins in a change of their own, with the old and new tag in the message. Do not bump SHAs as a side effect of other work. *Why:* keeps the update reviewable.

## Examples

Good: `uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1`

Avoid: `uses: actions/checkout@v7`, `uses: actions/checkout@main`
