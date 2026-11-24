# Threat coverage

Draft, 2026-11-24. This table checks the instruction files in this repo against recent supply-chain incidents relevant to AI-assisted development. It describes the files as they are today, including what they miss.

## How to read this

**Scope test.** An incident is in scope only if an agent's own decisions (what to select, install, pin, run, trust or read) can reduce the risk or the blast radius. It is out of scope where only the publisher, maintainer or CI owner can fix it, such as hardening a release pipeline, protecting runner tokens or running signing infrastructure. Many incidents are in scope for the consumer side only.

**Limits.** These files are instructions to an agent. An agent can ignore them. They cannot stop a compromise of a package that looks legitimate; the most they can do is make the agent less likely to be the first to install it, and limit what runs when it does.

**Sourcing.** One source per incident, read on 2026-11-24. Details not stated by the source are marked as such. The "Rule addressing it" column names files in this repo as they stand now.

## Coverage table

| Incident | Date | Vector | In scope? | Rule or overlay addressing it today | Gap |
|---|---|---|---|---|---|
| **Shai-Hulud, TensorLake wave** (`tensorlake@0.5.144` on npm) [1] | 2026-10-08; flagged about 11 minutes after publication | A `preinstall` script ran a payload shipped inside the package. It stole credentials and AI-tool and MCP configuration. The source does not state how the publisher was compromised. | Yes: version choice and install scripts | `skills/overlays/ecosystems/npm-node.skills.md` ("be cautious of packages with install scripts"). The foundational files only cover scripts that download more code, which this one did not need to. | No version-age cooldown. No default-off rule for install scripts. |
| **Axios** (`axios@1.14.1`, `0.30.4` on npm) [2] | 2026-03-31; live about 3 hours | A compromised maintainer account published versions that added a new dependency whose `postinstall` downloaded a remote-access tool. | Yes: version choice, lockfile discipline, install scripts | `skills/foundational/oss-selection-baseline.skills.md` (exact versions, committed lockfiles); `skills/overlays/ecosystems/npm-node.skills.md` (`npm ci`). These help only if no update happened in the window. | No cooldown. No rule to check a lockfile diff for an unexpected new transitive package. |
| **ChainDrop** (keyv and cacheable packages on npm; 444 packages per the source) [3] | 2026-08-04; spread over about 4 hours | A compromised maintainer identity. A `preinstall` script ran a payload shipped in the package, which spread using stolen tokens and planted hooks in `.claude/settings.json` and `.vscode/tasks.json`. Headline packages were published through trusted publishing with valid SLSA provenance. | Yes: version choice, install scripts, how much weight provenance gets | None effective. `skills/foundational/oss-selection-strict.skills.md` says to prefer packages with provenance, which these had. | No cooldown (the source recommends 3 to 7 days). No provenance caveat. No install-script default. |
| **Miasma** (`@redhat-cloud-services` packages on npm; at least 32 releases) [4] | 2026-06-01; most versions revoked within hours | A compromised employee GitHub account added a workflow that published through OIDC. A `preinstall` script ran an obfuscated stealer that republished other packages. Releases carried valid SLSA provenance. | Consumer side: yes. The account compromise and workflow hardening: out of scope. | None effective, as for ChainDrop. | Same as ChainDrop. |
| **Slopsquatting** (package names invented by LLMs, then registered by attackers) [5] | Examples from 2024 to February 2026 | An agent or developer installs a name the model made up. | Yes: this is the agent's own selection | `skills/foundational/oss-selection-baseline.skills.md` ("verify package names carefully to avoid typosquatting"), one line. | No rule to confirm the package exists and is the intended one before installing. No lookalike check. Download counts are treated as a trust signal. |
| **LiteLLM 1.107.0** (PyPI wheels and official Docker images) [6] | 2026-10-21; wheels live about 1 hour 43 minutes | A leaked key gave an attacker an organisation owner token. The artifacts were built, signed and published by the legitimate pipeline, with provenance naming a lookalike repository. No install script: a `.pth` file ran a stealer at every Python start. | Consumer side: yes (version choice, exact pins, image digests). The key leak: out of scope. | `skills/overlays/ecosystems/python-pip.skills.md` (exact pins); `skills/overlays/ecosystems/container-images.skills.md` (digests, as an optional extra). | No cooldown. No provenance caveat or check that the named source repository is the expected one. Preferring wheels does not help here. Digest pinning is optional. |
| **TeamPCP chain** (Trivy actions, Checkmarx KICS actions, LiteLLM 1.82.7 and 1.82.8) [7] | 2026-03-19 to 2026-03-23 | A compromised service account force-pushed malicious code to 76 of 77 `trivy-action` version tags. Stolen tokens were used to do the same to KICS action tags and to upload malicious LiteLLM releases, one with a `.pth` payload. | Consumer side: yes (how Actions are referenced, version choice). Token theft and the publishers' pipelines: out of scope. | `skills/overlays/artifact-types/ci-actions-build-tools.skills.md` allows "specific versions or commit SHAs", so tag references pass. This overlay is in no packaged preset. | Full commit SHA is not required. No cooldown. The reported Bitwarden CLI stage is not covered by the source used and is not assessed here. |
| **elementary-data 0.23.3** (PyPI and a GHCR image, including `:latest`) [8] | 2026-04-24; live about 8 to 10 hours | Script injection through a pull-request comment gave an attacker the repository token, which was used to tag a release. The legitimate pipeline published it. Payload was a `.pth` credential stealer. | Consumer side: yes (version choice, no `latest`). The workflow injection: out of scope. | `skills/foundational/oss-selection-baseline.skills.md` (avoid `latest`, pin versions). | No cooldown. Digest pinning is optional. |
| **postmark-mcp** (MCP server on npm) [9] | 2025-09-15 to 2025-09-25 | A package published by an individual account added a hidden BCC of every outgoing email in a later release. The source could not establish whether the publisher had any link to the vendor. | Yes: selection, pinning and updating of an MCP server | `skills/overlays/artifact-types/mcp-servers-connectors.skills.md` (prefer official servers, pin versions, no unreviewed auto-update). This is the best existing coverage, but the overlay is in no packaged preset. | No check that the publisher is the vendor it names. No cooldown on MCP server updates. |
| **ContextCrush** (Context7 MCP server) [10] | Disclosed 2026-03-05; fixed 2026-02-23 | Any registered library owner could set "custom rules" that the genuine server delivered verbatim to coding agents. No exploitation in the wild was reported. | Yes: what the agent treats as an instruction | None. | No rule that documentation feeds, tool descriptions and tool output are data, not instructions. |
| **GlassWorm** (Open VSX and VS Code extensions) [11] | From 2025-10-17 | Malicious new versions of existing extensions reached users through extension auto-update and spread with stolen credentials. | Partly: an agent choosing or recommending extensions is in scope. Auto-update on a user's editor is the user's setting. | None. `docs/design-principles.md` mentions plugins as dependencies; no skill file has rules for them. | No IDE extension rules. |
| **Clinejection and `cline@2.3.0`** [12] | 2026-02-17; live about 8 hours | A GitHub issue title prompt-injected an AI triage agent in CI into running `npm install` from an attacker's fork. That exposed publish tokens, which were used to publish a version whose `postinstall` installed another global package. | Both sides: an agent acting on untrusted issue text is in scope; so are version choice and install scripts for consumers. Token hygiene: out of scope. | None for the injection. `skills/overlays/ecosystems/npm-node.skills.md` for install scripts, weakly. | No untrusted-input rule. No cooldown. No install-script default. |

## What the table shows

- Nine of the twelve rows are a malicious **new version of an established package, action or extension**. Six of them state how long the version stayed available: between about 1 hour 43 minutes and about 10 hours. GlassWorm is the exception among those with timing: some extensions were still downloadable three days later. The current files check package age, which passes all nine.
- Three rows carried **valid provenance attestations** (ChainDrop, Miasma, LiteLLM 1.107.0), and a fourth was published by the project's legitimate pipeline (elementary-data). The current files recommend provenance without qualification.
- Five rows ran through an **install script**. In at least three of them (TensorLake, ChainDrop, Miasma) the malicious payload was inside the package, not downloaded by the script. Three rows used a **`.pth` file**, which runs without any install script, so script controls do not address it.
- Two rows are **instructions reaching the agent through content it reads**. The current files have no rule for that.

## Sources

| # | Source | Published |
|---|---|---|
| 1 | Socket, https://www.socket.dev/blog/tensorlake-compromise | 2026-10-08 |
| 2 | Snyk, https://snyk.io/jp/blog/axios-npm-package-compromised-supply-chain-attack-delivers-cross-platform/ | 2026-03-31 |
| 3 | StepSecurity, https://www.stepsecurity.io/blog/chaindrop-npm-worm | 2026-08-04 |
| 4 | Snyk, https://snyk.io/blog/miasma-supply-chain-attack-malicious-code-redhat-cloud-services-npm-packages/ | 2026-06-01 |
| 5 | Aikido, https://aikido.dev/blog/slopsquatting-ai-package-hallucination-attacks | 2026-02-20 |
| 6 | StepSecurity, https://www.stepsecurity.io/blog/litellm-1-107-0-compromised-pypi-backdoored-wheels-credential-stealer | 2026-10-21 |
| 7 | Palo Alto Networks Unit 42, https://unit42.paloaltonetworks.com/teampcp-supply-chain-attacks/ | 2026-03-31, updated 2026-04-09 |
| 8 | Snyk, https://snyk.io/blog/malicious-release-of-elementary-data-pypi-package-steals-cloud-credentials-from-data-engineers/ | 2026-04-28 |
| 9 | Snyk, https://snyk.io/blog/malicious-mcp-server-on-npm-postmark-mcp-harvests-emails | 2025-09-25 |
| 10 | Noma Security, https://noma.security/blog/contextcrush-context7-the-mcp-server-vulnerability/ | 2026-03-05 |
| 11 | BleepingComputer, https://bleepingcomputer.com/news/security/self-spreading-glassworm-malware-hits-openvsx-vs-code-registries | 2025-10-20 |
| 12 | Snyk, https://snyk.io/blog/cline-supply-chain-attack-prompt-injection-github-actions | 2026-02-19 |

Background on package-name hallucination: Spracklen et al., "We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs", USENIX Security 2025, https://www.usenix.org/conference/usenixsecurity25/presentation/spracklen. Across 16 models and 576,000 code samples, hallucinated packages averaged at least 5.2% for commercial models and 21.7% for open-source models.

## Not assessed

- The Bitwarden CLI stage reported for the TeamPCP chain.
- Later waves of GlassWorm and other extension incidents.
- Malicious container images outside the two image cases above.
