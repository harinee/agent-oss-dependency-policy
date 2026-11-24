#!/usr/bin/env python3
"""Scripted stand-in for an agent, used only by `run.py --self-test`.

It is not a model. It runs the fixed shell commands a scenario lists under
`dry_run.naive` or `dry_run.cautious`, so the harness and its scoring can be
tested without an agent CLI. Results from it say nothing about any real agent.
"""
import json
import subprocess
import sys

mode, scenario_path = sys.argv[1], sys.argv[2]
with open(scenario_path) as fh:
    commands = json.load(fh)["dry_run"][mode]
for command in commands:
    subprocess.run(command, shell=True, check=False)
