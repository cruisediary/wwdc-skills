---
framework: Xcode
title: "What's new in Xcode"
session: WWDC25-10135
year: 2025
applies_to: iOS 26+
status: reference-only
superseded_by: null
shape: migration
related:
  - 2024/WWDC24-10135-whats-new-in-xcode.md
---

# Xcode — What's New in Xcode (WWDC25)

Xcode 26 introduces expanded AI-assisted code completion, Swift 6.2 migration tooling, Liquid Glass preview support, and improved build performance.

## What's new

- **Enhanced predictive code completion** — builds on Xcode 16's AI completion with broader context awareness and multi-line suggestion support
- **Swift 6.2 migration assistant** — fix-its for removing redundant `@MainActor` annotations and flagging `nonisolated(unsafe)` usages; integrates with the concurrency checker
- **Liquid Glass preview** — SwiftUI and UIKit previews render Liquid Glass materials accurately without requiring a physical device
- **Explicit modules improvements** — continued build time improvements from Xcode 16's explicit module system; new dependency graph visualization
- **Simulator updates** — visionOS 26 and iOS 26 simulators with improved Liquid Glass rendering fidelity
- **Testing improvements** — Swift Testing integration deepened; additional test result filtering and re-run capabilities (see Apple docs)

## Before / After

**Before (Xcode 16 — redundant `@MainActor` required manual removal):**
```swift
// Developer had to manually find and remove redundant annotations
@MainActor
class MyViewController: UIViewController {
    @MainActor func update() { ... }
}
```

**After (Xcode 26 — fix-it removes redundant annotations automatically):**
```swift
// Xcode 26 warns: "@MainActor is redundant on UIViewController subclass"
// Fix-it: Remove @MainActor
class MyViewController: UIViewController {
    func update() { ... }  // implicit @MainActor via UIViewController conformance
}
```

## Migration steps

1. Install Xcode 26 and open the project — Swift 6.2 migration warnings appear automatically for redundant `@MainActor` and `nonisolated(unsafe)` usages
2. Use "Fix All Issues" in the Issue navigator to apply bulk fix-its for actor isolation cleanup
3. Build with the iOS 26 / visionOS 26 SDK and review Liquid Glass rendering in previews before testing on device
4. Check build times — explicit modules are more aggressive in Xcode 26; very large targets may need `OTHER_SWIFT_FLAGS` tuning
5. Migrate remaining XCTest suites to Swift Testing using the migration fix-its (see WWDC24-10196 for XCTest migration guide)

## Compatibility notes

- Xcode 26 requires macOS 15+ to install
- Projects can still target older iOS/visionOS versions; iOS 26 SDK features require `#available` guards
- Predictive code completion requires an internet connection for model inference (behavior may vary in offline environments)
- Explicit module build improvements are automatically applied; no build setting change required
