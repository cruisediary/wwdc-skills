---
framework: SwiftUI
title: "Demystify SwiftUI"
session: WWDC21-10022
year: 2021
applies_to: iOS 15+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/swiftui.md
---

# Demystify SwiftUI (WWDC21)

Explains the three core concepts SwiftUI uses internally to decide what to render and when to update: **identity**, **lifetime**, and **dependencies**.

## Mental model

```
Identity   — is this the same view or a different one?
Lifetime   — how long does this view (and its state) live?
Dependency — what data does this view read, and when should it redraw?
```

## Identity

SwiftUI uses two kinds of identity to track views across updates:

### Structural identity (implicit)

- SwiftUI infers identity from a view's **type and position in the view hierarchy**
- If the same view type appears in the same conditional branch in the same position, it is the *same* view instance
- Changing branches in an `if`/`else` or using `switch` creates *new* views with fresh lifetimes

```swift
// WRONG — SwiftUI sees two different structural positions; both Dog and Cat
// have separate lifetimes and their state resets on every toggle
if isPet {
    DogView()
        .someModifier()
} else {
    CatView()
        .someModifier()
}

// RIGHT — if the views are the same type, keep them in the same structural position
// and use conditional modifiers to differentiate
AnimalView()
    .foregroundColor(isPet ? .brown : .gray)
```

### Explicit identity (`.id(_:)`)

- Assign a stable `Hashable` value to pin a view's identity to data
- Changing the `.id` value destroys the old view and creates a brand-new one — useful to reset `@State`

```swift
// Changing userId resets the profile form's state completely
ProfileFormView(user: user)
    .id(user.id)
```

## Lifetime

- A view's lifetime begins when it first appears and ends when it disappears from the hierarchy
- `@State` is created once per lifetime — its initial value is set only on first appearance
- Using structural identity incorrectly can cause unexpected state resets or state persistence

```swift
// State is preserved as long as the view stays in the same structural position
struct CounterView: View {
    @State private var count = 0
    var body: some View {
        Button("\(count)") { count += 1 }
    }
}
```

## Dependencies

- Every source of data a view reads is a **dependency** — `@State`, `@Binding`, `@ObservedObject`, `@EnvironmentObject`, `@Environment`
- SwiftUI re-invokes `body` only when a dependency changes
- `body` should be a **pure function of its inputs** — side effects in `body` cause bugs

```swift
// Each view declares its own narrow dependency — SwiftUI only re-renders
// the views whose dependencies actually changed
struct TitleView: View {
    @ObservedObject var model: ContentModel   // re-renders only when model publishes
    var body: some View { Text(model.title) }
}

struct BadgeView: View {
    @ObservedObject var model: ContentModel
    var body: some View { Text("\(model.badgeCount)") }
}
// If only badgeCount changes, only BadgeView re-renders — TitleView is unaffected
```

## Key patterns

```swift
// Prefer AnyView only when absolutely necessary — it erases type information
// and hides identity from SwiftUI, preventing optimisations
// BAD
func makeView(condition: Bool) -> some View {
    if condition {
        return AnyView(Text("Yes"))
    } else {
        return AnyView(Image(systemName: "xmark"))
    }
}

// GOOD — use @ViewBuilder instead
@ViewBuilder
func makeView(condition: Bool) -> some View {
    if condition {
        Text("Yes")
    } else {
        Image(systemName: "xmark")
    }
}

// Stable identity for List rows — use the item's own identifier
List(items) { item in
    RowView(item: item)   // item.id is used as identity by ForEach
}
// vs unstable identity (index-based) which breaks animations and state
List(Array(items.enumerated()), id: \.offset) { _, item in
    RowView(item: item)   // avoid — offset changes on insertion/deletion
}
```

## Summary rules

1. Keep the same view type in the same structural position across state changes when you want to preserve state
2. Use `.id(_:)` to explicitly reset state when the underlying data identity changes
3. Narrow your dependencies — split large `@ObservedObject` types into smaller ones so fewer views redraw
4. Avoid `AnyView` in hot paths — it hides structural identity from SwiftUI

## Compatibility notes

- These concepts apply to all SwiftUI versions; session was updated context for iOS 15 / SwiftUI 3
- `@StateObject` (iOS 14+) vs `@ObservedObject`: `@StateObject` owns the object and ties its lifetime to the view; `@ObservedObject` does not own it
- The dependency graph is evaluated lazily — only views that are currently in the hierarchy are tracked
