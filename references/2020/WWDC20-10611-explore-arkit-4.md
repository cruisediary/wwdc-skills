---
framework: ARKit
title: "Explore ARKit 4"
session: WWDC20-10611
year: 2020
applies_to: iOS 14+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/arkit.md
---

# Explore ARKit 4

ARKit 4 introduced depth data from the LiDAR scanner, Location Anchors for geo-referenced AR, and scene geometry improvements.

## Quick start

```swift
import ARKit
import RealityKit

// Location Anchor — place AR content at a real-world GPS coordinate
let coordinate = CLLocationCoordinate2D(latitude: 37.3318, longitude: -122.0312)
let geoAnchor = ARGeoAnchor(name: "ApplePark", coordinate: coordinate)

let config = ARGeoTrackingConfiguration()
arView.session.run(config)
arView.session.add(anchor: geoAnchor)
```

## Key APIs

| API | Description |
|---|---|
| `ARGeoAnchor` | Anchor placed at a GPS coordinate + optional altitude |
| `ARGeoTrackingConfiguration` | Session configuration enabling Location Anchors |
| `ARGeoTrackingStatus` | Tracks accuracy: `.notAvailable`, `.initializing`, `.localizing`, `.tracking` |
| `ARDepthData` | Per-frame depth map captured by the LiDAR scanner |
| `ARFrame.sceneDepth` | `ARDepthData?` available on LiDAR-equipped devices |
| `ARFrame.smoothedSceneDepth` | Temporally smoothed `ARDepthData?` |
| `ARMeshAnchor` | Scene geometry mesh from LiDAR scene reconstruction |
| `ARMeshGeometry` | Vertex, face, and classification buffers for a mesh anchor |
| `ARMeshClassification` | Semantic labels: `.wall`, `.floor`, `.ceiling`, `.table`, `.seat`, `.door`, `.window` |
| `ARBodyAnchor` | 2D/3D body tracking anchor (improvements in ARKit 4) |
| `ARBodyTrackingConfiguration` | Enables body tracking |

## Common patterns

**Reading depth data from LiDAR:**
```swift
func session(_ session: ARSession, didUpdate frame: ARFrame) {
    guard let depthData = frame.sceneDepth else { return }
    let depthMap: CVPixelBuffer = depthData.depthMap
    let confidenceMap: CVPixelBuffer? = depthData.confidenceMap
    // Process depth map — e.g., closest point distance
}
```

**Checking Location Anchor availability:**
```swift
ARGeoTrackingConfiguration.checkAvailability(at: coordinate) { available, error in
    if available {
        let config = ARGeoTrackingConfiguration()
        arView.session.run(config)
    }
}
```

**Handling scene geometry mesh anchors:**
```swift
func session(_ session: ARSession, didAdd anchors: [ARAnchor]) {
    for anchor in anchors.compactMap({ $0 as? ARMeshAnchor }) {
        let geometry = anchor.geometry
        // geometry.vertices, geometry.faces, geometry.classification
    }
}
```

**Enabling scene reconstruction:**
```swift
let config = ARWorldTrackingConfiguration()
if ARWorldTrackingConfiguration.supportsSceneReconstruction(.meshWithClassification) {
    config.sceneReconstruction = .meshWithClassification
}
arView.session.run(config)
```

## Gotchas

- `ARGeoTrackingConfiguration` requires internet connectivity for localization data; `ARGeoTrackingStatus` tracks readiness
- Location Anchors are only available in supported cities — check `ARGeoTrackingConfiguration.isSupported` and `checkAvailability(at:completion:)`
- `ARFrame.sceneDepth` is only available on LiDAR-equipped devices (iPhone 12 Pro and later, iPad Pro 2020 and later)
- `ARDepthData.confidenceMap` provides per-pixel confidence (`ARConfidenceLevel`) — use it to filter low-confidence depth samples
- Scene geometry mesh anchors require `sceneReconstruction` to be set on the configuration
- `ARMeshClassification` accuracy is scene-dependent; always check `.none` classification as a fallback
- ARKit 4 canonical reference (`canonical/arkit.md`) notes ARKit is superseded by RealityKit + visionOS for spatial computing
