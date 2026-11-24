# Scanners and Security Tools

> Rules for adding and updating scanners, linters with network access, and other security tooling.

## When to use this

Apply when adding or updating vulnerability scanners, SAST or DAST tools, secret scanners or their CI integrations. Requires a foundational file.

## Instructions

- **SCN-1 (ASK)** Adding a scanner or security tool. State what it reads and where its results go. *Why:* ART-1; scanners see the whole codebase and often CI secrets, and have been the entry point of attacks (TeamPCP).
- **SCN-2 (NOTE)** Pin the tool: exact version, action SHA or image digest. AGE-1 applies. Being a security tool earns no exemption. *Why:* scanner releases have been hijacked like any other package.
- **SCN-3 (NOTE)** Give the tool read-only access and the narrowest token that works. *Why:* limits what a compromised release can do.
- **SCN-4 (ASK)** The tool uploads source code or findings to an external service. *Why:* the team decides what leaves the organisation.
- **SCN-5 (ASK)** Suppressing, ignoring or baselining findings. Record the reason next to the suppression. *Why:* silent suppression hides real findings.
