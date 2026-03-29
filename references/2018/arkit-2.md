---
framework: ARKit
session: WWDC18-602
year: 2018
applies_to: iOS 12+
status: deprecated
superseded_by: canonical/arkit.md
shape: migration
related:
  - canonical/arkit.md
---

## What's new

- **Multi-user AR sessions** — share an ARWorldMap between devices so multiple users see the same virtual content in the same physical space.
- **ARImageTrackingConfiguration** — track 2D images in the environment without world tracking; useful for museum-style or poster AR.
- **Object scanning and detection** — `ARObjectScanningConfiguration` captures a 3D object; `ARReferenceObject` enables detection at runtime.
- **Environment texturing** — `ARWorldTrackingConfiguration.environmentTexturing` captures the real environment and applies it to SceneKit materials for realistic reflections.
- **AR Quick Look** — display `.usdz` 3D models in AR directly from Safari, Messages, or your app via `QLPreviewController` with no ARKit code required.
- **Save and restore world maps** — serialize an `ARWorldMap` to persist anchors and re-localize in the same space across app launches.

## Before / After

**ARKit 1 — single-user session (iOS 11)**

```swift
// One device, no sharing
let configuration = ARWorldTrackingConfiguration()
sceneView.session.run(configuration)
```

**ARKit 2 — multi-user session with world map sharing (iOS 12)**

```swift
// Host: capture and send the world map
sceneView.session.getCurrentWorldMap { worldMap, error in
    guard let worldMap else { return }
    // Encode and send worldMap to peer via MultipeerConnectivity
    let data = try! NSKeyedArchiver.archivedData(
        withRootObject: worldMap, requiringSecureCoding: true)
    session.send(data, toPeers: session.connectedPeers, with: .reliable)
}

// Guest: receive and apply
let worldMap = try! NSKeyedUnarchiver.unarchivedObject(
    ofClass: ARWorldMap.self, from: receivedData)!
let configuration = ARWorldTrackingConfiguration()
configuration.initialWorldMap = worldMap
sceneView.session.run(configuration, options: [.resetTracking, .removeExistingAnchors])
```

**Image tracking (new in ARKit 2)**

```swift
let configuration = ARImageTrackingConfiguration()
let referenceImages = ARReferenceImage.referenceImages(
    inGroupNamed: "AR Resources", bundle: nil)!
configuration.trackingImages = referenceImages
configuration.maximumNumberOfTrackedImages = 4
sceneView.session.run(configuration)
```

## Migration steps

1. Update deployment target to iOS 12+.
2. To add multi-user support: implement `getCurrentWorldMap` on the host and `initialWorldMap` assignment on guests; use MultipeerConnectivity or any transport layer.
3. To persist anchors across launches: archive the `ARWorldMap` to disk on `viewWillDisappear` and unarchive on next launch.
4. To add image tracking: add reference images to an `AR Resources` asset catalog group and switch to `ARImageTrackingConfiguration` (or set `detectionImages` on `ARWorldTrackingConfiguration` to keep world tracking).
5. For AR Quick Look: export assets as `.usdz` and present via `QLPreviewController` — no additional ARKit code needed.

## Compatibility notes

- Multi-user world map sharing requires iOS 12+; `ARImageTrackingConfiguration` requires iOS 12+.
- Environment texturing with `automatic` mode is GPU-intensive — test on device.
- Object scanning must be done in a separate app phase using `ARObjectScanningConfiguration`; it cannot run alongside world tracking.
- ARKit 2 APIs are still present in iOS 18, but the recommended modern path for new projects is RealityKit. See `canonical/arkit.md` for the deprecation context.
