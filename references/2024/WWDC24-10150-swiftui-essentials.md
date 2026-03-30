---
framework: SwiftUI
title: "SwiftUI essentials"
session: WWDC24-10150
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/swiftui.md
---

# SwiftUI — SwiftUI Essentials (WWDC24)

A foundational guide to SwiftUI's declarative model: views as functions of state, the property wrapper hierarchy, and the `@Observable` macro.

## What changed and why

UIKit manages views imperatively: you create a `UIView`, hold a reference to it, and mutate it directly (`label.text = "..."`, `view.isHidden = true`). This leads to complex, error-prone synchronization between your data model and the on-screen representation.

SwiftUI replaces this with a **declarative model**: you describe *what* the UI should look like for a given state, and the framework figures out *how* to update the render tree. When state changes, SwiftUI re-evaluates affected view bodies and applies the minimal diff to the underlying layers.

The result is:
- Less code for common patterns (lists, navigation, forms)
- Automatic diffing — no manual `reloadData()` or `setNeedsLayout()`
- A single source of truth per piece of state, reducing synchronization bugs

The `@Observable` macro (introduced in iOS 17, emphasized in iOS 18 guidance) replaces `ObservableObject`/`@Published`, requiring less boilerplate and enabling more granular view invalidation.

## Mental model

**Views are functions of state** — the same state always produces the same view. SwiftUI `View` structs are value types that are re-created on every state change; they are blueprints, not mutable objects. The framework owns the actual render tree.

```
State ──→ View body ──→ Render tree diff ──→ Screen update
  ↑                                                │
  └────────────── user interaction ───────────────┘
```

Key rules:
- **`@State`** — local mutable state owned by a single view; the view body re-runs when it changes
- **`@Binding`** — a read-write reference into another view's `@State`; changes propagate back to the owner
- **`@Environment`** — injected values from the environment (system or custom); views read without knowing the source
- **`@Observable`** — a model class whose property accesses are tracked; only views that read a changed property re-render
- Never hold a strong reference to a SwiftUI view — views are transient value types

## Usage

**`@State` for local state:**
```swift
struct CounterView: View {
    @State private var count = 0

    var body: some View {
        VStack {
            Text("Count: \(count)")
            Button("Increment") { count += 1 }
        }
    }
}
```

**`@Binding` to share state:**
```swift
struct ToggleRow: View {
    @Binding var isOn: Bool   // Owned by a parent view

    var body: some View {
        Toggle("Enable feature", isOn: $isOn)
    }
}

struct ParentView: View {
    @State private var featureEnabled = false

    var body: some View {
        ToggleRow(isOn: $featureEnabled)
    }
}
```

**`@Environment` for dependency injection:**
```swift
// Reading a system environment value
struct ThemeAwareView: View {
    @Environment(\.colorScheme) private var colorScheme

    var body: some View {
        Text("Hello")
            .foregroundStyle(colorScheme == .dark ? .white : .black)
    }
}

// Injecting a custom model
struct RootView: View {
    var body: some View {
        ContentView()
            .environment(AppSettings())
    }
}

struct ContentView: View {
    @Environment(AppSettings.self) private var settings
    // ...
}
```

**`@Observable` for model objects:**
```swift
@Observable
class UserModel {
    var name: String = ""
    var isLoggedIn: Bool = false
    // No @Published needed — @Observable tracks property access automatically
}

struct ProfileView: View {
    var model: UserModel  // Passed in; no @ObservedObject wrapper needed

    var body: some View {
        Text(model.name)  // View re-renders only when `name` changes
    }
}
```

**Conditional and dynamic views:**
```swift
struct FeedView: View {
    @State private var items: [Item] = []
    @State private var isLoading = true

    var body: some View {
        Group {
            if isLoading {
                ProgressView()
            } else {
                List(items) { item in
                    ItemRow(item: item)
                }
            }
        }
        .task {
            items = await fetchItems()
            isLoading = false
        }
    }
}
```

## Adopting this pattern

For UIKit developers transitioning to SwiftUI, the key mindset shifts are:

| UIKit pattern | SwiftUI equivalent |
|---|---|
| Subclass `UIViewController`, override lifecycle methods | Write a `View` struct with a `body` property |
| Hold `IBOutlet` references, mutate them directly | Bind to `@State`; the framework updates the view |
| `delegate` / `target-action` for callbacks | Pass closures or `@Binding` down the view tree |
| `NotificationCenter` for app-wide events | `@Environment` or `@Observable` model in the environment |
| `UITableView` + `UITableViewDataSource` | `List` with a `ForEach` over an `Identifiable` collection |
| `viewDidLoad` / `viewWillAppear` | `.onAppear` / `.task` modifiers |
| `UINavigationController.pushViewController` | `NavigationStack` with `NavigationLink` |

**The most important rule:** stop thinking about views as mutable objects. A `View` struct is destroyed and re-created on every body evaluation. Store state in `@State`, `@Binding`, or `@Observable` models — not in view properties.
