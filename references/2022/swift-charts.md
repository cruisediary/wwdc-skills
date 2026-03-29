---
framework: Swift Charts
session: WWDC22-10136
year: 2022
applies_to: iOS 16+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/swift-charts.md
---

# Swift Charts — WWDC22 Introduction

Swift Charts was introduced at WWDC22 as a SwiftUI-native declarative charting framework, replacing manual drawing or third-party libraries.

## What's new

- `Chart` container view — declarative composition using marks
- `BarMark`, `LineMark`, `PointMark`, `AreaMark`, `RuleMark`, `RectangleMark`
- `.value("Label", value)` encoding API — semantic data binding
- `.foregroundStyle(by:)` — automatic color encoding and legend generation
- `ChartXAxis` / `ChartYAxis` / `ChartLegend` — customizable axes and legends
- Automatic accessibility support — VoiceOver reads chart data
- Adaptive to Dynamic Type and dark mode

## Before / After

**Before (manual drawing or UIKit):**
```swift
// No native chart API — required third-party libraries (Charts/DGCharts)
// or manual Core Graphics drawing:
override func draw(_ rect: CGRect) {
    let context = UIGraphicsGetCurrentContext()!
    // calculate bar rects from data...
    context.fill(barRect)
}
```

**After (Swift Charts):**
```swift
Chart(salesData) { item in
    BarMark(
        x: .value("Month", item.month),
        y: .value("Revenue", item.revenue)
    )
}
```

## Migration steps

1. Add `import Charts` — no package dependency needed (system framework)
2. Replace custom drawing or third-party chart views with `Chart { }` + mark types
3. Map data properties to `.value("Label", property)` encodings
4. Use `.foregroundStyle(by:)` for color-coded series
5. Add `ChartXAxis`/`ChartYAxis` modifiers for custom axis formatting

## Compatibility notes

- Requires iOS 16+, macOS 13+
- No migration from specific third-party libraries — rewrite chart views against Swift Charts API
- Third-party chart libraries remain valid for iOS 15 and earlier deployment targets
