---
framework: Xcode
title: "What's New in Xcode"
session: WWDC19-401
year: 2019
applies_to: iOS 13+
status: reference-only
superseded_by: null
shape: migration
related: []
---

# What's New in Xcode (WWDC19)

Xcode 11 ships with the SwiftUI canvas, a code minimap, Swift Package Manager integration in the IDE, and device condition simulation for testing.

## What's new

- **SwiftUI Canvas (Previews)** — split editor shows a live, interactive preview of SwiftUI views alongside the source; no simulator needed for visual iteration
- **Minimap** — a condensed overview of the entire file on the right side of the editor; click or drag to jump to any location
- **Swift Package Manager integration** — add, remove, and update SPM packages directly in File > Swift Packages; no Homebrew or command line required
- **`#if DEBUG` / Editor Conditions** — simulate device conditions (network link conditioner, thermal state, location) from the Xcode debug toolbar without leaving the IDE
- **Source Control improvements** — per-line code authorship (blame) inline in the editor gutter; stash support
- **Test Plans** — `.xctestplan` files configure multiple test runs with different environment variables, arguments, and schemes

## Before / After

**Adding a dependency (before Xcode 11):**
```
1. Install CocoaPods or Carthage via Homebrew
2. Create/edit Podfile or Cartfile
3. Run `pod install` / `carthage update` in Terminal
4. Open .xcworkspace (CocoaPods) or link frameworks manually (Carthage)
5. Commit the lockfile and generated artefacts
```

**Adding a dependency (Xcode 11 + SPM):**
```
File > Add Packages…
→ Paste GitHub URL
→ Choose version rule
→ Done — Xcode resolves, fetches, and links the package automatically
```

**Iterating on UI (before SwiftUI canvas):**
```
Edit source → ⌘R → wait for build → navigate to screen → observe → repeat
```

**Iterating on UI (Xcode 11 SwiftUI canvas):**
```
Edit source → canvas live-updates → click to interact → no full build for layout changes
```

## Migration steps

1. Open your project in Xcode 11 — SPM packages can be added immediately without changing the project format for other team members.
2. Migrate any existing CocoaPods/Carthage dependencies that have SPM support to reduce build system complexity.
3. Adopt `#Preview { }` (Xcode 15) or `PreviewProvider` (Xcode 11–14) for any new SwiftUI views to get live canvas feedback.
4. Enable Test Plans (`Product > Test Plan > New Test Plan`) for projects with multiple test configurations (debug vs release, different locales).
5. Use the Minimap for navigating large files — add `// MARK: -` comments to create visible section dividers in the minimap.

## Compatibility notes

- SwiftUI Previews require macOS 10.15 (Catalina) or later on the development Mac
- SPM is integrated but uses `.xcworkspace`-compatible resolution — existing CocoaPods workspaces are unaffected
- Test Plans (`.xctestplan`) require Xcode 11+ and are ignored by older Xcode versions
- The minimap is always available regardless of SwiftUI or iOS target version
