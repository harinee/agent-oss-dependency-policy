# 🛡️ Agent OSS Guardrails

> **Safe, composable instructions for AI agents managing open source dependencies**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](docs/contribution-guide.md)

---

## 🚀 Get Started in 3 Steps

### **Step 1: Copy a pre-packaged file** 📦
Choose based on your project type:

```bash
# ✨ Most common - General projects
cp packaged/baseline-general.skills.md .clinerules/oss-guardrails.md

# 🐍 Python production projects
cp packaged/python-sensitive-repo.skills.md .clinerules/oss-guardrails.md

# 🟢 Node.js with autonomous agent
cp packaged/npm-high-autonomy.skills.md .clinerules/oss-guardrails.md

# 🔒 High-autonomy agent needing strict controls
cp packaged/strict-agent-high-autonomy.skills.md .clinerules/oss-guardrails.md
```

### **Step 2: That's it!** ✅
Your AI agent will now follow these guardrails when selecting dependencies.

### **Step 3: (Optional) Customize** 🔧
Need different rules? See [📖 Advanced: Custom Combinations](#-advanced-custom-combinations) below.

---

## 🎯 What is this?

**Problem:** AI agents can add risky dependencies faster than humans can review them.

**Solution:** Give your AI agent clear, readable instructions on selecting safer dependencies.

**How it works:** These instruction files guide agents toward:
- ✅ Well-maintained packages
- ✅ Pinned versions
- ✅ Official registries
- ✅ Minimal dependencies
- ✅ Security best practices

**Compatible with:** Cursor, Cline, GitHub Copilot, Aider, Windsurf, and other AI coding agents

**Reality check:** These are guidelines, not security controls. They complement (not replace) scanning tools and code review.

---

## 📦 Pre-Packaged Options (Recommended)

| Package | When to Use | Command |
|---------|-------------|---------|
| **baseline-general** | Most projects, internal tools, learning | `cp packaged/baseline-general.skills.md .clinerules/` |
| **python-sensitive-repo** | Python production systems | `cp packaged/python-sensitive-repo.skills.md .clinerules/` |
| **npm-high-autonomy** | Node.js with autonomous agent | `cp packaged/npm-high-autonomy.skills.md .clinerules/` |
| **strict-agent-high-autonomy** | Agent with broad permissions | `cp packaged/strict-agent-high-autonomy.skills.md .clinerules/` |

> 💡 **Tip:** Start with `baseline-general` if unsure. You can always switch later!

---

## 🔧 Advanced: Custom Combinations

Want to customize? Build your own by combining files:

### **Foundation** (Pick one)
- `skills/foundational/oss-selection-baseline.skills.md` - Balanced safety
- `skills/foundational/oss-selection-strict.skills.md` - Maximum security

### **+ Add what your agent can do**
- `skills/overlays/capabilities/agent-can-install-packages.skills.md`
- `skills/overlays/capabilities/agent-can-run-shell.skills.md`
- `skills/overlays/capabilities/agent-can-use-tools-or-mcp.skills.md`
- `skills/overlays/capabilities/agent-can-open-pr.skills.md`

### **+ Add your tech stack**
- `skills/overlays/ecosystems/npm-node.skills.md`
- `skills/overlays/ecosystems/python-pip.skills.md`
- `skills/overlays/ecosystems/java-maven-gradle.skills.md`
- `skills/overlays/ecosystems/container-images.skills.md`

### **Example: Custom Node.js setup**
```bash
cat skills/foundational/oss-selection-baseline.skills.md \
    skills/overlays/capabilities/agent-can-install-packages.skills.md \
    skills/overlays/ecosystems/npm-node.skills.md \
    > .clinerules/oss-guardrails.md
```

**📖 Need help deciding?** See the [detailed selection guide](docs/how-to-choose.md)

---

## 📁 Repository Structure

```
packaged/                  # 👈 START HERE - Ready-to-use files
├── baseline-general.skills.md
├── python-sensitive-repo.skills.md
├── npm-high-autonomy.skills.md
└── strict-agent-high-autonomy.skills.md

skills/                    # For custom combinations
├── foundational/          # baseline or strict
└── overlays/
    ├── capabilities/      # what agent can do
    ├── ecosystems/        # language-specific
    ├── artifact-types/    # CI/CD, scanners, MCP
    └── contexts/          # prototype, production, regulated

examples/                  # Usage examples
docs/                      # Detailed guides
```

---

## 📖 Learn More

| Document | What You'll Learn |
|----------|----------|
| [**Quick Start Guide**](docs/QUICK_START.md) | 5-minute setup walkthrough |
| [**How to Choose**](docs/how-to-choose.md) | Decision guide with examples |
| [**Why This Exists**](docs/why-this-exists.md) | Supply chain risks & problem context |
| [**Design Principles**](docs/design-principles.md) | 15 core principles |
| [**Mapping to Standards**](docs/mapping-to-standards.md) | SLSA, OWASP, NIST alignment |

---

## 🎯 Different AI Agents

### For Cline/Roo (Recommended location)
```bash
cp packaged/baseline-general.skills.md .clinerules/oss-guardrails.md
```

### For Cursor
```bash
cp packaged/baseline-general.skills.md .cursorrules
```

### For GitHub Copilot
```bash
mkdir -p .github
cp packaged/baseline-general.skills.md .github/copilot-instructions.md
```

### For Aider
Add to `.aider.conf.yml`:
```yaml
read: packaged/baseline-general.skills.md
```

### Global (All projects)
```bash
# Cline - applies to all projects
mkdir -p ~/Documents/Cline/Rules/
cp packaged/baseline-general.skills.md ~/Documents/Cline/Rules/oss-guardrails.md
```

---

## ❓ FAQ

**Q: Which file should I choose?**  
A: Start with `baseline-general.skills.md` - it works for most projects.

**Q: Do I need to modify the files?**  
A: No! Use them as-is. Customize only if you have specific needs.

**Q: Will this block my agent from working?**  
A: No, these are guidelines that help your agent make better choices, not hard blocks.

**Q: Do I still need security scanning tools?**  
A: Yes! These guardrails complement (don't replace) tools like Snyk, Dependabot, etc.

**Q: Can I use multiple files?**  
A: Yes, you can combine them - see [Advanced: Custom Combinations](#-advanced-custom-combinations)

---

## 🤝 Contributing

Contributions welcome! See [Contribution Guide](docs/contribution-guide.md)

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

<div align="center">

**Practical supply chain guidance for AI agents** 🛡️

Built with lessons from [SLSA](https://slsa.dev/), [OWASP](https://owasp.org/), [NIST SSDF](https://csrc.nist.gov/Projects/ssdf)

[⬆ Back to Top](#-agent-oss-guardrails)

</div>
