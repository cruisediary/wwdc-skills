# wwdc-skills

Claude Code skills for every Apple WWDC session — APIs, code examples, and migration guides updated yearly

This repository packages Apple WWDC session content (WWDC18–WWDC25) as structured reference files for iOS/Swift developers. It works as a Claude Code skill you invoke from the CLI, and as a reference library you can drop into any Claude Code setup.

## Usage

### As a Claude Code skill

Add this skill to your Claude Code configuration, then ask questions naturally:

```
What's new in SwiftData?
Migrate my app from Combine to AsyncSequence
Show me WWDC23 Observation session
```

SKILL.md is the entry point. It reads `references/INDEX.md` to locate the right reference file, then returns a focused answer in one of three shapes: code-first, guide-first, or migration (before/after).

### As a reference library

Individual files in `references/` can be copied into any project's `.claude/skills/` or `.claude/references/` directory. Each file is self-contained and works without the rest of this repo.

The `docs/` directory contains internal design documentation and does not need to be copied.

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

Canonical files in `references/canonical/` always reflect current best practice regardless of which year a framework was introduced. When a framework evolves across years, the canonical file is the authoritative source.

## How it works

`SKILL.md` is the router. On each invocation it reads `references/INDEX.md` to find the right file, then loads it and generates a response.

Three query modes (evaluated in priority order):

1. **Migration** — detected by keywords like "migrate", "convert", "replace", or "before/after". Returns a side-by-side before/after diff with explanation.
2. **Year/session** — detected when a WWDC year or session name is specified. Returns guide-first content for that session.
3. **Current API** (default) — returns a code-first answer using the canonical best practice for the topic.

## Contributing

To add a new year, create a `references/YYYY/` directory and add session files following the schema in the design spec (`docs/`). Append the new rows to `references/INDEX.md` so the router can find them. Update any affected canonical files in `references/canonical/` to reflect API changes or new best practices introduced that year.
