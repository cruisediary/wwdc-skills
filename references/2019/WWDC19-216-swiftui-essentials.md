---
framework: SwiftUI
title: "SwiftUI Essentials"
session: WWDC19-216
year: 2019
applies_to: iOS 13+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/swiftui.md
---

# SwiftUI Essentials (WWDC19)

Covers the core mental model behind SwiftUI: declarative UI, the `View` protocol, view composition, modifier chaining, `Group`, and the layout system.

## What changed and why

UIKit required imperative mutations — you called methods to change the UI in response to events, and had to ensure the UI was always consistent with state. SwiftUI introduces a declarative model: you describe *what* the UI should look like for a given state, and the framework figures out what to change when state updates.

Key shift:
- **Imperative (UIKit):** `label.text = "Hi"` — you mutate the view directly
- **Declarative (SwiftUI):** `Text(greeting)` — the view is re-derived from state automatically

## Mental model

**The `View` protocol:**
```swift
protocol View {
    associatedtype Body: View
    @ViewBuilder var body: Self.Body { get }
}
```
Every piece of SwiftUI UI is a value type (struct) conforming to `View`. Views are cheap to create — they describe layout, they are not the actual rendered objects.

**Modifiers return new views:**
```swift
// Each modifier wraps the previous view in a new layer
Text("Hello")
    .font(.title)          // -> ModifiedContent<Text, _FontModifier>
    .foregroundColor(.red) // -> ModifiedContent<..., _ForegroundColorModifier>
    .padding()             // -> ModifiedContent<..., _PaddingLayout>
```
Modifier order matters — `.padding().background()` differs from `.background().padding()`.

**`@ViewBuilder`** allows multiple views inside a closure without explicit `Group`:
```swift
var body: some View {
    // @ViewBuilder makes this closure return a TupleView
    Text("Line 1")
    Text("Line 2")
    Text("Line 3")
}
```

## Usage

**View composition — break UI into small structs:**
```swift
struct ProfileView: View {
    var body: some View {
        VStack {
            AvatarView()
            NameLabel(name: "Alex")
            BioText(bio: "iOS Developer")
        }
    }
}

struct AvatarView: View {
    var body: some View {
        Image(systemName: "person.circle.fill")
            .resizable()
            .frame(width: 80, height: 80)
            .clipShape(Circle())
    }
}
```

**`Group` — apply modifiers to multiple views at once:**
```swift
Group {
    Text("First")
    Text("Second")
    Text("Third")
}
.font(.headline)
.foregroundColor(.secondary)
```
`Group` does not add layout — it just groups views for modifier application or to work around the 10-view limit in a `@ViewBuilder` closure.

**Layout system — stacks with alignment and spacing:**
```swift
HStack(alignment: .top, spacing: 12) {
    Image(systemName: "star.fill")
    VStack(alignment: .leading) {
        Text("Title").font(.headline)
        Text("Subtitle").font(.subheadline)
    }
}
```

**`ZStack` for overlapping views:**
```swift
ZStack(alignment: .bottomTrailing) {
    Image("background")
    Text("Overlay text")
        .padding(8)
        .background(.black.opacity(0.6))
        .foregroundColor(.white)
}
```

## Adopting this pattern

1. Build UI as a tree of small, focused `View` structs — each should fit on one screen.
2. Prefer modifier chaining over subclassing; each modifier is a separate, inspectable layer.
3. Use `Group` when you need to apply the same modifiers to a collection of sibling views.
4. Use `@ViewBuilder` in custom container views to accept view content from callers.
5. Avoid embedding logic in `body` — extract computed properties or helper view structs for clarity.
