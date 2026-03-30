---
framework: MapKit
title: "What's new in MapKit"
session: WWDC24-10109
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: migration
related: []
---

## What's new

- `MapCircle` and `MapPolygon` — SwiftUI overlay types for drawing shapes directly on a `Map`
- `LookAround` improvements — smoother scene loading and new initializer options
- `MapFeature` selection — tap on map POIs and get typed `MapFeature` values in a selection binding
- `Map` initializer with `scope` — coordinates map camera between multiple `Map` views or a `Map` and a `MapCompass`/`MapUserLocationButton`

## Before / After

```swift
// BEFORE (iOS 17): adding overlays required MKMapViewRepresentable and delegate code
// No native SwiftUI overlay shapes

// AFTER (iOS 17+, polished in iOS 18): native SwiftUI map overlays
import MapKit
import SwiftUI

struct RegionMap: View {
    let center = CLLocationCoordinate2D(latitude: 37.7749, longitude: -122.4194)

    var body: some View {
        Map {
            MapCircle(center: center, radius: 500)
                .foregroundStyle(.blue.opacity(0.2))
                .stroke(.blue, lineWidth: 2)

            MapPolygon(coordinates: [
                CLLocationCoordinate2D(latitude: 37.780, longitude: -122.415),
                CLLocationCoordinate2D(latitude: 37.775, longitude: -122.410),
                CLLocationCoordinate2D(latitude: 37.770, longitude: -122.420),
            ])
            .foregroundStyle(.red.opacity(0.15))
        }
    }
}
```

```swift
// MapFeature selection — user taps a POI, you get a typed selection
import MapKit
import SwiftUI

struct FeatureSelectingMap: View {
    @State private var selectedFeature: MapFeature?

    var body: some View {
        Map(selection: $selectedFeature) {
            // map content
        }
        .onChange(of: selectedFeature) { _, feature in
            if let feature {
                print("Selected: \(feature.title ?? "unknown")")
            }
        }
    }
}
```

```swift
// Map scope — sync compass and user location button to a specific Map
import MapKit
import SwiftUI

@Namespace var mapScope

var body: some View {
    Map(scope: mapScope) {
        // map content
    }
    .overlay(alignment: .topTrailing) {
        VStack {
            MapCompass(scope: mapScope)
            MapUserLocationButton(scope: mapScope)
        }
        .padding()
    }
    .mapScope(mapScope)
}
```

## Migration steps

1. Replace `MKCircle`/`MKPolygon` overlay delegates in `MKMapViewRepresentable` with native `MapCircle`/`MapPolygon` in SwiftUI `Map` content builders.
2. Migrate POI tap handling (previously done via `mapView(_:didSelect:)` delegate) to a `Map(selection:)` binding returning `MapFeature`.
3. If you display multiple map controls outside the map, adopt `@Namespace` + `mapScope(_:)` to coordinate them.
4. For LookAround: update to new `LookAroundPreview` initializers if you use the SwiftUI component — see Apple docs for any parameter changes.

## Compatibility notes

- `MapCircle`, `MapPolygon`, and `MapFeature` selection were introduced in iOS 17 — iOS 18 refines them; verify exact availability per API.
- The `scope` parameter on `Map` initializer is iOS 17+.
- `LookAround` (SwiftUI `LookAroundPreview`) is available on iOS 16+.
- All MapKit SwiftUI APIs require `import MapKit`; UIKit `MKMapView` equivalents remain available for deployment targets below iOS 17.
