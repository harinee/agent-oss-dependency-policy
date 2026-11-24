#!/usr/bin/env python3
"""Check that dependency references in a repository are pinned.

Usage:
  python3 check_pins.py [path] [--allow-registry HOST ...]

Checks (rule IDs refer to the policy files in this repository):
  PIN-4  GitHub workflow `uses:` references are full 40-character commit SHAs.
         If .github/workflows/actions.lock exists, only reusable-workflow
         calls are checked, because the lockfile does not cover them.
  PIN-5  Dockerfile `FROM` images carry a sha256 digest.
  PIN-1  package.json has a lockfile beside it; requirements*.txt entries use `==`.
  SRC-1  package.json and requirements files do not point at git or URL sources,
         `latest` or `*`; package-lock.json `resolved` URLs use an allowed registry.

What this does NOT catch:
  - whether a pinned version, SHA or digest is safe, or how old it is
  - whether a SHA belongs to the action's own repository and not a fork
  - images referenced in Compose files, Kubernetes manifests or CI config
  - ecosystems other than npm and pip requirements files
  - anything an agent does outside the files in the repository

Exit status: 0 if clean, 1 if there are findings, 2 on a usage error.
Standard library only.
"""
import json
import pathlib
import re
import sys

SKIP_DIRS = {".git", "node_modules", "vendor", "dist", "build", ".venv", "venv", "__pycache__"}
SHA40 = re.compile(r"^[0-9a-f]{40}$")
DIGEST = re.compile(r"@sha256:[0-9a-f]{64}$")
USES = re.compile(r"^\s*(?:-\s*)?uses:\s*['\"]?([^'\"\s#]+)")
FROM = re.compile(r"^\s*FROM\s+(?:--\S+\s+)*(\S+)(?:\s+AS\s+(\S+))?", re.IGNORECASE)
LOCKFILES = ("package-lock.json", "npm-shrinkwrap.json", "pnpm-lock.yaml", "yarn.lock", "bun.lock", "bun.lockb")
LOCAL_SPEC = ("file:", "link:", "workspace:", "portal:", "patch:", "catalog:", "npm:")


def walk(root):
    for path in sorted(root.rglob("*")):
        if path.is_file() and not (set(path.relative_to(root).parts[:-1]) & SKIP_DIRS):
            yield path


def check_workflow(path, has_lock, findings):
    for n, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
        m = USES.match(line)
        if not m:
            continue
        ref = m.group(1)
        if ref.startswith("./"):
            continue
        if ref.startswith("docker://"):
            if not DIGEST.search(ref):
                findings.append((path, n, "PIN-5", f"container action without digest: {ref}"))
            continue
        target, _, version = ref.partition("@")
        reusable = "/.github/workflows/" in target
        if has_lock and not reusable:
            continue
        if not SHA40.match(version):
            findings.append((path, n, "PIN-4", f"not pinned to a full commit SHA: {ref}"))


def check_dockerfile(path, findings):
    stages = set()
    for n, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
        m = FROM.match(line)
        if not m:
            continue
        image, alias = m.group(1), m.group(2)
        if alias:
            stages.add(alias.lower())
        if image.lower() == "scratch" or image.lower() in stages - ({alias.lower()} if alias else set()):
            continue
        if "$" in image:
            findings.append((path, n, "PIN-5", f"image set by a build argument, cannot verify: {image}"))
        elif not DIGEST.search(image):
            findings.append((path, n, "PIN-5", f"image without digest: {image}"))


def check_package_json(path, findings):
    try:
        data = json.loads(path.read_text())
    except (ValueError, OSError) as exc:
        findings.append((path, 1, "PIN-1", f"cannot parse: {exc}"))
        return
    if not isinstance(data, dict):
        return
    has_deps = False
    for section in ("dependencies", "devDependencies", "optionalDependencies"):
        for name, spec in (data.get(section) or {}).items():
            has_deps = True
            spec = str(spec).strip()
            if spec.startswith(LOCAL_SPEC):
                continue
            if spec in ("", "*", "x", "latest", "next"):
                findings.append((path, 1, "SRC-1", f"{section}.{name}: unpinned spec '{spec}'"))
            elif re.match(r"^(git\+|git:|github:|gitlab:|bitbucket:|https?:)", spec) or re.match(r"^[\w.-]+/[\w.-]+(#.*)?$", spec):
                findings.append((path, 1, "SRC-1", f"{section}.{name}: not from a registry: {spec}"))
    # Only the top-level manifest of a tree needs its own lockfile.
    parent_has_manifest = any((p / "package.json").is_file() for p in path.parent.parents)
    if has_deps and not parent_has_manifest and not any((path.parent / lf).exists() for lf in LOCKFILES):
        findings.append((path, 1, "PIN-1", "dependencies declared but no lockfile beside package.json"))


def check_package_lock(path, allowed, findings):
    try:
        data = json.loads(path.read_text())
    except (ValueError, OSError) as exc:
        findings.append((path, 1, "PIN-1", f"cannot parse: {exc}"))
        return
    for name, entry in (data.get("packages") or {}).items():
        url = entry.get("resolved") if isinstance(entry, dict) else None
        if not url or url.startswith("file:"):
            continue
        host = re.sub(r"^[a-z+]+://([^/]+).*$", r"\1", url)
        if host not in allowed:
            findings.append((path, 1, "SRC-1", f"{name or '(root)'} resolved from {host}"))


def check_requirements(path, findings):
    for n, raw in enumerate(path.read_text(errors="replace").splitlines(), 1):
        line = raw.split(" #")[0].strip()
        if not line or line.startswith("#") or line.startswith("-") or line.endswith("\\") and "==" in line:
            continue
        if line.startswith("--hash") or line.startswith("sha256:"):
            continue
        if re.match(r"^(git\+|https?:)", line) or " @ " in line:
            findings.append((path, n, "SRC-1", f"not from an index: {line}"))
        elif "==" not in line:
            findings.append((path, n, "PIN-1", f"not pinned with ==: {line}"))


def main(argv):
    args = [a for a in argv if a != "--help" and a != "-h"]
    if len(args) != len(argv):
        print(__doc__)
        return 0
    allowed = {"registry.npmjs.org"}
    paths = []
    it = iter(args)
    for a in it:
        if a == "--allow-registry":
            host = next(it, None)
            if host is None:
                print("--allow-registry needs a host", file=sys.stderr)
                return 2
            allowed.add(host)
        else:
            paths.append(a)
    if len(paths) > 1:
        print("give at most one path", file=sys.stderr)
        return 2
    root = pathlib.Path(paths[0] if paths else ".").resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    has_lock = (root / ".github" / "workflows" / "actions.lock").is_file()
    findings = []
    for path in walk(root):
        rel = path.relative_to(root)
        name = path.name
        if rel.parts[:2] == (".github", "workflows") and path.suffix in (".yml", ".yaml"):
            check_workflow(path, has_lock, findings)
        elif name == "Dockerfile" or name.startswith("Dockerfile.") or name.endswith(".Dockerfile"):
            check_dockerfile(path, findings)
        elif name == "package.json":
            check_package_json(path, findings)
        elif name == "package-lock.json":
            check_package_lock(path, allowed, findings)
        elif re.match(r"^requirements.*\.txt$", name):
            check_requirements(path, findings)
    for path, line, rule, message in findings:
        print(f"{path.relative_to(root)}:{line}: {rule} {message}")
    if findings:
        print(f"{len(findings)} finding(s)")
        return 1
    print("dependency pin check: no findings")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
