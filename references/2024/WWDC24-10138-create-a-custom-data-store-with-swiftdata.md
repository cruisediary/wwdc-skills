---
framework: SwiftData
title: "Create a custom data store with SwiftData"
session: WWDC24-10138
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/swiftdata.md
---

# SwiftData — Create a Custom Data Store with SwiftData (WWDC24)

iOS 18 decouples `ModelContainer` from SQLite by introducing the `DataStore` protocol, allowing any storage backend — in-memory, JSON files, remote APIs, or custom databases — to back a SwiftData model graph.

## What changed and why

Before iOS 18, `ModelContainer` always used SQLite as its storage engine. This made SwiftData unsuitable for use cases that require custom persistence: syncing with a remote datastore, storing models in a JSON file, using an in-memory store for tests, or embedding a non-SQLite database. The only workaround was to bypass SwiftData entirely and maintain a parallel persistence layer.

iOS 18 introduces the `DataStore` protocol. `ModelContainer` is now a *driver model* — it coordinates the model graph, relationships, and change tracking — while `DataStore` is the *storage driver* that handles the actual read/write operations. The two are connected at container configuration time, and the rest of SwiftData (`@Query`, `ModelContext`, relationships) works identically regardless of which backend is in use.

## Mental model

Think of `ModelContainer` as a database connection pool and `DataStore` as the database engine beneath it. The container speaks in terms of `ModelContext`, `PersistentModel`, and change sets; the `DataStore` implementation translates those into whatever storage primitives it needs.

```
@Query / ModelContext
        │
        ▼
 ModelContainer (driver model)
        │  coordinates model graph, change tracking
        ▼
   DataStore (storage driver)
        │  implements fetch / save / delete
        ▼
 Storage backend (SQLite / JSON file / in-memory / remote API)
```

Key responsibilities of a `DataStore` implementation:
- **`fetch(_:)`** — execute a `FetchDescriptor` and return matching persistent models
- **`save(_:)`** — persist a `DataStoreSaveChanges` batch (inserts, updates, deletes)
- **`delete(_:)`** — remove models matching a descriptor
- The store manages its own serialization format; SwiftData only sees `PersistentModel` values

## Usage

**Defining a minimal in-memory DataStore:**
```swift
import SwiftData

final class InMemoryStore: DataStore {
    typealias Configuration = InMemoryStoreConfiguration

    required init(_ configuration: InMemoryStoreConfiguration, migrationPlan: (any SchemaMigrationPlan.Type)?) throws {
        // Initialize internal storage
    }

    func fetch<T>(_ request: DataStoreFetchRequest<T>) throws -> DataStoreFetchResult<T, DefaultSnapshot> where T: PersistentModel {
        // Filter in-memory models and return matching snapshots
        fatalError("Implement filtering against in-memory store")
    }

    func save(_ request: DataStoreSaveRequest) throws -> DataStoreSaveResult {
        // Apply inserts, updates, deletes to in-memory store
        fatalError("Implement mutation against in-memory store")
    }
}

struct InMemoryStoreConfiguration: DataStoreConfiguration {
    typealias Store = InMemoryStore
    var name: String
    var schema: Schema?
}
```

**Wiring a custom store into ModelContainer:**
```swift
let schema = Schema([Article.self, Tag.self])
let config = InMemoryStoreConfiguration(name: "in-memory")

let container = try ModelContainer(
    for: schema,
    configurations: ModelConfiguration(schema: schema),
    dataStoreClass: InMemoryStore.self
)
```

**Using the container — identical to the default SQLite container:**
```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(container)
    }
}

struct ContentView: View {
    @Query var articles: [Article]
    @Environment(\.modelContext) private var context

    var body: some View {
        List(articles) { article in Text(article.title) }
    }
}
```

## Adopting this pattern

Choose a custom `DataStore` when:

| Use case | Benefit |
|---|---|
| Unit testing SwiftData code | In-memory store — fast, isolated, no disk I/O |
| Persisting models as JSON | Human-readable files, easy to version in git |
| Syncing with a remote server | Implement `fetch`/`save` as API calls; SwiftData handles the model graph |
| Embedding a non-SQLite database (Realm, LevelDB) | Adapt the foreign database's API behind `DataStore` |

Adoption checklist:
1. Create a class conforming to `DataStore` and a matching `DataStoreConfiguration` struct
2. Implement `fetch(_:)`, `save(_:)`, and optionally `delete(_:)` with your backend's read/write primitives
3. Pass `dataStoreClass:` to `ModelContainer(for:configurations:dataStoreClass:)` at app startup
4. All `@Query`, `@Model`, and `ModelContext` code continues to work without changes
5. For test targets, create a shared `ModelContainer` factory that swaps in the in-memory store
