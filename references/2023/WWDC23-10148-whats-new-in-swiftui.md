---
framework: SwiftUI
title: "What's new in SwiftUI"
session: WWDC23-10148
year: 2023
applies_to: iOS 17+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/swiftui.md
  - canonical/observation.md
---

# What's new in SwiftUI (WWDC23)

SwiftUI in iOS 17 adds the `@Observable` macro, `#Preview`, scroll APIs, `ContentUnavailableView`, and TipKit integration.

## What's new

- `@Observable` macro — replaces `ObservableObject`/`@Published` with fine-grained property tracking
- `@Bindable` — new property wrapper for binding into an `@Observable` class
- `#Preview` macro — replaces `PreviewProvider` with a simpler freestanding macro syntax
- `ContentUnavailableView` — built-in empty-state view (title, image, description)
- `.scrollPosition(id:)` — programmatic scroll-to by item identity
- `.scrollTargetBehavior(_:)` / `.scrollTargetLayout()` — paging and snap-scroll
- `TipKit.Tip` protocol — in-app feature discovery tips via `TipView` / `.popoverTip(_:)`
- `.searchable` improvements — search scopes and tokens
- `@Environment` can now hold `@Observable` objects directly (no `environmentObject`)
- `Inspector` panel via `.inspector(isPresented:content:)` (see WWDC23-10162)

## Before / After

**Observable model:**
```swift
// Before (iOS 16)
class CounterModel: ObservableObject {
    @Published var count = 0
}
struct CounterView: View {
    @StateObject private var model = CounterModel()
    var body: some View { Text("\(model.count)") }
}

// After (iOS 17)
@Observable
class CounterModel {
    var count = 0
}
struct CounterView: View {
    @State private var model = CounterModel()
    var body: some View { Text("\(model.count)") }
}
```

**Preview macro:**
```swift
// Before
struct MyView_Previews: PreviewProvider {
    static var previews: some View { MyView() }
}

// After
#Preview {
    MyView()
}
```

**ContentUnavailableView:**
```swift
// Before: custom empty state
if items.isEmpty {
    VStack { Image(systemName: "tray"); Text("No items") }
}

// After
if items.isEmpty {
    ContentUnavailableView("No Items", systemImage: "tray", description: Text("Add something to get started."))
}
```

**Scroll position:**
```swift
// Before: no built-in programmatic scroll-to by id in List/ScrollView
// After
@State private var scrolledItemID: Item.ID?

ScrollView {
    LazyVStack {
        ForEach(items) { item in
            ItemRow(item: item)
                .id(item.id)
        }
    }
    .scrollTargetLayout()
}
.scrollPosition(id: $scrolledItemID)
```

## Migration steps

1. Replace `ObservableObject` + `@Published` with `@Observable` (see WWDC23-10149 for full guide)
2. Replace `PreviewProvider` structs with `#Preview { }` macro
3. Replace custom empty-state views with `ContentUnavailableView` where appropriate
4. Replace manual `ScrollViewReader` + `scrollTo` with `.scrollPosition(id:)` for list scenarios
5. Remove `.environmentObject` / `@EnvironmentObject` in favour of `.environment` / `@Environment(Type.self)`

## Compatibility notes

- `@Observable`, `@Bindable`, `#Preview` require iOS 17+ / Swift 5.9+
- `ContentUnavailableView` requires iOS 17+
- `.scrollPosition(id:)` requires iOS 17+
- `TipKit` requires iOS 17+
- `ObservableObject` continues to compile — migration is incremental
