---
framework: SwiftUI
title: "Animate with springs"
session: WWDC23-10158
year: 2023
applies_to: iOS 17+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/swiftui.md
---

# Animate with springs (WWDC23)

iOS 17 introduces a unified spring animation API that replaces several overlapping spring types with a single, physically-grounded model based on **duration** and **bounce**.

## What changed and why

Previously SwiftUI had `spring(response:dampingFraction:blendDuration:)` and `interpolatingSpring(stiffness:damping:)`. The new API unifies these with a friendlier surface: `Animation.spring(duration:bounce:)` where `duration` is the settling time and `bounce` controls how much the spring overshoots (0 = critically damped, 1 = maximum bounce).

## Mental model

- **Duration** (`duration: TimeInterval`) — approximately how long the animation takes to settle. Think of it as the perceived speed.
- **Bounce** (`bounce: Double`, range 0…1) — how much the value overshoots and oscillates. 0 is smooth (no overshoot), higher values add playful elasticity.
- Use `Animation.spring` (the new API) for UI transitions; use `interpolatingSpring` when you need direct control over physical `stiffness` and `damping` parameters.
- Springs are velocity-preserving — if a gesture interrupts an ongoing animation, the new spring picks up at the current velocity for a fluid feel.
- Custom `Animatable` types let you animate your own value types by decomposing them into `AnimatableData`.

## Usage

**Basic spring animation:**
```swift
withAnimation(.spring(duration: 0.4, bounce: 0.3)) {
    isExpanded.toggle()
}
```

**Applying a spring to a specific modifier:**
```swift
Rectangle()
    .frame(width: isExpanded ? 300 : 100)
    .animation(.spring(duration: 0.5, bounce: 0.25), value: isExpanded)
```

**Smooth (no overshoot) spring:**
```swift
.animation(.spring(duration: 0.35, bounce: 0), value: isVisible)
```

**Using interpolatingSpring for physics control:**
```swift
withAnimation(.interpolatingSpring(stiffness: 170, damping: 15)) {
    position = newPosition
}
```

**Custom Animatable type:**
```swift
struct ArcShape: Shape {
    var angle: Double   // in radians

    var animatableData: Double {
        get { angle }
        set { angle = newValue }
    }

    func path(in rect: CGRect) -> Path {
        // draw arc using self.angle
        Path()
    }
}
```

**Repeating spring (new in iOS 17):**
```swift
.animation(.spring(duration: 0.4, bounce: 0.5).repeatCount(3, autoreverses: true), value: trigger)
```

## Adopting this pattern

1. Replace `spring(response:dampingFraction:)` with `spring(duration:bounce:)` — `response` ≈ `duration`, and `bounce` = 1 − `dampingFraction` (roughly).
2. Prefer `.spring(duration:bounce:)` for UI feedback animations (button press, card expand).
3. Use `bounce: 0` when you want smooth deceleration without overshoot (e.g., keyboard avoidance).
4. For gesture-driven animations, SwiftUI handles velocity continuity automatically — no extra work needed.
5. Implement `Animatable` on custom `Shape` or `ViewModifier` types to make their properties smoothly animatable.
