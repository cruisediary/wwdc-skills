---
framework: SF Symbols
title: "What's new in SF Symbols 6"
session: WWDC24-10188
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: migration
related: []
---

## What's new

- New animation presets: `.wiggle`, `.rotate`, `.breathe`
- `symbolEffect` modifier supports repeat with options (`repeatCount`, `continuous`)
- Variable color improvements — finer control over how variable color layers animate
- New symbols added to the SF Symbols library (800+ new glyphs)

## Before / After

```swift
// BEFORE (iOS 17): limited animation presets — bounce, pulse, variableColor, scale
Image(systemName: "bell")
    .symbolEffect(.bounce)

// AFTER (iOS 18): wiggle, rotate, breathe presets
Image(systemName: "bell")
    .symbolEffect(.wiggle)          // wobbles back and forth

Image(systemName: "arrow.clockwise")
    .symbolEffect(.rotate)          // continuous rotation

Image(systemName: "heart")
    .symbolEffect(.breathe)         // pulsing scale effect
```

```swift
// Repeat options
Image(systemName: "star")
    .symbolEffect(.bounce, options: .repeat(3))     // bounce 3 times
    .symbolEffect(.bounce, options: .repeating)     // bounce continuously

// Trigger-based discrete animation
@State private var trigger = 0

Image(systemName: "checkmark.circle")
    .symbolEffect(.bounce, value: trigger)

Button("Confirm") { trigger += 1 }
```

```swift
// Variable color — animate layers in sequence or simultaneously
Image(systemName: "wifi")
    .symbolEffect(.variableColor.iterative)      // layer by layer (default behavior)

Image(systemName: "wifi")
    .symbolEffect(.variableColor.cumulative)     // layers fill up cumulatively

Image(systemName: "speaker.wave.3")
    .symbolEffect(.variableColor.reversing)      // animate forward then reverse
```

```swift
// Combining effects
Image(systemName: "bolt.fill")
    .symbolEffect(.pulse)
    .symbolEffect(.scale.up, isActive: isHighlighted)
```

## Migration steps

1. Replace custom scale/opacity animations on `Image(systemName:)` with `.breathe` or `.pulse` where appropriate — system animations are better optimized and respect accessibility settings.
2. Where you previously used `.symbolEffect(.variableColor)` without options, review the new `.iterative`, `.cumulative`, and `.reversing` variants to pick the right semantic.
3. Animations that should stop after N repetitions: replace continuous timers with `.options: .repeat(N)`.
4. Check your symbol names against the SF Symbols 6 app — some symbols were renamed or have new variants; compile-time checks won't catch string-based symbol name changes.

## Compatibility notes

- `.wiggle`, `.rotate`, `.breathe` require iOS 18+ / macOS 15+.
- `.symbolEffect` itself is available on iOS 17+ / macOS 14+; the repeat options API was also introduced in iOS 17 but extended in iOS 18.
- All `symbolEffect` animations automatically pause when the user has Reduce Motion enabled — you do not need to check `UIAccessibility.isReduceMotionEnabled` manually for symbol animations.
- SF Symbols 6 glyphs are only available at runtime on iOS 18+/macOS 15+ — using a new symbol name on an older OS renders nothing; provide a fallback with `Image(systemName:) ?? Image(systemName: "fallback")` or conditional availability.
