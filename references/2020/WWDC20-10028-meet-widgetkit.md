---
framework: WidgetKit
title: "Meet WidgetKit"
session: WWDC20-10028
year: 2020
applies_to: iOS 14+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/widgetkit.md
---

# Meet WidgetKit

WidgetKit replaces Today Extensions with a SwiftUI-native, timeline-driven widget system for the home screen and Notification Center.

## Quick start

```swift
import WidgetKit
import SwiftUI

// 1. Define a TimelineEntry
struct SimpleEntry: TimelineEntry {
    let date: Date
    let relevance: TimelineEntryRelevance?
}

// 2. Implement TimelineProvider
struct SimpleProvider: TimelineProvider {
    func placeholder(in context: Context) -> SimpleEntry {
        SimpleEntry(date: .now, relevance: nil)
    }

    func getSnapshot(in context: Context, completion: @escaping (SimpleEntry) -> Void) {
        completion(SimpleEntry(date: .now, relevance: nil))
    }

    func getTimeline(in context: Context, completion: @escaping (Timeline<SimpleEntry>) -> Void) {
        let entries = [SimpleEntry(date: .now, relevance: nil)]
        let timeline = Timeline(entries: entries, policy: .atEnd)
        completion(timeline)
    }
}

// 3. Build the widget view
struct SimpleWidgetView: View {
    let entry: SimpleEntry
    var body: some View {
        Text(entry.date, style: .time)
    }
}

// 4. Declare the widget
struct SimpleWidget: Widget {
    let kind = "SimpleWidget"

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: SimpleProvider()) { entry in
            SimpleWidgetView(entry: entry)
        }
        .configurationDisplayName("Simple")
        .description("Shows the current time.")
        .supportedFamilies([.systemSmall, .systemMedium, .systemLarge])
    }
}

// 5. Bundle multiple widgets
@main
struct MyWidgets: WidgetBundle {
    var body: some Widget {
        SimpleWidget()
        // AnotherWidget()
    }
}
```

## Key APIs

| API | Description |
|---|---|
| `Widget` | Protocol that defines a widget extension entry point |
| `WidgetBundle` | Groups multiple `Widget` types in one extension |
| `TimelineProvider` | Supplies placeholder, snapshot, and timeline entries |
| `TimelineEntry` | Protocol requiring a `date: Date` property |
| `Timeline(entries:policy:)` | Wraps entries with a refresh policy |
| `TimelineReloadPolicy` | `.atEnd`, `.after(_:)`, `.never` — controls next reload |
| `StaticConfiguration` | Widget with no user configuration |
| `IntentConfiguration` | Widget backed by a `INIntent` for user configuration |
| `WidgetFamily` | `.systemSmall`, `.systemMedium`, `.systemLarge` |
| `TimelineEntryRelevance` | Score and duration hint for Smart Stack ordering |
| `WidgetCenter` | `reloadTimelines(ofKind:)`, `reloadAllTimelines()` |

## Common patterns

**Scheduling future entries:**
```swift
func getTimeline(in context: Context, completion: @escaping (Timeline<SimpleEntry>) -> Void) {
    var entries: [SimpleEntry] = []
    let now = Date()
    for offset in 0..<5 {
        let entryDate = Calendar.current.date(byAdding: .hour, value: offset, to: now)!
        entries.append(SimpleEntry(date: entryDate, relevance: nil))
    }
    // Reload from the network after the last entry
    let timeline = Timeline(entries: entries, policy: .atEnd)
    completion(timeline)
}
```

**Intent-based (configurable) widget:**
```swift
struct ConfigurableProvider: IntentTimelineProvider {
    func placeholder(in context: Context) -> SimpleEntry { SimpleEntry(date: .now, relevance: nil) }

    func getSnapshot(for configuration: ConfigurationIntent, in context: Context,
                     completion: @escaping (SimpleEntry) -> Void) {
        completion(SimpleEntry(date: .now, relevance: nil))
    }

    func getTimeline(for configuration: ConfigurationIntent, in context: Context,
                     completion: @escaping (Timeline<SimpleEntry>) -> Void) {
        completion(Timeline(entries: [SimpleEntry(date: .now, relevance: nil)], policy: .atEnd))
    }
}
```

**Triggering a reload from the main app:**
```swift
WidgetCenter.shared.reloadTimelines(ofKind: "SimpleWidget")
```

## Gotchas

- Widget views are rendered as snapshots — no timers, video, or interactive SwiftUI (before iOS 17 interactive widgets)
- `getSnapshot` should return immediately with placeholder-quality data; used in the widget gallery
- `placeholder` is called when WidgetKit has no data yet — keep it cheap and redacted-looking
- Maximum timeline entries returned in one `getTimeline` call is not documented; stay under ~100
- `WidgetFamily` must be declared in `supportedFamilies`; omit a family to hide it from the gallery
- `IntentConfiguration` requires a custom Siri Intent Definition file and an Intents extension (or Intents UI extension) in older OS; see WWDC20-10033 for view-side guidance
