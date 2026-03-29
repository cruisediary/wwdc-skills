---
framework: Swift Charts
status: current
applies_to: iOS 16+
shape: code-first
superseded_by: null
history:
  - year: 2022
    file: 2022/swift-charts.md
    summary: Swift Charts introduction
---

# Swift Charts

Apple's declarative charting framework (iOS 16+, macOS 13+) built on SwiftUI. Define charts as a composition of marks — no subclassing or delegate patterns.

## Quick start

```swift
import Charts
import SwiftUI

struct SalesData: Identifiable {
    let id = UUID()
    let month: String
    let revenue: Double
}

let data = [
    SalesData(month: "Jan", revenue: 12000),
    SalesData(month: "Feb", revenue: 15000),
    SalesData(month: "Mar", revenue: 9500),
    SalesData(month: "Apr", revenue: 18000),
]

// Bar chart
struct RevenueChart: View {
    var body: some View {
        Chart(data) { item in
            BarMark(
                x: .value("Month", item.month),
                y: .value("Revenue", item.revenue)
            )
            .foregroundStyle(.blue)
        }
        .frame(height: 200)
        .padding()
    }
}

// Line chart
Chart(data) { item in
    LineMark(
        x: .value("Month", item.month),
        y: .value("Revenue", item.revenue)
    )
    PointMark(
        x: .value("Month", item.month),
        y: .value("Revenue", item.revenue)
    )
}
```

## Key APIs

| API | Purpose |
|---|---|
| `Chart` | Container view; iterates over data to produce marks |
| `BarMark` | Rectangular bar — categorical or numeric |
| `LineMark` | Line connecting data points |
| `PointMark` | Scatter plot point |
| `AreaMark` | Filled area under a line |
| `RuleMark` | Horizontal or vertical reference line |
| `.value("Label", value)` | Encodes a data dimension with a semantic label |
| `.foregroundStyle(by:)` | Color-encode a dimension (auto-generates legend) |
| `ChartXAxis` / `ChartYAxis` | Customize axis labels and marks |
| `.chartXScale(domain:)` | Set explicit axis domain |
| `.chartOverlay` | Add interactive overlay for touch/hover |

## Common patterns

```swift
// Multi-series line chart with legend
struct MultiSeriesChart: View {
    var body: some View {
        Chart {
            ForEach(seriesData) { series in
                ForEach(series.points) { point in
                    LineMark(
                        x: .value("Date", point.date),
                        y: .value("Value", point.value)
                    )
                    .foregroundStyle(by: .value("Series", series.name))
                }
            }
        }
    }
}

// Annotation on a mark
BarMark(x: .value("Month", item.month), y: .value("Revenue", item.revenue))
    .annotation(position: .top) {
        Text("$\(item.revenue, format: .number)")
            .font(.caption)
    }

// Rule mark for threshold line
RuleMark(y: .value("Target", 15000))
    .foregroundStyle(.red)
    .lineStyle(StrokeStyle(dash: [5]))
    .annotation(position: .trailing) {
        Text("Target").font(.caption).foregroundStyle(.red)
    }

// Interactive chart with chartOverlay
Chart(data) { item in
    BarMark(x: .value("Month", item.month), y: .value("Revenue", item.revenue))
}
.chartOverlay { proxy in
    GeometryReader { geo in
        Rectangle().fill(.clear).contentShape(Rectangle())
            .onTapGesture { location in
                let x = proxy.value(atX: location.x, as: String.self)
                // handle selection
            }
    }
}
```

## Gotchas

- Data must conform to `Plottable` — `String`, `Int`, `Double`, `Date` work out of the box
- `.foregroundStyle(by:)` automatically generates a legend; use `.chartLegend(.hidden)` to suppress
- Use `.chartXScale(domain:)` to prevent auto-scaling from clipping data
- Charts adapt to Dynamic Type and respect accessibility settings
- For very large datasets, aggregate before passing to `Chart` — it renders synchronously on the main thread
