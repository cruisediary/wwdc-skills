---
framework: Swift Package Manager
title: "What's New in Swift Package Manager"
session: WWDC17-411
year: 2017
applies_to: iOS 11+
status: deprecated
superseded_by: null
shape: code-first
related: []
---

> **Deprecated:** Covers SPM as shipped with Swift 4 / Xcode 9. The `Package.swift` manifest format has evolved significantly through SwiftPM 5.x. Use Swift Package Index documentation for current syntax.

## Quick start

```swift
// Package.swift (swift-tools-version:4.0)
import PackageDescription

let package = Package(
    name: "MyLibrary",
    products: [
        .library(name: "MyLibrary", targets: ["MyLibrary"]),
    ],
    dependencies: [
        .package(url: "https://github.com/apple/swift-argument-parser", from: "0.0.1"),
    ],
    targets: [
        .target(name: "MyLibrary", dependencies: []),
        .testTarget(name: "MyLibraryTests", dependencies: ["MyLibrary"]),
    ]
)
```

## Key APIs

| Concept | Description |
|---|---|
| `Package.swift` | Manifest file at package root; declares targets, products, dependencies |
| `.target` | A module with Swift/C source; maps to one build product |
| `.testTarget` | A test module linked with XCTest |
| `.product` | What the package exposes (library or executable) |
| `from: "1.0.0"` | Semantic version lower bound; resolver picks highest compatible version |
| `swift build` / `swift test` | CLI commands for building and testing |

## Common patterns

**Xcode 9 integration**

In Xcode 9, SPM packages could be opened as an Xcode project via `swift package generate-xcodeproj`. This workflow is deprecated in favor of native Xcode SPM support added in Xcode 11.

## Gotchas

- `swift-tools-version` at the top of `Package.swift` must match the Swift toolchain version; mismatches produce cryptic errors.
- `generate-xcodeproj` is no longer needed in Xcode 11+.
- `from: "0.0.1"` allows major-version bumps; prefer `.upToNextMajor(from:)` for stability.
