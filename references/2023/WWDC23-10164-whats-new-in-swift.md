---
framework: Swift
title: "What's new in Swift"
session: WWDC23-10164
year: 2023
applies_to: iOS 17+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/swift-macros.md
---

# What's New in Swift (WWDC23)

Swift 5.9 introduced macros, parameter packs, expression-level `if`/`switch`, and `nonisolated(unsafe)` for concurrency.

## What's new

- **Swift macros** — compile-time code generation via `@attached` and `#freestanding` macros; shipped as Swift packages
- **Parameter packs** (`repeat each T`) — variadic generics enabling functions and types that work with any number of type parameters
- **`if` and `switch` as expressions** — these control-flow constructs can now be used as the right-hand side of an assignment or as a function return value
- **`nonisolated(unsafe)`** — opts a stored property out of actor isolation checking; a last-resort escape hatch for interop with C/Objective-C APIs
- **Improved `#if` in member position** — conditional compilation blocks can appear inside types and extensions without restrictions
- **Observation framework** — `@Observable` replaces `ObservableObject`/`@Published` (see WWDC23-10149)
- **SwiftData** — `@Model` is itself an attached macro (see WWDC23-10187)

## Before / After

**if/switch as expressions:**

Before:
```swift
let color: Color
if isSelected {
    color = .blue
} else {
    color = .gray
}
```

After (Swift 5.9):
```swift
let color: Color = if isSelected { .blue } else { .gray }
```

**Parameter packs:**

Before (requires overloads for each arity):
```swift
func zip<A, B>(_ a: A, _ b: B) -> (A, B) { (a, b) }
func zip<A, B, C>(_ a: A, _ b: B, _ c: C) -> (A, B, C) { (a, b, c) }
// etc.
```

After (Swift 5.9 — one generic definition):
```swift
func zip<each T>(_ value: repeat each T) -> (repeat each T) {
    (repeat each value)
}
let pair   = zip(1, "hello")           // (Int, String)
let triple = zip(1, "hello", true)     // (Int, String, Bool)
```

**nonisolated(unsafe):**

Before (required `@unchecked Sendable` workaround):
```swift
final class Bridge: @unchecked Sendable {
    var legacyCPointer: UnsafeMutableRawPointer
}
```

After:
```swift
final class Bridge: Sendable {
    nonisolated(unsafe) var legacyCPointer: UnsafeMutableRawPointer
}
```

## Migration steps

1. Update to Xcode 15 / Swift 5.9 toolchain — no source changes required for existing code
2. Adopt `if`/`switch` as expressions where it reduces `var` declarations — a readability improvement, not a requirement
3. Evaluate `@Observable` as a replacement for `ObservableObject` in new views (requires iOS 17+ deployment target)
4. For macro adoption: add `swift-syntax` as a package dependency and create a macro target when ready to write custom macros
5. Use `repeat each T` only where overload explosion is a real problem; it has a steeper learning curve than regular generics
6. Use `nonisolated(unsafe)` only for C interop or legacy stored properties that cannot be made `Sendable` — prefer actor isolation for new code

## Compatibility notes

- All Swift 5.9 features require Xcode 15+ and the Swift 5.9 compiler; no minimum deployment target restrictions for language features
- `@Observable` and `@Model` require iOS 17+ / macOS 14+ at runtime (they use observation runtime support)
- Parameter packs produce `(repeat each T)` tuple types — these cannot be iterated with `for-in` directly in Swift 5.9; use `repeat` expressions instead
- `nonisolated(unsafe)` suppresses actor isolation warnings but provides no runtime safety guarantees — any unsynchronized access is still a data race
