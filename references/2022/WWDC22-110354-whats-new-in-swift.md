---
framework: Swift
title: "What's new in Swift"
session: WWDC22-110354
year: 2022
applies_to: iOS 16+
status: reference-only
superseded_by: null
shape: migration
related: []
---

# What's new in Swift — WWDC22

Swift 5.7 was introduced at WWDC22 with significant language ergonomics improvements, a new regex engine, and the `Clock` protocol for time-based abstractions.

## What's new

- `if let` shorthand — `if let x` instead of `if let x = x` (shadow shorthand)
- `any` keyword for existentials — `any Equatable` makes the boxing explicit and visible
- `some` for primary associated types — `some Collection<Int>` constrains the element type
- Regex literals — `/pattern/` syntax compiled and type-checked at build time
- `Regex<Output>` type and `RegexBuilder` DSL for composable, readable patterns
- `Clock` protocol — `ContinuousClock`, `SuspendingClock`; `sleep(until:clock:)` on `Task`
- `Duration` type — strongly typed time intervals used with `Clock`
- Improved string processing — `BidirectionalCollection` matching, `firstMatch(of:)`, `wholeMatch(of:)`
- Opaque result types in parameter position — `func f(_ x: some Equatable)`
- Distributed actors (see WWDC22-110356 for full coverage)

## Before / After

**Before (optional binding — verbose shadow):**
```swift
if let value = value {
    print(value)
}
```

**After (Swift 5.7 shorthand):**
```swift
if let value {
    print(value)
}
```

**Before (existential — implicit boxing):**
```swift
func log(_ value: Equatable) { ... }
```

**After (explicit `any`):**
```swift
func log(_ value: any Equatable) { ... }
```

**Regex literal:**
```swift
let pattern = /(\d{4})-(\d{2})-(\d{2})/
if let match = input.firstMatch(of: pattern) {
    let year = match.1   // Substring, compile-time typed
}
```

**Clock / Duration:**
```swift
let clock = ContinuousClock()
let elapsed = await clock.measure {
    await doWork()
}
// elapsed is a Duration
try await Task.sleep(until: .now + .seconds(2), clock: .continuous)
```

## Migration steps

1. Replace `if let x = x` with `if let x` throughout the codebase (Xcode fix-it available)
2. Add `any` keyword to bare existential types flagged by the Swift 5.7 compiler
3. Migrate `NSRegularExpression` patterns to regex literals or `RegexBuilder` where iOS 16+ is the target
4. Replace `DispatchTime` / `DispatchWallTime` with `Clock` + `Duration` in new async code
5. Adopt `some Collection<Element>` constrained opaque types to remove unnecessary generics

## Compatibility notes

- `if let` shorthand and `any` keyword require Swift 5.7 (Xcode 14)
- Regex literals require iOS 16+ / macOS 13+ at runtime (older OS → use `try! NSRegularExpression(...)`)
- `Clock` and `Duration` are available on iOS 16+ / macOS 13+
- The `any` keyword is a warning in Swift 5.7 and an error in Swift 6
