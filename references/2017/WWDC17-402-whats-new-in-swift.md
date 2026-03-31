---
framework: Swift
title: "What's New in Swift"
session: WWDC17-402
year: 2017
applies_to: iOS 11+
status: deprecated
superseded_by: null
shape: code-first
related: []
---

> **Deprecated:** Covers Swift 4.0 new features. All APIs described here are superseded by Swift 5.x/6.x. Useful as historical reference for migration context.

## Quick start

```swift
// Codable — Swift 4's killer feature
struct User: Codable {
    let name: String
    let age: Int
}
let json = """{"name":"Alice","age":30}""".data(using: .utf8)!
let user = try! JSONDecoder().decode(User.self, from: json)
print(user.name)  // Alice
```

## Key APIs

| Feature | Description |
|---|---|
| `Codable` (`Encodable & Decodable`) | Automatic JSON/plist serialization for structs and classes |
| `JSONEncoder` / `JSONDecoder` | Encode/decode `Codable` types to/from JSON |
| One-sided ranges (`array[2...]`, `array[..<5]`) | Partial range expressions for slicing |
| Multi-line string literals (`"""..."""`) | Strings spanning multiple lines without `\n` escaping |
| `Dictionary.init(grouping:by:)` | Groups a sequence into a dictionary by key |
| `Dictionary.init(uniqueKeysWithValues:)` | Build dictionary from key-value pairs |
| `String` subscript via `StringProtocol` | Subscripting returns `Substring`, not `String` |
| `@objc` inference removal | Swift 4 requires explicit `@objc`; removes implicit exposure to Obj-C |

## Common patterns

**Custom CodingKeys**

```swift
struct Product: Codable {
    let productName: String
    let priceUSD: Double

    enum CodingKeys: String, CodingKey {
        case productName = "product_name"
        case priceUSD = "price_usd"
    }
}
```

**Grouping with Dictionary**

```swift
let words = ["one", "two", "three", "four"]
let byLength = Dictionary(grouping: words, by: \.count)
// [3: ["one", "two"], 4: ["four"], 5: ["three"]]
```

## Gotchas

- `Substring` is not `String` — call `String(substring)` before storing or passing to APIs expecting `String`.
- `@objc` must now be explicit on members that need Obj-C exposure; `dynamic` alone is insufficient.
- `Dictionary(uniqueKeysWithValues:)` traps on duplicate keys — use `Dictionary(_:uniquingKeysWith:)` when duplicates are possible.
