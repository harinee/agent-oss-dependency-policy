# Why this exists

## What changed

AI coding agents now read requirements, write code, choose dependencies and run install commands, often with nobody reviewing each step. Dependency governance was designed for people making a few deliberate choices. An agent makes many, quickly, and with habits that attackers can predict.

| What an agent can do | Why it matters |
|---|---|
| Add several dependencies in one step | Faster than a person reviews them |
| Edit manifests and lockfiles | Changes that are easy to skim past in review |
| Pull in transitive dependencies | Dozens of packages nobody chose by name |
| Install tools, MCP servers and extensions | These run with access to code, credentials and the agent itself |
| Add CI actions | These run with access to secrets and deploy credentials |
| Choose base images | Everything in the image ships |

## The risks

### Malicious and hijacked packages

Attackers publish malicious packages under plausible names, or take over the account of a real maintainer and publish a bad version of a real package.

- event-stream, 2018: a malicious dependency was added to a popular package and downloaded nearly 8 million times; the payload targeted one wallet application ([Snyk](https://snyk.io/blog/a-post-mortem-of-the-malicious-event-stream-backdoor/)).
- ua-parser-js, 2021: hijacked versions installed a cryptominer ([GitHub advisory](https://github.com/advisories/GHSA-pjwm-rvh2-c87w)).
- colors.js and faker.js, 2022: sabotaged by their own maintainer ([BleepingComputer](https://www.bleepingcomputer.com/news/security/dev-corrupts-npm-libs-colors-and-faker-breaking-thousands-of-apps/)).

Incidents from 2025 and 2026, including several that targeted AI coding agents directly, are in [threat-coverage.md](threat-coverage.md). The pattern there is consistent: a bad new version of a trusted package, live for a few hours.

An agent is exposed in two specific ways. It may install a package name it invented. And it tends to take the newest version, which is exactly what a hijacker has just published.

### Unpinned references

A version range, a `latest` tag, or an Action referenced by tag can resolve to something different tomorrow.

```json
"dependencies": {
  "express": "^4.0.0",
  "lodash": "*",
  "axios": "latest"
}
```

Pinning alone is not enough. An agent that picks the newest version on the day it is published pins the malicious one. That is why the policy adds a version cooldown.

### Compromised privileged tools

Build tools, scanners and CI actions run with more access than a library does.

- Codecov, 2021: a modified uploader script exported credentials from customers' CI environments ([Codecov](https://about.codecov.io/security-update/)).
- SolarWinds, 2020: a compromised build system shipped a backdoor in signed updates ([CISA, FBI and ODNI joint statement](https://www.cisa.gov/news-events/news/joint-statement-federal-bureau-investigation-fbi-cybersecurity-and-0)).

### Code that runs at install time

Many package managers run scripts from a package when it is installed. Recent npm malware used this to run its payload before any code was imported.

### Instructions hidden in content

Agents read READMEs, issues, documentation feeds and tool output. Text placed there can be written to look like instructions. This risk is new with agents and has no counterpart in older dependency guidance.

## What these files do

They give the agent short, specific rules in the place it reads instructions:

- check that a package exists and is the one intended
- prefer a version that has been public for a few days
- keep install scripts off unless approved
- pin by exact version, commit SHA or digest
- treat content read while working as data, not instructions
- stop and ask before adding privileged tools

The rules are tuned by context (prototype, production, regulated) and come with ecosystem-specific commands.

## What they do not do

They are advice to the agent, not a security control. An agent can ignore them. They sit alongside other layers and replace none of them.

| Layer | Role |
|---|---|
| Agent policy (this repository) | Steers the agent before a dependency is chosen |
| Package-manager and CI configuration | Enforces what can be enforced |
| Scanning and SBOM tools | Find known problems in what was added |
| Code review | A person decides |
| Incident response | Deals with what got through |

The policy is the weakest of these, because it can be ignored. It is also the only one that acts at the moment of choice.

See [limitations.md](limitations.md) for what it cannot do, and [how-to-choose.md](how-to-choose.md) to pick a preset.
