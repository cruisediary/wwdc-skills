---
framework: Xcode
title: "What's new in Xcode"
session: WWDC24-10135
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: migration
related: []
---

## What's new

- **Predictive code completion**: On-device ML model suggests multi-token completions as you type; accepts with Tab
- **Swift 6 migration assistant**: Build setting `SWIFT_STRICT_CONCURRENCY` steps you up incrementally; new migration guide in the Report navigator
- **Explicit modules** (see WWDC24-10171): Xcode 16 builds Swift and Clang modules explicitly for faster, more parallelized builds
- **RealityKit debugger**: New debug gauge in the Debug bar; inspect entity hierarchy, components, and transforms in a live scene viewer
- **Source Control improvements**: Inline blame annotations in the editor gutter; cherry-pick commits from the Changes navigator

## Before / After

```swift
// Before (Xcode 15): no on-device completion; manual Sendable annotations
// After (Xcode 16): predictive completion suggests full expressions inline

// Swift 6 migration: start with minimal concurrency warnings
// Before: SWIFT_STRICT_CONCURRENCY = minimal (default in Xcode 15)
// After:  SWIFT_STRICT_CONCURRENCY = complete  (Xcode 16 target for Swift 6)

// RealityKit debugger: previously required print statements to inspect entities
// After: pause execution → Debug bar → RealityKit icon → live entity inspector
```

## Migration steps

1. Open project in Xcode 16; note any new Swift 6 warnings in Issue navigator
2. Set `SWIFT_STRICT_CONCURRENCY = targeted` in Build Settings to surface concurrency issues incrementally
3. Use the Migration Guide (Product > Swift Migration) to review recommended fixes
4. Enable explicit modules: `SWIFT_PACKAGE_ENABLE_EXPLICIT_MODULES = YES` (on by default for new projects)
5. For RealityKit apps: run on device or simulator, pause, then tap the RealityKit debugger icon in the Debug bar to inspect the live scene
6. Review inline blame via Editor > Show Source Control Changes to identify regression commits

## Compatibility notes

- Predictive code completion: Xcode 16+ only; runs fully on-device (no network required)
- Swift 6 strict concurrency: opt-in per target; existing code continues to compile under Swift 5 mode
- Explicit modules: Xcode 16+ build system; transparent to source code
- RealityKit debugger: requires RealityKit 2+ (iOS 14+), fully featured on iOS 18 / visionOS 2
