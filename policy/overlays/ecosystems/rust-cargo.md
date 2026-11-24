# Rust / Cargo

> How to apply the foundational rules with Cargo and crates.io.

## When to use this

Apply to Rust projects. Requires a foundational file.

## Instructions

- **RS-1 (NOTE)** Use `https://crates.io/api/v1/crates/<name>/<version>` for the foundational checks: `created_at` is the publish time (AGE-1) and `published_by` is the account (PUB-1). Send a User-Agent header. *Why:* these are the facts the rules depend on.
- **RS-2 (NOTE)** If the project's Cargo config sets a minimum publish age (`registry.global-min-publish-age`, Rust 1.100 or later), rely on it and report its value. Otherwise apply AGE-1 yourself. Do not lower the setting; that needs an ASK. *Why:* config is enforced, instructions are not.
- **RS-3 (NOTE)** After `cargo add`, confirm `Cargo.lock` holds the version you intended (`cargo update -p <name> --precise <version>` sets it). Commit `Cargo.lock` for applications. Build with `--locked` in CI. *Why:* PIN-1; a requirement like `1.2.3` in `Cargo.toml` is a range.
- **RS-4 (NOTE)** Build scripts (`build.rs`) and procedural macros run code at build time and cannot be switched off. State when a new crate has either. This replaces SCR-1 for Rust; it becomes an ASK only when AGE-2 or AGE-3 also applies. *Why:* most widely used crates have them, so asking every time would be noise.
- **RS-5 (ASK)** Adding a `git` or `path` dependency, or a `[patch]` section. *Why:* SRC-1.
- **RS-6 (NOTE)** `cargo install` builds and installs a binary: apply every rule first and use `--version <exact> --locked`. *Why:* same exposure as `npx`.
- **RS-7 (NOTE)** If the project uses `cargo audit`, `cargo deny` or `cargo vet`, run it and report new findings. Do not loosen its configuration; that needs an ASK. *Why:* these are the project's own checks.

## Examples

Good: `cargo add serde@1.0.215` then `cargo build --locked`

Avoid: `cargo add some-crate --git https://github.com/someone/fork`
