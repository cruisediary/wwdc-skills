---
framework: Observation
status: current
applies_to: iOS 17+
shape: guide-first
superseded_by: null
history:
  - year: 2023
    file: 2023/observation.md
    summary: "@Observable macro replacing ObservableObject/@Published"
---

# Observation

The `@Observable` macro (iOS 17+, Swift 5.9+) provides fine-grained dependency tracking for model objects used in SwiftUI, replacing `ObservableObject` and `@Published`.

## What changed and why

`ObservableObject` notified all subscribers whenever *any* `@Published` property changed, causing unnecessary SwiftUI view updates. `@Observable` uses per-property tracking — a view only re-renders when the specific properties it accesses change. This eliminates the `@Published` boilerplate and improves performance automatically.

## Mental model

```
ObservableObject + @Published  →  @Observable
@StateObject                   →  @State (for owned instances)
@ObservedObject                →  @Bindable (when you need $ binding access)
                                   or plain let/var for read-only access
@EnvironmentObject             →  @Environment(MyType.self)
```

`@Observable` is macro-generated. Every stored property becomes trackable automatically — no annotation needed. Only computed properties and properties you explicitly mark `@ObservationIgnored` are excluded.

## Usage

```swift
import Observation
import SwiftUI

// 1. Define your observable model — no ObservableObject, no @Published
@Observable
class UserViewModel {
    var name = ""
    var isLoading = false

    @ObservationIgnored  // exclude from tracking
    private var internalCache: [String: Any] = [:]

    func load() async {
        isLoading = true
        // fetch...
        isLoading = false
    }
}

// 2. Use in SwiftUI — @State owns it, no @StateObject needed
struct ProfileView: View {
    @State private var vm = UserViewModel()

    var body: some View {
        VStack {
            if vm.isLoading {
                ProgressView()
            } else {
                Text(vm.name)
            }
        }
        .task { await vm.load() }
    }
}

// 3. Pass as a parameter — no @ObservedObject needed
struct NameField: View {
    @Bindable var vm: UserViewModel  // use @Bindable for $vm.name binding access

    var body: some View {
        TextField("Name", text: $vm.name)
    }
}

// 4. Inject into environment
struct RootView: View {
    @State private var vm = UserViewModel()

    var body: some View {
        ContentView()
            .environment(vm)
    }
}

struct ContentView: View {
    @Environment(UserViewModel.self) private var vm

    var body: some View {
        Text(vm.name)
    }
}
```

## Adopting this pattern

Migrating from `ObservableObject`: see `2023/observation.md` for a step-by-step before/after guide. Key changes: remove `ObservableObject` conformance, remove all `@Published`, change `@StateObject` to `@State`, change `@ObservedObject` to `@Bindable` (if binding access needed) or plain property. Change `@EnvironmentObject` injection to `.environment(value)` and retrieval to `@Environment(Type.self)`.
