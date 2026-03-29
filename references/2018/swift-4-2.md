---
framework: Swift
session: WWDC18-401
year: 2018
applies_to: Xcode 10 / Swift 4.2
status: deprecated
superseded_by: null
shape: migration
related: []
---

## What's new

- **`CaseIterable` protocol** — synthesizes an `allCases` static property on enums with no associated values.
- **Synthesized `Hashable` conformance** — compiler auto-synthesizes `hash(into:)` for structs and enums; `hashValue` is now derived from `hash(into:)`.
- **Random number generation** — new standard-library APIs: `Int.random(in:)`, `Double.random(in:)`, `Bool.random()`, `Array.randomElement()`, `Array.shuffled()`.
- **`Bool.toggle()`** — flips a Bool in place without `= !value`.
- **Conditional conformances in standard library** — `Optional`, `Array`, `Dictionary` now conditionally conform to `Equatable`, `Hashable`, and `Encodable/Decodable` when their element types do.
- **`SE-0193` cross-module inlining** — `@inlinable` attribute for performance-critical library code.
- **Implicit `@objc` removal** — Swift 4.2 is stricter; `@objc` is no longer inferred for members of `NSObject` subclasses in most cases (first warned in Swift 4, enforced here).

## Before / After

**Random numbers — before (arc4random_uniform)**

```swift
// Swift 4.1 and earlier
let roll = Int(arc4random_uniform(6)) + 1          // 1...6
let chance = Double(arc4random()) / Double(UInt32.max)  // 0.0..<1.0

var items = [1, 2, 3, 4, 5]
// Shuffle required a manual Fisher-Yates loop or GameplayKit
```

**Random numbers — after (Swift 4.2)**

```swift
let roll = Int.random(in: 1...6)
let chance = Double.random(in: 0..<1)
let flip = Bool.random()

var items = [1, 2, 3, 4, 5]
let shuffled = items.shuffled()          // non-mutating
items.shuffle()                          // in-place
let pick = items.randomElement()         // Optional<Int>
```

**CaseIterable — before**

```swift
enum Direction { case north, south, east, west }
let all: [Direction] = [.north, .south, .east, .west]  // manual list
```

**CaseIterable — after (Swift 4.2)**

```swift
enum Direction: CaseIterable { case north, south, east, west }
print(Direction.allCases)  // [.north, .south, .east, .west]
for direction in Direction.allCases { ... }
```

**Bool.toggle()**

```swift
// Before
isEnabled = !isEnabled

// After
isEnabled.toggle()
```

**Hashable synthesis**

```swift
// Before — manual hash implementation required
struct Point: Hashable {
    let x: Int, y: Int
    var hashValue: Int { return x.hashValue ^ y.hashValue &* 16777619 }
    static func == (lhs: Point, rhs: Point) -> Bool { lhs.x == rhs.x && lhs.y == rhs.y }
}

// After — synthesized automatically
struct Point: Hashable {
    let x: Int, y: Int
    // Equatable and Hashable synthesized; hash(into:) uses all stored properties
}
```

## Migration steps

1. Swift 4.2 ships with Xcode 10; change the Swift language version to 4.2 in Build Settings.
2. Replace `arc4random_uniform` / `arc4random` calls with `Int.random(in:)` / `Double.random(in:)`.
3. Add `: CaseIterable` to enums where you maintain manual `allCases` arrays and delete the manual arrays.
4. Remove manual `hashValue` implementations from structs/enums where the compiler can synthesize `Hashable`.
5. Audit `NSObject` subclasses: add explicit `@objc` to any methods that need Objective-C visibility and were relying on implicit inference.
6. Swift 4.2 is source-compatible with Swift 4 — migration is mostly additive with minimal breaking changes.

## Compatibility notes

- Swift 4.2 requires Xcode 10; compiled apps run on iOS 8+ (deployment target unchanged).
- `CaseIterable` synthesis only works for enums with no associated values; enums with associated values must implement `allCases` manually.
- The new random APIs use a cryptographically non-secure, but well-distributed, system generator by default; for security-sensitive values use `SecRandomCopyBytes`.
- Swift 4.2 is a transitional release — Swift 5 (Xcode 10.2) introduced ABI stability and is the milestone most teams treat as the modern baseline.
