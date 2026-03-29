---
framework: WidgetKit
session: WWDC20-10028
year: 2020
applies_to: iOS 14+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/widgetkit.md
---

# WidgetKit — WWDC20 Introduction

WidgetKit was introduced at WWDC20, replacing Today Extensions with a SwiftUI-native home screen widget API.

## What's new

- `Widget` protocol — declares the widget extension entry point
- `TimelineProvider` — supplies snapshots on a schedule
- `TimelineEntry` — a date-stamped data snapshot for the widget
- `WidgetConfiguration` — `StaticConfiguration` or `IntentConfiguration`
- `WidgetFamily` — `.systemSmall`, `.systemMedium`, `.systemLarge`
- Widget bundles (`@main WidgetBundle`) — ship multiple widget types from one extension

## Before / After

**Before (Today Extension — deprecated):**
```swift
// UIViewController-based Today widget
class TodayViewController: UIViewController, NCWidgetProviding {
    func widgetPerformUpdate(completionHandler: @escaping (NCUpdateResult) -> Void) {
        // update UI
        completionHandler(.newData)
    }
}
```

**After (WidgetKit):**
```swift
struct SimpleEntry: TimelineEntry { let date: Date }

struct SimpleProvider: TimelineProvider {
    func placeholder(in context: Context) -> SimpleEntry { SimpleEntry(date: .now) }
    func getSnapshot(in context: Context, completion: @escaping (SimpleEntry) -> Void) {
        completion(SimpleEntry(date: .now))
    }
    func getTimeline(in context: Context, completion: @escaping (Timeline<SimpleEntry>) -> Void) {
        completion(Timeline(entries: [SimpleEntry(date: .now)], policy: .atEnd))
    }
}

struct SimpleWidget: Widget {
    var body: some WidgetConfiguration {
        StaticConfiguration(kind: "Simple", provider: SimpleProvider()) { entry in
            Text(entry.date, style: .time)
        }
    }
}
```

## Migration steps

1. Create a new Widget Extension target in Xcode
2. Define a `TimelineEntry` struct for your widget's data model
3. Implement `TimelineProvider` (or `AppIntentTimelineProvider` for iOS 17+)
4. Build widget UI as a SwiftUI `View`
5. Declare widget with `StaticConfiguration` or `AppIntentConfiguration`
6. Remove the old Today Extension target

## Compatibility notes

- Requires iOS 14+
- Today Extensions remain on older OS versions but are deprecated
- `IntentConfiguration` → `AppIntentConfiguration` migration needed for iOS 17+
- Widget views have limited SwiftUI support — no ScrollView, List, or interactive controls (before iOS 17)
