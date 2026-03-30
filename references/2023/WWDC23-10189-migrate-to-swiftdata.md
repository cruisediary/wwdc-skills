---
framework: SwiftData
title: "Migrate to SwiftData"
session: WWDC23-10189
year: 2023
applies_to: iOS 17+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/swiftdata.md
---

# Migrate to SwiftData (WWDC23)

A step-by-step guide for migrating a Core Data app to SwiftData, including strategies for running both stacks in parallel during a phased migration.

## What's new

- SwiftData and Core Data can share the same persistent store file — you don't need to migrate all data
- `@Model` classes can coexist in a project with `NSManagedObject` subclasses during migration
- `NSPersistentCloudKitContainer` functionality is available in SwiftData via `ModelConfiguration` with a CloudKit database
- `NSPredicate` is replaced by `#Predicate<T>` — a type-safe, Swift-expression-based predicate macro

## Before / After

**Container setup:**

Before (Core Data):
```swift
// AppDelegate or a singleton
let container: NSPersistentContainer = {
    let c = NSPersistentContainer(name: "MyApp")
    c.loadPersistentStores { _, error in
        if let error { fatalError(error.localizedDescription) }
    }
    return c
}()
```

After (SwiftData):
```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup { ContentView() }
            .modelContainer(for: [Trip.self, Person.self])
    }
}
```

**Managed object vs @Model:**

Before:
```swift
class Trip: NSManagedObject {
    @NSManaged var name: String
    @NSManaged var destination: String
    @NSManaged var startDate: Date
}
```

After:
```swift
@Model
class Trip {
    var name: String
    var destination: String
    var startDate: Date
    init(name: String, destination: String, startDate: Date) {
        self.name = name; self.destination = destination; self.startDate = startDate
    }
}
```

**Fetch request vs @Query:**

Before:
```swift
@FetchRequest(sortDescriptors: [SortDescriptor(\Trip.startDate)])
var trips: FetchedResults<Trip>
```

After:
```swift
@Query(sort: \Trip.startDate) var trips: [Trip]
```

**NSPredicate vs #Predicate:**

Before:
```swift
NSPredicate(format: "destination == %@", "Cupertino")
```

After:
```swift
#Predicate<Trip> { $0.destination == "Cupertino" }
```

**Context access:**

Before:
```swift
@Environment(\.managedObjectContext) var context
```

After:
```swift
@Environment(\.modelContext) var context
```

## Migration steps

1. **Audit your model** — list all `NSManagedObject` subclasses, their attributes, relationships, and any migration policies
2. **Create equivalent `@Model` classes** — add SwiftData models alongside existing Core Data models; do not delete Core Data models yet
3. **Swap the container** — replace `NSPersistentContainer` with `.modelContainer(for:)` in the `App` struct; if using CloudKit, pass a `ModelConfiguration` with `cloudKitDatabase: .automatic`
4. **Replace `@FetchRequest`** with `@Query` in each SwiftUI view, and replace `@Environment(\.managedObjectContext)` with `@Environment(\.modelContext)`
5. **Convert predicates** — replace `NSPredicate` string predicates with `#Predicate<T>` closures
6. **Migrate sort descriptors** — replace `NSSortDescriptor(key:ascending:)` with `SortDescriptor(\Model.property)`
7. **Remove Core Data stack** — once all views and logic use SwiftData, delete the `.xcdatamodel` file, Core Data entity classes, and `NSPersistentContainer` setup
8. **Test on-device upgrade** — install the old version, then upgrade; SwiftData reads the existing SQLite store format when the schema matches

## Compatibility notes

- SwiftData requires iOS 17+, macOS 14+, watchOS 10+, tvOS 17+; Core Data must remain for apps supporting earlier OS versions
- SwiftData and Core Data can share the same `.sqlite` store file when model names and attributes align — allowing a parallel-stack approach where SwiftUI views migrate to `@Query` while UIKit/legacy views keep using `NSFetchedResultsController`
- `#Predicate` is checked at compile time and does not support all `NSPredicate` operators; complex predicates (e.g., `SUBQUERY`, `FUNCTION`) must be reimplemented or deferred
- No support for abstract entities or parent/child entity inheritance in WWDC23 SwiftData release — model these with protocol conformances instead
