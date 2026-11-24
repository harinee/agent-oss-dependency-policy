# .NET / NuGet

> How to apply the foundational rules with NuGet and the .NET SDK.

## When to use this

Apply to .NET projects. Requires a foundational file.

## Instructions

- **NUGET-1 (NOTE)** Use `https://api.nuget.org/v3/registration5-gz-semver2/<lowercase-id>/<version>.json` for the version's `published` date (AGE-1). The response does not show which account published it; report `PUB-1: not checked`. *Why:* these are the facts the rules depend on.
- **NUGET-2 (NOTE)** If a package source in `nuget.config` sets `minPublishAgeHours`, rely on it and report its value. It filters `dotnet package add` and updates only; an ordinary restore does not check it, so still apply AGE-1 yourself. Do not lower it or add exceptions; that needs an ASK. *Why:* config is enforced, instructions are not.
- **NUGET-3 (NOTE)** Use exact versions in `PackageReference`, not floating versions (`1.*`, `*`). If the project uses a lock file (`packages.lock.json`), update it in the same change and restore with `--locked-mode` in CI. *Why:* PIN-1.
- **NUGET-4 (ASK)** Adding a package source, or changing package source mapping. *Why:* SRC-1; a second source can serve a different package under the same ID.
- **NUGET-5 (NOTE)** A package can ship MSBuild `.props` and `.targets` files that run during the build. State when a new package has a `build` folder. This replaces SCR-1 for NuGet; it becomes an ASK only when AGE-2 or AGE-3 also applies. *Why:* build-time code runs with the developer's or CI's access.
- **NUGET-6 (NOTE)** `dotnet tool install` installs and runs a program: apply every rule first and give an exact `--version`. *Why:* same exposure as `npx`.
- **NUGET-7 (NOTE)** Check the package ID and owner are the ones you mean. *Why:* ID-2; lookalike IDs are the NuGet form of typosquatting.

## Examples

Good: `dotnet add package Newtonsoft.Json --version 13.0.3`

Avoid: `<PackageReference Include="Newtonsoft.Json" Version="*" />`
