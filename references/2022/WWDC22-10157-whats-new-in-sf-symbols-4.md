---
framework: SF Symbols
title: "What's new in SF Symbols 4"
session: WWDC22-10157
year: 2022
applies_to: iOS 16+
status: reference-only
superseded_by: null
shape: migration
related: []
---

# What's new in SF Symbols 4 — WWDC22

SF Symbols 4 introduced variable color (representing values like signal strength or volume), rendering mode improvements, and new symbol variants.

## What's new

- **Variable color** — symbols can represent a continuous value (0.0–1.0) by lighting portions of the symbol in sequence, e.g. `wifi` showing signal bars
- **Rendering mode improvements** — better automatic rendering mode selection; `.palette`, `.multicolor`, `.hierarchical`, `.monochrome`
- **New symbols** — 700+ new symbols in the SF Symbols 4 library
- **`.symbolVariant`** — apply circle, square, fill, slash variants declaratively in SwiftUI
- **`.symbolRenderingMode`** — explicitly set rendering mode in SwiftUI

## Variable color

```swift
// SwiftUI — pass a Double from 0.0 to 1.0
Image(systemName: "wifi")
    .symbolRenderingMode(.multicolor)
    .foregroundStyle(.blue)

// Variable color uses the symbol's defined variable color layers
Image(systemName: "speaker.wave.3")
    .symbolVariant(.fill)
    .foregroundStyle(.primary)
// Pass a value to control how many layers are active:
// (variable color API in SwiftUI uses the symbol directly;
//  UIKit uses UIImage(systemName:variableValue:))
```

**UIKit:**
```swift
let image = UIImage(systemName: "wifi", variableValue: 0.75)
// variableValue: 0.0–1.0 controls how much of the symbol is lit
imageView.image = image
```

**SwiftUI with variable value:**
```swift
// In SwiftUI, pass variableValue to Image via the designated initialiser
Image(systemName: "wifi", variableValue: signalStrength)
    .foregroundStyle(.blue)
// signalStrength: Double in 0.0...1.0
```

## Rendering modes

```swift
// Hierarchical — layers at different opacities of one color
Image(systemName: "cloud.sun.fill")
    .symbolRenderingMode(.hierarchical)
    .foregroundStyle(.orange)

// Palette — explicit color per layer
Image(systemName: "cloud.sun.fill")
    .symbolRenderingMode(.palette)
    .foregroundStyle(.gray, .yellow)

// Multicolor — built-in colors per symbol
Image(systemName: "cloud.sun.fill")
    .symbolRenderingMode(.multicolor)
```

## Symbol variants

```swift
// Apply fill, circle, square, slash variants
Image(systemName: "heart")
    .symbolVariant(.fill)           // heart.fill

Image(systemName: "bell")
    .symbolVariant(.slash)          // bell.slash

Image(systemName: "person")
    .symbolVariant(.circle.fill)    // person.circle.fill
```

Set environment-wide:
```swift
VStack {
    Image(systemName: "star")
    Image(systemName: "heart")
}
.symbolVariant(.fill)
```

## Before / After

**Variable color — signal/volume indicators:**

Before (iOS 15 and earlier — multiple symbols or manual layer swapping):
```swift
// No variable color API; required switching between symbol names manually
// e.g. "wifi", "wifi.1", "wifi.2", "wifi.3" based on signal level
let symbolName = signalLevel > 0.66 ? "wifi" : signalLevel > 0.33 ? "wifi.2" : "wifi.1"
Image(systemName: symbolName)
```

After (iOS 16+):
```swift
Image(systemName: "wifi", variableValue: signalStrength)
    .foregroundStyle(.blue)
// signalStrength: Double in 0.0...1.0
```

**Multi-color symbols:**

Before — foregroundColor with single color only:
```swift
Image(systemName: "cloud.sun.fill")
    .foregroundColor(.orange)
// No way to color individual layers differently
```

After (iOS 15+ for rendering modes, iOS 16 for full palette support):
```swift
// Hierarchical
Image(systemName: "cloud.sun.fill")
    .symbolRenderingMode(.hierarchical)
    .foregroundStyle(.orange)

// Palette — explicit color per layer
Image(systemName: "cloud.sun.fill")
    .symbolRenderingMode(.palette)
    .foregroundStyle(.gray, .yellow)
```

**Symbol variants:**

Before — hardcoded variant suffix in symbol name string:
```swift
Image(systemName: "heart.fill")
Image(systemName: "bell.slash")
Image(systemName: "person.circle.fill")
```

After (iOS 15+):
```swift
Image(systemName: "heart").symbolVariant(.fill)
Image(systemName: "bell").symbolVariant(.slash)
Image(systemName: "person").symbolVariant(.circle.fill)
```

## Migration steps

1. Replace `Image(systemName: "wifi")` with `Image(systemName: "wifi", variableValue: level)` for signal/volume-type indicators
2. Replace `.foregroundColor` + multi-symbol workarounds with `.symbolRenderingMode(.palette)` + `.foregroundStyle` for multi-color symbols
3. Use `.symbolVariant` instead of hardcoded `"heart.fill"` strings to keep variant logic semantic

## Compatibility notes

- Variable color (`variableValue:`) requires iOS 16+ / macOS 13+
- `.symbolVariant` and `.symbolRenderingMode` require iOS 15+ / macOS 12+
- The SF Symbols 4 app on macOS is required to browse and export new symbols
