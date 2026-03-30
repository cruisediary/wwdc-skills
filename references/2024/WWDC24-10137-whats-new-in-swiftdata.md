---
framework: SwiftData
title: "What's new in SwiftData"
session: WWDC24-10137
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/swiftdata.md
---

# SwiftData — What's New in SwiftData (WWDC24)

iOS 18 expands SwiftData with compound index and uniqueness constraint macros, a pluggable custom DataStore protocol, and history tracking for change auditing.

## What's new

- **`#Index` macro** — declares compound indexes on `@Model` classes for faster multi-predicate queries; accepts one or more keypaths to index together
- **`#Unique` macro** — enforces uniqueness constraints on one or more properties; SwiftData upserts on conflict rather than duplicating
- **Custom `DataStore` protocol** — `ModelContainer` no longer requires SQLite; any storage backend can be plugged in by conforming to `DataStore`
- **SwiftData history tracking** — `context.fetchHistory(_:)` (takes a `HistoryDescriptor<DefaultHistoryTransaction>`) returns an ordered list of inserts, updates, and deletes; persist the returned `HistoryToken` to query only changes since the last launch

## Before / After

**Before (no indexes — full table scan on compound predicates):**
```swift
@Model
class Article {
    var title: String
    var category: String
    var date: Date
}
```

**After (compound index improves query performance):**
```swift
@Model
class Article {
    #Index<Article>([\.category, \.date])

    var title: String
    var category: String
    var date: Date
}
```

**Uniqueness constraint — prevents duplicate slugs:**
```swift
@Model
class Article {
    #Unique<Article>([\.slug])

    var title: String
    var slug: String
    var date: Date
}
```

## Migration steps

1. Identify `@Model` classes that are queried with multi-property predicates and add `#Index<ModelType>([\.prop1, \.prop2])` inside the `@Model` class body
2. For properties that must be unique (slugs, UUIDs, external identifiers), add `#Unique<ModelType>([\.property])` inside the `@Model` class body
3. To migrate an existing store, SwiftData applies new indexes and constraints automatically on next container open — no manual migration descriptor required for index-only changes
4. For custom storage backends, implement the `DataStore` protocol (see WWDC24-10138) and pass to `ModelContainer(schema:configurations:)`
5. To start tracking history, create a `HistoryDescriptor<DefaultHistoryTransaction>` and call `context.fetchHistory(_:)` — e.g. `let transactions = try context.fetchHistory(HistoryDescriptor<DefaultHistoryTransaction>(predicate: nil))` — then persist the returned `HistoryToken` between launches

## Compatibility notes

- `#Index` and `#Unique` macros require iOS 18 / macOS 15 / watchOS 11 / tvOS 18
- Existing `@Model` classes without `#Index` continue to compile and run on iOS 17+; the macros are additive
- `#Unique` on a property that already has duplicate values will cause a conflict on first migration — resolve duplicates before deploying
- Custom `DataStore` protocol is iOS 18+ only; the default SQLite store remains available on iOS 17+
- History tracking requires iOS 18+; tokens are opaque and must be persisted (e.g., in `UserDefaults` or a separate model property) to survive app restarts
