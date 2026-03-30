---
framework: SwiftUI
title: "Inspectors in SwiftUI: Discover the details"
session: WWDC23-10162
year: 2023
applies_to: iOS 17+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/swiftui.md
---

# Inspectors in SwiftUI: Discover the details (WWDC23)

The `.inspector(isPresented:content:)` modifier introduces a trailing detail panel in SwiftUI that adapts to a push sheet on iPhone/compact and a side panel on iPad/regular.

## Quick start

```swift
struct ContentView: View {
    @State private var showInspector = false
    @State private var selectedItem: Item?

    var body: some View {
        NavigationSplitView {
            List(items, selection: $selectedItem) { item in
                Text(item.name)
            }
        } detail: {
            ItemDetailView(item: selectedItem)
                .inspector(isPresented: $showInspector) {
                    InspectorView(item: selectedItem)
                }
                .toolbar {
                    ToolbarItem(placement: .primaryAction) {
                        Button("Inspect", systemImage: "info.circle") {
                            showInspector.toggle()
                        }
                    }
                }
        }
    }
}
```

## Key APIs

| API | Purpose |
|---|---|
| `.inspector(isPresented:content:)` | Attaches an inspector panel to the view |
| `.inspectorColumnWidth(_:)` | Sets a fixed width for the inspector panel (regular-width only) |
| `.inspectorColumnWidth(min:ideal:max:)` | Sets a resizable width range for the panel |
| `InspectorCommands()` | Scene-level command group that adds a "Show Inspector" menu item |

## Common patterns

**Fixed-width inspector:**
```swift
.inspector(isPresented: $showInspector) {
    InspectorPanel()
        .inspectorColumnWidth(300)
}
```

**Resizable inspector:**
```swift
.inspector(isPresented: $showInspector) {
    InspectorPanel()
        .inspectorColumnWidth(min: 200, ideal: 300, max: 500)
}
```

**Adding a menu command:**
```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup { ContentView() }
            .commands { InspectorCommands() }
    }
}
```

**Passing selection into the inspector:**
```swift
.inspector(isPresented: $showInspector) {
    if let item = selectedItem {
        Form {
            LabeledContent("Name", value: item.name)
            LabeledContent("Size", value: item.size, format: .number)
        }
        .navigationTitle("Inspector")
    } else {
        ContentUnavailableView("No Selection", systemImage: "sidebar.right")
    }
}
```

## Gotchas

- On iPhone (compact horizontal size class), the inspector presents as a sheet instead of a side panel — design the inspector content to work in both contexts.
- `.inspectorColumnWidth` is silently ignored on compact/sheet presentation; use it only for column-width hints on iPad/Mac.
- The inspector is attached to the view it is declared on, not to the window — declare it on the content view that should share the screen with it.
- `InspectorCommands()` only wires up the keyboard shortcut and menu item; you still manage `isPresented` state yourself.
