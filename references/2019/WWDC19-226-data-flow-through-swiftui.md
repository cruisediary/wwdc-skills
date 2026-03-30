---
framework: SwiftUI
title: "Data Flow Through SwiftUI"
session: WWDC19-226
year: 2019
applies_to: iOS 13+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/swiftui.md
---

# Data Flow Through SwiftUI (WWDC19)

The canonical session on SwiftUI's state management primitives: `@State`, `@Binding`, `@ObservedObject`, and `@EnvironmentObject`.

## What changed and why

UIKit had no built-in state management — developers used delegates, notifications, KVO, and ad-hoc bindings. SwiftUI introduces a layered property-wrapper system that makes data ownership and flow explicit:

- **`@State`** — view owns the data; local, ephemeral
- **`@Binding`** — derived read-write reference into a parent's state; no ownership
- **`@ObservedObject`** — view references an external `ObservableObject`; does not own it
- **`@EnvironmentObject`** — `ObservableObject` injected into the environment; any descendant can read it

> Note: In iOS 17+, `@Observable` replaces `ObservableObject`/`@Published` (see WWDC23-10149).

## Mental model

**Ownership hierarchy:**

```
@State (owned by view)
    └─ $binding → @Binding (child view reads/writes parent state)

ObservableObject (external model)
    ├─ @ObservedObject (view observes but does not own)
    └─ @StateObject  (view owns the object — use this for creation)

.environmentObject(model)
    └─ @EnvironmentObject (any descendant grabs it from environment)
```

**Rule of thumb:**
- Use `@State` for simple, view-local value types (Bool, String, Int)
- Use `@StateObject` to create and own a model object in a view (iOS 14+)
- Use `@ObservedObject` to reference a model object created elsewhere
- Use `@EnvironmentObject` to avoid passing an object through every level of the hierarchy

## Usage

**`@State` and `@Binding`:**
```swift
struct ParentView: View {
    @State private var isExpanded = false

    var body: some View {
        VStack {
            Toggle("Expand", isOn: $isExpanded)
            if isExpanded {
                ChildView(isExpanded: $isExpanded)
            }
        }
    }
}

struct ChildView: View {
    @Binding var isExpanded: Bool

    var body: some View {
        Button("Collapse") { isExpanded = false }
    }
}
```

**`ObservableObject` + `@ObservedObject`:**
```swift
class CounterModel: ObservableObject {
    @Published var count = 0

    func increment() { count += 1 }
}

struct CounterView: View {
    // In iOS 14+, prefer @StateObject when this view creates the model
    @ObservedObject var model: CounterModel

    var body: some View {
        VStack {
            Text("Count: \(model.count)")
            Button("Increment") { model.increment() }
        }
    }
}
```

**`@EnvironmentObject` — app-wide settings:**
```swift
class AppSettings: ObservableObject {
    @Published var isDarkMode = false
}

// At root:
ContentView()
    .environmentObject(AppSettings())

// In any descendant:
struct SettingsView: View {
    @EnvironmentObject var settings: AppSettings

    var body: some View {
        Toggle("Dark Mode", isOn: $settings.isDarkMode)
    }
}
```

## Adopting this pattern

1. Start with `@State` for all local, view-private values.
2. Pass `$binding` down to children that need to mutate the value — the child declares `@Binding`.
3. Move data that multiple unrelated views need into an `ObservableObject`; inject it with `.environmentObject()` at a common ancestor.
4. In iOS 14+, always use `@StateObject` (not `@ObservedObject`) when the view is responsible for creating the model instance to avoid lifecycle issues.
5. In iOS 17+, replace `ObservableObject`/`@Published` with `@Observable` for simpler, fine-grained observation.
