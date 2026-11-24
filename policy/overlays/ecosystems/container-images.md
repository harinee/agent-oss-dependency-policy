# Container Images

> How to apply the foundational rules to base images and images in manifests.

## When to use this

Apply when writing Dockerfiles, Compose files, Kubernetes manifests or CI steps that pull images. Requires a foundational file.

## Instructions

- **IMG-1 (NOTE)** Apply PIN-5: write `name:tag@sha256:<digest>`. Get the digest from the registry yourself (`docker pull` prints it). Keep the tag so readers can see the version. *Why:* the digest is the only immutable reference.
- **IMG-2 (NOTE)** State the registry and publisher namespace of any new image. Apply ID-2 to image names. *Why:* lookalike namespaces exist on every registry.
- **IMG-3 (NOTE)** Apply AGE-1 to tags where the registry shows when a tag was pushed. Otherwise report `AGE-1: not checked`. *Why:* a re-pushed tag is the image form of a hijacked release.
- **IMG-4 (NOTE)** When updating, change tag and digest together and say what changed. Never update a digest without knowing which version it is. *Why:* keeps updates reviewable.
- **IMG-5 (NOTE)** SRC-2 applies inside `RUN` instructions. A file downloaded in a Dockerfile must be checked against a checksum written in the Dockerfile. *Why:* a build that fetches unverified code is not pinned.
- **IMG-6 (NOTE)** Packages installed inside the image follow the same rules as the project's own dependencies. *Why:* the image is part of the supply chain.

## Examples

Good: `FROM python:3.12.7-slim@sha256:<digest>`

Avoid: `FROM python:latest`, `FROM python:3.12`, `RUN curl -sSL https://example.com/install.sh | sh`
