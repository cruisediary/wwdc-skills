---
framework: WidgetKit
title: "Widgets code-along, Part 1: The adventure begins"
session: WWDC20-10034
year: 2020
applies_to: iOS 14+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/widgetkit.md
  - canonical/swiftui.md
---

# Widgets code-along, Part 1: The adventure begins

Step-by-step construction of the EmojiRanger widget — provider, entry, view, bundle, and placeholder. Companion to WWDC20-10028.

## Quick start

```swift
// The full EmojiRanger widget built in this session:

import WidgetKit
import SwiftUI

// Step 1: TimelineEntry — data snapshot with a date stamp
struct RangerEntry: TimelineEntry {
    let date: Date
    let character: RangerCharacter   // your app's model
}

// Step 2: TimelineProvider
struct RangerProvider: TimelineProvider {

    // Placeholder shown while first timeline loads
    func placeholder(in context: Context) -> RangerEntry {
        RangerEntry(date: .now, character: .panda)
    }

    // Snapshot for the widget gallery
    func getSnapshot(in context: Context, completion: @escaping (RangerEntry) -> Void) {
        completion(RangerEntry(date: .now, character: .panda))
    }

    // Full timeline — here we return a single entry
    func getTimeline(in context: Context, completion: @escaping (Timeline<RangerEntry>) -> Void) {
        let entry = RangerEntry(date: .now, character: RangerCharacter.current())
        let timeline = Timeline(entries: [entry], policy: .atEnd)
        completion(timeline)
    }
}

// Step 3: Widget view
struct EmojiRangerWidgetView: View {
    let entry: RangerEntry

    var body: some View {
        ZStack {
            Color("WidgetBackground")
            VStack {
                Text(entry.character.emoji)
                    .font(.system(size: 56))
                Text(entry.character.name)
                    .font(.headline)
                    .foregroundColor(.white)
            }
        }
    }
}

// Step 4: Widget declaration
struct EmojiRangerWidget: Widget {
    let kind = "EmojiRangerWidget"

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: RangerProvider()) { entry in
            EmojiRangerWidgetView(entry: entry)
        }
        .configurationDisplayName("Emoji Ranger")
        .description("Keep track of your favorite ranger.")
        .supportedFamilies([.systemSmall])
    }
}

// Step 5: WidgetBundle
@main
struct EmojiRangerWidgets: WidgetBundle {
    var body: some Widget {
        EmojiRangerWidget()
    }
}
```

## Key APIs

| API | Role in the code-along |
|---|---|
| `TimelineEntry` | Data model — must have `var date: Date` |
| `TimelineProvider` | Source of truth: `placeholder`, `getSnapshot`, `getTimeline` |
| `Timeline(entries:policy:)` | Wraps entries; `.atEnd` requests reload after last entry fires |
| `StaticConfiguration` | Non-configurable widget wired to the provider |
| `Widget` | Declares kind, configuration, and display metadata |
| `WidgetBundle` | `@main` root that vends all widget types |
| `.configurationDisplayName` | Name shown in the widget gallery picker |
| `.description` | Short description shown in the widget gallery |
| `.supportedFamilies` | Which sizes this widget supports |
| `WidgetPreviewContext` | Used in Xcode Previews to render a family size |

## Common patterns

**Xcode preview for a widget:**
```swift
struct EmojiRangerWidget_Previews: PreviewProvider {
    static var previews: some View {
        EmojiRangerWidgetView(entry: RangerEntry(date: .now, character: .panda))
            .previewContext(WidgetPreviewContext(family: .systemSmall))
    }
}
```

**Placeholder using `.redacted`:**
```swift
// WidgetKit automatically applies .redacted(.placeholder) to your view
// when placeholder(in:) data is displayed. Design the view to look
// reasonable in a redacted state — use real structure, not empty views.
struct EmojiRangerWidgetView: View {
    let entry: RangerEntry
    var body: some View {
        VStack {
            Text(entry.character.emoji)   // redacted as a gray blob
            Text(entry.character.name)    // redacted as a gray line
        }
    }
}
```

**Refreshing from the main app after a game event:**
```swift
// In the main app target:
import WidgetKit

func characterLeveledUp() {
    WidgetCenter.shared.reloadTimelines(ofKind: "EmojiRangerWidget")
}
```

## Gotchas

- The Widget Extension is a separate target — it cannot directly call main-app code; share models via a framework or app group
- `placeholder(in:)` must be synchronous and fast — do not make network calls here
- `getSnapshot` should also be fast; it powers the widget gallery preview
- `kind` string must be unique across all widgets in the bundle; used by `WidgetCenter` to target reloads
- Forgetting `@main` on `WidgetBundle` (or `Widget` if there is only one) prevents the extension from launching
- `supportedFamilies` defaults to all families if omitted — always declare explicitly to avoid unsupported layouts
