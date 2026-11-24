# Local overrides

<!--
Copy to .dependency-policy/overrides.md in your project and keep only the rows you need.
The policy (rule LOC-1) tells the agent to read this file first and apply it over the preset.

- Rule rows: the value is BLOCK, ASK or NOTE.
- Threshold rows: the value is a number.
- Any rule can be raised. Any rule can be lowered except ID-1, ID-3 and TRU-1.
- The agent must not create or edit this file. Protect it with CODEOWNERS or similar.
- This is advice to the agent, like the policy. Mirror threshold changes in your
  package-manager config (see enforcement/ in the policy repository).

The rows below are examples, not recommendations.
-->

| Rule or threshold | Value | Reason |
|---|---|---|
| version_cooldown_days | 14 | Matches our Renovate setting |
| min_package_age_days | 30 | We adopt young packages often; 90 asked too much |
| AGE-2 | ASK | New packages need a named owner here |
| SRC-2 | BLOCK | No pipe-to-shell installs in this repository |
| LIC-1 | ASK | Legal reviews every new licence |
