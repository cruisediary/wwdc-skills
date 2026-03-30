---
framework: ARKit
title: "What's New in ARKit 2"
session: WWDC18-602
year: 2018
applies_to: iOS 12+
status: deprecated
superseded_by: canonical/arkit.md
shape: migration
related:
  - canonical/arkit.md
---

> **Deprecated:** This session covers ARKit 2 (iOS 12). These APIs remain available but the recommended path for new spatial projects is RealityKit + visionOS. See `canonical/arkit.md` for deprecation context.

## What's new

- **Multi-user AR** — `ARWorldMap` serialization lets multiple devices share the same tracked space via MultipeerConnectivity.
- **Persistent AR** — save/restore `ARWorldMap` across app launches to place content in the same real-world location.
- **Image tracking** — `ARImageTrackingConfiguration` tracks 2D reference images without requiring full world tracking.
- **Object detection** — `ARObjectScanningConfiguration` scans a 3D object; `ARReferenceObject` detects it at runtime.
- **Environment texturing** — `ARWorldTrackingConfiguration.environmentTexturing = .automatic` captures real-world lighting for realistic reflections.
- **AR Quick Look** — display `.usdz` models in AR from Safari / Messages via `QLPreviewController` with no ARKit code.

## Before / After

**ARKit 1 — single device (iOS 11)**

```swift
let config = ARWorldTrackingConfiguration()
sceneView.session.run(config)
```

**ARKit 2 — world map sharing (iOS 12)**

```swift
// Host: capture and send
sceneView.session.getCurrentWorldMap { worldMap, _ in
    guard let worldMap else { return }
    let data = try! NSKeyedArchiver.archivedData(
        withRootObject: worldMap, requiringSecureCoding: true)
    // send `data` to peers via MultipeerConnectivity
}

// Guest: receive and apply
let worldMap = try! NSKeyedUnarchiver.unarchivedObject(
    ofClass: ARWorldMap.self, from: receivedData)!
let config = ARWorldTrackingConfiguration()
config.initialWorldMap = worldMap
sceneView.session.run(config, options: [.resetTracking, .removeExistingAnchors])
```

**Image tracking**

```swift
let config = ARImageTrackingConfiguration()
config.trackingImages = ARReferenceImage.referenceImages(
    inGroupNamed: "AR Resources", bundle: nil)!
config.maximumNumberOfTrackedImages = 4
sceneView.session.run(config)
```

## Migration steps

1. Set deployment target to iOS 12+.
2. Multi-user: implement `getCurrentWorldMap` on host, assign `initialWorldMap` on guests.
3. Persistence: archive `ARWorldMap` to disk on app background; unarchive and assign on next launch.
4. Image tracking: add reference images to an `AR Resources` asset catalog group; switch to `ARImageTrackingConfiguration` or set `detectionImages` on `ARWorldTrackingConfiguration`.
5. AR Quick Look: export assets as `.usdz`; present with `QLPreviewController` — no ARKit code required.

## Compatibility notes

- `ARWorldMap`, `ARImageTrackingConfiguration`, and `ARObjectScanningConfiguration` require iOS 12+.
- Environment texturing with `.automatic` is GPU-intensive — profile on device.
- ARKit 2 APIs are still present in iOS 18 but new projects should target RealityKit.
