# Ruby / Bundler

> How to apply the foundational rules with Bundler and RubyGems.

## When to use this

Apply to Ruby projects. Requires a foundational file.

## Instructions

- **GEM-1 (NOTE)** Use `https://rubygems.org/api/v1/versions/<gem>.json` for each version's `created_at` date (AGE-1, AGE-2) and `https://rubygems.org/api/v1/gems/<gem>.json` for the linked source repository (AGE-3). The API does not show which account pushed a version; report `PUB-1: not checked`. *Why:* these are the facts the rules depend on.
- **GEM-2 (NOTE)** If the project sets a Bundler `cooldown` (Bundler 4.0.13 or later), rely on it and report its value. Otherwise apply AGE-1 yourself. Do not lower it; that needs an ASK. *Why:* config is enforced, instructions are not.
- **GEM-3 (NOTE)** Commit `Gemfile.lock` with the `Gemfile` change. In CI, install with the `frozen` setting on. After adding a gem, confirm the lockfile holds the version you intended. *Why:* PIN-1; a `Gemfile` requirement is usually a range.
- **GEM-4 (ASK)** Adding a `git:`, `github:` or `path:` source for a gem, or a second `source` in the `Gemfile`. *Why:* SRC-1; a second source can serve a different gem under the same name.
- **GEM-5 (NOTE)** Gems with native extensions run their build code at install time, and this cannot be switched off. State when a new gem has native extensions. This replaces SCR-1 for Ruby; it becomes an ASK only when AGE-2 or AGE-3 also applies. *Why:* many widely used gems build native code, so asking every time would be noise.
- **GEM-6 (ASK)** Installing a gem outside the bundle with `gem install`. *Why:* it is not recorded in the `Gemfile` or the lockfile.
- **GEM-7 (NOTE)** If the project uses a dependency audit tool, run it and report new advisories. *Why:* known-bad versions are the cheapest thing to catch.

## Examples

Good: `bundle add rack --version "3.1.8"`

Avoid: `gem "rack", git: "https://github.com/someone/rack"`
