---
framework: SwiftData
session: WWDC24-10137
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/swiftdata.md
  - 2023/swiftdata.md
---

# SwiftData — WWDC24 Refinements

WWDC24 added constraints, custom storage, and history tracking to SwiftData.

## What's new

- `#Index([\.property])` — adds a database index for faster queries on specific properties
- `#Unique(\.property)` — enforces a uniqueness constraint; duplicate inserts upsert instead of error
- Custom `DataStore` protocol — implement non-SQLite backends (e.g., JSON, remote store)
- History tracking via `DefaultHistoryConfiguration` — observe what changed and when
- `modelContext.transaction { }` — explicit transaction boundaries

## Before / After

**Before (WWDC23 — no index constraints):**
```swift
@Model
class Article {
    var slug: String
    var title: String
}
// No way to enforce uniqueness or speed up slug lookups
```

**After (WWDC24 — index + uniqueness):**
```swift
@Model
#Index<Article>([\.slug])
#Unique<Article>(\.slug)
class Article {
    var slug: String
    var title: String
}
```

## Migration steps

1. Identify high-cardinality properties used in `#Predicate` filters → add `#Index`
2. Identify natural keys (slug, ISBN, UUID) → add `#Unique` to enable safe upserts
3. To use history tracking: add `DefaultHistoryConfiguration()` to `ModelConfiguration`
4. To use a custom store: conform a type to `DataStore` and pass it to `ModelConfiguration`

## Compatibility notes

- `#Index` and `#Unique` require iOS 18+, macOS 15+
- History tracking API requires iOS 18+
- Custom `DataStore` requires iOS 18+
- Existing WWDC23 SwiftData stores migrate automatically (no schema migration needed for adding indexes)
