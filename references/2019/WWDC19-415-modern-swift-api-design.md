---
framework: Swift
title: "Modern Swift API Design"
session: WWDC19-415
year: 2019
applies_to: iOS 13+
status: reference-only
superseded_by: null
shape: guide-first
related: []
---

# Modern Swift API Design (WWDC19)

Design principles for writing idiomatic Swift APIs: value types vs reference types, protocol-oriented design, naming conventions, and when (and when not) to reach for generics.

## What changed and why

Swift's type system and value semantics offer design choices that Objective-C and C++ developers may find unfamiliar. This session distils the Swift API Design Guidelines into actionable patterns for framework and library authors.

Key tensions the session addresses:
- Value types give safe, copy-on-write semantics but cannot support identity
- Reference types support identity and polymorphism but require careful ownership management
- Protocols enable powerful abstraction but add complexity — "don't start with a protocol"

## Mental model

**Prefer value types for data, reference types for identity:**

```
Value type (struct/enum)     Reference type (class)
─────────────────────────    ─────────────────────
Copied on assignment         Shared by reference
Thread-safe by default       Requires synchronisation
No identity                  Has identity (===)
Composable with COW          Supports inheritance
```

**Protocol design ladder — reach for each only when needed:**
1. Concrete type (struct or class)
2. Generic function with type constraints
3. Protocol (when multiple unrelated types truly share capability)
4. Protocol with associated types (PAT) — use sparingly; prefer generics at call site

## Usage

**Prefer structs for data models:**
```swift
// Prefer
struct User {
    var id: UUID
    var name: String
    var email: String
}

// Avoid class for pure data — unless you need identity or inheritance
```

**Naming conventions — clarity at the call site:**
```swift
// Prefer: reads naturally at call site
array.sorted()                   // nonmutating form — past tense / -ed
array.sort()                     // mutating form — imperative verb
string.lowercased()              // nonmutating, returning new value
view.addSubview(childView)       // verb phrase; object matches parameter role

// Avoid: redundant type in name (Swift is strongly typed)
func insertItemAtIndex(_ item: Item, at index: Int)  // ✗ redundant "Item"
func insert(_ item: Item, at index: Int)             // ✓
```

**Generics — when a real type constraint adds clarity:**
```swift
// Generic function: works for any Collection of Equatable elements
func allUnique<C: Collection>(_ collection: C) -> Bool
    where C.Element: Equatable {
    // ...
}

// Avoid over-constraining — if you only need Sequence, don't require Collection
```

**Protocol + default implementations — extend, don't inherit:**
```swift
protocol Drawable {
    func draw(in context: CGContext)
    var boundingRect: CGRect { get }
}

extension Drawable {
    // Default implementation in extension — conformers get this for free
    func draw(at point: CGPoint, in context: CGContext) {
        context.translateBy(x: point.x, y: point.y)
        draw(in: context)
    }
}
```

**`@discardableResult` — signal that ignoring the return value is intentional:**
```swift
@discardableResult
func save() -> Bool {
    // ...
}
// Callers can call save() or let success = save() without a warning
```

## Adopting this pattern

1. Start with a concrete type (struct). Only add a protocol when you have two or more unrelated types that share the same capability.
2. Follow the Swift Naming Guidelines: clarity at the call site is more important than brevity. Read usages aloud — they should sound like a sentence.
3. Use value semantics for data models; reserve classes for objects with identity (controllers, managers, view nodes).
4. Use generics with concrete constraints rather than existentials (`any Protocol`) when performance matters and the type is known at compile time.
5. Avoid retroactive conformances (conforming a type you don't own to a protocol you don't own) — they can cause conflicts in future SDK releases.
