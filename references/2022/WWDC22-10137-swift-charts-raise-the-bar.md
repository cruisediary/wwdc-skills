---
framework: Swift Charts
title: "Swift Charts: Raise the bar"
session: WWDC22-10137
year: 2022
applies_to: iOS 16+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/swift-charts.md
---

# Swift Charts: Raise the bar — WWDC22

Advanced customisation of Swift Charts: custom axes, annotations, scrollable charts, and accessibility.

## What changed and why

This companion session to the introductory Swift Charts talk focuses on going beyond default styling: custom axis labels, per-mark annotations, scrollable domains, and plot area backgrounds. These APIs address the gap between "good enough for a demo" and "production-quality chart" by giving developers explicit control over every visual layer without dropping out of the declarative model.

## Mental model

Swift Charts is a declarative layer system: you compose marks (bars, lines, points) by binding data values to visual channels (x, y, foreground), and the framework resolves the scale, axes, and layout automatically. Customisation is additive — `AxisMarks`, `.annotation`, and `.chartPlotStyle` all modify specific layers of that resolved chart without requiring you to redraw the whole thing from scratch. Think of it like CSS on top of an auto-layout engine: the defaults handle 80% of cases, and modifiers let you surgically override the remaining 20%.

## Custom axes

```swift
Chart(data) { item in
    BarMark(x: .value("Month", item.month), y: .value("Sales", item.count))
}
.chartXAxis {
    AxisMarks(values: .automatic(desiredCount: 6)) { value in
        AxisGridLine()
        AxisTick()
        AxisValueLabel {
            if let month = value.as(Date.self) {
                Text(month, format: .dateTime.month(.abbreviated))
            }
        }
    }
}
.chartYAxis {
    AxisMarks(position: .leading)
}
```

## Annotations on marks

```swift
Chart(data) { item in
    BarMark(x: .value("Month", item.month), y: .value("Sales", item.count))
        .annotation(position: .top, alignment: .center) {
            Text("\(item.count)")
                .font(.caption2)
                .foregroundStyle(.secondary)
        }
}
```

- `position:` — `.top`, `.bottom`, `.leading`, `.trailing`, `.overlay`
- `alignment:` — standard `Alignment` values

## Chart-level annotations (reference lines, bands)

```swift
Chart {
    ForEach(data) { item in
        LineMark(x: .value("Day", item.day), y: .value("Value", item.value))
    }
    RuleMark(y: .value("Goal", goal))
        .annotation(position: .top, alignment: .leading) {
            Text("Goal").font(.caption).foregroundStyle(.red)
        }
        .foregroundStyle(.red)
}
```

## Scrollable charts

```swift
Chart(data) { item in
    BarMark(x: .value("Day", item.day), y: .value("Count", item.count))
}
.chartScrollableAxes(.horizontal)
.chartXVisibleDomain(length: 30)   // show 30 units at a time
```

## Plot area customisation

```swift
Chart(data) { item in
    LineMark(x: .value("Date", item.date), y: .value("Temp", item.temp))
}
.chartPlotStyle { plotArea in
    plotArea
        .background(.blue.opacity(0.1))
        .border(.blue, width: 1)
}
```

## Accessibility

- Each mark automatically generates an audio graph
- Override accessibility per mark:
```swift
BarMark(x: .value("Month", item.month), y: .value("Sales", item.count))
    .accessibilityLabel(item.month)
    .accessibilityValue("\(item.count) units sold")
```
- The chart-level `.accessibilityChartDescriptor` modifier provides a full `AXChartDescriptorRepresentable` for custom audio graph descriptions

## Compatibility notes

- All advanced chart APIs (`chartScrollableAxes`, `AxisMarks`, `.annotation`) require iOS 16+ / macOS 13+
- `chartScrollableAxes` was introduced in iOS 16 but refined in later releases; test scrolling behaviour on device
