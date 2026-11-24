#!/usr/bin/env python3
"""Structural self-check for this repository. Standard library only.

  python3 scripts/selfcheck.py

Checks:
  1. policy file format (title, description, required sections)
  2. rule IDs: present, unique, levelled, with a rationale; baseline and strict agree
  3. rule IDs referenced anywhere are defined somewhere
  4. generated presets and Agent Skills folders match their sources
  5. Agent Skills front matter meets the specification's constraints
  6. internal links, anchors and repo paths quoted in docs resolve
  7. every overlay is in a preset and listed in docs/how-to-choose.md
  8. thresholds in docs and enforcement/ match the policy tables
  9. eval scenarios load

It checks structure and consistency. It does not check that the rules are
right, that sources are accurate, or that any agent follows the policy.
"""
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RULE = re.compile(r"^- \*\*([A-Z]+)-(\d+)(?: \((BLOCK|ASK|NOTE)\))?\*\* (.*)$")
UNLEVELLED = {"APR", "FIX", "OVR", "AUT"}  # escape hatches and the fail-closed rule have no level
errors = []
notes = []


def err(msg):
    errors.append(msg)


def rel(path):
    return str(path.relative_to(ROOT))


def md_files():
    return sorted(p for p in ROOT.rglob("*.md") if ".git" not in p.parts and "node_modules" not in p.parts and p.name != "AUDIT.md")


def parse_rules(path):
    rules = {}
    for n, line in enumerate(path.read_text().splitlines(), 1):
        m = RULE.match(line)
        if not m:
            if re.match(r"^- \*\*[A-Z]+-\d+", line):
                err(f"{rel(path)}:{n}: malformed rule line")
            continue
        prefix, num, level, text = m.groups()
        rid = f"{prefix}-{num}"
        if rid in rules:
            err(f"{rel(path)}:{n}: duplicate rule ID {rid}")
        if prefix in UNLEVELLED:
            if level:
                err(f"{rel(path)}:{n}: {rid} should not have a level")
        else:
            if not level:
                err(f"{rel(path)}:{n}: {rid} has no level")
            if "*Why:*" not in text:
                err(f"{rel(path)}:{n}: {rid} has no *Why:* rationale")
        rules[rid] = {"level": level, "statement": text.split("*Why:*")[0].strip(), "line": n}
    return rules


def parse_table(text, heading):
    """Rows of the first table after a heading, as lists of cell strings."""
    m = re.search(rf"^## {re.escape(heading)}\s*$", text, re.M)
    if not m:
        return None
    rows = []
    for line in text[m.end():].splitlines():
        if line.startswith("## "):
            break
        if line.startswith("|") and not re.match(r"^\|[\s:|-]+\|$", line):
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    return rows[1:] if rows else []


def thresholds(path):
    rows = parse_table(path.read_text(), "Tunable thresholds")
    return {r[0].strip("`"): r[1] for r in rows} if rows else {}


# 1 and 2: format and rules --------------------------------------------------
foundational = sorted((ROOT / "skills/foundational").glob("*.skills.md"))
overlays = sorted((ROOT / "skills/overlays").rglob("*.skills.md"))
defined = {}
prefix_owner = {}
for path in foundational + overlays:
    text = path.read_text()
    lines = text.splitlines()
    if not lines or not lines[0].startswith("# "):
        err(f"{rel(path)}: first line must be an H1 title")
    if not any(l.startswith("> ") for l in lines[:4]):
        err(f"{rel(path)}: missing one-line '> ' description under the title")
    for section in ("## When to use this", "## Instructions"):
        if section not in text:
            err(f"{rel(path)}: missing section '{section}'")
    if path in overlays and "Requires a foundational file." not in text:
        err(f"{rel(path)}: overlays must say 'Requires a foundational file.'")
    rules = parse_rules(path)
    if not rules:
        err(f"{rel(path)}: no rules found")
    for rid in rules:
        prefix = rid.split("-")[0]
        if path in overlays:
            owner = prefix_owner.setdefault(prefix, path)
            if owner != path:
                err(f"{rel(path)}: rule prefix {prefix} is already used by {rel(owner)}")
        defined.setdefault(rid, path)

if len(foundational) == 2:
    a, b = (parse_rules(p) for p in foundational)
    if set(a) != set(b):
        err(f"foundational files define different rule IDs: {sorted(set(a) ^ set(b))}")
    for rid in set(a) & set(b):
        if a[rid]["statement"] != b[rid]["statement"]:
            err(f"{rid}: rule text differs between the baseline and strict files")
    for prefix in {r.split('-')[0] for r in a}:
        if prefix in prefix_owner:
            err(f"rule prefix {prefix} is used by both a foundational file and {rel(prefix_owner[prefix])}")
else:
    err("expected exactly two foundational files")

# 3: references ---------------------------------------------------------------
prefixes = {rid.split("-")[0] for rid in defined}
for path in md_files() + sorted((ROOT / "enforcement").rglob("*.*")) + sorted((ROOT / "evals/scenarios").glob("*.json")):
    if not path.is_file() or path.suffix in (".pyc",):
        continue
    text = path.read_text(errors="replace")
    for m in re.finditer(r"(?<![A-Za-z0-9-])([A-Z]{2,5})-(\d+)(?![\w-])", text):
        if m.group(1) in prefixes and m.group(0) not in defined:
            err(f"{rel(path)}: refers to undefined rule {m.group(0)}")

# 4: generated files ------------------------------------------------------------
build = subprocess.run([sys.executable, str(ROOT / "scripts/build.py"), "--check"], capture_output=True, text=True)
if build.returncode != 0:
    err("generated files are stale:\n    " + build.stdout.strip().replace("\n", "\n    "))

# 5: Agent Skills front matter ---------------------------------------------------
for path in sorted((ROOT / "agent-skills").glob("*/SKILL.md")):
    text = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        err(f"{rel(path)}: no YAML front matter")
        continue
    front = m.group(1)
    name = re.search(r"^name: (.+)$", front, re.M)
    desc = re.search(r"^description: (.+)$", front, re.M)
    if not name:
        err(f"{rel(path)}: front matter has no name")
    else:
        value = name.group(1).strip()
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", value) or len(value) > 64:
            err(f"{rel(path)}: name must be 1-64 lowercase letters, digits and single hyphens")
        if value != path.parent.name:
            err(f"{rel(path)}: name '{value}' does not match its directory")
    if not desc:
        err(f"{rel(path)}: front matter has no description")
    else:
        value = json.loads(desc.group(1)) if desc.group(1).startswith('"') else desc.group(1)
        if not 1 <= len(value) <= 1024:
            err(f"{rel(path)}: description must be 1-1024 characters")
    if len(text.splitlines()) > 500:
        notes.append(f"{rel(path)}: {len(text.splitlines())} lines; the specification recommends under 500")


# 6: links, anchors, quoted paths --------------------------------------------------
def anchors(path):
    found = set()
    for line in path.read_text().splitlines():
        m = re.match(r"^#{1,6}\s+(.*)$", line)
        if m:
            slug = re.sub(r"[^\w\- ]", "", m.group(1).strip().lower()).replace(" ", "-")
            found.add(slug)
    return found


for path in md_files():
    text = re.sub(r"```.*?```", "", path.read_text(), flags=re.S)
    for m in re.finditer(r"\[[^\]]*\]\(([^)\s]+)\)", text):
        target = m.group(1)
        if re.match(r"^(https?:|mailto:)", target):
            continue
        file_part, _, anchor = target.partition("#")
        dest = (path.parent / file_part).resolve() if file_part else path
        if not dest.exists():
            err(f"{rel(path)}: broken link {target}")
        elif anchor and dest.suffix == ".md" and anchor not in anchors(dest):
            err(f"{rel(path)}: broken anchor {target}")
    for m in re.finditer(r"`((?:skills|packaged|agent-skills|enforcement|evals|scripts|docs|examples)/[\w./-]+\.\w+)`", text):
        if not (ROOT / m.group(1)).exists():
            err(f"{rel(path)}: refers to missing path {m.group(1)}")

# 7: reachability -------------------------------------------------------------------
presets = json.loads((ROOT / "presets.json").read_text())["presets"]
in_presets = {src for p in presets for src in p["sources"]}
how = (ROOT / "docs/how-to-choose.md").read_text()
for path in foundational + overlays:
    if rel(path) not in in_presets:
        err(f"{rel(path)}: not included in any preset")
    if rel(path) not in how:
        err(f"{rel(path)}: not listed in docs/how-to-choose.md")
for p in presets:
    if f"`{p['name']}`" not in how:
        err(f"preset {p['name']}: not listed in docs/how-to-choose.md")
    if sum(1 for s in p["sources"] if "/foundational/" in s) != 1 or "/foundational/" not in p["sources"][0]:
        err(f"preset {p['name']}: must start with exactly one foundational file")
    if sum(1 for s in p["sources"] if "/contexts/" in s) > 1:
        err(f"preset {p['name']}: at most one context overlay")

# 8: thresholds -------------------------------------------------------------------------
base = thresholds(ROOT / "skills/foundational/oss-selection-baseline.skills.md")
strict = thresholds(ROOT / "skills/foundational/oss-selection-strict.skills.md")
ctx = {name: thresholds(ROOT / f"skills/overlays/contexts/{file}.skills.md")
       for name, file in (("Prototype overlay", "prototype-low-risk"), ("Production overlay", "production"), ("Regulated overlay", "regulated-sensitive"))}
if not base:
    err("baseline file has no 'Tunable thresholds' table")
doc_rows = parse_table((ROOT / "docs/friction-model.md").read_text(), "Levels and thresholds by context") or []
header = ["Prototype overlay", "Baseline", "Strict", "Production overlay", "Regulated overlay"]
seen = set()
for row in doc_rows:
    key = row[0].strip("`")
    if key not in base:
        continue
    seen.add(key)
    expected = {"Baseline": base[key], "Strict": strict.get(key)}
    for name in ctx:
        expected[name] = ctx[name].get(key, "unchanged")
    for col, cell in zip(header, row[1:]):
        if cell != expected[col]:
            err(f"docs/friction-model.md: {key} / {col} is '{cell}', policy files say '{expected[col]}'")
for key in base:
    if key not in seen:
        err(f"docs/friction-model.md: threshold {key} missing from the context table")

days = int(base.get("version_cooldown_days", 0))
enforced = {
    "enforcement/npm/npmrc.example": rf"^min-release-age={days}$",
    "enforcement/pnpm/pnpm-workspace.example.yaml": rf"^minimumReleaseAge: {days * 1440}$",
    "enforcement/bun/bunfig.example.toml": rf"^minimumReleaseAge = {days * 86400}$",
    "enforcement/python/uv.example.toml": rf'^exclude-newer = "{days} days"$',
    "enforcement/cargo/config.example.toml": rf'^global-min-publish-age = "{days} days"$',
    "enforcement/dependabot/dependabot.example.yml": rf"^\s+default-days: {days}$",
    "enforcement/renovate/renovate.example.json": rf'"minimumReleaseAge": "{days} days"',
    "enforcement/yarn/yarnrc.example.yml": r'^npmMinimalAgeGate: "1w"$' if days == 7 else r"^$never",
}
for file, pattern in enforced.items():
    if not re.search(pattern, (ROOT / file).read_text(), re.M):
        err(f"{file}: cooldown does not match version_cooldown_days = {days}")
for file in ("docs/QUICK_START.md", "README.md"):
    text = (ROOT / file).read_text()
    for m in re.finditer(r"(\d+)-day (?:version )?cooldown", text):
        if int(m.group(1)) not in {days} | {int(v[k]) for v in ctx.values() for k in v if k == "version_cooldown_days"}:
            err(f"{file}: mentions a {m.group(1)}-day cooldown that no policy table defines")

# 9: scenarios ----------------------------------------------------------------------------
sys.path.insert(0, str(ROOT / "evals"))
try:
    import run as eval_run
    scenarios = eval_run.load_scenarios(ROOT / "evals/scenarios")
    for s in scenarios:
        if "dry_run" not in s:
            err(f"evals/scenarios/{s['id']}.json: no dry_run commands for the self-test")
except SystemExit as exc:
    err(f"eval scenarios: {exc}")

for n in notes:
    print("note:", n)
if errors:
    print("\n".join(f"FAIL {e}" for e in errors))
    print(f"\nselfcheck: {len(errors)} problem(s)")
    sys.exit(1)
print(f"selfcheck passed: {len(foundational) + len(overlays)} policy files, {len(defined)} rule IDs, "
      f"{len(presets)} presets, {len(md_files())} markdown files")
