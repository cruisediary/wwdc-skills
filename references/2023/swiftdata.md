---
framework: SwiftData
session: WWDC23-10187
year: 2023
applies_to: iOS 17+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/swiftdata.md
  - 2024/swiftdata.md
---

# SwiftData — WWDC23 Introduction

SwiftData replaced Core Data as the recommended persistence framework at WWDC23, providing a Swift-native declarative API.

## What's new

- `@Model` macro marks a class as a persistent entity — no `.xcdatamodel` file required
- `@Query` fetches and live-observes model arrays directly in SwiftUI views
- `ModelContainer` replaces `NSPersistentContainer`
- `ModelContext` replaces `NSManagedObjectContext`
- Relationships defined with `@Relationship(deleteRule:)`
- In-memory containers for testing via `ModelConfiguration(isStoredInMemoryOnly: true)`
- Migration support via `VersionedSchema` and `SchemaMigrationPlan`

## Before / After

**Before (Core Data):**
```swift
// NSManagedObject subclass
class Book: NSManagedObject {
    @NSManaged var title: String
    @NSManaged var author: String
}

// Fetch
let request = NSFetchRequest<Book>(entityName: "Book")
request.sortDescriptors = [NSSortDescriptor(key: "title", ascending: true)]
let books = try context.fetch(request)

// Insert
let book = Book(context: context)
book.title = "Dune"
try context.save()
```

**After (SwiftData WWDC23):**
```swift
@Model class Book {
    var title: String
    var author: String
    init(title: String, author: String) { self.title = title; self.author = author }
}

// In SwiftUI
@Query(sort: \Book.title) var books: [Book]

// Insert
context.insert(Book(title: "Dune", author: "Herbert"))
try context.save()
```

## Migration steps

1. Add `import SwiftData`; remove `import CoreData`
2. Replace `NSManagedObject` subclass + `.xcdatamodel` entries with `@Model class`
3. Replace `NSPersistentContainer` setup with `.modelContainer(for: ModelType.self)` in `App`
4. Replace `NSFetchRequest` + `@FetchRequest` with `@Query`
5. Replace `NSManagedObjectContext` injections with `@Environment(\.modelContext)`
6. Replace `context.save()` calls with `try context.save()`

## Compatibility notes

- Requires iOS 17+, macOS 14+, watchOS 10+, tvOS 17+
- No automatic migration path from existing Core Data stores in WWDC23 release — custom migration required
- Cannot mix `@Model` types with `NSManagedObject` in the same `ModelContainer`
