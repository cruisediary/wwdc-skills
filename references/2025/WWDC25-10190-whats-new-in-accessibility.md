---
framework: Accessibility
title: "What's new in accessibility"
session: WWDC25-10190
year: 2025
applies_to: iOS 26+
status: reference-only
superseded_by: null
shape: migration
related:
  - 2024/WWDC24-10190-catch-up-on-accessibility-in-swiftui.md
  - 2024/WWDC24-10191-whats-new-in-accessibility-for-apple-platforms.md
---

# Accessibility — What's New in Accessibility (WWDC25)

iOS 26 improves accessibility APIs for Liquid Glass surfaces, VoiceOver spatial audio on visionOS, and Dynamic Type support in new layout contexts.

## What's new

- **Liquid Glass accessibility** — system ensures Liquid Glass surfaces maintain sufficient contrast for VoiceOver and Display Accommodations; custom glass surfaces should be tested with Reduce Transparency enabled
- **VoiceOver improvements** — enhanced spatial audio cues for visionOS; improved reading order for adaptive layouts
- **Dynamic Type in new contexts** — `@ScaledMetric` and Dynamic Type scale correctly in Liquid Glass containers and updated toolbar contexts
- **Assistive Access updates** — new system-level accessibility modes; apps can declare compatibility (see Apple docs)
- **Personal Voice improvements** — continued enhancements to Personal Voice API for users who rely on synthesized speech (see Apple docs)

## Before / After

**Before (iOS 18 — Reduce Transparency on custom blurred surfaces):**
```swift
// Developers manually handled Reduce Transparency
struct BlurredCard: View {
    @Environment(\.accessibilityReduceTransparency) var reduceTransparency

    var body: some View {
        Text("Content")
            .background(
                reduceTransparency
                    ? AnyView(Color.systemBackground)
                    : AnyView(Color.clear.background(.ultraThinMaterial))
            )
    }
}
```

**After (iOS 26 — `.glassEffect()` handles Reduce Transparency automatically):**
```swift
// The system automatically removes Liquid Glass when Reduce Transparency is enabled.
// No manual environment check needed for .glassEffect().
struct GlassCard: View {
    var body: some View {
        Text("Content")
            .padding()
            .glassEffect()  // Automatically falls back to opaque surface with Reduce Transparency
    }
}

// For custom materials that don't use .glassEffect(), still check manually:
@Environment(\.accessibilityReduceTransparency) var reduceTransparency
```

## Migration steps

1. Test all custom blurred/translucent surfaces with Reduce Transparency enabled on iOS 26 — verify `.glassEffect()` automatic fallback
2. Check VoiceOver reading order in any views using new Liquid Glass tab bar or toolbar layouts
3. Audit `@ScaledMetric` usage in new iOS 26 layout contexts (toolbar, floating controls) — verify scaling at all Dynamic Type sizes
4. Test with Display Accommodations (Increase Contrast, Reduce Transparency) in both light and dark mode

## Compatibility notes

- `.glassEffect()` automatic Reduce Transparency handling is iOS 26+ only; custom material handling remains necessary for older OS targets
- VoiceOver spatial audio improvements are visionOS 26+
- Exact new API surface for Assistive Access compatibility declarations should be verified against Xcode 26 documentation
