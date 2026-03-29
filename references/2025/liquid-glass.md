---
framework: Liquid Glass
session: null
year: 2025
applies_to: iOS 26+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/liquid-glass.md
---

## What's new

Liquid Glass is a new design language shipped with iOS 26:

- **Liquid Glass replaces translucent materials** — `.glassEffect()` supersedes `.ultraThinMaterial`, `.thinMaterial`, `.regularMaterial` etc. for floating UI elements
- **Glass tinting** — color the glass with `.tint()` while preserving refraction and see-through quality
- **Specular highlights** — virtual light sources cast highlights on glass surfaces automatically
- **Dynamic depth blur** — blur intensity varies based on the distance of content behind the glass
- **GlassEffectContainer** — groups adjacent glass views into a single continuous glass slab for a cohesive look
- **System components auto-adopt** — sheets, navigation bars, toolbars, and tab bars receive Liquid Glass automatically; no code changes required for system chrome

## Before / After

**Before — translucent material overlay (iOS 15–17 style):**

```swift
struct InfoCard: View {
    var body: some View {
        VStack(alignment: .leading) {
            Text("Temperature")
                .font(.headline)
            Text("72°F")
                .font(.largeTitle)
        }
        .padding()
        .background(.ultraThinMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 16))
    }
}
```

**After — Liquid Glass (iOS 26+):**

```swift
struct InfoCard: View {
    var body: some View {
        VStack(alignment: .leading) {
            Text("Temperature")
                .font(.headline)
            Text("72°F")
                .font(.largeTitle)
        }
        .padding()
        .glassEffect()
        // Optional tint:
        // .tint(.blue)
    }
}
```

Note: `.glassEffect()` handles shape and clipping internally; the explicit `.clipShape` and `.background` are no longer needed.

## Migration steps

1. **Replace `.background(.ultraThinMaterial)` (and other material variants)** with `.glassEffect()` on custom floating UI elements such as cards, overlays, and HUDs.
2. **Remove manual `.clipShape` calls** paired with material backgrounds — `.glassEffect()` manages its own shape.
3. **Add `.tint(Color)`** after `.glassEffect()` wherever you previously used a colored overlay to tint a material.
4. **Wrap adjacent glass elements** in `GlassEffectContainer` when they should appear as a single continuous glass surface (e.g., a toolbar with multiple buttons).
5. **Leave system chrome alone** — navigation bars, tab bars, sheets, and toolbars adopt Liquid Glass automatically.
6. **Test on a real device** — the Simulator does not fully render glass refraction or specular highlights; visual results may differ from a physical device running iOS 26.

## Compatibility notes

- `.glassEffect()` and `GlassEffectContainer` require iOS 26+.
- On older OS versions, keep `.background(.ultraThinMaterial)` as the fallback or use `if #available(iOS 26, *) { ... }`.
- Liquid Glass is an iOS-first feature; macOS, tvOS, and watchOS have their own material systems that are unaffected.
