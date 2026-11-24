# Changelog

Notable changes to this project are recorded here.

## Unreleased

### Added

- EVD-1, missing evidence: a check that could not be completed is never a pass; unconfirmed package
  existence (ID-1) or version age (AGE-1) is an ASK, other checks proceed with `not checked`.
- LOC-1, local overrides: `.dependency-policy/overrides.md` changes rule levels and thresholds without
  editing the preset. ID-1, ID-3 and TRU-1 cannot be lowered there. Template in `examples/`.

- Rule IDs, a response level (BLOCK, ASK or NOTE) and a one-line rationale on every rule.
- Version-age cooldown (AGE-1), kept separate from package age and publisher change.
- "Tunable thresholds" table in each foundational file; defaults are labelled as hypotheses.
- Escape hatches: approved list, security-patch fast path, recorded override.
- Fail-closed behaviour when no human can answer, and an `agent-runs-unattended` overlay.
- Rules for install scripts, Actions by commit SHA, images by digest, provenance limits,
  lookalike names, publisher change, and content read by the agent as untrusted input.
- Overlays: Go, Rust, NuGet, RubyGems, GitHub Actions pinning, IDE extensions, third-party agent skills.
- Presets: `prototype-quick`, `java-production`, `go-service`, `rust-project`, `dotnet-project`,
  `ruby-project`, `agent-tooling`.
- `agent-skills/`: each preset as an Agent Skills folder with `SKILL.md` front matter.
- `enforcement/`: example package-manager, Dependabot and Renovate config, and a pin checker.
- `evals/`: scenario harness reporting catch rate and friction rate. No agent results are included.
- `scripts/build.py`, `scripts/selfcheck.py` and a CI workflow.
- `docs/threat-coverage.md`, `docs/response-model.md`, `docs/packaging.md`, `docs/limitations.md`.
- `CONTRIBUTING.md`, `SECURITY.md`, a `Makefile`, and issue and pull request templates.

### Changed

- **Renamed directories and files (breaking for copied paths).** `skills/` is now `policy/` and
  `packaged/` is now `presets/`; the `.skills.md` suffix is dropped (`packaged/baseline-general.skills.md`
  is now `presets/baseline-general.md`). The old names suggested these files were Agent Skills; only
  `agent-skills/` is. Preset names and `agent-skills/` paths are unchanged.
- The friction-model doc is now `docs/response-model.md` and explains each level by severity and
  confidence, with the count of rules per level checked by `scripts/selfcheck.py`.
- README and quick start rewritten around one adoption path: install one preset, per-agent commands,
  always-on versus on-demand, and what is advisory versus enforced.

- Presets are generated from `presets.json` as exact concatenations of their sources.
  Existing preset file names are unchanged; their content is longer and uses the new rules.
- Overlays refer to foundational rules by ID and no longer restate them.
- `npm-high-autonomy` now includes the unattended overlay.
- `docs/mapping-to-standards.md` cut down to mappings checked against the source.
- `examples/*.md` renamed to `examples/*.md`; they are documents, not policy files.
- Background docs rewritten in the same plain style as the README; emoji headings removed.
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
