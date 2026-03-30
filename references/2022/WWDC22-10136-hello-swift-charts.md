---
framework: Swift Charts
title: "Hello Swift Charts"
session: WWDC22-10136
year: 2022
applies_to: iOS 16+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/swift-charts.md
---

# Hello Swift Charts — WWDC22

Swift Charts is introduced as a SwiftUI-native, declarative charting framework. A chart is composed of *marks* — visual representations of data — combined in a `Chart` container.

## Quick start

| Mark | Use case |
|---|---|
| `BarMark` | Categorical comparison |
| `LineMark` | Trends over time |
| `PointMark` | Scatter plots, distributions |
| `AreaMark` | Cumulative or range data |
| `RuleMark` | Reference lines, thresholds |
| `RectangleMark` | Heatmaps, interval ranges |

## Key APIs

```swift
import Charts

struct SalesChart: View {
    let data: [SaleItem]

    var body: some View {
        Chart(data) { item in
            BarMark(
                x: .value("Month", item.month),
                y: .value("Sales", item.count)
            )
        }
    }
}
```

## Common patterns

```swift
Chart(data) { item in
    LineMark(
        x: .value("Date", item.date),
        y: .value("Revenue", item.revenue)
    )
    .foregroundStyle(by: .value("Region", item.region))
    .symbol(by: .value("Region", item.region))
}
```

- `.foregroundStyle(by:)` — automatic color mapping + legend generation
- `.symbol(by:)` — automatic symbol shape per series

## Mixing mark types

```swift
Chart(data) { item in
    BarMark(x: .value("Day", item.day), y: .value("Count", item.count))
    RuleMark(y: .value("Average", average))
        .foregroundStyle(.red)
        .lineStyle(StrokeStyle(dash: [5, 3]))
}
```

## Accessibility

- Swift Charts generates automatic accessibility descriptions for every mark
- VoiceOver reads individual data points by default
- Override with `.accessibilityLabel(_:)` and `.accessibilityValue(_:)` on marks

## Gotchas

- Swift Charts requires iOS 16+ / macOS 13+
- No import of third-party packages needed — system framework (`import Charts`)
- Charts adapts to Dynamic Type, dark mode, and high-contrast automatically
