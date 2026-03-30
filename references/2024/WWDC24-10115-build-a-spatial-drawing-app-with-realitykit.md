---
framework: RealityKit
title: "Build a spatial drawing app with RealityKit"
session: WWDC24-10115
year: 2024
applies_to: visionOS 2+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/visionos.md
---

# RealityKit — Build a Spatial Drawing App with RealityKit (WWDC24)

Create stroke-based 3D drawing using `LowLevelMesh` for dynamic geometry and `HandAnchor` from ARKit for real-time hand-position input.

## Quick start

```swift
import ARKit
import RealityKit
import SwiftUI

// 1. Track hand joints via ARKit
let session = ARKitSession()
let handTracking = HandTrackingProvider()

try await session.run([handTracking])

// 2. Read index-finger tip position each frame
for await update in handTracking.anchorUpdates {
    let anchor: HandAnchor = update.anchor
    guard anchor.isTracked,
          let indexTip = anchor.handSkeleton?.joint(.indexFingerTip) else { continue }

    // indexTip.anchorFromJointTransform is relative to the hand anchor
    let tipTransform = anchor.originFromAnchorTransform * indexTip.anchorFromJointTransform
    let tipPosition = SIMD3<Float>(tipTransform.columns.3.x,
                                   tipTransform.columns.3.y,
                                   tipTransform.columns.3.z)
    await drawingModel.addPoint(tipPosition)
}

// 3. Build stroke geometry with LowLevelMesh
actor DrawingModel {
    private var points: [SIMD3<Float>] = []
    private var meshEntity: ModelEntity?

    func addPoint(_ point: SIMD3<Float>) async {
        points.append(point)
        await rebuildMesh()
    }

    private func rebuildMesh() async {
        guard points.count >= 2 else { return }
        var descriptor = LowLevelMesh.Descriptor()
        descriptor.vertexAttributes = [
            .init(semantic: .position, format: .float3, offset: 0)
        ]
        descriptor.vertexBufferLayouts = [
            .init(bufferIndex: 0, bufferStride: MemoryLayout<SIMD3<Float>>.stride)
        ]
        descriptor.indexType = .uint32

        // Generate tube vertices around stroke points (simplified)
        let mesh = try? LowLevelMesh(descriptor: descriptor)
        // ... fill vertex and index buffers ...

        let meshResource = try? await MeshResource(from: mesh!)
        await MainActor.run {
            meshEntity?.model?.mesh = meshResource!
        }
    }
}
```

## Key APIs

| API | Purpose |
|---|---|
| `ARKitSession` | Manages ARKit data provider lifecycle |
| `HandTrackingProvider` | Streams `HandAnchor` updates for left/right hands |
| `HandAnchor` | Represents one hand; contains skeleton joint transforms |
| `HandSkeleton.joint(_:)` | Returns a `HandSkeleton.Joint` for a named joint (e.g. `.indexFingerTip`) |
| `HandSkeleton.Joint.anchorFromJointTransform` | 4×4 float matrix: joint pose relative to hand anchor origin |
| `HandAnchor.originFromAnchorTransform` | Hand anchor pose in world (ARKit origin) space |
| `LowLevelMesh` | Low-level GPU buffer abstraction for custom dynamic geometry |
| `LowLevelMesh.Descriptor` | Describes vertex layout, attributes, and index type |
| `MeshResource(from:)` | Wraps a `LowLevelMesh` into a RealityKit-renderable resource |
| `ModelComponent` | Attaches a `MeshResource` + `[Material]` to an entity |

## Common patterns

**Pinch-to-draw gesture (index + thumb proximity):**
```swift
func isPinching(_ anchor: HandAnchor) -> Bool {
    guard let index = anchor.handSkeleton?.joint(.indexFingerTip),
          let thumb = anchor.handSkeleton?.joint(.thumbTip) else { return false }
    let i = (anchor.originFromAnchorTransform * index.anchorFromJointTransform).columns.3
    let t = (anchor.originFromAnchorTransform * thumb.anchorFromJointTransform).columns.3
    let dist = simd_distance(SIMD3(i.x, i.y, i.z), SIMD3(t.x, t.y, t.z))
    return dist < 0.02  // 2 cm threshold
}
```

**Updating a `LowLevelMesh` in-place (avoid full reallocation every frame):**
```swift
// Pre-allocate with a maximum vertex count
var descriptor = LowLevelMesh.Descriptor()
// ... set attributes ...
descriptor.vertexCapacity = 10_000
descriptor.indexCapacity = 30_000
let mesh = try LowLevelMesh(descriptor: descriptor)

// Each frame: write into the existing buffers
mesh.withUnsafeMutableBytes(bufferIndex: 0) { rawBuffer in
    // overwrite vertex data in place
}
mesh.parts.replaceAll([
    LowLevelMesh.Part(indexCount: currentIndexCount,
                      topology: .triangleStrip,
                      bounds: currentBounds)
])
```

**Placing drawing content in an `ImmersiveSpace`:**
```swift
ImmersiveSpace(id: "drawing") {
    RealityView { content, _ in
        let root = Entity()
        root.name = "strokeRoot"
        content.add(root)
    }
}
.immersionStyle(selection: $style, in: .mixed)
```

## Gotchas

- `HandTrackingProvider` requires the `com.apple.developer.arkit.hand-tracking` entitlement — add it in Xcode's Signing & Capabilities or the session will fail silently
- `HandAnchor.handSkeleton` returns `nil` when the hand is not fully tracked; always guard before accessing joints
- `LowLevelMesh` buffers are GPU-resident — writes must happen on the render thread or via the provided `withUnsafeMutableBytes` API; do not cache raw pointers across frames
- `MeshResource(from:)` is `async` — call it from a `Task` and marshal the result to `@MainActor` before assigning to a `ModelComponent`
- ARKit world coordinates and RealityKit world coordinates share the same origin on visionOS — no coordinate-space conversion is needed when positioning entities at ARKit anchor positions
- Stroke rendering at 90 fps requires `LowLevelMesh` in-place updates; rebuilding a `MeshResource` from scratch each frame will cause frame drops
