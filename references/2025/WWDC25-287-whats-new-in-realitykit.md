---
framework: RealityKit
title: "What's new in RealityKit"
session: WWDC25-287
year: 2025
applies_to: visionOS 26+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/visionos.md
  - 2024/WWDC24-10103-whats-new-in-realitykit.md
---

# RealityKit — What's New in RealityKit (WWDC25)

WWDC25 builds on RealityKit's component-entity architecture with improved physics simulation, new material capabilities, and enhanced spatial audio integration for visionOS 26.

## What's new

- **Physics refinements** — improvements to `PhysicsSimulationComponent` and collision detection; more accurate rigid-body stacking and joint constraints (see Apple docs for specific API additions)
- **Material updates** — new `ShaderGraphMaterial` node types and updated `PhysicallyBasedMaterial` properties for finer control over surface appearance
- **Spatial audio improvements** — enhanced `SpatialAudioComponent` with room modeling and improved reverb simulation
- **Entity querying** — additional query APIs for filtering entities by component type at runtime (see Apple docs)
- **RealityView attachment updates** — improved attachment anchoring and layout within `RealityView` for visionOS 26 window styles

## Before / After

**Before (visionOS 2 — basic physics body setup):**
```swift
var entity = ModelEntity(mesh: .generateBox(size: 0.1))
entity.components.set(PhysicsBodyComponent(
    massProperties: .default,
    material: .default,
    mode: .dynamic
))
entity.components.set(CollisionComponent(shapes: [.generateBox(size: [0.1, 0.1, 0.1])]))
```

**After (visionOS 26 — physics API may have additional configuration; see Apple docs):**
```swift
// Existing code continues to compile; new API surface adds joint constraints
// and more granular collision filtering — refer to Xcode 26 RealityKit docs
var entity = ModelEntity(mesh: .generateBox(size: 0.1))
entity.components.set(PhysicsBodyComponent(
    massProperties: .default,
    material: .default,
    mode: .dynamic
))
entity.components.set(CollisionComponent(shapes: [.generateBox(size: [0.1, 0.1, 0.1])]))
// New in visionOS 26: joint and constraint APIs — see Apple docs
```

## Migration steps

1. Update `PhysicsSimulationComponent` usages if deprecated initializers are flagged by Xcode 26
2. Review `ShaderGraphMaterial` node graphs in Reality Composer Pro for new node types available in visionOS 26
3. Test spatial audio in the visionOS 26 simulator — `SpatialAudioComponent` behavior may differ with enhanced reverb modeling
4. Verify `RealityView` attachments render correctly in updated window styles (volumetric, immersive)

## Compatibility notes

- New WWDC25 RealityKit APIs target visionOS 26+; existing visionOS 2 code continues to compile
- `ShaderGraphMaterial` additions require Reality Composer Pro updated for Xcode 26
- Exact new component and property names should be verified against Xcode 26 RealityKit headers
