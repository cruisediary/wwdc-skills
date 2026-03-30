---
framework: RealityKit
title: "What's new in RealityKit"
session: WWDC24-10103
year: 2024
applies_to: visionOS 2+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/visionos.md
---

# RealityKit — What's New in RealityKit (WWDC24)

RealityKit gains `PhysicsSimulationComponent`, expanded `MeshResource` APIs, an updated `InputTargetComponent`, and `PortalComponent` for rendering scenes within bounded regions.

## What's new

- **`PhysicsSimulationComponent`** — attaches a physics simulation context to an entity subtree, allowing isolated physics worlds within a scene; entities in a subtree share one physics simulation
- **`MeshResource` generation APIs** — new static factories (`MeshResource.generateBox`, `MeshResource.generateSphere`, `MeshResource.generatePlane`) for synchronous mesh creation
- **`InputTargetComponent` updates** — allows finer-grained input shapes via `InputTargetComponent(allowedInputTypes:)`, supporting `.indirect` (pinch), `.direct` (hand touch), and `.all`
- **`PortalComponent`** — renders a child entity subtree through a portal surface; portal masks geometry so only what's "inside" the portal plane is visible from the outside
- **`RealityView` improvements** — `make` and `update` closures receive an `RealityViewContent` with new `add(_:)`, `remove(_:)`, and `entities` accessors for managing entity lifetimes more precisely
- **`TextureResource` async loading** — `TextureResource.generate(from:options:)` and async variants reduce hitches when loading large textures at runtime

## Before / After

**Before (visionOS 1 physics — single global simulation):**
```swift
// All entities shared one implicit physics world
let box = ModelEntity(mesh: .generateBox(size: 0.1))
box.components.set(PhysicsBodyComponent(massProperties: .default,
                                         material: .default,
                                         mode: .dynamic))
```

**After (visionOS 2 isolated `PhysicsSimulationComponent`):**
```swift
// Create an isolated simulation for an entity subtree
let simulationRoot = Entity()
simulationRoot.components.set(PhysicsSimulationComponent())

let box = ModelEntity(mesh: .generateBox(size: 0.1))
box.components.set(PhysicsBodyComponent(massProperties: .default,
                                         material: .default,
                                         mode: .dynamic))
simulationRoot.addChild(box)
```

**Mesh generation (synchronous factory):**
```swift
let mesh = MeshResource.generateBox(size: 0.2)
```

**Mesh generation from a custom descriptor:**
```swift
var descriptor = MeshDescriptor()
// ... fill descriptor ...
let mesh = try MeshResource.generate(from: descriptor)
```

**Before (InputTargetComponent — accepts all input):**
```swift
entity.components.set(InputTargetComponent())
```

**After (restrict to indirect pinch only):**
```swift
entity.components.set(InputTargetComponent(allowedInputTypes: .indirect))
```

## Migration steps

1. Wrap entity subtrees that need independent physics into a parent with `PhysicsSimulationComponent()` — this prevents cross-scene physics interference
2. Use `MeshResource.generateBox`, `generateSphere`, or `MeshResource.generate(from:)` for mesh creation; wrap in a background `Task` if needed to avoid blocking the main thread
3. Audit `InputTargetComponent` usages — explicitly set `allowedInputTypes` to `.indirect`, `.direct`, or `.all` rather than relying on the default
4. Adopt `PortalComponent` for contained-scene effects (e.g., a window into a miniature world) instead of camera layer tricks
5. Update `RealityView` `make` closures to use the new `content.add(_:)` / `content.remove(_:)` APIs for safer entity lifecycle management

## Compatibility notes

- `PhysicsSimulationComponent` and `PortalComponent` require visionOS 2+ / iOS 18+
- `MeshResource.generate(from:)` and the synchronous factory methods (`generateBox`, `generateSphere`, `generatePlane`) are available across visionOS and iOS; wrap in a background `Task` to avoid blocking the main thread when building large meshes
- `InputTargetComponent(allowedInputTypes:)` initializer is new in visionOS 2; the zero-argument initializer remains available on visionOS 1
- `RealityView` `update` closure improvements are source-compatible; no API removal in visionOS 1 builds
