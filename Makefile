# Common tasks. Everything uses the Python standard library; no install step.

.PHONY: build check selfcheck pins evals-selftest

build:            ## Regenerate packaged/ and agent-skills/ from presets.json
	python3 scripts/build.py

check: selfcheck pins evals-selftest  ## Run everything CI runs

selfcheck:        ## Structure, rule IDs, links, presets, thresholds
	python3 scripts/selfcheck.py

pins:             ## Pin check on this repository
	python3 enforcement/ci/check_pins.py .

evals-selftest:   ## Eval harness self-test (scripted stand-ins, no agent)
	python3 evals/run.py --self-test
