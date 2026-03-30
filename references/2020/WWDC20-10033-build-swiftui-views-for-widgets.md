---
framework: WidgetKit
title: "Build SwiftUI views for widgets"
session: WWDC20-10033
year: 2020
applies_to: iOS 14+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/widgetkit.md
  - canonical/swiftui.md
---

# Build SwiftUI views for widgets

Widget views are plain SwiftUI views with a constrained environment. This session covers the view-specific APIs, size classes, and layout guidance for building widget UI.

## Quick start

```swift
import WidgetKit
import SwiftUI

struct WidgetView: View {
    let entry: SimpleEntry

    // Read the widget family from the environment
    @Environment(\.widgetFamily) var family

    var body: some View {
        switch family {
        case .systemSmall:
            SmallView(entry: entry)
        case .systemMedium:
            MediumView(entry: entry)
        case .systemLarge:
            LargeView(entry: entry)
        @unknown default:
            SmallView(entry: entry)
        }
    }
}
```

## Key APIs

| API | Description |
|---|---|
| `@Environment(\.widgetFamily)` | Current `WidgetFamily` — drive layout branching |
| `@Environment(\.colorScheme)` | `.light` / `.dark` — widgets render in both |
| `Link(destination:)` | Deep-link tap target inside a widget view |
| `widgetURL(_:)` | Sets the URL for the entire widget (single tap target) |
| `ContainerRelativeShape` | Shape that matches the widget corner radius from the system |
| `AccessibilityChartDescriptor` | Protocol for widget-scoped chart accessibility |
| `redacted(reason:)` | Applied automatically in placeholder state |
| `.isPlaceholder` | Environment key (internal); use `redacted` instead |

## Common patterns

**Single deep-link for the whole widget:**
```swift
struct SmallWidgetView: View {
    let entry: SimpleEntry
    var body: some View {
        Text(entry.date, style: .time)
            .widgetURL(URL(string: "myapp://widget/small"))
    }
}
```

**Multiple tap targets (medium/large only):**
```swift
struct MediumWidgetView: View {
    let entry: FeedEntry
    var body: some View {
        HStack {
            ForEach(entry.items) { item in
                Link(destination: URL(string: "myapp://item/\(item.id)")!) {
                    ItemCell(item: item)
                }
            }
        }
    }
}
```

**Corner-matched background with ContainerRelativeShape:**
```swift
struct WidgetBackground: View {
    var body: some View {
        ContainerRelativeShape()
            .fill(Color.accentColor.gradient)
    }
}
```

**Placeholder / redacted state:**
```swift
struct PlaceholderView: View {
    var body: some View {
        // Use real view structure; WidgetKit applies .redacted(.placeholder) automatically
        VStack(alignment: .leading) {
            Text("Loading title")
            Text("Loading subtitle")
        }
        .padding()
    }
}
```

**Adaptive layout across families:**
```swift
struct AdaptiveView: View {
    @Environment(\.widgetFamily) var family
    var isSmall: Bool { family == .systemSmall }

    var body: some View {
        VStack(alignment: isSmall ? .center : .leading) {
            // layout adjusts based on family
        }
    }
}
```

## Gotchas

- `ScrollView`, `List`, and gesture-based interactive views are not supported in widgets (pre-iOS 17)
- Only `Link` and `widgetURL` provide interactivity; all other taps open the app
- `widgetURL` and `Link` cannot be combined in `.systemSmall` — only `widgetURL` is respected at small size
- Widgets render in both light and dark mode; always test both
- Avoid heavy `onAppear` logic — widget views are rendered as static snapshots
- `ContainerRelativeShape` should be preferred over hard-coded corner radii to match the system's widget corner style
- Previews work in Xcode canvas with `WidgetPreviewContext(family: .systemSmall)`
