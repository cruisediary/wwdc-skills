---
framework: RealityKit
title: "Explore materials in Reality Composer Pro"
session: WWDC23-10202
year: 2023
applies_to: visionOS 1+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/visionos.md
---

# Explore materials in Reality Composer Pro (WWDC23)

How to create and use `ShaderGraphMaterial` — node-based custom materials authored in Reality Composer Pro's ShaderGraph editor.

## What changed and why

Previously RealityKit's material options were limited to `SimpleMaterial`, `PhysicallyBasedMaterial`, and `UnlitMaterial`. visionOS and RealityKit 2 introduce `ShaderGraphMaterial` — a programmable material type defined by a node graph in Reality Composer Pro. This allows arbitrary visual effects, animated UVs, custom procedural patterns, and time-varying parameters — without writing Metal shaders by hand.

## Mental model

- **ShaderGraph** is a visual node-based editor inside Reality Composer Pro. Nodes represent math operations, texture samples, geometry attributes, and final surface outputs.
- A ShaderGraph material is compiled into a GPU shader when the RC Pro project is built by Xcode.
- At runtime the material is a `ShaderGraphMaterial` value. You can load it on any entity and mutate its exposed **parameters** (custom uniform inputs defined in the graph) from Swift.
- Parameters appear in the graph as "Promote to Parameter" nodes and can have any scalar, vector, color, or texture type.

## Usage

**Using a ShaderGraph material from RC Pro:**
```swift
import RealityKit

// Load an entity that already has a ShaderGraph material assigned in RC Pro
let entity = try await Entity(named: "GlowingOrb", in: realityKitContentBundle)
content.add(entity)
```

**Reading and modifying a parameter at runtime:**
```swift
// Get the material from the entity's ModelComponent
if var modelComponent = entity.components[ModelComponent.self] {
    // ShaderGraphMaterial is one of the materials in the array
    if var material = modelComponent.materials.first as? ShaderGraphMaterial {
        // Set a parameter named "Color" (as defined in the ShaderGraph)
        try material.setParameter(name: "Color", value: .color(.red))
        modelComponent.materials = [material]
        entity.components[ModelComponent.self] = modelComponent
    }
}
```

**Available parameter value types:**
```swift
// Scalar
try material.setParameter(name: "Intensity", value: .float(2.5))

// Vector
try material.setParameter(name: "Offset", value: .simd2Float([0.1, 0.2]))

// Color
try material.setParameter(name: "TintColor", value: .color(.systemBlue))

// Texture
let textureResource = try await TextureResource(named: "noise", in: realityKitContentBundle)
try material.setParameter(name: "NoiseMap", value: .textureResource(textureResource))
```

**Animating a parameter over time:**
```swift
// Use a RealityView update closure or a Timer/Task to drive parameter changes
var angle: Float = 0
Timer.scheduledTimer(withTimeInterval: 1/60, repeats: true) { _ in
    angle += 0.02
    try? material.setParameter(name: "Phase", value: .float(angle))
    // Re-assign to entity...
}
```

**Building a simple ShaderGraph in RC Pro (workflow summary):**
1. Open RC Pro > select a scene > create a new ShaderGraph material asset.
2. Connect input nodes (UV, time, noise texture) through math nodes to a `PBR Surface` or `Unlit Surface` output node.
3. Right-click any input port > "Promote to Parameter" to expose it as a named Swift-accessible uniform.
4. Assign the material to an entity in the scene.
5. Build in Xcode — the ShaderGraph compiles to Metal.

## Adopting this pattern

1. Use ShaderGraph for visual effects that would require writing a Metal shader on other platforms (animated patterns, custom PBR variations, procedural geometry coloring).
2. Expose only the parameters you need to change at runtime via "Promote to Parameter" — keep the graph clean.
3. Set parameters via `ShaderGraphMaterial.setParameter(name:value:)` and always write the mutated material back to `ModelComponent.materials`.
4. Use the `time` built-in input node in ShaderGraph for smooth, GPU-driven animation without any Swift timing code.
5. Profile material complexity in RC Pro's Statistics panel — complex node graphs increase shader compilation time and GPU cost.
