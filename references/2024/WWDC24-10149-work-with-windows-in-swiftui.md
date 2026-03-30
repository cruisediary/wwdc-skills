---
framework: SwiftUI
title: "Work with windows in SwiftUI"
session: WWDC24-10149
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/swiftui.md
---

# SwiftUI — Work with Windows in SwiftUI (WWDC24)

iOS 18 and macOS 15 expand SwiftUI's window management APIs with improved placement control, resizability, and programmatic open/dismiss for auxiliary windows.

## Quick start

```swift
import SwiftUI

// 1. Declare a WindowGroup with a stable ID in your App
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }

        WindowGroup("Inspector", id: "inspector") {
            InspectorView()
        }
        .windowResizability(.contentSize)
        .defaultWindowPlacement { content, context in
            // Position relative to the main window
            let mainFrame = context.defaultDisplay.visibleRect
            return WindowPlacement(.trailing(mainFrame))
        }
    }
}

// 2. Open the auxiliary window from any view
struct ContentView: View {
    @Environment(\.openWindow) private var openWindow

    var body: some View {
        Button("Open Inspector") {
            openWindow(id: "inspector")
        }
    }
}
```

## Key APIs

| API | Purpose |
|---|---|
| `@Environment(\.openWindow) var openWindow` | Opens a window by ID or with a value |
| `openWindow(id:)` | Opens a `WindowGroup` with the matching string ID |
| `openWindow(value:)` | Opens a `WindowGroup` typed to the passed `Codable` value |
| `@Environment(\.dismissWindow) var dismissWindow` | Dismisses a window by ID from within or outside the window |
| `@Environment(\.dismiss) var dismiss` | Dismisses the current window from within it |
| `WindowGroup(id:) { }` | Scene declaration for an auxiliary window |
| `.windowResizability(.contentSize)` | Locks window size to its content's ideal size |
| `.windowResizability(.contentMinSize)` | Sets the minimum size from content; allows user resizing above that |
| `.defaultWindowPlacement { content, context in }` | Returns a `WindowPlacement` controlling the window's initial position |
| `.defaultSize(width:height:)` | Sets the initial size of a window that has user-resizable content |

## Common patterns

**Opening an auxiliary window with data:**
```swift
// Scene declaration
WindowGroup("Detail", id: "item-detail", for: Item.ID.self) { $itemID in
    if let itemID {
        ItemDetailView(itemID: itemID)
    }
}

// Caller
@Environment(\.openWindow) private var openWindow

Button("Open Detail") {
    openWindow(value: item.id)
}
```

**Setting default window size:**
```swift
WindowGroup("Settings", id: "settings") {
    SettingsView()
}
.defaultSize(width: 480, height: 320)
.windowResizability(.contentMinSize)
```

**Dismissing a window programmatically from outside:**
```swift
struct ControlBar: View {
    @Environment(\.dismissWindow) private var dismissWindow

    var body: some View {
        Button("Close Inspector") {
            dismissWindow(id: "inspector")
        }
    }
}
```

**Pushing a window to a specific display position:**
```swift
.defaultWindowPlacement { _, context in
    let screen = context.defaultDisplay.visibleRect
    let size = CGSize(width: 400, height: 600)
    let origin = CGPoint(
        x: screen.maxX - size.width - 20,
        y: screen.minY + 20
    )
    return WindowPlacement(CGRect(origin: origin, size: size))
}
```

## Gotchas

- **macOS and iPadOS only** — `openWindow`, `dismissWindow`, and multi-window `WindowGroup` scenes are not supported on iPhone. The environment value is present but a no-op on unsupported platforms.
- **ID stability** — window IDs are persisted by the system for session restoration. Changing an ID breaks any saved window state.
- **`windowResizability(.contentSize)` requires a fixed-size content view** — if the content view has unbounded size, the window will collapse. Provide explicit `.frame(width:height:)` or use `.contentMinSize` instead.
- **Value-typed `WindowGroup` requires `Codable`** — the value passed to `openWindow(value:)` must be `Codable` and `Hashable` so the system can persist and deduplicate windows.
- **Multiple windows for same ID** — `openWindow(id:)` opens a new window each call unless the window is already open, in which case it brings the existing window to front (macOS) or is a no-op (iPadOS).
