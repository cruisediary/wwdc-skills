---
framework: Swift Package Manager
title: "Getting to Know Swift Package Manager"
session: WWDC18-411
year: 2018
applies_to: iOS 12+
status: deprecated
superseded_by: null
shape: guide-first
related: []
---

> **Deprecated:** This session covers SPM 0.x (Swift 4.2 era), before Xcode integration. The `Package.swift` manifest format and CLI commands shown here evolved significantly in Swift 5.x. For current SPM usage in Xcode projects, consult current Apple documentation.

## What changed and why

In 2018, Swift Package Manager was a command-line-only tool — no Xcode integration. Developers used it for server-side Swift, CLI tools, and cross-platform libraries. Xcode 11 (2019) introduced first-class SPM support; the patterns here are primarily of historical interest.

## Mental model

```
Package.swift  (manifest — defines targets, products, dependencies)
Sources/
  MyLib/       (library target)
  MyApp/       (executable target)
Tests/
  MyLibTests/  (test target)
```

A **Package** has **targets** (code units) and **products** (what it exposes: libraries or executables). **Dependencies** are other packages referenced by URL and version range.

## Usage

**Minimal Package.swift (Swift 4.2 format)**

```swift
// swift-tools-version:4.2
import PackageDescription

let package = Package(
    name: "MyLibrary",
    products: [
        .library(name: "MyLibrary", targets: ["MyLibrary"]),
    ],
    dependencies: [
        .package(url: "https://github.com/apple/swift-log.git", from: "1.0.0"),
    ],
    targets: [
        .target(name: "MyLibrary", dependencies: ["Logging"]),
        .testTarget(name: "MyLibraryTests", dependencies: ["MyLibrary"]),
    ]
)
```

**CLI commands (pre-Xcode integration)**

```bash
swift build                        # compile all targets
swift test                         # run all test targets
swift run MyExecutable             # build and run an executable target
swift package init --type library  # scaffold a new library package
swift package init --type executable
swift package update               # update resolved dependency versions
swift package generate-xcodeproj   # generate an Xcode project (deprecated in Xcode 12)
```

## Adopting this pattern

- `swift-tools-version` at the top of `Package.swift` controls which manifest API is available — always use the minimum version your team can support.
- In Xcode 11+, add packages via File > Add Packages instead of `swift package generate-xcodeproj`.
- Replace `.package(url:from:)` with `.package(url:exact:)` for reproducible builds in CI environments.
- Test targets must end in `Tests` by convention; the test runner discovers them automatically.

## Compatibility notes

- `swift-tools-version:4.2` manifests still parse in modern Swift toolchains.
- `swift package generate-xcodeproj` was deprecated in Xcode 12 and removed in Xcode 14 — migrate to native Xcode SPM integration.
- Server-side Swift packages (Vapor, Hummingbird) still use the same `Package.swift` manifest format.
