---
framework: Accessibility
title: "Create accessible spatial experiences"
session: WWDC23-10034
year: 2023
applies_to: visionOS 1+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/visionos.md
---

# Create accessible spatial experiences (WWDC23)

Guidance for making visionOS apps accessible, covering VoiceOver spatial audio, hover effects, head-gaze focus, and reduced motion.

## What changed and why

Accessibility on visionOS has unique challenges: content exists in 3D space, input is through gaze and pinch rather than touch, and there is no traditional screen. VoiceOver on visionOS uses spatial audio to indicate where elements are in space. Developers need to think about semantic labels, focus order, and hover feedback.

## Mental model

- **VoiceOver in spatial computing** — VoiceOver reads elements using 3D spatial audio, so element position and label convey location. Use `.accessibilityLabel` to describe what something is and what it does.
- **Hover effects** — Elements that respond to gaze should show a hover effect so users know they are targeted. SwiftUI adds hover effects automatically to standard controls; use `.hoverEffect()` for custom views.
- **Head-gaze focus** — Users look at a control and pinch to activate it. Ensure tap targets are large enough (minimum 60pt equivalent) and clearly labelled.
- **Reduce motion** — Respect `accessibilityReduceMotion` for animations; spatial animations can cause discomfort for some users.
- **Accessibility labels for 3D content** — RealityKit entities in a `RealityView` can be labelled using `.accessibilityLabel(_:)` on the `RealityView`, or per-entity via the `AccessibilityComponent`.

## Usage

**Basic label and hint on a custom control:**
```swift
Button(action: launchRocket) {
    RocketShape()
}
.accessibilityLabel("Launch rocket")
.accessibilityHint("Activates the main engine and begins the launch sequence")
```

**Hover effect on a custom interactive view:**
```swift
RoundedRectangle(cornerRadius: 12)
    .fill(.blue)
    .frame(width: 80, height: 80)
    .hoverEffect()  // Standard system highlight on gaze
    .onTapGesture { handleTap() }
```

**Grouping elements for VoiceOver:**
```swift
VStack {
    Text("Launch status")
    Text(statusMessage)
}
.accessibilityElement(children: .combine)
.accessibilityLabel("Launch status: \(statusMessage)")
```

**Accessibility for RealityKit entities:**
```swift
RealityView { content in
    let planet = try? await Entity(named: "Earth", in: bundle)
    // Attach an AccessibilityComponent
    var accessibility = AccessibilityComponent()
    accessibility.label = "Earth"
    accessibility.value = "The third planet from the Sun"
    planet?.components[AccessibilityComponent.self] = accessibility
    if let planet { content.add(planet) }
}
```

**Respecting reduced motion:**
```swift
struct OrbitAnimation: View {
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    var body: some View {
        PlanetView()
            .rotationEffect(.degrees(angle))
            .animation(reduceMotion ? nil : .linear(duration: 10).repeatForever(autoreverses: false),
                       value: angle)
    }
}
```

**Accessibility rotor for spatial content:**
```swift
.accessibilityRotor("Planets") {
    ForEach(planets) { planet in
        AccessibilityRotorEntry(planet.name, id: planet.id)
    }
}
```

## Adopting this pattern

1. Add `.accessibilityLabel` and `.accessibilityHint` to all interactive custom views and RealityKit entities.
2. Add `.hoverEffect()` to any view that responds to gaze-based targeting.
3. Use `.accessibilityElement(children: .combine)` to merge related labels into a single focused element.
4. Attach `AccessibilityComponent` to RealityKit entities that users can interact with.
5. Check `accessibilityReduceMotion` before starting continuous or looping spatial animations.
6. Test with VoiceOver in the simulator — activate VoiceOver, then navigate with the trackpad (simulating gaze) and click (simulating pinch).
