---
framework: SwiftData
title: "Build an app with SwiftData"
session: WWDC23-10154
year: 2023
applies_to: iOS 17+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/swiftdata.md
---

# Build an App with SwiftData (WWDC23)

A practical walkthrough building a full SwiftUI app with SwiftData, covering `@Query` with sort/filter, relationships, `List` integration, and iCloud sync.

## Quick start

```swift
import SwiftData
import SwiftUI

@Model
class Trip {
    var name: String
    var destination: String
    var startDate: Date
    var endDate: Date

    @Relationship(deleteRule: .cascade)
    var bucketList: [BucketListItem] = []

    init(name: String, destination: String, startDate: Date, endDate: Date) {
        self.name = name
        self.destination = destination
        self.startDate = startDate
        self.endDate = endDate
    }
}

@Model
class BucketListItem {
    var title: String
    var isCompleted: Bool
    var trip: Trip?

    init(title: String) {
        self.title = title
        self.isCompleted = false
    }
}

@main
struct TripApp: App {
    var body: some Scene {
        WindowGroup { ContentView() }
            .modelContainer(for: Trip.self)
    }
}
```

## Key APIs

| API | Purpose |
|---|---|
| `@Query(sort:)` | Fetches models sorted by a key path |
| `@Query(filter:sort:)` | Fetches models with a predicate and sort |
| `@Query(sort:order:)` | Controls ascending/descending sort order |
| `List(models) { ... }` | Renders a SwiftUI List driven by a `@Query` result |
| `.onDelete(perform:)` | Handles swipe-to-delete in a `ForEach` over query results |
| `ModelConfiguration(isStoredInMemoryOnly:)` | Creates an in-memory store for testing/previews |
| `ModelConfiguration(cloudKitDatabase:)` | Enables iCloud sync |
| `context.insert(_:)` | Inserts a new model instance |
| `context.delete(_:)` | Deletes a model instance |

## Common patterns

**List with swipe-to-delete:**
```swift
struct TripListView: View {
    @Query(sort: \Trip.startDate, order: .forward) var trips: [Trip]
    @Environment(\.modelContext) private var context

    var body: some View {
        List {
            ForEach(trips) { trip in
                NavigationLink(trip.name, value: trip)
            }
            .onDelete { indexSet in
                for index in indexSet {
                    context.delete(trips[index])
                }
            }
        }
    }
}
```

**Filtered @Query:**
```swift
struct UpcomingTripsView: View {
    @Query(filter: #Predicate<Trip> { $0.startDate > .now },
           sort: \Trip.startDate)
    var upcomingTrips: [Trip]
}
```

**Dynamic filter passed from parent:**
```swift
struct TripListView: View {
    @Query var trips: [Trip]

    init(searchText: String) {
        let predicate = #Predicate<Trip> { trip in
            searchText.isEmpty || trip.name.localizedStandardContains(searchText)
        }
        _trips = Query(filter: predicate, sort: \Trip.startDate)
    }
}
```

**iCloud sync:**
```swift
@main
struct TripApp: App {
    var body: some Scene {
        WindowGroup { ContentView() }
            .modelContainer(for: Trip.self,
                            configurations: ModelConfiguration(
                                cloudKitDatabase: .automatic
                            ))
    }
}
```

**In-memory container for SwiftUI previews:**
```swift
#Preview {
    TripListView()
        .modelContainer(for: Trip.self, inMemory: true)
}
```

**Accessing relationships:**
```swift
struct TripDetailView: View {
    let trip: Trip

    var body: some View {
        List(trip.bucketList) { item in
            Label(item.title, systemImage: item.isCompleted ? "checkmark.circle" : "circle")
        }
    }
}
```

## Gotchas

- `@Query` rebuilds the SwiftUI view whenever the underlying store changes — keep queries in leaf views to limit re-render scope
- Passing a `@Query` result as an array to a child view loses live-update behavior; pass the container via `.modelContainer` or use `@Query` directly in the child view
- `ModelConfiguration(cloudKitDatabase: .automatic)` requires the CloudKit capability and a valid container identifier in the entitlements — all `@Model` properties must be optional or have defaults because CloudKit can return nil for any attribute
- `isStoredInMemoryOnly: true` and `cloudKitDatabase:` are mutually exclusive
- `@Relationship(deleteRule: .cascade)` only triggers when `context.delete()` is called on the owner; directly deleting related objects does not cascade upward
