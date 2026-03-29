---
framework: Swift Macros
session: WWDC23-10166
year: 2023
applies_to: iOS 17+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/swift-macros.md
---

# Swift Macros — WWDC23 Introduction

Swift Macros were introduced at WWDC23 (Swift 5.9) as a type-safe, compile-time code generation mechanism.

## What's new

- `@freestanding(expression)` — macro that produces a value expression
- `@freestanding(declaration)` — macro that produces one or more declarations
- `@attached(member)` — adds members (properties, methods) to a type
- `@attached(accessor)` — adds property accessors
- `@attached(peer)` — adds a peer declaration alongside the annotated declaration
- `@attached(conformance)` — adds a protocol conformance to a type
- `@attached(memberAttribute)` — adds attributes to members of a type
- Macros distributed as Swift Packages with a `macro` + compiler plugin target
- Testing via `assertMacroExpansion` from `SwiftSyntaxMacrosTestSupport`
- Expansion visible in Xcode: right-click → Expand Macro

## Before / After

**Before (manual Equatable implementation):**
```swift
struct Point {
    let x: Double
    let y: Double
}

extension Point: Equatable {
    static func == (lhs: Point, rhs: Point) -> Bool {
        lhs.x == rhs.x && lhs.y == rhs.y
    }
}
```

**After (macro-synthesized):**
```swift
// Swift already synthesizes Equatable for structs with Equatable members,
// but for a custom example using a macro:
@CustomEquatable  // hypothetical macro
struct Point {
    let x: Double
    let y: Double
}
// The macro generates the == implementation at compile time
```

*Real-world example: `@Observable` is an attached member macro that generates observation tracking boilerplate for every stored property.*

## Migration steps

1. Add `swift-syntax` as a package dependency (version matching your Swift toolchain)
2. Add a `macro` target to Package.swift declaring the macro signature
3. Add a `compilerPlugin` executable target implementing the macro using `SwiftSyntaxMacros`
4. Implement the appropriate `Macro` protocol (`ExpressionMacro`, `MemberMacro`, etc.)
5. Write expansion tests with `assertMacroExpansion` before using the macro in production code
6. Distribute via Swift Package Manager — macros cannot be distributed as pre-built binaries

## Compatibility notes

- Requires Swift 5.9+, Xcode 15+
- `swift-syntax` version must match the Swift toolchain version exactly
- Macros run in a sandboxed compiler plugin process — no filesystem or network access
- Cannot be distributed as pre-built binaries (source required)
