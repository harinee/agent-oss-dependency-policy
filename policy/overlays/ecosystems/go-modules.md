# Go Modules

> How to apply the foundational rules with the Go toolchain.

## When to use this

Apply to Go projects. Requires a foundational file.

## Instructions

- **GO-1 (NOTE)** Use `go list -m -json <module>@<version>` for the version's timestamp and `go list -m -versions <module>` for the available versions. *Why:* these are the facts AGE-1 depends on.
- **GO-2 (NOTE)** The Go toolchain has no release-age setting. Apply AGE-1 yourself and request an exact version: `go get <module>@v1.2.3`. Do not use `@latest` without checking what it resolves to. *Why:* nothing enforces the cooldown for you here.
- **GO-3 (NOTE)** A module path is a repository address. Check the host and owner are the ones you mean. *Why:* ID-2; lookalike owners and paths are the Go form of typosquatting.
- **GO-4 (ASK)** Changing checksum or proxy behaviour: `GOSUMDB=off`, `GONOSUMDB`, `GOPRIVATE`, `GOINSECURE`, `GOFLAGS=-mod=mod`. *Why:* these turn off the checksum database or let `go.mod` change silently.
- **GO-5 (ASK)** Adding a `replace` directive that points to a fork or a local path. *Why:* SRC-1; the build then uses code other than the module named.
- **GO-6 (NOTE)** Commit `go.mod` and `go.sum` together. *Why:* PIN-1.
- **GO-7 (NOTE)** Go modules have no install scripts, so SCR-1 rarely applies. `go run <module>@<version>` and `go install <module>@<version>` do execute downloaded code: apply every rule first and give an exact version. *Why:* same exposure as `npx`.
- **GO-8 (NOTE)** If the project uses `govulncheck`, run it and report new findings. *Why:* known-bad versions are the cheapest thing to catch.

## Examples

Good: `go get github.com/google/uuid@v1.6.0`

Avoid: `go get github.com/google/uuid@latest`, `GOFLAGS=-mod=mod go build ./...`
