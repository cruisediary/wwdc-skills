---
framework: SwiftData
title: "Meet SwiftData"
session: WWDC23-10187
year: 2023
applies_to: iOS 17+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/swiftdata.md
---

# Meet SwiftData (WWDC23)

SwiftData is the Swift-native persistence framework introduced at WWDC23, replacing Core Data with a declarative, macro-driven API.

## Quick start

```swift
import SwiftData

// 1. Define a model
@Model
class Trip {
    var name: String
    var destination: String
    var startDate: Date
    var endDate: Date

    init(name: String, destination: String, startDate: Date, endDate: Date) {
        self.name = name
        self.destination = destination
        self.startDate = startDate
        self.endDate = endDate
    }
}

// 2. Set up the container in your App
@main
struct TripApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: Trip.self)
    }
}

// 3. Query in a SwiftUI view
struct TripListView: View {
    @Query(sort: \Trip.startDate) var trips: [Trip]
    @Environment(\.modelContext) private var context

    var body: some View {
        List(trips) { trip in
            Text(trip.name)
        }
        .toolbar {
            Button("Add") {
                let trip = Trip(name: "WWDC", destination: "Cupertino",
                                startDate: .now, endDate: .now)
                context.insert(trip)
            }
        }
    }
}
```

## Key APIs

| API | Purpose |
|---|---|
| `@Model` | Marks a class as a SwiftData persistent model |
| `@Query` | Fetches and live-observes an array of models in a SwiftUI view |
| `ModelContainer` | The persistent store; equivalent to `NSPersistentContainer` |
| `ModelContext` | Unit of work for inserting, deleting, and saving; equivalent to `NSManagedObjectContext` |
| `\.modelContext` | Environment key to access the context injected by `.modelContainer()` |
| `context.insert(_:)` | Registers a new model instance for persistence |
| `context.delete(_:)` | Marks a model instance for deletion |
| `try context.save()` | Persists pending changes (auto-save is also supported) |
| `.modelContainer(for:)` | Scene/View modifier that creates and injects a `ModelContainer` |

## Common patterns

**Inserting a model:**
```swift
let item = MyModel(value: "hello")
context.insert(item)
// Auto-save triggers on the next run loop; call try context.save() for immediate persistence
```

**Deleting a model:**
```swift
context.delete(item)
```

**Filtering with @Query:**
```swift
@Query(filter: #Predicate<Trip> { $0.destination == "Cupertino" },
       sort: \Trip.startDate)
var trips: [Trip]
```

**In-memory container for previews and tests:**
```swift
let config = ModelConfiguration(isStoredInMemoryOnly: true)
let container = try ModelContainer(for: Trip.self, configurations: config)
```

**Accessing context in a non-view type:**
```swift
// Pass the context explicitly or use @Environment in views
func addTrip(context: ModelContext) {
    let trip = Trip(name: "Test", destination: "SF", startDate: .now, endDate: .now)
    context.insert(trip)
}
```

## Gotchas

- `@Model` requires a class (not struct); all stored properties become persisted columns automatically
- `@Query` can only be used in SwiftUI views — it relies on the `modelContext` environment value
- Auto-save does not guarantee immediate write to disk; call `try context.save()` when timing matters
- A `ModelContainer` is tied to a specific set of model types — adding a new `@Model` type requires updating the container configuration (or triggers automatic migration in simple cases)
- `ModelContext` is not `Sendable`; do not share it across actor boundaries — create a background context via `ModelContext(container)` for off-main-thread work
