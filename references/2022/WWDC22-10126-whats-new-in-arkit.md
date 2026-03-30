---
framework: ARKit
title: "What's new in ARKit"
session: WWDC22-10126
year: 2022
applies_to: iOS 16+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/arkit.md
---

# What's new in ARKit — WWDC22

ARKit 6 introduced 4K video capture, improved motion capture, and refinements to plane detection and scene understanding.

## What's new

- **4K video capture** — `ARWorldTrackingConfiguration` can now deliver 4K camera frames on supported devices (iPhone 11 Pro and later, iPad Pro)
- **HDR video** — high dynamic range video capture support
- **Improved motion capture** — `ARBodyTrackingConfiguration` refinements for more accurate body joint tracking
- **Background thread `ARSession`** — sessions can run on a background thread for reduced main-thread load
- **`ARGeoTrackingConfiguration` improvements** — expanded city coverage for GPS-anchored AR
- **Plane classification improvements** — more accurate horizontal and vertical plane detection

## 4K video capture

```swift
import ARKit

let configuration = ARWorldTrackingConfiguration()

// Check for 4K support
if ARWorldTrackingConfiguration.supportsFrameSemantics(.personSegmentationWithDepth) {
    // Device supports advanced features
}

// Configure 4K video format
let videoFormats = ARWorldTrackingConfiguration.supportedVideoFormats
if let format4K = videoFormats.first(where: { $0.imageResolution.width >= 3840 }) {
    configuration.videoFormat = format4K
}

let session = ARSession()
session.run(configuration)
```

## Body tracking (ARBodyTrackingConfiguration)

```swift
let bodyConfig = ARBodyTrackingConfiguration()
session.run(bodyConfig)

// In ARSessionDelegate
func session(_ session: ARSession, didUpdate anchors: [ARAnchor]) {
    for anchor in anchors {
        guard let bodyAnchor = anchor as? ARBodyAnchor else { continue }
        let skeleton = bodyAnchor.skeleton

        // Access joint transforms
        let hipTransform = skeleton.modelTransform(for: .root)
        let leftHandTransform = skeleton.modelTransform(for: .leftHand)
    }
}
```

## ARGeoAnchor (geo tracking)

```swift
let geoConfig = ARGeoTrackingConfiguration()
session.run(geoConfig)

// Place an anchor at a real-world GPS coordinate
let anchor = ARGeoAnchor(
    name: "landmark",
    coordinate: CLLocationCoordinate2D(latitude: 37.7749, longitude: -122.4194)
)
session.add(anchor: anchor)
```

## Migration steps

1. Update `videoFormat` selection logic to prefer 4K formats on capable devices
2. For body tracking apps, test against improved skeleton accuracy on iOS 16
3. Review `ARBodyAnchor.skeleton` joint names — some joint names refined in ARKit 6

## Compatibility notes

- 4K capture requires iPhone 11 Pro or later, iPad Pro (2020 and later); check `supportedVideoFormats`
- `ARBodyTrackingConfiguration` requires an iPhone (not iPad)
- ARKit is superseded by RealityKit + visionOS ARKit for spatial computing — see `canonical/arkit.md`
