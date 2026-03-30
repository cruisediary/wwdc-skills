# wwdc-skills

Claude Code skills for every Apple WWDC session — APIs, code examples, and migration guides updated yearly

This repository packages Apple WWDC session content (WWDC18–WWDC25) as structured reference files for iOS/Swift developers. It works as a Claude Code skill you invoke from the CLI, and as a reference library you can drop into any Claude Code setup.

## Installation

### As an agentskills-compatible skill

This skill follows the [agentskills](https://github.com/agentskills/agentskills) open format. Install it into your skills directory:

```bash
# User-level (available in all projects)
git clone https://github.com/cruisediary/wwdc-skills ~/.agents/skills/wwdc-skills

# Or project-level
git clone https://github.com/cruisediary/wwdc-skills .agents/skills/wwdc-skills
```

Once installed, Claude Code will discover it automatically from the skill catalog.

### As a Claude Code reference library

Clone or copy individual files from `references/` into any project:

```bash
# Full library
git clone https://github.com/cruisediary/wwdc-skills

# Single file (self-contained, no dependencies)
curl -O https://raw.githubusercontent.com/cruisediary/wwdc-skills/main/references/canonical/swiftui.md
```

## Usage

### As a Claude Code skill

Add this skill to your Claude Code configuration, then ask questions naturally:

```
What's new in SwiftData?
Migrate my app from Combine to AsyncSequence
Show me WWDC23 Observation session
WWDC24-10179
```

SKILL.md is the entry point. It reads `references/INDEX.md` to locate the right reference file, then returns a focused answer in one of three shapes: code-first, guide-first, or migration (before/after).

### As a reference library

Individual files in `references/` can be copied into any project's `.claude/skills/` or `.claude/references/` directory. Each file is self-contained and works without the rest of this repo.

## What's covered

| Year | Key Topics |
|------|-----------|
| WWDC18 | Swift 4.2, ARKit 2, Create ML, Siri Shortcuts |
| WWDC19 | SwiftUI, Combine |
| WWDC20 | App Clips, WidgetKit |
| WWDC21 | Swift Concurrency (async/await, actors) |
| WWDC22 | Swift Charts, NavigationStack |
| WWDC23 | SwiftData, Observation, Swift Macros, visionOS |
| WWDC24 | SwiftData refinements (#Index, #Unique), Swift Testing |
| WWDC25 | Liquid Glass, Swift Concurrency (default isolation), WebView |

150+ session files across WWDC18–WWDC25. Canonical files in `references/canonical/` always reflect current best practice regardless of which year a framework was introduced.

## How it works

`SKILL.md` is the router. On each invocation it reads `references/INDEX.md` to find the right file, then loads it and generates a response.

Five query modes (evaluated in priority order):

1. **Migration** — "migrate", "convert", "replace", or "before/after". Returns a side-by-side before/after diff.
2. **Session ID** — exact session ID like `WWDC24-10179` or `WWDC18-713`. Loads that session directly.
3. **Year/session** — WWDC year + framework name. Returns session-specific content.
4. **Session title** — partial title match against session names in INDEX.md.
5. **Current API** (default) — loads the canonical best-practice file for the framework.

## Contributing

To add a new year, create a `references/YYYY/` directory and add session files following the schema in `SKILL.md`. Append new rows to `references/INDEX.md`. Update affected canonical files in `references/canonical/` to reflect the latest best practices.

Run `python3 scripts/audit.py` to verify structural integrity before submitting.

## License

MIT © [cruisediary](https://github.com/cruisediary)
