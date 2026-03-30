---
framework: SwiftData
title: "SwiftData: Dive into inheritance and schema migration"
session: WWDC25-291
year: 2025
applies_to: iOS 26+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/swiftdata.md
  - 2024/WWDC24-10137-whats-new-in-swiftdata.md
---

# SwiftData — What's New in SwiftData (WWDC25)

WWDC25 continues the SwiftData evolution with improved predicate support, additional `@Model` capabilities, and performance refinements. Specific API details should be confirmed against Xcode 26 release notes.

## What's new

- **Expanded `#Predicate` support** — additional operators and compound predicates; closer parity with `NSPredicate` capabilities (see Apple docs for exact additions)
- **`@Model` property refinements** — improved handling of optional relationships and cascade delete rules in complex schemas
- **Performance improvements** — batch fetch and insert operations are more efficient; `FetchDescriptor` gains additional sort/filter options
- **History tracking enhancements** — building on WWDC24's `ModelContext.fetchHistory` / `HistoryToken` APIs; improved change coalescing (see Apple docs)
- **CloudKit sync improvements** — better conflict resolution for multi-device scenarios

## Before / After

**Before (iOS 18 — limited `#Predicate` compound expressions):**
```swift
// Some compound predicates required workarounds
let descriptor = FetchDescriptor<Item>(
    predicate: #Predicate { $0.isActive && $0.score > 50 }
)
```

**After (iOS 26 — expanded predicate operators; see Apple docs for new additions):**
```swift
// Additional operators available — refer to Xcode 26 SwiftData documentation
// for the complete list of supported #Predicate expressions
let descriptor = FetchDescriptor<Item>(
    predicate: #Predicate { $0.isActive && $0.score > 50 }
    // New: additional string, collection, and date operators
)
```

## Migration steps

1. Run the app on iOS 26 to surface any SwiftData deprecation warnings — address flagged APIs
2. Review `@Relationship` delete rules in your schema; WWDC25 may add new rule options — test cascade behavior
3. If using `ModelContext.fetchHistory`, update to any new API shape introduced in iOS 26 (check release notes)
4. For CloudKit sync: test conflict resolution on multiple devices after the iOS 26 update

## Compatibility notes

- New WWDC25 SwiftData APIs require iOS 26+; existing SwiftData code continues to compile on iOS 17+
- `#Predicate` additions may require re-evaluation of custom NSPredicate fallbacks — test thoroughly
- Exact new API surface should be verified against Xcode 26 SDK documentation before adopting
