---
framework: SwiftData
title: "Dive deeper into SwiftData"
session: WWDC23-10196
year: 2023
applies_to: iOS 17+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/swiftdata.md
---

# Dive Deeper into SwiftData (WWDC23)

Advanced SwiftData topics: `FetchDescriptor`, `#Predicate`, `SortDescriptor`, batch deletes, and performance best practices for production apps.

## What changed and why

`@Query` is designed for SwiftUI views. For non-view code — background processing, repositories, unit tests — SwiftData exposes `FetchDescriptor<T>` as the Swift-native equivalent of `NSFetchRequest`. Paired with `#Predicate` and `SortDescriptor`, it provides compile-time-safe, type-checked fetching without requiring a view hierarchy.

## Mental model

- `FetchDescriptor<T>` describes what to fetch: filter, sort, limit, offset, and prefetch behavior.
- `#Predicate<T>` is a macro that turns a Swift closure into a predicate expression tree — checked at compile time, no format strings.
- `SortDescriptor` wraps a key path and a sort order; multiple descriptors can be composed.
- `context.fetch(_:)` executes the descriptor and returns `[T]`.
- `context.fetchCount(_:)` returns an `Int` without materializing objects — use this for existence checks and badges.
- `context.delete(model:where:includeSubclasses:)` deletes matching objects in a single operation without loading them into memory.

## Usage

**Basic FetchDescriptor:**
```swift
let descriptor = FetchDescriptor<Trip>(
    predicate: #Predicate { $0.destination == "Cupertino" },
    sortBy: [SortDescriptor(\Trip.startDate, order: .forward)]
)
let trips = try context.fetch(descriptor)
```

**Limiting results:**
```swift
var descriptor = FetchDescriptor<Trip>(
    sortBy: [SortDescriptor(\Trip.startDate)]
)
descriptor.fetchLimit = 10
descriptor.fetchOffset = 20  // for pagination
let page = try context.fetch(descriptor)
```

**Count without materializing:**
```swift
let count = try context.fetchCount(
    FetchDescriptor<Trip>(predicate: #Predicate { $0.startDate > .now })
)
```

**Compound #Predicate:**
```swift
let predicate = #Predicate<Trip> { trip in
    trip.destination == "Cupertino" && trip.startDate > .now
}
```

**Multiple sort descriptors:**
```swift
let descriptor = FetchDescriptor<Trip>(
    sortBy: [
        SortDescriptor(\Trip.destination),
        SortDescriptor(\Trip.startDate, order: .reverse)
    ]
)
```

**Batch delete:**
```swift
// Deletes matching objects without loading them — much more efficient for large sets
try context.delete(
    model: Trip.self,
    where: #Predicate { $0.endDate < .now }
)
```

**Prefetching relationships:**
```swift
var descriptor = FetchDescriptor<Trip>()
descriptor.relationshipKeyPathsForPrefetching = [\.bucketList]
let trips = try context.fetch(descriptor)
// Accessing trip.bucketList does not trigger additional fetches
```

**Background fetch with a separate ModelContext:**
```swift
Task.detached {
    let backgroundContext = ModelContext(container)
    let descriptor = FetchDescriptor<Trip>(
        predicate: #Predicate { $0.startDate > .now }
    )
    let trips = try backgroundContext.fetch(descriptor)
    // process trips...
}
```

## Adopting this pattern

- Replace any `NSFetchRequest` in non-view code with `FetchDescriptor`
- Replace `NSPredicate(format:)` strings with `#Predicate<T>` closures — the compiler will flag type mismatches
- Use `fetchCount` instead of `fetch` when you only need to know whether results exist (avoids loading objects into memory)
- Use batch delete for cleanup tasks (expired cache, completed items) rather than fetching and individually deleting
- Pass `ModelContext(container)` to background tasks rather than sharing the main-thread context
