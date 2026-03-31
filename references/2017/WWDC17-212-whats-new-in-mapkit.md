---
framework: MapKit
title: "What's New in MapKit"
session: WWDC17-212
year: 2017
applies_to: iOS 11+
status: reference-only
superseded_by: null
shape: code-first
related: []
---

> **Reference-only (iOS 11+):** MapKit improvements from iOS 11 remain in iOS 18. Cluster annotations and `MKMarkerAnnotationView` remain the standard approach for annotation display.

## Quick start

```swift
import MapKit

let mapView = MKMapView(frame: view.bounds)
view.addSubview(mapView)
mapView.register(MKMarkerAnnotationView.self,
                 forAnnotationViewWithReuseIdentifier: MKMapViewDefaultAnnotationViewReuseIdentifier)

let annotation = MKPointAnnotation()
annotation.coordinate = CLLocationCoordinate2D(latitude: 37.3318, longitude: -122.0312)
annotation.title = "Apple Park"
mapView.addAnnotation(annotation)
```

## Key APIs

| Type | Role |
|---|---|
| `MKMarkerAnnotationView` | Standard pin with callout; replaces `MKPinAnnotationView` |
| `MKAnnotationView.clusteringIdentifier` | Groups nearby annotations into clusters when set |
| `MKClusterAnnotation` | Represents a group of merged annotations |
| `MKMapView.register(_:forAnnotationViewWithReuseIdentifier:)` | Register annotation view class for reuse |
| `MKMapItem` | App-side representation of a location; use `openInMaps()` |

## Common patterns

**Cluster annotations**

```swift
class MyAnnotationView: MKMarkerAnnotationView {
    override init(annotation: MKAnnotation?, reuseIdentifier: String?) {
        super.init(annotation: annotation, reuseIdentifier: reuseIdentifier)
        clusteringIdentifier = "myCluster"
    }
    required init?(coder: NSCoder) { super.init(coder: coder) }
}
```

## Gotchas

- Register annotation view classes in `viewDidLoad` before the map loads annotations.
- `MKMapViewDefaultClusterAnnotationViewReuseIdentifier` provides a default cluster view; customize by subclassing `MKAnnotationView` and overriding `prepareForDisplay`.
