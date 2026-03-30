---
framework: RealityKit
title: "Enhance your app with Reality Composer Pro"
session: WWDC23-10273
year: 2023
applies_to: visionOS 1+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/visionos.md
---

# Enhance your app with Reality Composer Pro (WWDC23)

How to load Reality Composer Pro content in Swift, trigger animations, and wire up behaviors to app logic using the trigger/action API.

## Quick start

```swift
import RealityKit
import SwiftUI

struct GardenView: View {
    var body: some View {
        RealityView { content in
            // Load the root scene from the RC Pro package
            guard let scene = try? await Entity(named: "GardenScene",
                                                in: realityKitContentBundle) else { return }
            content.add(scene)

            // Trigger a named behavior defined in RC Pro
            if let flowerEntity = scene.findEntity(named: "Sunflower") {
                flowerEntity.components[BehaviorComponent.self]?.triggers["Bloom"]?.fire()
            }
        }
    }
}
```

## Key APIs

| API | Purpose |
|---|---|
| `Entity(named:in:)` | Async load a named scene/entity from an RC Pro bundle |
| `realityKitContentBundle` | Auto-generated accessor for the `.realitycomposerpro` package bundle |
| `entity.findEntity(named:)` | Find a descendant entity by name |
| `BehaviorComponent` | Component storing trigger/action pairs authored in RC Pro |
| `ParticleEmitterComponent` | Component for particle systems; exposes `mainEmitter` settings |
| `AudioFileResource` | A loaded audio asset that can be played on an entity |
| `entity.playAudio(_:)` | Plays spatial audio attached to an entity |

## Common patterns

**Loading and positioning RC Pro content:**
```swift
RealityView { content in
    if let tree = try? await Entity(named: "OakTree", in: realityKitContentBundle) {
        tree.position = [0.5, 0, -1.5]
        tree.scale = SIMD3(repeating: 0.8)
        content.add(tree)
    }
}
```

**Triggering a named behavior:**
```swift
// "Bloom" is the trigger name set in RC Pro's behavior graph
flowerEntity.components[BehaviorComponent.self]?.triggers["Bloom"]?.fire()
```

**Updating particle emitter at runtime:**
```swift
if var emitter = entity.components[ParticleEmitterComponent.self] {
    emitter.mainEmitter.birthRate = 200
    emitter.mainEmitter.color = .evolving(start: .single(.yellow), end: .single(.red))
    entity.components[ParticleEmitterComponent.self] = emitter
}
```

**Playing spatial audio on an entity:**
```swift
if let audioResource = try? await AudioFileResource(named: "wind.wav",
                                                     in: realityKitContentBundle) {
    entity.playAudio(audioResource)
}
```

**Animating a component property via AnimationResource:**
```swift
// Play a named animation clip authored in RC Pro's timeline
if let anim = entity.availableAnimations.first(where: { $0.name == "FlyIn" }) {
    entity.playAnimation(anim.repeat(count: 1))
}
```

## Gotchas

- `Entity(named:in:)` loads the entity asynchronously — always `await` it in a `Task` or the `RealityView` make closure (which is itself async).
- `findEntity(named:)` searches the entire subtree — use unique names in RC Pro to avoid ambiguity.
- `BehaviorComponent` trigger names are case-sensitive and must match exactly what was authored in RC Pro.
- Changes to `ParticleEmitterComponent` must be written back to `entity.components` after mutation (value-type semantics).
- The generated `realityKitContentBundle` accessor is available only after adding the `.realitycomposerpro` package to your Xcode target's "Copy Bundle Resources" build phase.
