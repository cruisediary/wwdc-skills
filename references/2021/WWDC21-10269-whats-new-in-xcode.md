---
framework: Xcode
title: "What's new in Xcode"
session: WWDC21-10269
year: 2021
applies_to: iOS 15+
status: reference-only
superseded_by: null
shape: migration
related: []
---

# What's New in Xcode (WWDC21)

Xcode 13 additions: Swift Package Collections, source control improvements (pull request review in Xcode), Vim keybindings, column breakpoints, and Xcode Cloud integration.

## What's new

- **Swift Package Collections** — curated, shareable lists of Swift packages (JSON feed format)
- **Source control — pull request review** — view, comment on, and approve pull requests from GitHub/Bitbucket/GitLab directly in Xcode
- **Vim keybindings** — full Vim modal editing in the source editor (enable in Preferences → Text Editing → Editing)
- **Column breakpoints** — set a breakpoint on a specific expression within a line (right-click → Add Column Breakpoint)
- **Xcode Cloud** — CI/CD integrated into Xcode (see WWDC21-10267)
- **Improved test results** — richer test result bundles with video, screenshots, and diagnostics
- **`#available` code completion** — Xcode suggests platform/version combinations
- **Improved Swift Package Manager** — local package overrides, build tool plugins (preview)

## Key workflows

### Swift Package Collections

```
Xcode → File → Add Packages…
  → Click the "+" in the source list
  → Add a collection URL (e.g., https://swiftpackageindex.com/packages.json)
  → Browse and add packages from the collection

# A Swift Package Collection is a JSON file:
{
  "name": "My Team Packages",
  "packages": [
    { "url": "https://github.com/org/package.git" },
    ...
  ]
}
# Distribute via HTTPS; sign with a developer certificate for trust
```

### Source control — Pull Requests

```
Source Control Navigator (⌘2) → Pull Requests tab
  → View open PRs from connected GitHub/Bitbucket/GitLab accounts
  → Click a PR → see diff, comments, CI status
  → Add inline comments, approve, request changes
  → Merge directly from Xcode
```

### Vim keybindings

```
Preferences → Text Editing → Editing → Enable Vim Key Bindings
  → Normal mode: h/j/k/l navigation, dd delete line, yy yank, p paste
  → Insert mode: i/a/o
  → Visual mode: v/V
  → Command: :w (save), :wq, :q!
  → Escape: return to Normal mode
  → Ctrl+[ : also returns to Normal mode
```

### Column breakpoints

```
In the source editor:
  → Right-click any expression on a line
  → "Add Column Breakpoint"
  → Debugger pauses at that specific expression, not the whole line
  → Useful for chained calls: a.b().c().d() — break at exactly .c()
```

### Improved test results

```
Test Navigator → Click a failed test
  → View screenshots captured at failure
  → View video replay of UI test execution
  → View CPU/memory diagnostics during test run
  → Download .xcresult bundle for offline analysis
```

## Migration steps

1. Evaluate adding a Swift Package Collection URL for your team's internal packages — reduces friction compared to individual package URLs
2. Connect GitHub/Bitbucket/GitLab in Preferences → Accounts to enable PR review in Xcode
3. Enable Vim keybindings in Preferences → Text Editing if desired — can be toggled without affecting other developers
4. Use column breakpoints instead of adding `print()` statements to debug chained expressions

## Compatibility notes

- Xcode 13 requires macOS 11.3+ (Big Sur) or macOS 12 (Monterey)
- Swift Package Collections require Swift 5.5 toolchain and SPM 5.5
- Pull request review supports GitHub (OAuth or token), Bitbucket Cloud, and GitLab; on-premise versions require additional configuration
- Vim keybindings are per-machine, stored in Xcode preferences — not shared via source control
- Column breakpoints are stored in `.xcbreakpoints` — can be committed to source control for team sharing
