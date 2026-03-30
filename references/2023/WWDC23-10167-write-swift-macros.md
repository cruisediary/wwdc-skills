---
framework: Swift Macros
title: "Write Swift macros"
session: WWDC23-10167
year: 2023
applies_to: iOS 17+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/swift-macros.md
---

# Write Swift Macros (WWDC23)

A step-by-step guide to authoring a Swift macro: setting up the package, implementing with `SwiftSyntax`, using `MacroExpansionContext`, and emitting diagnostics.

## What changed and why

Before macros, Swift developers had to choose between hand-written boilerplate and external code generators (Sourcery, GYB). Swift 5.9 macros integrate code generation directly into the compiler pipeline — the macro implementation is type-safe Swift code that manipulates a `SwiftSyntax` tree, runs in a sandboxed plugin process, and its output is visible in Xcode like any other source file.

## Mental model

- A macro has two parts: a **declaration** (the public API in a library target) and an **implementation** (a compiler plugin executable that does the work).
- The implementation receives a `SwiftSyntax` node representing the call site and returns new syntax nodes.
- `MacroExpansionContext` provides utilities: generating unique names, emitting diagnostics, getting source location.
- `SwiftSyntaxMacros` defines the protocols your macro type must conform to (`ExpressionMacro`, `MemberMacro`, etc.).
- Tests use `assertMacroExpansion` to verify input → output transformations as strings.

## Usage

**Package.swift structure:**
```swift
let package = Package(
    name: "MyMacros",
    targets: [
        // The library that declares the macro — imported by users
        .target(name: "MyMacros", dependencies: ["MyMacrosPlugin"]),
        // The compiler plugin that implements the macro
        .macro(name: "MyMacrosPlugin", dependencies: [
            .product(name: "SwiftSyntaxMacros", package: "swift-syntax"),
            .product(name: "SwiftCompilerPlugin", package: "swift-syntax"),
        ]),
        // Test target
        .testTarget(name: "MyMacrosTests", dependencies: [
            "MyMacros",
            .product(name: "SwiftSyntaxMacrosTestSupport", package: "swift-syntax"),
        ]),
    ]
)
```

**Macro declaration (MyMacros/MyMacros.swift):**
```swift
@freestanding(expression)
public macro stringify<T>(_ value: T) -> (T, String) =
    #externalMacro(module: "MyMacrosPlugin", type: "StringifyMacro")
```

**Macro implementation (MyMacrosPlugin/StringifyMacro.swift):**
```swift
import SwiftSyntax
import SwiftSyntaxMacros

public struct StringifyMacro: ExpressionMacro {
    public static func expansion(
        of node: some FreestandingMacroExpansionSyntax,
        in context: some MacroExpansionContext
    ) -> ExprSyntax {
        guard let argument = node.argumentList.first?.expression else {
            // emit a diagnostic and return a placeholder
            context.diagnose(Diagnostic(
                node: node,
                message: MacroExpansionErrorMessage("Expected an argument")
            ))
            return "((), \"\")"
        }
        return "(\(argument), \(literal: argument.description))"
    }
}
```

**Registering the plugin:**
```swift
// MyMacrosPlugin/MyMacrosPlugin.swift
import SwiftCompilerPlugin
import SwiftSyntaxMacros

@main
struct MyMacrosPlugin: CompilerPlugin {
    let providingMacros: [Macro.Type] = [StringifyMacro.self]
}
```

**Emitting diagnostics:**
```swift
// Warning at the call site
context.diagnose(Diagnostic(
    node: Syntax(argument),
    message: MacroExpansionWarningMessage("Consider simplifying this expression")
))

// Error that stops expansion
context.diagnose(Diagnostic(
    node: Syntax(node),
    message: MacroExpansionErrorMessage("Missing required argument")
))
```

**Testing the macro:**
```swift
import SwiftSyntaxMacrosTestSupport
import XCTest
@testable import MyMacrosPlugin

final class StringifyMacroTests: XCTestCase {
    let testMacros: [String: Macro.Type] = ["stringify": StringifyMacro.self]

    func testStringify() {
        assertMacroExpansion(
            "#stringify(1 + 2)",
            expandedSource: "(1 + 2, \"1 + 2\")",
            macros: testMacros
        )
    }
}
```

## Adopting this pattern

1. Use the Xcode "Swift Macro" package template (`File > New > Package`) to scaffold the structure
2. Start by writing the expected expansion as a test in `assertMacroExpansion` — test-first makes macro development much faster
3. Use `SwiftSyntax`'s structured types (e.g., `FunctionCallExprSyntax`, `AttributeSyntax`) rather than string manipulation
4. Use `context.makeUniqueName(_:)` when generating variable or function names to avoid collisions with user code
5. Emit diagnostics with `context.diagnose` rather than `fatalError` — this gives users actionable error messages in Xcode
6. Keep the implementation target small; heavy logic belongs in a regular library that the plugin calls into (for testability)
