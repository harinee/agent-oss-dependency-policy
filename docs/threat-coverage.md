# Threat coverage

Last reviewed 2026-11-24. This table checks the policy files in this repository against recent supply-chain incidents relevant to AI-assisted development, and says what remains uncovered.

## How to read this

**Scope test.** An incident is in scope only if an agent's own decisions (what to select, install, pin, run, trust or read) can reduce the risk or the blast radius. It is out of scope where only the publisher, maintainer or CI owner can fix it, such as hardening a release pipeline, protecting runner tokens or running signing infrastructure. Many incidents are in scope for the consumer side only.

**"Addressed" means a rule exists, not that it works.** These files are instructions to an agent. An agent can ignore them, and whether agents follow them has not been measured here (see [`evals/`](../evals/README.md)). They cannot stop a compromise of a package that looks legitimate; at best they make the agent less likely to be among the first to install it, and limit what runs when it does.

**Sourcing.** One source per incident, read on 2026-11-24. Details not stated by the source are marked as such. Foundational rules (IDs without an overlay prefix) are in both files under `policy/foundational/`.

## Coverage table

| Incident | Date | Vector | In scope? | Rule or overlay addressing it | Gap |
|---|---|---|---|---|---|
| **Shai-Hulud, TensorLake wave** (`tensorlake@0.5.144` on npm) [1] | 2026-10-08; flagged about 11 minutes after publication | A `preinstall` script ran a payload shipped inside the package. It stole credentials and AI-tool and MCP configuration. The source does not state how the publisher was compromised. | Yes: version choice and install scripts | AGE-1 (cooldown), SCR-1 (install scripts off); `policy/overlays/ecosystems/npm-node.md` NPM-7 | A payload that runs when the package is imported, not installed, is not stopped by SCR-1. |
| **Axios** (`axios@1.14.1`, `0.30.4` on npm) [2] | 2026-03-31; live about 3 hours | A compromised maintainer account published versions that added a new dependency whose `postinstall` downloaded a remote-access tool. | Yes: version choice, lockfile discipline, install scripts | AGE-1, PUB-1, PIN-1, PIN-3 (unexpected new transitive package), SCR-1 | The cooldown applies to the version the agent selects. A transitive dependency resolved fresh can still be new unless the package manager enforces the cooldown (see `enforcement/`). |
| **ChainDrop** (keyv and cacheable packages on npm; 444 packages per the source) [3] | 2026-08-04; spread over about 4 hours | A compromised maintainer identity. A `preinstall` script ran a payload shipped in the package, which spread using stolen tokens and planted hooks in `.claude/settings.json` and `.vscode/tasks.json`. Headline packages were published through trusted publishing with valid SLSA provenance. | Yes: version choice, install scripts, how much weight provenance gets | AGE-1, SCR-1, PRV-1 (provenance never lowers a level); `policy/overlays/capabilities/agent-can-install-packages.md` INS-4 (stop if agent or editor configuration changed) | INS-4 detects the planted hooks after the fact; it does not prevent them. |
| **Miasma** (`@redhat-cloud-services` packages on npm; at least 32 releases) [4] | 2026-06-01; most versions revoked within hours | A compromised employee GitHub account added a workflow that published through OIDC. A `preinstall` script ran an obfuscated stealer that republished other packages. Releases carried valid SLSA provenance. | Consumer side: yes. The account compromise and workflow hardening: out of scope. | AGE-1, SCR-1, PRV-1 | Same as Shai-Hulud. |
| **Slopsquatting** (package names invented by LLMs, then registered by attackers) [5] | Examples from 2024 to February 2026 | An agent or developer installs a name the model made up. | Yes: this is the agent's own selection | ID-1 (name must resolve; no substitution), ID-2 (lookalikes), AGE-3 (new package with no repository or publisher history), ADP-1 (downloads are not evidence of safety) | A squatted name that has aged past `min_package_age_days` and links a plausible repository passes these checks. |
| **LiteLLM 1.107.0** (PyPI wheels and official Docker images) [6] | 2026-10-21; wheels live about 1 hour 43 minutes | A leaked key gave an attacker an organisation owner token. The artifacts were built, signed and published by the legitimate pipeline, with provenance naming a lookalike repository. No install script: a `.pth` file ran a stealer at every Python start. | Consumer side: yes (version choice, exact pins, image digests). The key leak: out of scope. | AGE-1, PRV-1 (check the source repository named), PIN-5 (digest); `policy/overlays/ecosystems/python-pip.md` PY-6 (report new `.pth` files) | PY-6 reports a `.pth` file after install; nothing prevents it running. The cooldown is the only rule that avoids the install. |
| **TeamPCP chain** (Trivy actions, Checkmarx KICS actions, LiteLLM 1.82.7 and 1.82.8) [7] | 2026-03-19 to 2026-03-23 | A compromised service account force-pushed malicious code to 76 of 77 `trivy-action` version tags. Stolen tokens were used to do the same to KICS action tags and to upload malicious LiteLLM releases, one with a `.pth` payload. | Consumer side: yes (how Actions are referenced, version choice). Token theft and the publishers' pipelines: out of scope. | PIN-4 (Actions by commit SHA); `policy/overlays/artifact-types/github-actions.md`; `policy/overlays/artifact-types/scanners-security-tools.md` SCN-2; AGE-1 | The source used does not itself recommend SHA pinning; that mapping is this repository's reading, supported by GitHub's guidance that tags can be moved. The reported Bitwarden CLI stage is not covered by the source and is not assessed. |
| **elementary-data 0.23.3** (PyPI and a GHCR image, including `:latest`) [8] | 2026-04-24; live about 8 to 10 hours | Script injection through a pull-request comment gave an attacker the repository token, which was used to tag a release. The legitimate pipeline published it. Payload was a `.pth` credential stealer. | Consumer side: yes (version choice, no `latest`). The workflow injection: out of scope for consumers; `policy/overlays/artifact-types/ci-actions-build-tools.md` CI-4 covers an agent writing such a workflow. | AGE-1, PIN-5; `policy/overlays/ecosystems/python-pip.md` PY-6 | Same as LiteLLM 1.107.0. |
| **postmark-mcp** (MCP server on npm) [9] | 2025-09-15 to 2025-09-25 | A package published by an individual account added a hidden BCC of every outgoing email in a later release. The source could not establish whether the publisher had any link to the vendor. | Yes: selection, pinning and updating of an MCP server | ART-1; `policy/overlays/artifact-types/mcp-servers-connectors.md` MCP-1 to MCP-4 | The malicious behaviour persisted for about a week, close to the default cooldown. A pinned, already-approved server is not re-examined. |
| **ContextCrush** (Context7 MCP server) [10] | Disclosed 2026-03-05; fixed 2026-02-23 | Any registered library owner could set "custom rules" that the genuine server delivered verbatim to coding agents. No exploitation in the wild was reported. | Yes: what the agent treats as an instruction | TRU-1; `policy/overlays/artifact-types/mcp-servers-connectors.md` MCP-5 | Depends entirely on the agent holding to the rule under a well-crafted injection. |
| **GlassWorm** (Open VSX and VS Code extensions) [11] | From 2025-10-17 | Malicious new versions of existing extensions reached users through extension auto-update and spread with stolen credentials. | Partly: an agent choosing or recommending extensions is in scope. Auto-update on a user's editor is the user's setting. | ART-1; `policy/overlays/artifact-types/ide-extensions.md` EXT-1 to EXT-4 | Extensions the user already has, with auto-update on, are outside the agent's decisions. |
| **Clinejection and `cline@2.3.0`** [12] | 2026-02-17; live about 8 hours | A GitHub issue title prompt-injected an AI triage agent in CI into running `npm install` from an attacker's fork. That exposed publish tokens, which were used to publish a version whose `postinstall` installed another global package. | Both sides: an agent acting on untrusted issue text is in scope; so are version choice and install scripts for consumers. Token hygiene: out of scope. | TRU-1, SRC-1, AGE-1, SCR-1; `policy/overlays/capabilities/agent-can-open-pr.md` PR-5; `policy/overlays/artifact-types/ci-actions-build-tools.md` CI-4 | Same as ContextCrush for the injection. |

## What the table shows

- Nine of the twelve rows are a malicious **new version of an established package, action or extension**. Six of them state how long the version stayed available: between about 1 hour 43 minutes and about 10 hours. GlassWorm is the exception among those with timing: some extensions were still downloadable three days later. This is why the version cooldown (AGE-1) is separate from package age.
- Three rows carried **valid provenance attestations** (ChainDrop, Miasma, LiteLLM 1.107.0), and a fourth was published by the project's legitimate pipeline (elementary-data). This is why PRV-1 treats provenance as information only.
- Five rows ran through an **install script**. In at least three of them (TensorLake, ChainDrop, Miasma) the malicious payload was inside the package, not downloaded by the script. This is why SCR-1 covers all install scripts, not just ones that fetch code.
- Three rows used a **`.pth` file**, which runs without any install script. No rule here prevents that; the cooldown avoids the install and PY-6 reports it afterwards.
- Two rows are **instructions reaching the agent through content it reads** (TRU-1).

## Gaps that apply to every row

- A malicious version that survives longer than the cooldown is not caught by any rule here.
- PUB-1 can be checked on npm and crates.io, which expose the publishing account per version. On PyPI, NuGet and RubyGems the agent reports it as not checked.
- All twelve incidents are assessed against npm, PyPI, Actions, images, MCP servers and extensions. None involved NuGet, RubyGems, Go or Cargo, so those overlays are untested against a real case.

See [limitations.md](limitations.md) for the full list.

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
