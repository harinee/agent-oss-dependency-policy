# How to choose

Install **one preset**. A preset already contains a foundational rule set and the overlays that suit its use case, so there is nothing else to install. Build your own combination only if no preset fits.

| Term | What it is | Do you install it? |
|---|---|---|
| Preset | One ready-made file: a foundational rule set plus bundled overlays | **Yes, exactly one** |
| Foundational file | The rule set itself: `baseline` or `strict` | Only inside a preset or your own combination |
| Overlay | Extra rules for a capability, ecosystem, artifact type or context. Additive; incomplete on its own. | Only to extend a preset |
| Agent Skill | The same preset in the on-demand Agent Skills format | Instead of the preset file, not as well as it |

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
| `dotnet-project` | baseline | .NET projects using NuGet. |
| `ruby-project` | baseline | Ruby projects using Bundler. |
| `agent-tooling` | baseline | Projects where the agent may add MCP servers, editor extensions or agent skills. |

Each preset file lists exactly what it includes at the top. The definitions are in [`presets.json`](../presets.json).

### A preset is close but not exact

Overlays are additive. Append the missing one to the preset:

```bash
# Node.js project, human in the session: baseline-general plus the npm overlay
cat presets/baseline-general.md policy/overlays/ecosystems/npm-node.md > my-policy.md
```

Do not join two presets: each carries its own copy of the foundational rules.

## Building your own

A combination is one foundational file plus any overlays.

### 1. Foundation (exactly one)

| File | Use for |
|---|---|
| `policy/foundational/oss-selection-baseline.md` | General development, internal tools |
| `policy/foundational/oss-selection-strict.md` | Production and sensitive systems. Same rules; three levels are stricter. |

### 2. Capabilities (what the agent can do)

| If the agent can | Add |
|---|---|
| Run install commands | `policy/overlays/capabilities/agent-can-install-packages.md` |
| Run shell commands | `policy/overlays/capabilities/agent-can-run-shell.md` |
| Add or call tools and MCP servers | `policy/overlays/capabilities/agent-can-use-tools-or-mcp.md` |
| Commit or open pull requests | `policy/overlays/capabilities/agent-can-open-pr.md` |
| Run with no human in the session | `policy/overlays/capabilities/agent-runs-unattended.md` |

### 3. Ecosystems (any number)

| Project uses | Add |
|---|---|
| npm, pnpm, Yarn, Bun | `policy/overlays/ecosystems/npm-node.md` |
| pip, uv, Poetry, PDM | `policy/overlays/ecosystems/python-pip.md` |
| Maven, Gradle | `policy/overlays/ecosystems/java-maven-gradle.md` |
| Go modules | `policy/overlays/ecosystems/go-modules.md` |
| Cargo | `policy/overlays/ecosystems/rust-cargo.md` |
| NuGet | `policy/overlays/ecosystems/dotnet-nuget.md` |
| Bundler, RubyGems | `policy/overlays/ecosystems/ruby-bundler.md` |
| Container images | `policy/overlays/ecosystems/container-images.md` |

Ecosystems without an overlay (for example PHP) still get the foundational rules, without ecosystem-specific commands.

### 4. Artifact types (any number)

| Agent may add or change | Add |
|---|---|
| CI workflows and build tools | `policy/overlays/artifact-types/ci-actions-build-tools.md` |
| GitHub Actions references | `policy/overlays/artifact-types/github-actions.md` |
| MCP servers and connectors | `policy/overlays/artifact-types/mcp-servers-connectors.md` |
| Scanners and security tools | `policy/overlays/artifact-types/scanners-security-tools.md` |
| Editor extensions | `policy/overlays/artifact-types/ide-extensions.md` |
| Third-party agent skills, rules, hooks | `policy/overlays/artifact-types/agent-skills.md` |

### 5. Context (at most one)

| Context | Add |
|---|---|
| Prototype | `policy/overlays/contexts/prototype-low-risk.md` |
| Production | `policy/overlays/contexts/production.md` |
| Regulated or sensitive | `policy/overlays/contexts/regulated-sensitive.md` |

What each context changes is tabled in [response-model.md](response-model.md#levels-and-thresholds-by-context).

### Join them

```bash
cat policy/foundational/oss-selection-strict.md \
    policy/overlays/capabilities/agent-can-install-packages.md \
    policy/overlays/ecosystems/python-pip.md \
    policy/overlays/ecosystems/container-images.md \
    policy/overlays/contexts/production.md \
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
| The policy interrupts too often, or not enough | Add packages to the approved list, or change a level or threshold in the overrides file. See [response-model.md](response-model.md#customizing). |
| A supply-chain incident affects you | Check [threat-coverage.md](threat-coverage.md) for the rule involved |
