---
framework: visionOS
title: "Explore the USD ecosystem"
session: WWDC23-10086
year: 2023
applies_to: visionOS 1+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/visionos.md
---

# Explore the USD ecosystem (WWDC23)

An overview of Universal Scene Description (USD), the USDZ container format, and the Reality Composer Pro pipeline for authoring spatial assets.

## What changed and why

visionOS doubles down on USD as the standard 3D interchange format. USDZ (a zip-archived USD package) is the recommended delivery format for spatial apps. Reality Composer Pro (new in 2023) is the professional authoring tool for creating, compositing, and behaviorally scripting USDZ assets for use in RealityKit.

## Mental model

- **USD** — A scene description standard developed by Pixar. A USD file (`.usd`, `.usda` text, `.usdc` binary, or `.usdz` zip archive) describes geometry, materials, lights, and animation.
- **USDZ** — A zero-compression zip archive containing a USD stage plus textures and other assets. The recommended format for distributing RealityKit content.
- **Reality Composer Pro** — Xcode-integrated tool for building `.realitykomposer2` project packages that compile to USDZ/Reality archives. Supports particle emitters, physics, audio, behaviors, and ShaderGraph materials.
- **Asset pipeline** — 3D content created in DCC tools (Maya, Blender, Cinema 4D) is exported to USD/USDZ, optionally refined in Reality Composer Pro, then loaded in Swift via `Entity.load(named:in:)` or `Model3D`.
- **Optimization** — Reduce polygon count with LOD, use ASTC-compressed textures, bake lighting where possible. Reality Composer Pro provides a Statistics panel for asset analysis.

## Usage

**Loading a USDZ in SwiftUI (simple, static):**
```swift
Model3D(named: "ArcticFox") { phase in
    switch phase {
    case .success(let model):
        model.resizable().scaledToFit()
    case .failure:
        Image(systemName: "exclamationmark.triangle")
    case .empty:
        ProgressView()
    @unknown default:
        EmptyView()
    }
}
```

**Loading a Reality Composer Pro bundle in RealityKit:**
```swift
// The bundle is generated from a .realitykomposer2 project added to your Xcode project
import RealityKit

// Access the generated bundle accessor
let entity = try await Entity(named: "Scene", in: realityKitContentBundle)
```

**USDZ quick reference — asset requirements:**
- Coordinate system: Y-up, right-handed
- Units: meters (1 unit = 1 meter in visionOS)
- Texture formats: PNG, JPEG, ASTC (.ktx2) for best performance
- Recommended mesh budget: < 100k triangles per entity for interactive content

**Reality Composer Pro pipeline:**
1. Create a new `.realitykomposer2` project in Reality Composer Pro (via Xcode > File > New > Reality Composer Pro Project).
2. Import USDZ assets from DCC tools.
3. Add particle emitters, physics settings, audio components, or ShaderGraph materials in the editor.
4. Add the project to your Xcode target; it generates a Swift bundle accessor (`realityKitContentBundle`).
5. Load named scenes at runtime via `Entity(named:in:)`.

**Previewing USDZ on device:**
- Use Quick Look to preview USDZ files in AR/spatial mode directly from Files or Mail.
- Use `ARQuickLookPreviewItem` (iOS) or the system viewer (visionOS) via `UIActivityViewController` / `ShareLink`.

## Adopting this pattern

1. Export 3D assets from DCC tools as USDZ with Y-up orientation and meter scale.
2. Use Reality Composer Pro for adding behaviors, physics, and materials rather than doing it entirely in code.
3. Use `Model3D` for static display; use `RealityView` + `Entity.load` for interactive or animated content.
4. Compress textures to ASTC for best GPU memory performance on visionOS.
5. Profile asset load time with the RealityKit Trace Instrument and reduce polygon/texture budgets accordingly.
