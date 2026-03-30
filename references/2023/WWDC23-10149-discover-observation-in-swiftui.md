---
framework: Observation
title: "Discover Observation in SwiftUI"
session: WWDC23-10149
year: 2023
applies_to: iOS 17+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/observation.md
  - canonical/swiftui.md
---

# Discover Observation in SwiftUI (WWDC23)

The Observation framework introduces `@Observable`, which replaces `ObservableObject` and `@Published` with automatic, fine-grained property tracking.

## What changed and why

`ObservableObject` invalidates an entire view whenever any `@Published` property changes — even if the view never reads that property. `@Observable` tracks only the properties that each view actually accesses during rendering, so views re-render only when their specific dependencies change. This gives better performance with no extra work from the developer.

The old `@StateObject` / `@ObservedObject` / `@EnvironmentObject` trio is replaced by `@State` / plain reference / `@Environment(Type.self)`.

## Mental model

- Mark your model class with `@Observable` — no `@Published` needed on any property.
- Store the model in a view using `@State` (owned) or a plain `let`/`var` (passed in).
- When you need a `Binding` to a property of an `@Observable` object, wrap the reference in `@Bindable`.
- Pass the model through the environment with `.environment(model)` and retrieve with `@Environment(MyModel.self)`.
- The framework tracks which properties are read during `body` evaluation and re-invokes `body` only when those properties change.
- Use `@ObservationIgnored` to exempt a property from tracking (e.g., a cache or a constant).
- Use `withObservationTracking(_:onChange:)` for observation outside SwiftUI (e.g., in a ViewModel or UIKit layer).

## Usage

**Defining an observable model:**
```swift
import Observation

@Observable
class LibraryModel {
    var books: [Book] = []
    var selectedBook: Book?
    @ObservationIgnored var cache: [String: Book] = [:]
}
```

**Owning a model in a view:**
```swift
struct LibraryView: View {
    @State private var model = LibraryModel()

    var body: some View {
        List(model.books) { book in
            Text(book.title)
        }
    }
}
```

**Binding to a property (requires @Bindable):**
```swift
struct BookDetailView: View {
    @Bindable var book: Book   // Book must be @Observable

    var body: some View {
        TextField("Title", text: $book.title)
    }
}
```

**Environment injection and retrieval:**
```swift
// Inject
WindowGroup {
    RootView()
        .environment(libraryModel)
}

// Retrieve
struct SomeChildView: View {
    @Environment(LibraryModel.self) private var model

    var body: some View {
        Text("Books: \(model.books.count)")
    }
}
```

**Manual observation outside SwiftUI:**
```swift
withObservationTracking {
    // Access properties to register dependencies
    _ = model.books.count
} onChange: {
    // Called once when any accessed property changes
    print("books changed")
}
```

## Adopting this pattern

1. Add `import Observation` (or rely on SwiftUI re-exporting it).
2. Replace `class MyModel: ObservableObject` with `@Observable class MyModel`.
3. Remove all `@Published` annotations.
4. In views: `@StateObject` → `@State`, `@ObservedObject` → `@Bindable` (if bindings needed) or plain property.
5. Environment: `.environmentObject(m)` → `.environment(m)`, `@EnvironmentObject var m: T` → `@Environment(T.self) var m`.
6. Existing `ObservableObject` types continue to work — incremental migration is safe.
