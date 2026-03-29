---
framework: Swift Macros
status: current
applies_to: iOS 17+
shape: guide-first
superseded_by: null
history:
  - year: 2023
    file: 2023/swift-macros.md
    summary: Swift Macros introduction — attached and freestanding macros, Swift Syntax
---

# Swift Macros

Compile-time code generation via Swift macros (Swift 5.9+, iOS 17+). Macros replace boilerplate that previously required code generators, Sourcery, or verbose protocol conformances.

## What changed and why

Before Swift Macros, repetitive Swift code (Equatable conformances, Codable keys, logging wrappers) required either manual implementation or external code generation tools that ran outside the Swift compiler. Macros are type-checked at compile time, debuggable in Xcode (right-click → Expand Macro), and distributed as Swift packages with full source visibility.

## Mental model

```
Freestanding macro  = standalone expression or declaration
                      (#Preview, #expect, #Predicate)
Attached macro      = annotates an existing declaration
                      (@Model, @Observable, @Test)

Macro roles:
  @attached(member)       — adds members to the annotated type
  @attached(accessor)     — adds getters/setters to a property
  @attached(peer)         — adds a sibling declaration
  @attached(conformance)  — adds a protocol conformance
  @freestanding(expression) — produces a value
  @freestanding(declaration) — produces declarations
```

Macros expand at compile time. The expansion is visible, debuggable, and produces the same code as if you'd written it by hand.

## Usage

```swift
// Using built-in macros
import SwiftUI
import SwiftData

@Observable        // attached member macro — generates observation boilerplate
class ViewModel { var count = 0 }

@Model             // attached member + conformance macro — generates persistence boilerplate
class Book { var title = "" }

#Preview {         // freestanding declaration macro
    ContentView()
}

// Writing a custom macro
// Package.swift macro target:
// .macro(name: "Stringify", dependencies: ["swift-syntax"])

// Macro declaration (in macro module)
@freestanding(expression)
public macro stringify<T>(_ value: T) -> (T, String) =
    #externalMacro(module: "MyMacrosPlugin", type: "StringifyMacro")

// Macro implementation (in plugin module)
import SwiftSyntaxMacros
import SwiftSyntax

public struct StringifyMacro: ExpressionMacro {
    public static func expansion(
        of node: some FreestandingMacroExpansionSyntax,
        in context: some MacroExpansionContext
    ) throws -> ExprSyntax {
        guard let argument = node.argumentList.first?.expression else {
            throw MacroExpansionErrorMessage("Missing argument")
        }
        return "(\(argument), \(literal: argument.description))"
    }
}

// Usage
let (value, code) = #stringify(42 + 58)
// value = 100, code = "42 + 58"
```

## Adopting this pattern

Macros require a Swift Package with a separate `macro` target and a compiler plugin target. Test macros using `assertMacroExpansion` from `SwiftSyntaxMacrosTestSupport`. Expand any macro in Xcode by right-clicking → Expand Macro — the expansion shows exactly what the compiler sees.
