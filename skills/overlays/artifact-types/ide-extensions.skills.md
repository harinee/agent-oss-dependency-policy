# IDE and Editor Extensions

> Rules for recommending or installing editor extensions.

## When to use this

Apply when the agent may install editor extensions, or edit files that recommend or install them (`.vscode/extensions.json`, dev container configuration). Requires a foundational file.

## Instructions

- **EXT-1 (ASK)** Installing an extension, or adding one to a recommendations or dev container file. State the full extension ID and publisher. *Why:* ART-1; extensions run with the developer's access (GlassWorm).
- **EXT-2 (ASK)** You cannot confirm the publisher ID is the vendor's own, for example through a link from the vendor's documentation. *Why:* ID-2; marketplaces contain lookalike extensions.
- **EXT-3 (NOTE)** Install an exact version where the mechanism allows it (`code --install-extension <publisher>.<name>@<version>`). Apply AGE-1. *Why:* malicious updates to existing extensions reached users automatically.
- **EXT-4 (ASK)** Changing extension auto-update settings in either direction. *Why:* it is the user's editor; turning auto-update on removes the cooldown.
- **EXT-5 (NOTE)** Install counts and ratings are not evidence of safety. *Why:* ADP-1.
- **EXT-6 (NOTE)** The same extension may differ between marketplaces. Name the marketplace you checked. *Why:* GlassWorm spread first through one registry.
