---
framework: RealityKit
title: "Work with Reality Composer Pro"
session: WWDC23-10083
year: 2023
applies_to: visionOS 1+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/visionos.md
---

# Work with Reality Composer Pro (WWDC23)

Reality Composer Pro is the visionOS authoring tool integrated with Xcode for building USDZ-based spatial scenes with particle emitters, physics, audio, and behavioral triggers.

## What changed and why

Reality Composer (iOS app) is replaced by **Reality Composer Pro** — a macOS app bundled with Xcode 15. It introduces a professional scene editor, a timeline system, and a node-based ShaderGraph material editor. Projects are stored as `.realitycomposerpro` packages versioned alongside your Xcode project.

## Mental model

- **Project structure** — A `.realitycomposerpro` package contains one or more USD scenes plus imported assets (USDZ, audio, textures). The package is added as an Xcode target and generates a Swift bundle accessor (`realityKitContentBundle`).
- **Scene hierarchy** — Every scene is a USD stage. You compose entities (prims) in a tree, add components (physics, audio, particle emitters), and layer materials.
- **Behaviors** — Visual trigger/action pairs that respond to events (scene load, tap, collision) without writing code. Useful for simple one-shot animations or sounds.
- **Timeline editor** — Sequence property animations on a keyframe timeline for cinematic or tutorial sequences.
- **Particle emitters** — Drag-and-drop emitters for fire, sparks, smoke, confetti, etc. Exposed as `ParticleEmitterComponent` at runtime.
- **ShaderGraph** — Node-based material editor for custom USDZ materials compiled to GPU shaders. See WWDC23-10202.

## Usage

**Setting up a Reality Composer Pro project:**
1. In Xcode: File > New > Reality Composer Pro Project.
2. Add the generated `.realitycomposerpro` package to your app target.
3. The build system generates a `realityKitContentBundle` accessor.

**Loading a scene at runtime:**
```swift
import RealityKit

// Load a scene named "GardenScene" from the RC Pro bundle
let garden = try await Entity(named: "GardenScene", in: realityKitContentBundle)
content.add(garden)
```

**Accessing a specific entity by name:**
```swift
let tree = garden.findEntity(named: "OakTree")
tree?.position.y += 0.1
```

**Using behaviors (trigger/action defined in RC Pro):**

Behaviors authored in Reality Composer Pro fire automatically when a scene loads — no Swift code required for simple tap-to-animate flows. For programmatic behavior triggering, consult the RealityKit `BehaviorComponent` documentation in the current SDK, as the exact API surface varies by RealityKit version.

**Accessing a particle emitter component:**
```swift
if var emitter = entity.components[ParticleEmitterComponent.self] {
    emitter.mainEmitter.birthRate = 500
    entity.components[ParticleEmitterComponent.self] = emitter
}
```

**Scene statistics — performance checklist:**
- Open Statistics panel (View > Statistics) in RC Pro to inspect polygon count and texture memory per entity.
- Target < 100k triangles for interactive objects.
- Use `.ktx2` (ASTC) textures to reduce GPU memory by ~75% versus uncompressed.

## Adopting this pattern

1. Add a `.realitycomposerpro` project alongside your Xcode project and add it as a package dependency to your app target.
2. Author scene composition, particle effects, and simple behaviors in RC Pro rather than in Swift code — keep code for logic, use RC Pro for visual content.
3. Load scenes with `Entity(named:in:)` referencing `realityKitContentBundle`.
4. Use `findEntity(named:)` to retrieve specific sub-entities for runtime manipulation.
5. Profile asset performance in RC Pro's Statistics panel before shipping.
