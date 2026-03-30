---
framework: MapKit
title: "Meet MapKit for SwiftUI"
session: WWDC23-10043
year: 2023
applies_to: iOS 17+
status: reference-only
superseded_by: null
shape: code-first
related: []
---

# Meet MapKit for SwiftUI (WWDC23)

iOS 17 introduces a redesigned SwiftUI `Map` view with a content builder, `Marker`, `Annotation`, `MapCircle`, `MapPolyline`, camera control, and search integration.

## Quick start

```swift
import SwiftUI
import MapKit

struct PlacesMap: View {
    let places: [Place]

    var body: some View {
        Map {
            ForEach(places) { place in
                Marker(place.name, coordinate: place.coordinate)
            }
        }
    }
}
```

## Key APIs

| API | Purpose |
|---|---|
| `Map { }` | SwiftUI Map view with a content builder closure |
| `Marker(_:coordinate:)` | Standard balloon pin annotation |
| `Annotation(_:coordinate:content:)` | Custom SwiftUI view annotation |
| `MapCircle(center:radius:)` | Circle overlay drawn on the map |
| `MapPolyline(coordinates:)` | Polyline overlay (route path) |
| `MapPolygon(coordinates:)` | Polygon overlay |
| `MapCameraPosition` | Represents a camera state (region, item, rect, userLocation) |
| `.mapStyle(_:)` | Switches between `.standard`, `.imagery`, `.hybrid` |
| `.mapControls { }` | Customises which map controls appear (compass, zoom, etc.) |
| `MapReader { proxy in }` | Provides coordinate ↔ screen point conversion |
| `MKLocalSearch` | Search for map items by query string |

## Common patterns

**Camera control:**
```swift
@State private var cameraPosition: MapCameraPosition = .region(
    MKCoordinateRegion(center: CLLocationCoordinate2D(latitude: 37.33, longitude: -122.01),
                       span: MKCoordinateSpan(latitudeDelta: 0.05, longitudeDelta: 0.05))
)

Map(position: $cameraPosition) {
    // content
}
```

**Custom annotation view:**
```swift
Map {
    ForEach(cafes) { cafe in
        Annotation(cafe.name, coordinate: cafe.coordinate) {
            Image(systemName: "cup.and.saucer.fill")
                .foregroundStyle(.brown)
                .padding(6)
                .background(.white, in: Circle())
        }
    }
}
```

**Circle overlay (e.g., radius around a point):**
```swift
Map {
    MapCircle(center: userLocation, radius: 500)  // 500m radius
        .foregroundStyle(.blue.opacity(0.2))
        .stroke(.blue, lineWidth: 2)
}
```

**Map style:**
```swift
Map { /* … */ }
    .mapStyle(.hybrid(elevation: .realistic))
```

**Converting screen point to coordinate:**
```swift
MapReader { proxy in
    Map { /* … */ }
        .onTapGesture { screenPoint in
            if let coord = proxy.convert(screenPoint, from: .local) {
                print("Tapped: \(coord)")
            }
        }
}
```

**Local search:**
```swift
@State private var results: [MKMapItem] = []

func search(for query: String, near region: MKCoordinateRegion) async {
    let request = MKLocalSearch.Request()
    request.naturalLanguageQuery = query
    request.region = region
    let search = MKLocalSearch(request: request)
    if let response = try? await search.start() {
        results = response.mapItems
    }
}
```

## Gotchas

- The new SwiftUI `Map` with a content builder requires iOS 17+; the old `Map(coordinateRegion:)` initialiser still works on iOS 14+.
- `MapAnnotation` (iOS 14–16) is replaced by `Annotation` in iOS 17; the old type is deprecated.
- `Marker` uses the system tint color by default; customise with `.tint(_:)`.
- Adding too many annotations (thousands) will degrade performance — cluster or paginate for large datasets.
- User location requires `NSLocationWhenInUseUsageDescription` in Info.plist and `CLLocationManager` authorisation before showing `.userLocation` content.
