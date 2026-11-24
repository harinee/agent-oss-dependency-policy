# Python / pip Ecosystem

> How to apply the foundational rules with pip, uv, Poetry and PDM.

## When to use this

Apply to Python projects. Requires a foundational file.

## Instructions

### Looking things up

- **PY-1 (NOTE)** Use `https://pypi.org/pypi/<name>/json` for the foundational checks: each release file has an upload time (AGE-1, AGE-2) and the project links its repository (AGE-3). If you cannot find who uploaded a release, report `PUB-1: not checked`. *Why:* these are the facts the rules depend on.

### Cooldown

- **PY-2 (NOTE)** If the project sets a release-age option (`--uploaded-prior-to` in pip, `exclude-newer` in uv, `solver.min-release-age` in Poetry, `--exclude-newer` in PDM), rely on it and report its value. Do not lower it or add exclusions; that needs an ASK. *Why:* config is enforced, instructions are not.

### Installing

- **PY-3 (NOTE)** Pin exact versions (`name==1.2.3`). Use the project's lockfile (`uv.lock`, `poetry.lock`, `pdm.lock`) or a requirements file with `--hash` entries. A requirements file without hashes is a pin list, not a lockfile; say so if that is all the project has. *Why:* PIN-1.
- **PY-4 (NOTE)** Install into the project's virtual environment. Installing into the system or user Python needs an ASK. *Why:* keeps the change visible and reversible.

### Code that runs at install or start-up

- **PY-5 (ASK)** A source distribution runs its build code when installed. Prefer wheels (`--only-binary :all:`). If only a source distribution exists, apply SCR-1. *Why:* building from source executes code from the package.
- **PY-6 (NOTE)** A wheel can still run code at every interpreter start through a `.pth` file. After installing, report any new `.pth` file in site-packages that contains an `import` line. Wheels are not a safety check. *Why:* this is how the payload ran in LiteLLM and elementary-data.

### After installing

- **PY-7 (NOTE)** If the project uses an audit tool such as `pip-audit`, run it and report new advisories. *Why:* known-bad versions are the cheapest thing to catch.

## Examples

Good: `uv add 'requests==2.32.3'`, `pip install --only-binary :all: --require-hashes -r requirements.txt`

Avoid: `pip install requests`, `pip install --upgrade -r requirements.txt`, `pip install git+https://...`
