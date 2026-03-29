---
framework: SwiftData
status: current
applies_to: iOS 17+
shape: code-first
superseded_by: null
history:
  - year: 2023
    file: 2023/swiftdata.md
    summary: Initial introduction — @Model, @Query, ModelContainer, ModelContext
  - year: 2024
    file: 2024/swiftdata.md
    summary: "#Index, #Unique, Custom DataStore, history tracking"
---

# SwiftData

Apple's declarative persistence framework for Swift, replacing Core Data for new projects (iOS 17+, macOS 14+).

## Quick start

```swift
import SwiftData
import SwiftUI

// 1. Define your model
@Model
class Book {
    var title: String
    var author: String
    var dateAdded: Date

    @Relationship(deleteRule: .cascade)
    var reviews: [Review] = []

    init(title: String, author: String) {
        self.title = title
        self.author = author
        self.dateAdded = .now
    }
}

@Model
class Review {
    var content: String
    var rating: Int
    var book: Book?

    init(content: String, rating: Int) {
        self.content = content
        self.rating = rating
    }
}

// 2. Set up the container in your App
@main
struct BookApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: [Book.self, Review.self])
    }
}

// 3. Query and display data
struct ContentView: View {
    @Query(sort: \Book.title) var books: [Book]
    @Environment(\.modelContext) var context

    var body: some View {
        List(books) { book in
            Text(book.title)
        }
        .toolbar {
            Button("Add") {
                context.insert(Book(title: "Dune", author: "Herbert"))
            }
        }
    }
}
```

## Key APIs

| API | Purpose |
|---|---|
| `@Model` | Marks a class as a SwiftData entity (must be a `class`) |
| `@Query` | Fetches and observes a model array in a SwiftUI view |
| `@Relationship(deleteRule:)` | Declares a relationship; `cascade` deletes children with parent |
| `ModelContainer` | The database — holds schema and configuration |
| `ModelContext` | The unit of work — insert, delete, fetch, save |
| `modelContainer(for:)` | SwiftUI modifier to inject the container into the environment |
| `@Environment(\.modelContext)` | Access the context inside a SwiftUI view |
| `#Index([\.prop])` | (iOS 18+) Adds a database index for faster queries |
| `#Unique(\.prop)` | (iOS 18+) Enforces uniqueness constraint on a property |

## Common patterns

```swift
// Filtered query
@Query(filter: #Predicate<Book> { $0.rating > 3 }, sort: \Book.title)
var topBooks: [Book]

// Manual fetch outside SwiftUI
let descriptor = FetchDescriptor<Book>(
    predicate: #Predicate { $0.author == "Herbert" },
    sortBy: [SortDescriptor(\.title)]
)
let results = try context.fetch(descriptor)

// Delete
context.delete(book)
try context.save()

// In-memory container (for previews/tests)
let config = ModelConfiguration(isStoredInMemoryOnly: true)
let container = try ModelContainer(for: Book.self, configurations: config)
```

## Gotchas

- `@Model` requires a `class`, not a `struct`
- SwiftData models are Observable — no need to add `@Observable` separately
- Relationships must be declared on both sides or use `@Relationship` explicitly
- `modelContainer(for:)` must list all model types; unlisted types are not persisted
- Avoid capturing `ModelContext` in closures across actor boundaries — fetch in the right context
- iOS 17 minimum: use Core Data for earlier deployment targets
