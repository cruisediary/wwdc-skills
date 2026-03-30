---
framework: ARKit
title: "Evolve your ARKit app for spatial experiences"
session: WWDC23-10091
year: 2023
applies_to: visionOS 1+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/arkit.md
  - canonical/visionos.md
---

# Evolve your ARKit app for spatial experiences (WWDC23)

How to migrate an iOS ARKit app to visionOS, covering the shift from `ARSession` to `ARKitSession`, anchor differences, and RealityKit rendering changes.

## What's new

- `ARKitSession` replaces `ARSession` on visionOS — new async/await API, no delegate pattern
- `WorldTrackingProvider` replaces `ARWorldTrackingConfiguration`
- `PlaneDetectionProvider` replaces `ARPlaneDetectionConfiguration`
- `HandTrackingProvider` is new (no equivalent on iOS ARKit)
- `AnchorUpdate<T>` async sequence replaces `ARSessionDelegate` callbacks
- No `ARFrame` / `ARCamera` access on visionOS — use `WorldTrackingProvider.queryDeviceAnchor`
- `WorldAnchor` replaces `ARAnchor` for placing persistent content in the world
- RealityKit rendering: no `ARSCNView` or `ARView` (iOS) — use `RealityView` (visionOS)

## Before / After

**Session setup:**
```swift
// iOS (before)
let session = ARSession()
let config = ARWorldTrackingConfiguration()
config.planeDetection = [.horizontal, .vertical]
session.delegate = self
session.run(config)

// visionOS (after)
let session = ARKitSession()
let worldTracking = WorldTrackingProvider()
let planeDetection = PlaneDetectionProvider(alignments: [.horizontal, .vertical])
try await session.run([worldTracking, planeDetection])
```

**Handling anchor updates:**
```swift
// iOS (before) — ARSessionDelegate
func session(_ session: ARSession, didAdd anchors: [ARAnchor]) {
    for anchor in anchors {
        if let plane = anchor as? ARPlaneAnchor { handlePlane(plane) }
    }
}

// visionOS (after) — AsyncSequence
Task {
    for await update in planeDetection.anchorUpdates {
        switch update.event {
        case .added, .updated: handlePlane(update.anchor)
        case .removed: removePlane(update.anchor)
        }
    }
}
```

**Getting device pose:**
```swift
// iOS (before) — from ARFrame
let transform = session.currentFrame?.camera.transform

// visionOS (after) — from WorldTrackingProvider
let deviceAnchor = worldTracking.queryDeviceAnchor(atTimestamp: CACurrentMediaTime())
let transform = deviceAnchor?.originFromAnchorTransform
```

**Placing a world anchor:**
```swift
// iOS (before)
let anchor = ARAnchor(transform: transform)
session.add(anchor: anchor)

// visionOS (after)
let worldAnchor = WorldAnchor(originFromAnchorTransform: transform)
try await worldTracking.addAnchor(worldAnchor)
```

**Rendering view:**
```swift
// iOS (before)
let arView = ARView(frame: .zero)
// add AnchorEntity to arView.scene

// visionOS (after) — SwiftUI + RealityView
RealityView { content in
    // add Entity to content
}
```

## Migration steps

1. Remove `ARSession`, `ARConfiguration` subclasses, and `ARSessionDelegate`.
2. Create `ARKitSession` and add `WorldTrackingProvider` (+ other providers as needed).
3. Call `session.run([...])` with `try await` — handle authorization errors.
4. Replace `ARSessionDelegate` callbacks with `for await` loops over `provider.anchorUpdates`.
5. Replace `ARView` with a SwiftUI `RealityView`; replace `AnchorEntity` attachment pattern with direct `content.add(entity)` and entity position tracking via anchor transforms.
6. Replace `ARAnchor` with `WorldAnchor` for persistent placed content.

## Compatibility notes

- visionOS ARKit and iOS ARKit share the `ARKit` framework name but have largely separate APIs — most iOS `AR*` types are unavailable on visionOS.
- `HandTrackingProvider` and `SceneReconstructionProvider` have no iOS equivalent.
- Authorization on visionOS requires entries in `Info.plist` (`NSWorldSensingUsageDescription`, `NSHandsTrackingUsageDescription`).
- iOS ARKit apps compiled for visionOS will need significant refactoring — there is no thin compatibility shim.
