# How to choose

Start with a preset. Build your own combination only if none fits.

## Presets

| Preset | Foundation | Use for |
|---|---|---|
| `baseline-general` | baseline | General development. Start here if unsure. |
| `prototype-quick` | baseline | Prototypes and experiments. 1-day cooldown, less reporting. |
| `npm-high-autonomy` | baseline | Node.js with an agent running unattended; includes MCP rules. |
| `python-sensitive-repo` | strict | Python in regulated or sensitive settings. 14-day cooldown. |
| `strict-agent-high-autonomy` | strict | Production, with an agent that can change CI, containers and tools. |
| `java-production` | strict | JVM services in production. |
| `go-service` | baseline | Go services with containers and GitHub Actions. |
| `rust-project` | baseline | Rust projects. |
| `agent-tooling` | baseline | Projects where the agent may add MCP servers, editor extensions or agent skills. |

Each preset file lists exactly what it includes at the top. The definitions are in [`presets.json`](../presets.json).

A project that spans several of these can concatenate two presets' overlays; see "Building your own" below.

## Building your own

A combination is one foundational file plus any overlays.

### 1. Foundation (exactly one)

| File | Use for |
|---|---|
| `skills/foundational/oss-selection-baseline.skills.md` | General development, internal tools |
| `skills/foundational/oss-selection-strict.skills.md` | Production and sensitive systems. Same rules; three levels are stricter. |

### 2. Capabilities (what the agent can do)

| If the agent can | Add |
|---|---|
| Run install commands | `skills/overlays/capabilities/agent-can-install-packages.skills.md` |
| Run shell commands | `skills/overlays/capabilities/agent-can-run-shell.skills.md` |
| Add or call tools and MCP servers | `skills/overlays/capabilities/agent-can-use-tools-or-mcp.skills.md` |
| Commit or open pull requests | `skills/overlays/capabilities/agent-can-open-pr.skills.md` |
| Run with no human in the session | `skills/overlays/capabilities/agent-runs-unattended.skills.md` |

### 3. Ecosystems (any number)

| Project uses | Add |
|---|---|
| npm, pnpm, Yarn, Bun | `skills/overlays/ecosystems/npm-node.skills.md` |
| pip, uv, Poetry, PDM | `skills/overlays/ecosystems/python-pip.skills.md` |
| Maven, Gradle | `skills/overlays/ecosystems/java-maven-gradle.skills.md` |
| Go modules | `skills/overlays/ecosystems/go-modules.skills.md` |
| Cargo | `skills/overlays/ecosystems/rust-cargo.skills.md` |
| Container images | `skills/overlays/ecosystems/container-images.skills.md` |

There is no overlay yet for NuGet or RubyGems. The foundational rules still apply to them.

### 4. Artifact types (any number)

| Agent may add or change | Add |
|---|---|
| CI workflows and build tools | `skills/overlays/artifact-types/ci-actions-build-tools.skills.md` |
| GitHub Actions references | `skills/overlays/artifact-types/github-actions.skills.md` |
| MCP servers and connectors | `skills/overlays/artifact-types/mcp-servers-connectors.skills.md` |
| Scanners and security tools | `skills/overlays/artifact-types/scanners-security-tools.skills.md` |
| Editor extensions | `skills/overlays/artifact-types/ide-extensions.skills.md` |
| Third-party agent skills, rules, hooks | `skills/overlays/artifact-types/agent-skills.skills.md` |

### 5. Context (at most one)

| Context | Add |
|---|---|
| Prototype | `skills/overlays/contexts/prototype-low-risk.skills.md` |
| Production | `skills/overlays/contexts/production.skills.md` |
| Regulated or sensitive | `skills/overlays/contexts/regulated-sensitive.skills.md` |

What each context changes is tabled in [friction-model.md](friction-model.md).

### Join them

```bash
cat skills/foundational/oss-selection-strict.skills.md \
    skills/overlays/capabilities/agent-can-install-packages.skills.md \
    skills/overlays/ecosystems/python-pip.skills.md \
    skills/overlays/ecosystems/container-images.skills.md \
    skills/overlays/contexts/production.skills.md \
    > my-policy.md
```

Put the foundational file first. Then copy `my-policy.md` to where your agent reads instructions; see [QUICK_START.md](QUICK_START.md).

## Typical combinations

|  | Prototype | Internal tool | Production | Regulated |
|---|---|---|---|---|
| Foundation | baseline | baseline | strict | strict |
| Capabilities | as applicable | as applicable | as applicable | as applicable |
| Ecosystems | as applicable | as applicable | as applicable | as applicable |
| Artifact types | optional | optional | recommended | recommended |
| Context | prototype | none | production | regulated |

## When to revisit

| Event | Action |
|---|---|
| The project goes to production | Move to strict, or add the production overlay |
| The agent gains a capability | Add the matching capability overlay |
| The agent starts running unattended | Add `agent-runs-unattended` |
| The policy interrupts too often | Add packages to the approved list, or adjust a threshold. See [friction-model.md](friction-model.md). |
| A supply-chain incident affects you | Check [threat-coverage.md](threat-coverage.md) for the rule involved |
