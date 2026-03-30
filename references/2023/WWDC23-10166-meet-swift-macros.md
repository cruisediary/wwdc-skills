---
framework: Swift Macros
title: "Meet Swift macros"
session: WWDC23-10166
year: 2023
applies_to: iOS 17+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/swift-macros.md
---

# Meet Swift Macros (WWDC23)

An introduction to Swift macros: freestanding macros (`#stringify`, `#require`), attached macros (`@Model`, `@Observable`), and visualizing expansion in Xcode 15.

## Quick start

```swift
// Freestanding expression macro — produces a value
let (value, code) = #stringify(1 + 2)
// value == 3, code == "1 + 2"

// Attached member macro — adds members to a type
@Observable
class Counter {
    var count = 0
    // @Observable synthesizes observation tracking for `count`
}

// Using a macro from a package
import MacroPackage
#warning("This is a compile-time warning from a macro")
```

## Key APIs

| API | Purpose |
|---|---|
| `#freestanding(expression)` | Macro role: produces a value expression at the call site |
| `#freestanding(declaration)` | Macro role: produces one or more declarations |
| `@attached(member)` | Macro role: adds members (properties, methods, initializers) to the annotated type |
| `@attached(accessor)` | Macro role: adds `get`/`set`/`willSet`/`didSet` accessors to a property |
| `@attached(peer)` | Macro role: adds a peer declaration alongside the annotated declaration |
| `@attached(conformance)` | Macro role: adds a protocol conformance |
| `@attached(memberAttribute)` | Macro role: adds attributes to members of the annotated type |
| `#stringify(_:)` | Example macro from Swift macro package templates — returns `(value, sourceCode)` |
| `#require(_:)` | Swift Testing macro — fails a test if the expression is nil or false |

## Common patterns

**Declaring a freestanding expression macro:**
```swift
// In a macro declaration module:
@freestanding(expression)
public macro stringify<T>(_ value: T) -> (T, String) =
    #externalMacro(module: "MyMacrosPlugin", type: "StringifyMacro")
```

**Declaring an attached member macro:**
```swift
@attached(member, names: named(init), named(storage))
public macro MyModel() =
    #externalMacro(module: "MyMacrosPlugin", type: "ModelMacro")
```

**Using @Observable (Apple's built-in attached macro):**
```swift
import Observation

@Observable
class Library {
    var books: [Book] = []
    var selectedBook: Book?
}

// The macro generates:
// - Observation storage backing store
// - Access tracking wrappers for each stored property
// - Conformance to Observable protocol
```

**Expanding a macro in Xcode:**
- Right-click on a macro invocation → "Expand Macro"
- The expanded source appears inline in the editor as a read-only overlay

**Viewing expansion during tests:**
```swift
import SwiftSyntaxMacrosTestSupport

assertMacroExpansion(
    """
    #stringify(1 + 2)
    """,
    expandedSource: """
    (1 + 2, "1 + 2")
    """,
    macros: testMacros
)
```

## Gotchas

- Macros are distributed as Swift packages with a compiler plugin target — they cannot be included in a framework or pre-built binary
- The `swift-syntax` package version must exactly match the Swift toolchain version (Xcode manages this automatically for SPM dependencies)
- Freestanding macros start with `#`; attached macros start with `@` — the role determines the syntax
- Macro expansion is deterministic and sandboxed — no filesystem access, no network, no randomness
- Xcode 15's "Expand Macro" feature is the primary debugging tool; there is no step-debugger for macro code
- `@Observable` is an Apple framework macro, not user-defined; it cannot be customized, only used
