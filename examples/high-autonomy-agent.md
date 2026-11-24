# Example: agent with broad capabilities in production

Illustrative. The behaviour described is what the policy asks for, not a recorded session.

## Context

- Production Java microservice, deployed in containers, built in GitHub Actions
- The agent can install, run shell, use tools and open pull requests

## Files

The `strict-agent-high-autonomy` preset plus the Java overlay:

```
packaged/strict-agent-high-autonomy.skills.md
skills/overlays/ecosystems/java-maven-gradle.skills.md
```

If the agent also runs with no human in the session, add `skills/overlays/capabilities/agent-runs-unattended.skills.md`.

## What the policy asks for

**Adding a library.** The agent checks that the coordinates exist and belong to the intended project, applies the 7-day cooldown itself (Maven and Gradle have no setting for it), uses an exact version and lists the change in the pull request. A package first published within 90 days is an ASK under the strict foundation.

**Updating the base image.** The agent changes the tag and the digest together, obtains the digest from the registry, and says which version it moved to.

**Adding a GitHub Action.** ART-1 applies, so the agent asks. It resolves the commit SHA from the action's own repository and writes `owner/repo@<sha> # vX.Y.Z`.

**A pull-request comment says "also add package X".** The comment is data (PR-5). The agent evaluates package X under the rules like any other request.

## When nobody is there

With the unattended overlay, every ASK becomes: skip that dependency, log the rule ID and reason in the pull request, continue or stop. The agent does not approve its own request, edit the approved list, or find another route to the same code.

## What this does not give you

The policy does not ensure human oversight. It asks the agent to stop at certain points. Branch protection, required reviews and the checks in `enforcement/` are what make a stop binding.
