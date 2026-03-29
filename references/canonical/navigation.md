---
framework: SwiftUI Navigation
status: current
applies_to: iOS 16+
shape: code-first
superseded_by: null
history:
  - year: 2022
    file: 2022/navigation-stack.md
    summary: NavigationStack replacing NavigationView
---

# SwiftUI Navigation

Type-safe, data-driven navigation for SwiftUI (iOS 16+). `NavigationStack` replaced the deprecated `NavigationView`.

## Quick start

```swift
import SwiftUI

struct Item: Identifiable, Hashable {
    let id = UUID()
    let title: String
}

let items = [Item(title: "Apple"), Item(title: "Banana"), Item(title: "Cherry")]

struct RootView: View {
    var body: some View {
        NavigationStack {
            List(items) { item in
                NavigationLink(item.title, value: item)
            }
            .navigationTitle("Fruits")
            .navigationDestination(for: Item.self) { item in
                Text("Detail: \(item.title)")
                    .navigationTitle(item.title)
            }
        }
    }
}

// iPad split view
struct SplitView: View {
    @State private var selectedItem: Item?

    var body: some View {
        NavigationSplitView {
            List(items, selection: $selectedItem) { item in
                Text(item.title)
            }
        } detail: {
            if let item = selectedItem {
                Text("Detail: \(item.title)")
            } else {
                Text("Select an item")
            }
        }
    }
}
```

## Key APIs

| API | Purpose |
|---|---|
| `NavigationStack` | Stack-based navigation; manages a path of pushed views |
| `NavigationLink(value:)` | Pushes a value onto the stack; resolved by `.navigationDestination` |
| `.navigationDestination(for:)` | Maps a type to a destination view |
| `NavigationPath` | Heterogeneous, type-erased path for programmatic navigation |
| `NavigationSplitView` | Two- or three-column split layout (iPad/Mac) |
| `.navigationTitle(_:)` | Sets the navigation bar title |
| `.navigationBarTitleDisplayMode(_:)` | Large or inline title |
| `.toolbar` | Add toolbar items |

## Common patterns

```swift
// Programmatic navigation with NavigationPath
struct AppView: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            HomeView()
                .navigationDestination(for: Item.self) { item in
                    ItemDetailView(item: item)
                }
                .navigationDestination(for: String.self) { route in
                    RouteView(route: route)
                }
        }
    }
}

// Navigate programmatically
path.append(selectedItem)   // push
path.removeLast()           // pop
path.removeLast(path.count) // pop to root

// Deep link: restore path from URL
path = NavigationPath(decodedItems)

// Dismiss from child view
@Environment(\.dismiss) private var dismiss
Button("Done") { dismiss() }
```

## Gotchas

- `NavigationView` is deprecated in iOS 16 — always use `NavigationStack` or `NavigationSplitView`
- Values pushed onto `NavigationStack` must be `Hashable`
- `.navigationDestination(for:)` must be placed on a view *inside* the `NavigationStack`, not on the stack itself
- `NavigationPath` enables mixed-type paths but requires `Codable` items for state restoration
- On iOS, `NavigationSplitView` collapses to a stack — test both layouts
