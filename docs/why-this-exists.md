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

## Where this acts

Most supply-chain controls act after the agent has already chosen and installed a package.

| Stage | Typical control | What has already happened |
|---|---|---|
| **Agent selects and installs** | **Usually nothing. This policy acts here.** | |
| Pull request | Review, software composition analysis, licence scan | Install scripts have run on the developer's machine or runner, with its credentials |
| Merge and build | SBOM, signing, provenance | The dependency is in the lockfile |
| Afterwards | Vulnerability alerts, incident response | The dependency is in production |

An agent adds three habits that attackers can predict: it installs names from memory, it takes the newest version, and it acts on text it reads.

## Attack patterns that keep recurring

The names change; the patterns do not. Each row is one sourced example and the rule that addresses the pattern.

| Pattern | Example | Rule |
|---|---|---|
| **Hijacked release of a trusted package**, removed within hours | `ua-parser-js`, 2021: three versions published from a hijacked maintainer account carried malware ([GitHub advisory](https://github.com/advisories/GHSA-pjwm-rvh2-c87w)) and were live for about four hours ([Rapid7](https://www.rapid7.com/blog/post/2021/10/25/npm-library-ua-parser-js-hijacked-what-you-need-to-know/)). `axios`, 2026: about three hours ([Snyk](https://snyk.io/jp/blog/axios-npm-package-compromised-supply-chain-attack-delivers-cross-platform/)). | AGE-1: do not take a version younger than the cooldown |
| **A new publisher** | `event-stream`, 2018: the maintainer handed the package to a volunteer, who added a malicious dependency ([issue thread](https://github.com/dominictarr/event-stream/issues/116)) | PUB-1: ask when the publisher changes |
| **Code that runs at install time** | Shai-Hulud, 2025: a self-replicating worm spread through post-install scripts across more than 500 npm packages ([CISA](https://www.cisa.gov/news-events/alerts/2025/09/23/widespread-supply-chain-compromise-impacting-npm-ecosystem)) | SCR-1: install scripts stay off |
| **Mutable tags** | `tj-actions/changed-files`, 2025: version tags were repointed to a commit that printed CI secrets to logs, in an action used by over 23,000 repositories ([GitHub advisory](https://github.com/advisories/GHSA-mrrh-fwg8-r2c3)) | PIN-4, PIN-5: Actions by commit SHA, images by digest |
| **Package names that do not exist** | Across 16 code-generating models, at least 5.2% of packages suggested by commercial models and 21.7% by open-source models were invented ([USENIX Security 2025](https://www.usenix.org/conference/usenixsecurity25/presentation/spracklen)). Attackers register such names. | ID-1: the name must resolve; no substitutes |
| **Instructions hidden in content** | Clinejection, 2026: a GitHub issue title prompt-injected an AI triage agent, which led to an unauthorised `cline` release ([Snyk](https://snyk.io/blog/cline-supply-chain-attack-prompt-injection-github-actions)) | TRU-1: content is data, not instructions |

Twelve recent incidents with sources, scope and the remaining gap for each: [threat-coverage.md](threat-coverage.md).

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
