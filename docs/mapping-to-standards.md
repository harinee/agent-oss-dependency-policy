# Relation to standards and other guidance

These files do not implement any standard, and using them does not make a project compliant with one. This page lists places where published guidance asks for something that an agent's dependency decisions touch, so that teams working to those documents can see where this repository fits.

Only items checked against the source on 2026-11-24 are listed. Earlier versions of this page contained mappings that were wrong; they have been removed.

## NIST SSDF (SP 800-218 v1.1, February 2022)

| Practice or task | Text | Related rules |
|---|---|---|
| PW.4 | "Reuse Existing, Well-Secured Software When Feasible Instead of Duplicating Functionality" | DEP-1 |
| PW.4.1 | "Acquire and maintain well-secured software components (e.g., software libraries, modules, middleware, frameworks) from commercial, open-source, and other third-party developers for use by the organization's software." | ID-1 to ID-3, AGE-1 to AGE-3, PUB-1, SRC-1 |
| PW.4.4 | "Verify that acquired commercial, open-source, and all other third-party software components comply with the requirements, as defined by the organization, throughout their life cycles." | The policy is one way to state such requirements to an agent. It does not verify anything. |

Source: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf. A draft of version 1.2 was published on 2025-12-17 and had not been finalised when this was checked.

## OWASP Top 10 CI/CD Security Risks

| Risk | Related rules |
|---|---|
| CICD-SEC-3: Dependency Chain Abuse | AGE-1, ID-1, ID-2, PIN-1 to PIN-5, SCR-1 |
| CICD-SEC-4: Poisoned Pipeline Execution (PPE) | CI-3, CI-4 |
| CICD-SEC-8: Ungoverned Usage of 3rd Party Services | ART-1, CI-1 |

Source: https://owasp.org/www-project-top-10-ci-cd-security-risks/

## CIS Controls v8

| Safeguard | Text | Related rules |
|---|---|---|
| 16.4 | "Establish and Manage an Inventory of Third-Party Software Components" | PIN-1 (manifest and lockfile kept current) |
| 16.5 | "Use Up-to-Date and Trusted Third-Party Software Components" | The selection rules as a whole |

Source: https://controls-assessment-specification.readthedocs.io/en/latest/control-16/control-16.5.html

## SLSA

SLSA Build levels (L0 to L3 in the current specification, v1.2) are requirements on whoever builds and publishes an artifact. They are not requirements on choosing dependencies, and the specification has no consumer or dependency track. A consumer's role is to verify provenance.

That is why PRV-1 treats provenance as information and never as proof of safety: provenance shows where and how something was built. Three incidents in [threat-coverage.md](threat-coverage.md) shipped malicious releases with valid provenance.

Source: https://slsa.dev/spec/v1.2/build-track-basics

## Guidance on AI assistants

- **OpenSSF, "Security-Focused Guide for AI Code Assistant Instructions"** (2025-08-01). The closest published guidance to this repository. It includes "Do not add dependencies that may be malicious or hallucinated" and "Use popular, community-trusted libraries for common tasks." This repository goes further on version age, install scripts, pinning and untrusted content, and deliberately does not use popularity as a trust signal. https://best.openssf.org/Security-Focused-Guide-for-AI-Code-Assistant-Instructions
- **OWASP Top 10 for LLM Applications 2025, LLM03: Supply Chain.** Covers third-party package and model risk for LLM applications. https://genai.owasp.org/llmrisk/llm032025-supply-chain/
- **OWASP Top 10 for Agentic Applications for 2026** (2025-12-09). Not mapped here; the entry list was not read from the primary document. https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/

## Not mapped

ISO/IEC 27001, the EU Cyber Resilience Act and SBOM guidance were listed in earlier versions of this page. They are not mapped now because the mappings could not be checked against primary text.
