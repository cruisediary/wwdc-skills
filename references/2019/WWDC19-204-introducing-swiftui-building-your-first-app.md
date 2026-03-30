---
framework: SwiftUI
title: "Introducing SwiftUI: Building Your First App"
session: WWDC19-204
year: 2019
applies_to: iOS 13+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/swiftui.md
---

# Introducing SwiftUI: Building Your First App (WWDC19)

The session that introduced SwiftUI at WWDC19, walking through building a first app using `Text`, `VStack`, `HStack`, `Button`, and `@State` with live previews in Xcode.

## Quick start

```swift
import SwiftUI

struct ContentView: View {
    @State private var name = ""

    var body: some View {
        VStack(spacing: 16) {
            Text("Hello, \(name.isEmpty ? "World" : name)!")
                .font(.largeTitle)

            HStack {
                TextField("Enter your name", text: $name)
                    .textFieldStyle(.roundedBorder)
                Button("Clear") { name = "" }
            }
            .padding()
        }
    }
}

// Live preview — no simulator needed
#Preview {
    ContentView()
}
```

## Key APIs

| API | Description |
|-----|-------------|
| `Text(_ content:)` | Displays a string; chainable with `.font()`, `.foregroundColor()`, `.bold()` |
| `VStack(spacing:)` | Vertical stack layout container |
| `HStack(spacing:)` | Horizontal stack layout container |
| `Button(_ label:action:)` | Tappable button with a closure action |
| `@State` | Property wrapper for local mutable view state; changes trigger view re-render |
| `$binding` | Derived two-way `Binding` from a `@State` property |
| `TextField(_ label:text:)` | Single-line editable text input bound to a `String` |
| `Image(_ name:)` / `Image(systemName:)` | Displays an asset or SF Symbol |
| `.padding()` | Adds default or custom padding around a view |
| `.font(_:)` | Sets the text font (`.title`, `.body`, `.caption`, etc.) |
| `PreviewProvider` | Legacy preview struct (Xcode < 15); replaced by `#Preview` macro |

## Common patterns

**Toggle state with a Button:**
```swift
struct ToggleView: View {
    @State private var isOn = false

    var body: some View {
        Button(isOn ? "Turn Off" : "Turn On") {
            isOn.toggle()
        }
        .buttonStyle(.borderedProminent)
    }
}
```

**List of items:**
```swift
struct FruitList: View {
    let fruits = ["Apple", "Banana", "Cherry"]

    var body: some View {
        List(fruits, id: \.self) { fruit in
            Text(fruit)
        }
    }
}
```

**NavigationView + NavigationLink (iOS 13–15 pattern):**
```swift
// Note: NavigationView deprecated in iOS 16 — use NavigationStack
NavigationView {
    List(items) { item in
        NavigationLink(item.name, destination: DetailView(item: item))
    }
    .navigationTitle("Items")
}
```

## Gotchas

- `@State` is local to the view — it is destroyed when the view leaves the hierarchy. For shared or persisted state, use `@ObservedObject` / `@EnvironmentObject`.
- `body` must return a single `View`. Wrap multiple views in `VStack`, `HStack`, `ZStack`, or `Group` when you need to return more than one.
- Live Preview requires Xcode 11+ and a Mac running macOS Catalina (10.15)+.
- `NavigationView` was deprecated in iOS 16 — migrate to `NavigationStack` for new projects.
- `PreviewProvider` is deprecated in Xcode 15 — use the `#Preview { }` macro instead.
