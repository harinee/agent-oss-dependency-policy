"""Shared code for the eval shims. Never touches the network or installs anything.

The runner sets:
  EVAL_FIXTURE  path to a JSON file with the fake registry for this scenario
  EVAL_LOG      path to a JSON-lines file where every shim call is recorded
"""
import json
import os
import pathlib
import sys


def fixture():
    with open(os.environ["EVAL_FIXTURE"]) as fh:
        return json.load(fh)


def log(entry):
    entry["cwd"] = os.getcwd()
    with open(os.environ["EVAL_LOG"], "a") as fh:
        fh.write(json.dumps(entry) + "\n")


def split_spec(spec):
    """'name@1.2.3' -> ('name', '1.2.3'); '@scope/name' -> ('@scope/name', None)."""
    at = spec.rfind("@")
    if at > 0:
        return spec[:at], spec[at + 1:]
    return spec, None


def package_doc(name):
    """Registry document for a package, shaped like the npm registry's, or None."""
    pkg = fixture()["packages"].get(name)
    if pkg is None:
        return None
    versions = {}
    time = {"created": pkg["created"], "modified": max(v["published"] for v in pkg["versions"].values())}
    for ver, v in pkg["versions"].items():
        time[ver] = v["published"]
        doc = {
            "name": name,
            "version": ver,
            "_npmUser": {"name": v.get("publisher", pkg.get("publisher", "unknown"))},
            "scripts": v.get("scripts", {}),
            "dist": {"tarball": f"https://registry.npmjs.org/{name}/-/{name.split('/')[-1]}-{ver}.tgz"},
        }
        if pkg.get("repository"):
            doc["repository"] = {"type": "git", "url": pkg["repository"]}
        versions[ver] = doc
    doc = {
        "name": name,
        "dist-tags": {"latest": pkg["latest"]},
        "versions": versions,
        "time": time,
        "maintainers": [{"name": m} for m in pkg.get("maintainers", [pkg.get("publisher", "unknown")])],
        "weeklyDownloads": pkg.get("weekly_downloads"),
    }
    if pkg.get("repository"):
        doc["repository"] = {"type": "git", "url": pkg["repository"]}
    return doc


def resolve(name, wanted):
    """Return (doc, version) or (None, None). Anything that is not an exact
    existing version resolves to latest, as a plain `npm install name` would."""
    doc = package_doc(name)
    if doc is None:
        return None, None
    if wanted and wanted.lstrip("=v") in doc["versions"]:
        return doc, wanted.lstrip("=v")
    return doc, doc["dist-tags"]["latest"]


def scripts_disabled(argv):
    if "--ignore-scripts" in argv or "--ignore-scripts=true" in argv:
        return True
    npmrc = pathlib.Path(".npmrc")
    if npmrc.is_file():
        for line in npmrc.read_text().splitlines():
            if line.replace(" ", "").lower() == "ignore-scripts=true":
                return True
    return False


def not_found(name):
    sys.stderr.write(f"npm error code E404\nnpm error 404 Not Found - GET https://registry.npmjs.org/{name} - Not found\n")
    return 1
