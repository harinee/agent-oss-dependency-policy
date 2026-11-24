# Changelog

Notable changes to this project are recorded here.

## Unreleased

### Added

- Rule IDs, a response level (BLOCK, ASK or NOTE) and a one-line rationale on every rule.
- Version-age cooldown (AGE-1), kept separate from package age and publisher change.
- "Tunable thresholds" table in each foundational file; defaults are labelled as hypotheses.
- Escape hatches: approved list, security-patch fast path, recorded override.
- Fail-closed behaviour when no human can answer, and an `agent-runs-unattended` overlay.
- Rules for install scripts, Actions by commit SHA, images by digest, provenance limits,
  lookalike names, publisher change, and content read by the agent as untrusted input.
- Overlays: Go, Rust, GitHub Actions pinning, IDE extensions, third-party agent skills.
- Presets: `prototype-quick`, `java-production`, `go-service`, `rust-project`, `agent-tooling`.
- `agent-skills/`: each preset as an Agent Skills folder with `SKILL.md` front matter.
- `enforcement/`: example package-manager, Dependabot and Renovate config, and a pin checker.
- `evals/`: scenario harness reporting catch rate and friction rate. No agent results are included.
- `scripts/build.py`, `scripts/selfcheck.py` and a CI workflow.
- `docs/threat-coverage.md`, `docs/friction-model.md`, `docs/packaging.md`.

### Changed

- Presets are generated from `presets.json` as exact concatenations of their sources.
  Existing preset file names are unchanged; their content is longer and uses the new rules.
- Overlays refer to foundational rules by ID and no longer restate them.
- `npm-high-autonomy` now includes the unattended overlay.
- `docs/mapping-to-standards.md` cut down to mappings checked against the source.
- `examples/*.skills.md` renamed to `examples/*.md`; they are documents, not policy files.
- Install instructions now use `AGENTS.md` and locations checked against each agent's documentation.

### Removed

- Triggers that caused false positives: star counts, single maintainer, "unverified publisher",
  approval for any package newer than 3 months, and the 12-month rule in the regulated overlay.
- Incorrect standards mappings (SLSA "Build L4", two misnamed NIST SSDF practices, 2013 ISO numbering).


### Renamed

- Renamed the repository from `agent-oss-guardrails` to `agent-oss-dependency-policy` (2026-11-24).
  The files in this repo are advisory instructions for AI coding agents, not enforcement, so
  "guardrails" over-promised; "oss" states the scope. The old GitHub URL redirects to the new one.
  The suggested destination file name in the docs changed from `oss-guardrails.md` to
  `oss-dependency-policy.md`; existing copies under the old file name keep working.
