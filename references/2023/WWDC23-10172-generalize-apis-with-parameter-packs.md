---
framework: Swift
title: "Generalize APIs with parameter packs"
session: WWDC23-10172
year: 2023
applies_to: iOS 17+
status: reference-only
superseded_by: null
shape: guide-first
related: []
---

# Generalize APIs with Parameter Packs (WWDC23)

Swift 5.9 variadic generics: `repeat each T`, `Pack`, `each value` — enabling APIs that work over any number of type parameters without overload explosion.

## What changed and why

Before Swift 5.9, functions operating on heterogeneous tuples required a family of overloads (`func f<A>(_: A)`, `func f<A, B>(_: A, _ b: B)`, …). SwiftUI's `TupleView`, `ViewBuilder`, and `Group` all used this pattern, capped at 10 children. Parameter packs replace that family with a single generic definition that handles any arity — and the compiler verifies it at each call site.

## Mental model

- **Type parameter pack**: `<each T>` — declares a pack of zero or more type parameters.
- **Value parameter pack**: `_ values: repeat each T` — a function parameter that captures one value per type in the pack.
- **Pack expansion**: `repeat each value` — expands the pack, operating on each element.
- **Pack iteration**: currently done via `repeat` expressions, not `for-in` (as of Swift 5.9).
- The result type of a pack-returning function is a tuple `(repeat each T)`.

## Usage

**Basic variadic generic function:**
```swift
// Returns a tuple of the same types as the inputs
func makeTuple<each T>(_ values: repeat each T) -> (repeat each T) {
    return (repeat each values)
}

let pair   = makeTuple(1, "hello")        // (Int, String)
let triple = makeTuple(1, "hello", true)  // (Int, String, Bool)
```

**Applying a transformation to each element:**
```swift
// Map each element independently
func printAll<each T>(_ values: repeat each T) {
    repeat print(each values)
}

printAll(42, "Swift", true)
// prints: 42, Swift, true (each on its own line)
```

**Constrained pack — requiring Equatable:**
```swift
// Checking equality across parameter packs (Swift 5.9)
// Note: for-in over pack expansions is not supported in Swift 5.9.
// Use recursive tuple comparison or constrain to Equatable+count checks.
// A common pattern is to convert to arrays where the element count is known:
func zip<each T, each U>(
    _ first: repeat each T,
    _ second: repeat each U
) -> (repeat (each T, each U)) {
    return (repeat (each first, each second))
}
```

**Applying a protocol requirement to each type in a pack:**
```swift
func encode<each T: Encodable>(_ values: repeat each T) throws -> [Data] {
    var results: [Data] = []
    repeat results.append(try JSONEncoder().encode(each values))
    return results
}
```

**Use case: zero-overload zip:**
```swift
func zip<each T>(_ values: repeat each T) -> (repeat each T) {
    (repeat each values)
}
// Replaces the entire overload family for (A, B), (A, B, C), etc.
```

**SwiftUI analogy — how TupleView now works conceptually:**
```swift
// Conceptual; actual SwiftUI implementation may differ
struct TupleView<each Content: View>: View {
    var content: (repeat each Content)

    var body: some View {
        // Expand each Content view
        repeat (each content)
    }
}
```

## Adopting this pattern

- Use parameter packs when you have an existing overload family where the only difference is the number of generic type parameters
- The primary practical benefit in app code is eliminating artificial arity limits (like SwiftUI's 10-view limit before ViewBuilder improvements)
- For library authors: replace `func f<A, B, C>` overload families with a single `func f<each T>` — backward compatible because existing call sites still compile
- In Swift 5.9, you cannot use `for-in` over a pack expansion — use `repeat expr` statements instead
- Pack expansions work in function parameters, return types, tuple types, and `repeat` expressions — not in arrays or other collections directly
- Avoid packs for simple same-type variadic inputs (`[T]` is simpler when all elements have the same type)
