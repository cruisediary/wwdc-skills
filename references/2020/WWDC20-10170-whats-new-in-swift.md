---
framework: Swift
title: "What's new in Swift"
session: WWDC20-10170
year: 2020
applies_to: iOS 14+
status: reference-only
superseded_by: null
shape: migration
related: []
---

# What's new in Swift — WWDC20 (Swift 5.3)

Swift 5.3 shipped with Xcode 12 and iOS 14. Key themes: expressive language features, diagnostics improvements, and cross-platform (Linux/Windows) progress.

## What's new

- `where` clauses on contextually generic members
- Multiple trailing closures syntax
- `@main` attribute for entry points
- Multi-pattern `catch` clauses
- Implicit `self` capture in closures when `self` is a value type or after `[self]` capture
- `Float16` type
- `ContiguousArray` and collection diffing improvements
- Swift Package Manager: resources, localization, binary targets (`binaryTarget`)
- Improved compiler diagnostics ("expression too complex" error eliminated for many cases)

## Before / After

**Multiple trailing closures (before):**
```swift
// Swift 5.2 — second closure must be in parentheses
UIView.animate(withDuration: 0.3, animations: {
    view.alpha = 0
}, completion: { _ in
    view.removeFromSuperview()
})
```

**Multiple trailing closures (after):**
```swift
// Swift 5.3 — both closures as trailing syntax
UIView.animate(withDuration: 0.3) {
    view.alpha = 0
} completion: { _ in
    view.removeFromSuperview()
}
```

**Multi-pattern catch (before):**
```swift
do {
    try riskyOperation()
} catch NetworkError.timeout {
    handle(.timeout)
} catch NetworkError.noConnection {
    handle(.noConnection)
}
```

**Multi-pattern catch (after):**
```swift
do {
    try riskyOperation()
} catch NetworkError.timeout, NetworkError.noConnection {
    handle(.networkUnavailable)
}
```

**`where` on contextually generic members (before):**
```swift
// Had to subclass or add non-generic overloads
```

**`where` on contextually generic members (after):**
```swift
extension Collection {
    func sum() -> Element where Element: Numeric {
        reduce(.zero, +)
    }
}
```

**`@main` attribute:**
```swift
// Before: required a top-level expression file (main.swift)
// After: any type can be the entry point
@main
struct CLI {
    static func main() {
        print("Hello from @main")
    }
}
```

**`Float16`:**
```swift
let half: Float16 = 1.5
// Useful for ML model inputs, GPU compute, memory-constrained buffers
```

**SPM binary targets:**
```swift
// Package.swift
let package = Package(
    name: "MyPackage",
    targets: [
        .binaryTarget(
            name: "SomePrebuiltLib",
            url: "https://example.com/SomePrebuiltLib.xcframework.zip",
            checksum: "abc123..."
        )
    ]
)
```

## Migration steps

1. Adopt multiple trailing closure syntax in existing code (purely additive; old syntax still works)
2. Collapse redundant single-pattern catch clauses into multi-pattern catch where appropriate
3. Add `where` clauses to extension members instead of duplicating logic in subclasses
4. Migrate command-line tool entry points to `@main` (requires removing `main.swift`)
5. For SPM packages with bundled resources, add `.process("Resources")` to target resources

## Compatibility notes

- Swift 5.3 ships with Xcode 12; back-deployment of binaries to iOS 13 and earlier is supported
- `@main` and `App` protocol work together — `@main struct MyApp: App` is the idiomatic iOS 14 entry point
- `Float16` is available on all Apple platforms but hardware-accelerated only on A-series / Apple Silicon
- Binary targets in SPM only support `.xcframework` format; source-only packages continue to work as before
- Multi-pattern catch requires all patterns in a clause to bind the same variables (or none)
