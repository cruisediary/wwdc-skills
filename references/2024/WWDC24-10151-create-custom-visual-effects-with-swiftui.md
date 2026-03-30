---
framework: SwiftUI
title: "Create custom visual effects with SwiftUI"
session: WWDC24-10151
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/swiftui.md
---

# SwiftUI — Create Custom Visual Effects with SwiftUI (WWDC24)

iOS 18 introduces `MeshGradient` for multicolor gradients and `.visualEffect` for scroll-linked and geometry-driven effects without UIKit.

## Quick start

```swift
import SwiftUI

// MeshGradient — 3×3 grid of control points and colors
struct GradientBackground: View {
    var body: some View {
        MeshGradient(
            width: 3, height: 3,
            points: [
                [0.0, 0.0], [0.5, 0.0], [1.0, 0.0],
                [0.0, 0.5], [0.5, 0.5], [1.0, 0.5],
                [0.0, 1.0], [0.5, 1.0], [1.0, 1.0]
            ],
            colors: [
                .blue,   .purple, .indigo,
                .teal,   .cyan,   .mint,
                .green,  .yellow, .orange
            ]
        )
    }
}

// .visualEffect — read geometry, apply effects without breaking layout
struct ParallaxCard: View {
    var body: some View {
        Image("landscape")
            .visualEffect { content, geometry in
                content.offset(y: geometry.frame(in: .global).minY * 0.3)
            }
    }
}
```

## Key APIs

| API | Purpose |
|---|---|
| `MeshGradient(width:height:points:colors:)` | Multicolor gradient defined by a 2D grid of SIMD2 control points and colors |
| `.visualEffect { content, geometry in }` | Reads the view's `GeometryProxy` and applies effects without affecting layout |
| `.scrollTransition { content, phase in }` | Applies a transition effect as the view enters/exits the scroll viewport |
| `.colorEffect(_:)` | Applies a Metal shader as a per-pixel color transformation |
| `.layerEffect(_:maxSampleOffset:)` | Applies a Metal shader that can sample neighboring pixels |
| `.distortionEffect(_:maxSampleOffset:)` | Applies a Metal shader that distorts the view's geometry |
| `ScrollGeometry` | Provides scroll offset, content size, and visible rect inside `.scrollTransition` |

## Common patterns

**Parallax scroll effect using `.visualEffect`:**
```swift
ScrollView {
    LazyVStack {
        ForEach(items) { item in
            ItemCard(item: item)
                .visualEffect { content, geometry in
                    let frame = geometry.frame(in: .scrollView)
                    let offset = frame.minY / 4   // 25% parallax ratio
                    return content.offset(y: offset)
                }
        }
    }
}
```

**Fade and scale cards as they enter the viewport with `.scrollTransition`:**
```swift
ScrollView {
    LazyVStack {
        ForEach(items) { item in
            ItemCard(item: item)
                .scrollTransition { content, phase in
                    content
                        .opacity(phase.isIdentity ? 1 : 0.4)
                        .scaleEffect(phase.isIdentity ? 1 : 0.85)
                }
        }
    }
}
```

**Animated mesh gradient background:**
```swift
struct AnimatedGradientView: View {
    @State private var phase: CGFloat = 0

    var body: some View {
        MeshGradient(
            width: 3, height: 3,
            points: animatedPoints(phase: phase),
            colors: [
                .blue, .purple, .indigo,
                .teal, .cyan,   .mint,
                .green, .yellow, .orange
            ]
        )
        .onAppear {
            withAnimation(.linear(duration: 4).repeatForever(autoreverses: true)) {
                phase = 1
            }
        }
    }

    func animatedPoints(phase: CGFloat) -> [SIMD2<Float>] {
        [
            [0.0, 0.0], [0.5, 0.0], [1.0, 0.0],
            [0.0, 0.5], [Float(0.5 + 0.1 * phase), 0.5], [1.0, 0.5],
            [0.0, 1.0], [0.5, 1.0], [1.0, 1.0]
        ]
    }
}
```

**Custom color effect with a Metal shader:**
```swift
// Requires a .metal file with a color function
struct SaturationShaderView: View {
    var body: some View {
        Image("photo")
            .colorEffect(ShaderLibrary.saturation(.float(0.5)))
    }
}
```

## Gotchas

- **`.visualEffect` runs on every layout pass** — keep the closure fast. Avoid creating new objects, performing string formatting, or calling expensive functions inside the closure. Prefer simple arithmetic on `CGFloat` values.
- **`.visualEffect` does not affect layout** — the closure receives the view's laid-out frame and returns a modified content, but changes to position/size inside the closure are *visual only*. Other views still see the original frame.
- **`.scrollTransition` requires a `ScrollView` ancestor** — using it outside a `ScrollView` results in the identity phase always being active (no transition).
- **`MeshGradient` requires iOS 18+** — guard with `if #available(iOS 18, *)` for backward-compatible apps. There is no system-provided fallback.
- **Metal shaders (`.colorEffect`, `.layerEffect`, `.distortionEffect`) require a `.metal` file in the target** — they are compile-time, not runtime; missing functions produce a black/clear view without a crash, making debugging harder.
- **`MeshGradient` point count must equal `width × height`** — mismatched arrays produce a runtime crash.
