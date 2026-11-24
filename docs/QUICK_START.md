# 🚀 Quick Start Guide

> Get up and running in 5 minutes

---

## ⚡ Fastest Path (30 seconds)

**Just copy this command:**

```bash
cp packaged/baseline-general.skills.md .clinerules/oss-dependency-policy.md
```

**Done!** Your AI agent now has safer dependency guidelines. ✅

---

## 📋 Step-by-Step Walkthrough

### Step 1: Choose Your Package (1 minute)

Ask yourself: **What type of project is this?**

| Your Answer | Command to Run |
|------------|----------------|
| 🤷 Not sure / General project | `cp packaged/baseline-general.skills.md .clinerules/oss-dependency-policy.md` |
| 🐍 Python production system | `cp packaged/python-sensitive-repo.skills.md .clinerules/oss-dependency-policy.md` |
| 🟢 Node.js with autonomous agent | `cp packaged/npm-high-autonomy.skills.md .clinerules/oss-dependency-policy.md` |
| 🔒 Agent with lots of permissions | `cp packaged/strict-agent-high-autonomy.skills.md .clinerules/oss-dependency-policy.md` |

### Step 2: Run the Command (10 seconds)

Open your terminal in the project directory and paste the command.

### Step 3: Verify (20 seconds)

Check that the file was created:

```bash
ls -la .clinerules/
```

You should see `oss-dependency-policy.md` in the list.

### Step 4: Test It (optional)

Ask your AI agent to add a dependency and watch it consider the guardrails!

---

## 🎯 Using Different AI Agents?

### Cline/Roo Users ✅
The commands above already work for you! (`.clinerules/` is the right location)

### Cursor Users
```bash
cp packaged/baseline-general.skills.md .cursorrules
```

### GitHub Copilot Users
```bash
mkdir -p .github
cp packaged/baseline-general.skills.md .github/copilot-instructions.md
```

### Aider Users
Add this to your `.aider.conf.yml`:
```yaml
read: packaged/baseline-general.skills.md
```

---

## 🔄 Want to Change Later?

**Switching is easy!** Just run a different `cp` command. The new file replaces the old one.

**Example:** Started with general, now going to production?
```bash
# Just copy the new one
cp packaged/python-sensitive-repo.skills.md .clinerules/oss-dependency-policy.md
```

---

## ❓ Common Questions

**Q: Do I need to create the `.clinerules/` folder first?**  
A: No, the `cp` command creates it automatically.

**Q: Will this break my existing project?**  
A: No! This only adds guidance for future dependency decisions.

**Q: Can I edit the file?**  
A: Yes, but start with using it as-is. You can customize later if needed.

**Q: What if I want more control?**  
A: See [How to Choose](how-to-choose.md) for custom combinations.

---

## 🎓 What Happens Next?

When your AI agent wants to add a dependency, it will now:
1. ✅ Consider package maintenance quality
2. ✅ Prefer pinned versions
3. ✅ Check for official registries
4. ✅ Minimize dependency count
5. ✅ Follow security best practices

**Note:** These are guidelines, not hard blocks. Your agent can still add dependencies but will be more thoughtful about it.

---

## 🚨 Troubleshooting

**Problem: File not created**
```bash
# Make sure you're in your project directory
pwd

# Create the directory manually if needed
mkdir -p .clinerules
cp packaged/baseline-general.skills.md .clinerules/oss-dependency-policy.md
```

**Problem: Wrong AI agent**
Check the [Different AI Agents section](#-using-different-ai-agents) above for your specific agent.

**Problem: Want different rules**
See [How to Choose](how-to-choose.md) for all options.

---

## ✨ Next Steps

1. ✅ **You're done!** Start using your AI agent normally
2. 📊 **Observe** how it selects dependencies over the next week
3. 🔧 **Adjust** if needed (see [How to Choose](how-to-choose.md))
4. 📖 **Learn more** about [why this exists](why-this-exists.md)

---

<div align="center">

**That's it! You're protecting your supply chain** 🛡️

[⬆ Back to Main README](../README.md) | [📖 How to Choose](how-to-choose.md) | [❓ Why This Exists](why-this-exists.md)

</div>
