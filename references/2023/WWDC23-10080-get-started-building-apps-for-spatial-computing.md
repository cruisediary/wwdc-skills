---
framework: visionOS
title: "Get started with building apps for spatial computing"
session: WWDC23-10080
year: 2023
applies_to: visionOS 1+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/visionos.md
---

# Get started with building apps for spatial computing (WWDC23)

An overview of the three spatial computing app styles and the SwiftUI/RealityKit building blocks used to construct them.

## What changed and why

visionOS introduces a new dimension to Apple's app platform. Unlike iOS and macOS, space is the canvas — apps can exist as windows, as volumetric 3D containers, or as fully immersive environments. This session maps familiar SwiftUI concepts (scenes, views) to their visionOS equivalents.

## Mental model

visionOS apps use one or more of three **space types**:

| Space type | Description | SwiftUI type |
|---|---|---|
| **Shared Space** | Multiple apps coexist; windows float around the user | Default (any `WindowGroup`) |
| **Shared Space + Volume** | A 3D bounding box for your content within the Shared Space | `WindowGroup` + `.windowStyle(.volumetric)` |
| **Full Space** | Your app takes over the whole environment; other apps hidden | `ImmersiveSpace` |

Within those spaces you compose views using:
- Standard SwiftUI views and `NavigationStack` / `NavigationSplitView` inside `WindowGroup`
- `Model3D` for simple static 3D assets
- `RealityView` for interactive RealityKit content
- Ornaments (`.ornament(attachmentAnchor:content:)`) for controls attached to a window but floating in 3D space

## Usage

**Declaring a Window and a Volume:**
```swift
import SwiftUI
import RealityKit

@main
struct MyApp: App {
    var body: some Scene {
        // Standard 2D window
        WindowGroup {
            ContentView()
        }

        // 3D volume
        WindowGroup(id: "globe") {
            GlobeView()
        }
        .windowStyle(.volumetric)
        .defaultSize(width: 0.5, height: 0.5, depth: 0.5, in: .meters)
    }
}
```

**Declaring an Immersive Space:**
```swift
ImmersiveSpace(id: "garden") {
    GardenView()
}
.immersionStyle(selection: .constant(.full), in: .full)
```

**Opening a Volume or Immersive Space from a view:**
```swift
struct LaunchView: View {
    @Environment(\.openWindow) private var openWindow
    @Environment(\.openImmersiveSpace) private var openImmersiveSpace

    var body: some View {
        VStack {
            Button("Show Globe") { openWindow(id: "globe") }
            Button("Enter Garden") {
                Task { await openImmersiveSpace(id: "garden") }
            }
        }
    }
}
```

**Loading a USDZ model:**
```swift
Model3D(named: "Robot") { model in
    model.resizable().scaledToFit()
} placeholder: {
    ProgressView()
}
```

**Window ornament:**
```swift
ContentView()
    .ornament(attachmentAnchor: .scene(.bottom)) {
        HStack { /* toolbar buttons */ }
            .glassBackgroundEffect()
    }
```

## Adopting this pattern

1. Start with a standard `WindowGroup` — existing SwiftUI apps mostly just compile for visionOS.
2. Add `.windowStyle(.volumetric)` for content that benefits from depth (models, data visualisations).
3. Add an `ImmersiveSpace` only for fully immersive experiences; close it when the user needs to return to the shared space.
4. Use `.glassBackgroundEffect()` on visionOS to get the standard glass material on HUD / toolbar elements.
5. Test in the simulator; hand gestures (tap, pinch-drag) map to pointer + mouse events for basic interactivity.
