# Java / Maven / Gradle Ecosystem

> How to apply the foundational rules with Maven and Gradle.

## When to use this

Apply to JVM projects. Requires a foundational file.

## Instructions

- **JVM-1 (NOTE)** Neither Maven nor Gradle has a built-in release-age setting that we could find. Apply AGE-1 yourself: look up the version's publish date in the repository's metadata before choosing it. *Why:* nothing enforces the cooldown for you here.
- **JVM-2 (NOTE)** Use exact versions. No version ranges, no dynamic versions (`1.+`, `latest.release`). `SNAPSHOT` versions in a release build need an ASK. *Why:* PIN-1; these resolve to something different later.
- **JVM-3 (NOTE)** If the project uses Gradle dependency locking or dependency verification, update those files in the same change. Do not disable them. *Why:* they are the project's lockfile and integrity data.
- **JVM-4 (ASK)** Adding a repository that the build does not already use. *Why:* SRC-1; a second repository can serve a different artifact under the same coordinates.
- **JVM-5 (ASK)** Adding a Maven or Gradle plugin. Pin its version. *Why:* ART-1; plugins run code inside the build.
- **JVM-6 (NOTE)** Check the group ID belongs to the project you mean. *Why:* ID-2; lookalike group IDs are the JVM form of typosquatting.
- **JVM-7 (NOTE)** Use the right scope (`test`, `provided`, `runtime`). *Why:* test tools should not ship to production.

## Examples

Good: `implementation("com.fasterxml.jackson.core:jackson-databind:2.17.2")`

Avoid: `implementation("com.fasterxml.jackson.core:jackson-databind:2.+")`
