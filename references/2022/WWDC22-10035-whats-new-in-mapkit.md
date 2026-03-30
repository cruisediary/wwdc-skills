---
framework: MapKit
title: "What's new in MapKit"
session: WWDC22-10035
year: 2022
applies_to: iOS 16+
status: reference-only
superseded_by: null
shape: migration
related: []
---

# What's new in MapKit — WWDC22

iOS 16 introduced Look Around (street-level imagery), new map configurations, and improved MapKit APIs for hybrid and satellite views.

## What's new

- **Look Around** — street-level imagery, similar to Google Street View
  - `MKLookAroundSceneRequest` — fetch a Look Around scene for a coordinate
  - `MKLookAroundViewController` — UIKit view controller to display Look Around
  - `MKLookAroundSnapshotter` — generate a static image of a Look Around scene
- **Map configurations** — `MKMapConfiguration` subclasses replace `MKMapType` enum
  - `MKStandardMapConfiguration` — standard road map
  - `MKHybridMapConfiguration` — satellite imagery with road overlay
  - `MKImageryMapConfiguration` — pure satellite/aerial imagery
- **`MKMapView.preferredConfiguration`** — replaces `mapType` property

## Key code examples

### Look Around

```swift
import MapKit

// Request a Look Around scene
let coordinate = CLLocationCoordinate2D(latitude: 37.3318, longitude: -122.0312)
let request = MKLookAroundSceneRequest(coordinate: coordinate)

do {
    let scene = try await request.scene
    if let scene {
        let lookAroundVC = MKLookAroundViewController(scene: scene)
        present(lookAroundVC, animated: true)
    } else {
        // Look Around not available at this location
    }
} catch {
    print("Look Around unavailable: \(error)")
}
```

### Look Around snapshot

```swift
let snapshotter = MKLookAroundSnapshotter(scene: scene, options: .init())
let snapshot = try await snapshotter.snapshot
let image = snapshot.image   // UIImage
```

### Map configuration

```swift
let mapView = MKMapView()

// Standard map
mapView.preferredConfiguration = MKStandardMapConfiguration()

// Hybrid (satellite + roads) — replaces .hybrid mapType
let hybridConfig = MKHybridMapConfiguration()
hybridConfig.elevationStyle = .realistic   // 3D terrain
mapView.preferredConfiguration = hybridConfig

// Imagery only
mapView.preferredConfiguration = MKImageryMapConfiguration()
```

## Migration steps

1. Replace `mapView.mapType = .standard` with `mapView.preferredConfiguration = MKStandardMapConfiguration()`
2. Replace `.hybrid` with `MKHybridMapConfiguration()`
3. Replace `.satellite` with `MKImageryMapConfiguration()`
4. Add Look Around preview buttons to location detail screens where coverage is available

## Compatibility notes

- `MKLookAroundSceneRequest` and map configurations require iOS 16+ / macOS 13+
- `mapType` property still works on iOS 16 but is deprecated
- Look Around coverage is limited to supported cities/regions; always handle nil scene
