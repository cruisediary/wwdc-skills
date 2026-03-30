---
framework: Swift
title: "What's new in Swift"
session: WWDC21-10192
year: 2021
applies_to: iOS 15+
status: reference-only
superseded_by: null
shape: migration
related: []
---

# What's New in Swift (WWDC21)

Swift 5.5 additions: `async`/`await`, `Sendable`, `#if canImport`, property wrapper improvements, `@available` without version, and result builders (now stable).

## What's new

- **`async`/`await`** — see WWDC21-10132 for full detail
- **`actor` type** — see WWDC21-10133 for full detail
- **`Sendable` protocol** — marks types safe to pass across concurrency boundaries
- **`#if canImport(Module)`** — conditional compilation based on module availability
- **`@available` without version number** — `@available(*, unavailable)` and `@available(*, deprecated)` without specifying a platform version
- **Result builders (stable)** — formerly `_functionBuilder`, now `@resultBuilder`; used by `@ViewBuilder`, `@SceneBuilder`, etc.
- **`CGFloat` / `Double` interoperability** — implicit coercion between `CGFloat` and `Double`
- **`async let`** — parallel async bindings (see WWDC21-10134)
- **Improved property wrappers** — property wrappers can now be applied to function parameters

## Key APIs

```swift
// Sendable — marks a type safe to cross actor/task boundaries
struct UserID: Sendable {
    let value: Int
}

// Classes can be Sendable if they protect their state
final class Counter: @unchecked Sendable {
    private let lock = NSLock()
    private var _count = 0
    var count: Int {
        lock.lock(); defer { lock.unlock() }
        return _count
    }
}

// #if canImport — conditional compilation
#if canImport(UIKit)
import UIKit
typealias PlatformColor = UIColor
#elseif canImport(AppKit)
import AppKit
typealias PlatformColor = NSColor
#endif

// @available without version
@available(*, deprecated, renamed: "newFunction()")
func oldFunction() { }

@available(*, unavailable, message: "Use the async version instead")
func syncFetch(completion: (Data) -> Void) { }

// @resultBuilder (stable)
@resultBuilder
struct StringBuilder {
    static func buildBlock(_ components: String...) -> String {
        components.joined(separator: " ")
    }
}

@StringBuilder
func greeting() -> String {
    "Hello"
    "World"
}
// Result: "Hello World"

// CGFloat / Double interop — no explicit conversion needed
let width: CGFloat = 100
let scale: Double = 2.0
let scaled: CGFloat = width * scale   // no CGFloat(scale) needed in Swift 5.5+

// Property wrappers on function parameters
@propertyWrapper
struct Clamped {
    var wrappedValue: Int { didSet { wrappedValue = max(0, min(100, wrappedValue)) } }
    init(wrappedValue: Int) { self.wrappedValue = max(0, min(100, wrappedValue)) }
}

// Lazy locals (SE-0292)
func process() {
    lazy var result = expensiveComputation()
    if needsResult {
        use(result)   // computed only when accessed
    }
}
```

## Migration steps

1. Adopt `Sendable` on types passed between tasks or actors; the compiler warns in strict concurrency mode
2. Replace `as! CGFloat` casts with direct `Double`/`CGFloat` assignment where Swift 5.5 implicit coercion applies
3. Replace `_functionBuilder` (beta spelling) with `@resultBuilder` in any custom DSLs
4. Use `#if canImport(UIKit)` instead of `#if os(iOS) || os(watchOS) || os(tvOS)` for framework-availability checks

## Compatibility notes

- Swift 5.5 ships with Xcode 13, targeting iOS 15+ for async/await features
- `Sendable` warnings appear incrementally; `SWIFT_STRICT_CONCURRENCY = targeted` in build settings
- `CGFloat`/`Double` coercion is source-compatible — no existing code breaks
- Result builders (`@resultBuilder`) are ABI-stable from Swift 5.5 forward; `_functionBuilder` was renamed without behaviour change
