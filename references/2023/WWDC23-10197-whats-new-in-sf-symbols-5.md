---
framework: SF Symbols
title: "What's new in SF Symbols 5"
session: WWDC23-10197
year: 2023
applies_to: iOS 17+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/swiftui.md
---

# What's new in SF Symbols 5 (WWDC23)

SF Symbols 5 ships symbol animation effects — `.pulse`, `.bounce`, `.variable-color`, `.appear`, `.disappear`, and `.replace` — applied via the `.symbolEffect(_:)` modifier.

## What's new

- **Symbol animations** — New `symbolEffect` modifier applies discrete or continuous animation effects
- **`.bounce`** — One-shot scale-up then settle animation (draws attention)
- **`.pulse`** — Continuous fade pulsing of the symbol (or variable-color layers)
- **`.variableColor`** — Animates variable-color layers in sequence (progress, volume, signal)
- **`.appear` / `.disappear`** — Transition a symbol in or out
- **`.replace`** — Animated symbol swap (`.replace.offUp`, `.replace.downUp`, `.replace.magic`)
- **Universal application** — Works on `Image` (SwiftUI), `UIImageView`, `NSImageView`
- **5 new symbol categories** — Game controllers, home, accessibility, fitness, nature

## Before / After

**Static symbol display (unchanged):**
```swift
Image(systemName: "star.fill")
    .foregroundStyle(.yellow)
```

**Adding a continuous animation effect (new):**
```swift
// Before (iOS 16): no built-in symbol animation; needed custom view modifiers
Image(systemName: "antenna.radiowaves.left.and.right")

// After (iOS 17): continuous pulse
Image(systemName: "antenna.radiowaves.left.and.right")
    .symbolEffect(.pulse)
```

**Triggering a discrete effect:**
```swift
@State private var bounceCounter = 0

Image(systemName: "bell.fill")
    .symbolEffect(.bounce, value: bounceCounter)
Button("Ring") { bounceCounter += 1 }
```

**Variable-color animation:**
```swift
// Animates through the symbol's variable-color layers
Image(systemName: "speaker.wave.3.fill")
    .symbolEffect(.variableColor.iterative.reversing)
```

**Symbol replacement transition:**
```swift
@State private var isFilled = false

Image(systemName: isFilled ? "star.fill" : "star")
    .contentTransition(.symbolEffect(.replace.offUp))
    .onTapGesture { withAnimation { isFilled.toggle() } }
```

**UIKit usage:**
```swift
// Continuous
imageView.addSymbolEffect(.pulse)

// Discrete (triggers once)
imageView.addSymbolEffect(.bounce)

// Transition between symbols
imageView.setSymbolImage(UIImage(systemName: "heart.fill")!,
                         contentTransition: .replace.downUp)
```

## Migration steps

1. Remove any custom symbol-animation code (timer-based opacity toggles, scale animations) and replace with `.symbolEffect`.
2. Use `.symbolEffect(.pulse)` or `.symbolEffect(.variableColor)` for continuous indicators.
3. Use `.symbolEffect(.bounce, value:)` with a counter state for user-action feedback (taps, completions).
4. Use `.contentTransition(.symbolEffect(.replace))` for animated symbol swaps instead of a plain image swap.

## Compatibility notes

- All symbol effects require iOS 17+ / macOS 14+.
- `contentTransition(.symbolEffect(.replace))` requires iOS 17+.
- On iOS 16 and earlier, the symbol appears statically — no crash, just no animation.
- SF Symbols 5 app (macOS) is required to browse the new symbol library; use Xcode 15's asset catalog for custom symbols.
