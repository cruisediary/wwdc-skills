---
framework: WidgetKit
status: current
applies_to: iOS 14+
shape: code-first
superseded_by: null
history:
  - year: 2020
    file: 2020/widgetkit.md
    summary: "Initial introduction — TimelineProvider, Widget protocol, WidgetBundle"
  - year: 2022
    file: null
    summary: "Lock Screen widgets, accessory widget families"
  - year: 2023
    file: null
    summary: "Interactive widgets — Button/Toggle inside widget views"
  - year: 2024
    file: null
    summary: "AppIntentTimelineProvider replaces IntentTimelineProvider"
---

# WidgetKit

Framework for building home screen, lock screen, and StandBy widgets (iOS 14+). Widgets are SwiftUI views driven by a `TimelineProvider` that pre-renders snapshots on a schedule.

## Quick start

```swift
import WidgetKit
import SwiftUI
import AppIntents

// 1. Define your timeline entry
struct WeatherEntry: TimelineEntry {
    let date: Date
    let temperature: Int
    let condition: String
}

// 2. Implement a timeline provider
struct WeatherProvider: AppIntentTimelineProvider {
    typealias Entry = WeatherEntry
    typealias Intent = ConfigurationAppIntent

    func placeholder(in context: Context) -> WeatherEntry {
        WeatherEntry(date: .now, temperature: 72, condition: "Sunny")
    }

    func snapshot(for configuration: ConfigurationAppIntent, in context: Context) async -> WeatherEntry {
        WeatherEntry(date: .now, temperature: 72, condition: "Sunny")
    }

    func timeline(for configuration: ConfigurationAppIntent, in context: Context) async -> Timeline<WeatherEntry> {
        var entries: [WeatherEntry] = []
        let currentDate = Date()
        for hourOffset in 0..<5 {
            let entryDate = Calendar.current.date(byAdding: .hour, value: hourOffset, to: currentDate)!
            entries.append(WeatherEntry(date: entryDate, temperature: 72 + hourOffset, condition: "Sunny"))
        }
        return Timeline(entries: entries, policy: .atEnd)
    }
}

// 3. Build the widget view
struct WeatherWidgetView: View {
    var entry: WeatherEntry

    var body: some View {
        VStack {
            Text("\(entry.temperature)°")
                .font(.largeTitle)
            Text(entry.condition)
        }
        .containerBackground(.fill.tertiary, for: .widget)
    }
}

// 4. Declare the widget
@main
struct WeatherWidget: Widget {
    let kind = "WeatherWidget"

    var body: some WidgetConfiguration {
        AppIntentConfiguration(
            kind: kind,
            intent: ConfigurationAppIntent.self,
            provider: WeatherProvider()
        ) { entry in
            WeatherWidgetView(entry: entry)
        }
        .configurationDisplayName("Weather")
        .description("Current temperature and conditions.")
        .supportedFamilies([.systemSmall, .systemMedium, .accessoryCircular])
    }
}
```

## Key APIs

| API | Purpose |
|---|---|
| `TimelineEntry` | A snapshot of your widget's data at a specific date |
| `AppIntentTimelineProvider` | Supplies timeline entries with user-configurable intent |
| `Timeline(entries:policy:)` | Sequence of entries with a reload policy |
| `Widget` | Declares the widget extension entry point |
| `AppIntentConfiguration` | Widget config with user-customizable `AppIntent` |
| `WidgetFamily` | Size variants: `.systemSmall/Medium/Large`, `.accessoryCircular`, `.accessoryRectangular` |
| `.containerBackground` | Sets the widget background (required iOS 17+) |
| `Link` / `widgetURL` | Deep link from widget tap |
| `@Entry` | Simplifies environment value injection into widgets |

## Common patterns

```swift
// Deep link from widget tap
WeatherWidgetView(entry: entry)
    .widgetURL(URL(string: "myapp://weather/\(entry.condition)"))

// Lock screen widget (accessory family)
.supportedFamilies([.accessoryCircular, .accessoryRectangular, .accessoryInline])

// Preview in Xcode
#Preview(as: .systemSmall) {
    WeatherWidget()
} timeline: {
    WeatherEntry(date: .now, temperature: 72, condition: "Sunny")
    WeatherEntry(date: .now, temperature: 68, condition: "Cloudy")
}

// Reload timeline manually from app
WidgetCenter.shared.reloadTimelines(ofKind: "WeatherWidget")
WidgetCenter.shared.reloadAllTimelines()
```

## Gotchas

- Widgets cannot run arbitrary code on tap — use `widgetURL` or `Link` for deep links
- The system decides when to render — `TimelineProvider` provides data, not live code
- `AppIntentTimelineProvider` replaces the old `IntentTimelineProvider` (deprecated)
- `.containerBackground` is required in iOS 17+ — without it widgets appear with the default system background
- Widget views have limited SwiftUI support — no `ScrollView`, `List`, or `TextEditor`
