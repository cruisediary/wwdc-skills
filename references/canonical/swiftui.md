---
framework: SwiftUI
status: current
applies_to: iOS 13+
shape: code-first
superseded_by: null
history:
  - year: 2019
    file: 2019/swiftui.md
    summary: Initial introduction — View protocol, State, Binding, VStack/HStack/ZStack
---

# SwiftUI

Apple's declarative UI framework for building apps across all Apple platforms from a single codebase (iOS 13+, macOS 10.15+).

## Quick start

```swift
import SwiftUI

struct CounterView: View {
    @State private var count = 0

    var body: some View {
        VStack(spacing: 16) {
            Text("Count: \(count)")
                .font(.title)

            HStack {
                Button("−") { count -= 1 }
                    .buttonStyle(.bordered)
                Button("+") { count += 1 }
                    .buttonStyle(.bordered)
            }
        }
        .padding()
    }
}

// Child view receiving a binding
struct StepperView: View {
    @Binding var count: Int

    var body: some View {
        Stepper("Count: \(count)", value: $count)
    }
}

// Previews
#Preview {
    CounterView()
}
```

## Key APIs

| API | Purpose |
|---|---|
| `@State` | Local mutable state owned by this view |
| `@Binding` | Reference to state owned by a parent view |
| `@StateObject` | Owns and observes a reference type (pre-iOS 17) |
| `@ObservedObject` | Observes a reference type owned elsewhere (pre-iOS 17) |
| `@Observable` | iOS 17+ — modern replacement for `ObservableObject/@Published` |
| `@Environment` | Read values injected from the environment (e.g., `\.colorScheme`) |
| `@EnvironmentObject` | Read a reference type injected higher in the view tree (pre-iOS 17) |
| `VStack` / `HStack` / `ZStack` | Vertical, horizontal, depth layout containers |
| `NavigationStack` | Navigation with type-safe path (iOS 16+); replaces `NavigationView` |
| `List` | Scrollable list with row selection support |
| `ForEach` | Iterate over a collection to produce views |
| `.task { }` | Run async work tied to view lifetime |
| `.onChange(of:)` | React to value changes |
| `.sheet(isPresented:)` | Present a modal sheet |

## Common patterns

```swift
// Async data loading
struct UserProfile: View {
    @State private var user: User?

    var body: some View {
        Group {
            if let user {
                Text(user.name)
            } else {
                ProgressView()
            }
        }
        .task {
            user = try? await fetchUser(id: "123")
        }
    }
}

// Environment injection
struct RootApp: App {
    @StateObject private var store = AppStore()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(store)
        }
    }
}

// iOS 17+ with @Observable (preferred)
@Observable class ViewModel {
    var title = ""
}

struct ContentView: View {
    @State private var vm = ViewModel()

    var body: some View {
        Text(vm.title)
    }
}

// NavigationStack with type-safe path
NavigationStack {
    List(items) { item in
        NavigationLink(item.title, value: item)
    }
    .navigationDestination(for: Item.self) { item in
        ItemDetailView(item: item)
    }
}
```

## Gotchas

- `View` is a value type — never store mutable state in plain properties; use `@State`
- Views recompute when state changes — keep `body` computation cheap
- Use `@StateObject` (not `@ObservedObject`) when the view owns the object's lifetime
- On iOS 17+, prefer `@Observable` over `ObservableObject/@Published` for better performance
- `NavigationView` is deprecated in iOS 16 — use `NavigationStack` or `NavigationSplitView`
- Avoid calling `@State` setters in `body` synchronously — use `.onChange` or `.task`
