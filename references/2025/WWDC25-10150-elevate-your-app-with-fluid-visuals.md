---
framework: Liquid Glass
title: "Elevate your app with fluid visuals"
session: WWDC25-10150
year: 2025
applies_to: iOS 26+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/liquid-glass.md
  - 2025/liquid-glass.md
---

# Liquid Glass — Elevate Your App with Fluid Visuals (WWDC25)

This session is the primary guide for adopting Liquid Glass in custom app surfaces. It covers when to use `GlassEffect`, how to layer glass with content, tinting strategies, and performance considerations. The canonical reference is `canonical/liquid-glass.md`; this file records the session-specific framing.

## Concept

Liquid Glass is the new material system in iOS 26 / visionOS 26. Unlike `UIVisualEffectView`'s static blur, Liquid Glass adapts its refraction, tinting, and shadow in real time to content behind it. Key properties:

- **Refraction** — content behind glass is visually bent at edges
- **Adaptive tinting** — the glass surface picks up color from its background, shifting automatically in light/dark mode
- **Layering** — glass surfaces can be stacked, with each layer adding depth

## Step-by-step guide

### Step 1 — Identify surfaces that should use Liquid Glass

Use Liquid Glass for:
- Custom floating controls (volume sliders, playback bars, overlaid buttons)
- Cards or panels that float above scrollable content
- Custom sheets or action panels

Do NOT use Liquid Glass for:
- Opaque backgrounds or solid-color containers
- Every surface indiscriminately — overuse degrades legibility

### Step 2 — Apply `GlassEffect`

```swift
import SwiftUI

struct PlayerControls: View {
    var body: some View {
        HStack {
            Button(action: {}) { Image(systemName: "backward.fill") }
            Button(action: {}) { Image(systemName: "play.fill") }
            Button(action: {}) { Image(systemName: "forward.fill") }
        }
        .padding()
        .glassEffect()  // applies default Liquid Glass material
    }
}
```

### Step 3 — Customize tint and shape

```swift
// Tinted glass — picks up a color while remaining translucent
HStack { ... }
    .glassEffect(.regular.tint(.blue))

// Rounded rect shape (default is capsule for controls; use .rect for panels)
// See Apple docs for full GlassEffect shape options
```

### Step 4 — Avoid double-glass layering issues

If a glass surface sits inside a glass container (e.g., a glass button inside a glass sheet), use the appropriate layer variant to avoid visual over-blurring. Check Apple docs for the `interactive` vs `regular` material distinction.

### Step 5 — Test in both light and dark mode

Liquid Glass appearance shifts significantly between modes. Always test:
- Light mode with colorful backgrounds
- Dark mode with dark backgrounds
- Dynamic backgrounds (e.g., behind a video or animated gradient)

## Key APIs

| API | Purpose |
|---|---|
| `.glassEffect()` | Applies the default Liquid Glass material to a view's background |
| `.glassEffect(.regular.tint(_:))` | Applies tinted Liquid Glass |
| `GlassEffect` | The type describing the material style (regular, interactive, etc.) |
| `GlassBackgroundEffect` (UIKit/visionOS) | UIKit/visionOS equivalent; see Apple docs |

## Gotchas

- `.glassEffect()` requires iOS 26+ — always guard with `#available(iOS 26, *)` or set deployment target to iOS 26+
- Excessive use of glass surfaces can harm legibility, especially over low-contrast backgrounds
- Custom `Shape` clipping combined with `.glassEffect()` requires careful ordering of modifiers — glass must know the clipping shape; use `.glassEffect()` before `.clipShape()` in most cases (verify with Xcode previews)
- Performance: Liquid Glass is GPU-accelerated but avoid placing glass surfaces inside fast-scrolling lists without testing frame rate

## Compatibility notes

- iOS 26+ / visionOS 26+ only
- `.glassEffect()` has no back-deployment equivalent; use `UIVisualEffectView` with `.systemMaterial` for iOS 17 and earlier
- Exact modifier and type names should be verified against Xcode 26 SDK headers and WWDC25 session documentation
