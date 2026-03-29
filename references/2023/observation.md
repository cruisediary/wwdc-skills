---
framework: Observation
session: WWDC23-10149
year: 2023
applies_to: iOS 17+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/observation.md
---

# Observation — WWDC23 Introduction

The `@Observable` macro was introduced at WWDC23 (Swift 5.9) as a replacement for `ObservableObject` and `@Published`.

## What's new

- `@Observable` macro — marks a class for automatic per-property observation tracking
- `@Bindable` property wrapper — provides `$` binding access to an `@Observable` instance
- `withObservationTracking(_:onChange:)` — manual observation outside SwiftUI
- `@ObservationIgnored` — opt a property out of tracking
- Fine-grained updates — views only re-render when accessed properties change

## Before / After

**Before (ObservableObject):**
```swift
class UserViewModel: ObservableObject {
    @Published var name = ""
    @Published var isLoading = false
}

struct ProfileView: View {
    @StateObject private var vm = UserViewModel()

    var body: some View {
        Text(vm.name)
    }
}

struct NameField: View {
    @ObservedObject var vm: UserViewModel

    var body: some View {
        TextField("Name", text: $vm.name)
    }
}

// Environment injection
.environmentObject(vm)

// Retrieval
@EnvironmentObject var vm: UserViewModel
```

**After (@Observable):**
```swift
@Observable
class UserViewModel {
    var name = ""
    var isLoading = false
}

struct ProfileView: View {
    @State private var vm = UserViewModel()

    var body: some View {
        Text(vm.name)
    }
}

struct NameField: View {
    @Bindable var vm: UserViewModel

    var body: some View {
        TextField("Name", text: $vm.name)
    }
}

// Environment injection
.environment(vm)

// Retrieval
@Environment(UserViewModel.self) var vm
```

## Migration steps

1. Remove `ObservableObject` conformance from the class
2. Remove all `@Published` annotations from properties
3. Add `@Observable` macro to the class declaration
4. In views: change `@StateObject` → `@State`, `@ObservedObject` → `@Bindable` (if `$` bindings needed) or plain `let`/`var`
5. In injection: change `.environmentObject(vm)` → `.environment(vm)`
6. In retrieval: change `@EnvironmentObject var vm: Type` → `@Environment(Type.self) var vm`

## Compatibility notes

- Requires iOS 17+, macOS 14+, Swift 5.9+
- `ObservableObject` continues to work — migration is incremental
- `@Observable` and `ObservableObject` cannot be mixed on the same type
- `@Bindable` requires the type to be `@Observable`
