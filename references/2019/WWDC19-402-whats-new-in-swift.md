---
framework: Swift
title: "What's New in Swift"
session: WWDC19-402
year: 2019
applies_to: iOS 13+
status: reference-only
superseded_by: null
shape: migration
related: []
---

# What's New in Swift (WWDC19)

Swift 5.1 introduced the language features that make SwiftUI possible: opaque return types (`some View`), property wrappers (`@State`, `@Binding`), implicit returns from single-expression functions, and `@_functionBuilder` (later renamed `@resultBuilder`).

## What's new

- **Opaque return types** (`some Protocol`) — return a specific but unnamed type that conforms to a protocol; callers see the protocol, the compiler sees the concrete type
- **Property wrappers** (`@propertyWrapper`) — attach reusable get/set logic to a stored property; basis for `@State`, `@Binding`, `@Published`
- **Implicit return** — single-expression function and computed property bodies no longer need `return`
- **`@_functionBuilder`** — (experimental in 5.1; renamed `@resultBuilder` in Swift 5.4) enables `@ViewBuilder` and DSL-style closures
- **`Self` in class methods** — refer to the dynamic type with `Self` in protocols and classes
- **Module stability** — binary frameworks can be used across different Swift compiler versions

## Before / After

**Opaque return types — `some View`:**
```swift
// Before Swift 5.1: must name the concrete return type
// This was impossible for complex SwiftUI body types
func makeLabel() -> Text {
    Text("Hello")
}

// After (Swift 5.1): return "something that is a View"
func makeLabel() -> some View {
    Text("Hello")
        .font(.headline)
        .foregroundColor(.blue)
}
// The concrete type is inferred by the compiler; callers only see `some View`
```

**Property wrappers:**
```swift
// Before: manual get/set with backing storage
private var _count: Int = 0
var count: Int {
    get { _count }
    set { _count = newValue; notifyObservers() }
}

// After: declare a @propertyWrapper, use it like an attribute
@propertyWrapper
struct Clamped {
    private var value: Int
    private let range: ClosedRange<Int>
    var wrappedValue: Int {
        get { value }
        set { value = min(max(range.lowerBound, newValue), range.upperBound) }
    }
    init(wrappedValue: Int, _ range: ClosedRange<Int>) {
        self.range = range
        self.value = min(max(range.lowerBound, wrappedValue), range.upperBound)
    }
}

struct Settings {
    @Clamped(0...100) var volume = 50
}
```

**Implicit return:**
```swift
// Before
var doubled: Int {
    return value * 2
}

// After (Swift 5.1)
var doubled: Int { value * 2 }
```

## Migration steps

1. Update `swift-tools-version` in `Package.swift` to `5.1` if using Swift Package Manager.
2. Remove explicit `return` from single-expression computed properties and functions (optional, but idiomatic Swift).
3. Adopt `some Protocol` as return types for factory methods and protocol conformances where the concrete type is an implementation detail.
4. When defining custom property wrappers, implement `wrappedValue` as the primary accessor; optionally add `projectedValue` (accessed via `$name`) for a binding or publisher.
5. `@_functionBuilder` / `@resultBuilder` is for framework authors building DSLs — do not use the underscore-prefixed version in production code; use `@resultBuilder` (Swift 5.4+).

## Compatibility notes

- `some Protocol` requires Swift 5.1 / Xcode 11+
- Property wrappers require Swift 5.1 / Xcode 11+
- `@resultBuilder` (stable name) requires Swift 5.4 / Xcode 12.5+; `@_functionBuilder` (used internally by SwiftUI in iOS 13) is compiler-private and not for app code
- Module stability (`.swiftinterface`) is needed for binary Swift frameworks distributed without source
