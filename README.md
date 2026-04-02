# wwdc-skills

Claude Code skills for every Apple WWDC session — APIs, code examples, and migration guides from WWDC17 to WWDC25

This repository packages Apple WWDC session content as structured reference files for iOS/Swift developers. It works as a Claude Code skill you invoke from the CLI, and as a reference library you can drop into any Claude Code setup.

## Coverage

```
references/
├── canonical/          (17 files — always current best practice)
│   ├── arkit.md
│   ├── combine.md
│   ├── swiftui.md
│   └── ...
│
├── 2017/  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  25 sessions  [iOS 11]
│   ├── ARKit · Core ML · Vision
│   ├── Drag & Drop · PDFKit · Core NFC
│   └── Swift 4 · Xcode 9 · SiriKit
│
├── 2018/  ━━━━━━━━━━━━  11 sessions  [iOS 12]
│   ├── ARKit 2 · Create ML · Siri Shortcuts
│   └── Swift 4.2 · Network.framework
│
├── 2019/  ━━━━━━━━━━━━━━━━━  15 sessions  [iOS 13]
│   ├── SwiftUI · Combine · SF Symbols
│   └── Dark Mode · Sign in with Apple
│
├── 2020/  ━━━━━━━━━━━━━━━━━  15 sessions  [iOS 14]
│   ├── App Clips · WidgetKit · StoreKit 2
│   └── Swift Concurrency foundations
│
├── 2021/  ━━━━━━━━━━━━━━━━  14 sessions  [iOS 15]
│   ├── async/await · Actors · AsyncSequence
│   └── AttributedString · DocC
│
├── 2022/  ━━━━━━━━━━━━━━━━━━━━━━━  22 sessions  [iOS 16]
│   ├── Swift Charts · NavigationStack
│   ├── SwiftUI layout · TipKit
│   └── App Intents · Lock Screen widgets
│
├── 2023/  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  39 sessions  [iOS 17]
│   ├── SwiftData · Observation · Swift Macros
│   ├── visionOS · RealityKit 4
│   └── Swift Testing (preview) · StoreKit 3
│
├── 2024/  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  40 sessions  [iOS 18]
│   ├── Swift Testing · SwiftData refinements
│   ├── SwiftUI Mesh gradient · Xcode 16
│   └── Apple Intelligence foundations
│
└── 2025/  ━━━━━━━━━━━━━━━  14 sessions  [iOS 19]
    ├── Liquid Glass · Swift 6.1
    └── visionOS 3 · App Intents v3
```

**175 session files** across WWDC17–WWDC25 · **17 canonical** framework files

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

`SKILL.md` is the entry point. It reads `references/INDEX.md` to locate the right reference file, then returns a focused answer in one of three shapes: code-first, guide-first, or migration (before/after).

### As a reference library

Individual files in `references/` can be copied into any project's `.claude/skills/` or `.claude/references/` directory. Each file is self-contained and works without the rest of this repo.

## How it works

Five query modes (evaluated in priority order):

| Priority | Mode | Trigger | Returns |
|----------|------|---------|---------|
| 1 | **Migration** | "migrate", "convert", "replace" | Side-by-side before/after diff |
| 2 | **Session ID** | `WWDC24-10179`, `WWDC17-602` | That session directly |
| 3 | **Year + framework** | WWDC year + framework name | Session-specific content |
| 4 | **Title match** | Partial title search | Closest session match |
| 5 | **Current API** | Everything else | Canonical best-practice file |

Session ID formats:
- `WWDC17–19`, `WWDC25`: 3-digit (e.g. `WWDC17-602`)
- `WWDC20–24`: 5-digit (e.g. `WWDC24-10179`)
- `WWDC22`: some 6-digit (e.g. `WWDC22-110354`)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full schema and contribution guide.

Run `python3 scripts/audit.py` before submitting to verify structural integrity.

## License

MIT © [cruisediary](https://github.com/cruisediary)
