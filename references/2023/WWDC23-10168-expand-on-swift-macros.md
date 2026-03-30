---
framework: Swift Macros
title: "Expand on Swift macros"
session: WWDC23-10168
year: 2023
applies_to: iOS 17+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/swift-macros.md
---

# Expand on Swift Macros (WWDC23)

Advanced macro authoring: peer macros (`@AddAsync`), conformance macros, extension macros, `MemberMacro`, and rich compiler diagnostics.

## What changed and why

WWDC23-10167 covered freestanding expression macros. This session explores the full range of `@attached` macro roles that generate richer code transformations: peer declarations (e.g., generating an async overload alongside a completion-handler function), conformance additions, and member synthesis. It also demonstrates how macros can emit structured diagnostics — errors and warnings with fix-its — that appear in Xcode like native compiler messages.

## Mental model

- **Peer macro** (`@attached(peer)`) — generates a new top-level or member declaration *alongside* the annotated declaration, without modifying it. Classic use case: generate an `async` overload next to a completion-handler function.
- **Conformance macro** (`@attached(conformance)`) — adds a protocol conformance to the annotated type. Used by `@Observable`, `@Model`, etc.
- **Extension macro** (`@attached(extension)`) — generates an extension on the annotated type; the extension can add protocol conformances and members together.
- **Member macro** (`@attached(member)`) — adds new stored properties, methods, or initializers to the annotated type.
- **MemberAttribute macro** (`@attached(memberAttribute)`) — applies additional attributes to every member of the annotated type (e.g., applies `@objc` to every method).
- Diagnostics from macros appear in Xcode with full source location and optional fix-its, just like compiler warnings.

## Usage

**Peer macro — generate async overload:**
```swift
// Declaration
@attached(peer, names: overloaded)
public macro AddAsync() =
    #externalMacro(module: "MyMacrosPlugin", type: "AddAsyncMacro")

// Use
@AddAsync
func fetchData(completion: @escaping (Data?) -> Void) {
    // existing completion-handler implementation
}
// Macro generates:
// func fetchData() async -> Data? { ... }
```

**AddAsyncMacro implementation sketch:**
```swift
public struct AddAsyncMacro: PeerMacro {
    public static func expansion(
        of node: AttributeSyntax,
        providingPeersOf declaration: some DeclSyntaxProtocol,
        in context: some MacroExpansionContext
    ) throws -> [DeclSyntax] {
        guard let funcDecl = declaration.as(FunctionDeclSyntax.self) else { return [] }
        // Build async function syntax from funcDecl...
        // Return [asyncFuncDecl]
        return []  // implementation details omitted
    }
}
```

**Conformance macro:**

> **Gotcha:** In the final Xcode 15 release, `ExtensionMacro` replaced `ConformanceMacro` as the preferred approach for adding protocol conformances. `ExtensionMacro` (`@attached(extension)`) is the idiomatic shipping API in Xcode 15 / Swift 5.9 because it can add both conformances and members together in a single extension. Prefer `ExtensionMacro` over `ConformanceMacro` in new code.

```swift
@attached(conformance)
public macro Equatable() =
    #externalMacro(module: "MyMacrosPlugin", type: "EquatableMacro")

// ConformanceMacro protocol:
public struct EquatableMacro: ConformanceMacro {
    public static func expansion(
        of node: AttributeSyntax,
        providingConformancesOf declaration: some DeclGroupSyntax,
        in context: some MacroExpansionContext
    ) throws -> [(TypeSyntax, GenericWhereClauseSyntax?)] {
        return [("Equatable", nil)]
    }
}
```

**MemberMacro — synthesize stored property and init:**
```swift
public struct ModelMacro: MemberMacro {
    public static func expansion(
        of node: AttributeSyntax,
        providingMembersOf declaration: some DeclGroupSyntax,
        in context: some MacroExpansionContext
    ) throws -> [DeclSyntax] {
        return [
            "var _$persistentModelID: PersistentIdentifier = .init()"
        ]
    }
}
```

**Emitting diagnostics with fix-its:**
```swift
let diagnostic = Diagnostic(
    node: Syntax(node),
    message: MacroExpansionErrorMessage("@AddAsync requires a function with a completion handler"),
    fixIts: [
        FixIt(
            message: MacroExpansionFixItMessage("Add completion handler parameter"),
            changes: [
                // FixIt.Change describing the text edit
            ]
        )
    ]
)
context.diagnose(diagnostic)
```

**Multiple roles on one macro:**
```swift
// A macro can combine multiple attached roles
@attached(member, names: named(id), named(init))
@attached(conformance)
public macro Identifiable() =
    #externalMacro(module: "MyMacrosPlugin", type: "IdentifiableMacro")
```

## Adopting this pattern

- Use `@attached(peer)` to eliminate async/callback overload boilerplate — the pair stays in sync with a single implementation
- Use `@attached(conformance)` + `@attached(member)` together when you need to both add protocol conformance and synthesize the required members
- Use `@attached(extension)` when the synthesized members and conformance belong cleanly in an extension rather than the original type body
- Always emit diagnostics rather than silently failing or crashing — macros that produce no output without explanation confuse users
- Use `context.makeUniqueName(_:)` in peer macros to avoid name collisions with the original declaration
- Test each role independently with `assertMacroExpansion` before combining them
