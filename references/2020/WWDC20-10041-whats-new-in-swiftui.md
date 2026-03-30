---
framework: SwiftUI
title: "What's new in SwiftUI"
session: WWDC20-10041
year: 2020
applies_to: iOS 14+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/swiftui.md
---

# What's new in SwiftUI — WWDC20

iOS 14 / macOS 11 significantly expanded SwiftUI with new layout containers, state management improvements, media views, and more.

## What's new

- `LazyVGrid` / `LazyHGrid` — grid layouts with flexible, fixed, and adaptive column definitions
- `@StateObject` — own an `ObservableObject` lifecycle in a view (replaces `@ObservedObject` for ownership)
- `matchedGeometryEffect` — animate a view between two positions in the hierarchy
- `VideoPlayer` — embed AVKit video playback inline in a SwiftUI view
- `Map` — native MapKit map view with annotations
- `ProgressView` — indeterminate and determinate progress indicators
- `Label` — icon + text pairing with semantic meaning
- `TextEditor` — multi-line editable text field
- `OutlineGroup` / `DisclosureGroup` — hierarchical disclosure containers
- `Link` — tappable URL opener (also used in widgets)
- `ColorPicker` — inline color selection UI
- `SignInWithAppleButton` — native ASAuthorizationAppleIDButton in SwiftUI
- `GroupBox` — styled container grouping related content
- `Menu` — context/pull-down menus attached to a button
- `Toolbar` / `ToolbarItem` — declarative toolbar API across platforms

## Before / After

**Grid layout (before — manual HStack/VStack):**
```swift
// iOS 13 — manual row/column grids
VStack {
    HStack {
        ForEach(items.prefix(3)) { Text($0.name) }
    }
    HStack {
        ForEach(items.dropFirst(3).prefix(3)) { Text($0.name) }
    }
}
```

**Grid layout (after — LazyVGrid):**
```swift
let columns = [GridItem(.adaptive(minimum: 80))]

ScrollView {
    LazyVGrid(columns: columns, spacing: 12) {
        ForEach(items) { item in
            Text(item.name)
                .frame(minWidth: 80, minHeight: 80)
                .background(Color.accentColor.opacity(0.2))
        }
    }
    .padding()
}
```

**ObservableObject ownership (before — @ObservedObject risked deallocation):**
```swift
// iOS 13 — @ObservedObject does not own the object
struct CounterView: View {
    @ObservedObject var model = CounterModel()  // could be recreated on redraw
}
```

**ObservableObject ownership (after — @StateObject):**
```swift
// iOS 14 — @StateObject owns the lifetime
struct CounterView: View {
    @StateObject var model = CounterModel()  // created once, lives with the view
}
```

**Matched geometry effect:**
```swift
@Namespace var namespace

var body: some View {
    if showDetail {
        DetailView()
            .matchedGeometryEffect(id: "hero", in: namespace)
    } else {
        ThumbnailView()
            .matchedGeometryEffect(id: "hero", in: namespace)
    }
}
```

## Migration steps

1. Replace `@ObservedObject var model = SomeModel()` with `@StateObject` where the view owns the object
2. Replace custom grid implementations with `LazyVGrid` / `LazyHGrid` and `GridItem`
3. Replace `UIViewRepresentable` wrappers for `UIProgressView` and `MKMapView` with `ProgressView` and `Map`
4. Replace `UIViewRepresentable` for `AVPlayerViewController` with `VideoPlayer(player:)`
5. Adopt `Label` for icon+text pairs to get automatic accessibility and dynamic type support
6. Migrate toolbar buttons from `.navigationBarItems` (deprecated) to `Toolbar` / `ToolbarItem`

## Compatibility notes

- All APIs require iOS 14+ / macOS 11+
- `@StateObject` is the correct replacement for `@ObservedObject` when the view creates the object; `@ObservedObject` is still correct when the object is injected
- `matchedGeometryEffect` requires both views to be in the same view update cycle to animate; use `withAnimation`
- `VideoPlayer` requires `import AVKit`
- `Map` requires `import MapKit`; annotations use `MapAnnotation`, `MapMarker`, `MapPin`
