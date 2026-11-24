# npm / Node.js Ecosystem

> How to apply the foundational rules with npm, pnpm, Yarn and Bun.

## When to use this

Apply to Node.js projects. Requires a foundational file.

## Instructions

### Looking things up

- **NPM-1 (NOTE)** Use registry metadata for the foundational checks: `npm view <pkg> time --json` gives every version's publish date (AGE-1, AGE-2); `npm view <pkg>@<version> _npmUser` gives who published that version (PUB-1); `npm view <pkg> repository` gives the linked repository (AGE-3). *Why:* these are the facts the rules depend on.

### Cooldown

- **NPM-2 (NOTE)** If the project sets a release-age option (`min-release-age` in npm, `minimumReleaseAge` in pnpm or Bun, `npmMinimalAgeGate` in Yarn), rely on it and report its value. Do not lower it or add exclusions; that needs an ASK. *Why:* config is enforced, instructions are not.

### Installing

- **NPM-3 (NOTE)** Install exact versions: `npm install --save-exact <pkg>@<version>`. In CI use the frozen install (`npm ci` or the package manager's equivalent). *Why:* PIN-1.
- **NPM-4 (NOTE)** `npx`, `pnpm dlx` and `bunx` download and run a package at once. Treat them as an install: apply every rule first and give an exact version. *Why:* they skip the lockfile entirely.
- **NPM-5 (NOTE)** Put packages in the right section (`dependencies` or `devDependencies`). *Why:* dev tools should not ship to production.
- **NPM-6 (NOTE)** If you use `--force`, say why in one line. *Why:* it overrides conflict checks.

### Install scripts

- **NPM-7 (NOTE)** Apply SCR-1 with the project's package manager. If it already blocks dependency scripts by default, leave that on. Otherwise install with `--ignore-scripts`. Record approved packages in the manager's allowlist (`allowScripts` in npm, `allowBuilds` in pnpm, `trustedDependencies` in Bun, `dependenciesMeta` in Yarn). Never use an allow-all option. *Why:* SCR-1.

### After installing

- **NPM-8 (NOTE)** Run `npm audit` and report new advisories. `npm audit signatures` checks registry signatures and provenance; report its result under PRV-1. *Why:* known-bad versions are the cheapest thing to catch.

## Examples

Good: `npm install --save-exact --ignore-scripts left-pad@1.3.0`

Avoid: `npm install left-pad`, `npx some-tool`, `npm install --ignore-scripts=false`
