---
framework: RealityKit
title: "Optimize your 3D assets for spatial computing"
session: WWDC24-10186
year: 2024
applies_to: visionOS 2+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/visionos.md
---

# RealityKit — Optimize Your 3D Assets for Spatial Computing (WWDC24)

A practical guide to preparing USDZ assets for visionOS: LOD strategies, texture compression, and Reality Composer Pro workflows that reduce load times and GPU cost.

## What changed and why

Spatial computing places 3D content directly in the user's environment, often rendering multiple models simultaneously in a shared AR compositor. Unlike a traditional game with a single camera and a managed LOD pipeline, visionOS:

- Renders at high resolution for both eyes simultaneously
- Has strict compositor frame budgets (frame drops are very noticeable in AR)
- Must load assets quickly to avoid visible pop-in when users move between spaces

WWDC24 guidance formalises best practices that were implicit in visionOS 1 and adds new Reality Composer Pro tooling to enforce them at asset-creation time.

## Mental model

Think of asset optimization as a pipeline with three checkpoints:

1. **Geometry budget** — polygon count and draw calls per frame; use LODs and mesh merging to stay within limits
2. **Texture budget** — VRAM footprint; use KTX2 with ASTC compression and mip maps
3. **Load-time budget** — time from asset request to first render; smaller files and async loading prevent hitches

Reality Composer Pro acts as a linter and transformer for USDZ files, letting you bake LODs, compress textures, and validate budgets before shipping.

## Usage

**Exporting an optimized USDZ from Reality Composer Pro:**

1. Open the `.usda` or `.usdz` source in Reality Composer Pro
2. In the Statistics panel, inspect polygon count per mesh and texture memory per material
3. Add a `LevelOfDetail` component to any mesh with >50 k triangles — set transition distances appropriate to your scene scale
4. Select all textures → apply **ASTC 6×6** compression for color maps; **ASTC 8×8** for roughness/metallic masks
5. Run **Build** → Reality Composer Pro generates an optimized `.reality` bundle

**Loading assets asynchronously at runtime:**
```swift
import RealityKit

// Prefer async loading to avoid blocking the main thread
Task {
    let model = try await Entity(named: "Robot", in: .main)
    await MainActor.run {
        content.add(model)
    }
}
```

**Choosing the right texture format:**

| Use case | Recommended format | Notes |
|---|---|---|
| Diffuse / albedo | ASTC 6×6 | Good quality, ~2 bpp |
| Normal map | ASTC 4×4 | Higher precision needed |
| Roughness / metallic | ASTC 8×8 | Perceptual quality acceptable |
| Transparency mask | ASTC 6×6 with alpha | Avoid uncompressed RGBA |

**LOD distance guidelines for visionOS:**

| LOD tier | Approx. distance | Target polygon reduction |
|---|---|---|
| LOD 0 (full) | < 1 m | 100% (original) |
| LOD 1 | 1–3 m | 50% |
| LOD 2 | > 3 m | 10–20% |

## Adopting this pattern

If your visionOS 1 app shipped assets without LODs or uncompressed textures:

1. Audit current assets with the **Reality Composer Pro Statistics panel** — note any textures >4 MB or meshes >100 k triangles
2. Re-export source geometry from your DCC tool (Blender, Maya) with explicit LOD meshes at 50% and 15% reduction
3. Import into Reality Composer Pro; apply `LevelOfDetail` component with measured transition distances from user testing
4. Replace all `.png` / `.exr` textures with ASTC-compressed KTX2 textures; Reality Composer Pro's Build step handles this automatically for `.reality` bundles
5. Switch runtime loading from synchronous `Entity(named:)` to `async` variants; guard with `#available(visionOS 2, *)` if needed
6. Profile with the **RealityKit Debugger** in Xcode 16 to verify draw call counts and frame time before shipping
