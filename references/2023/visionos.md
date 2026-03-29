---
framework: visionOS
session: WWDC23-10080
year: 2023
applies_to: visionOS 1+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/visionos.md
---

## What's new

visionOS is a new platform introduced at WWDC23. As a new-platform introduction there is no prior visionOS version — this file covers what the platform provides at launch:

- **RealityView** — SwiftUI view hosting a RealityKit 3D scene with full entity/component access
- **ImmersiveSpace** — new scene type that takes over the user's environment for a fully spatial experience
- **WindowGroup** — familiar SwiftUI scene type rendered as a floating 2D panel in shared space
- **Volumes** — windowed 3D scenes with a fixed bounding box, visible alongside other apps
- **Spatial audio** — positional audio tied to entity position in the scene
- **Hand tracking** — skeletal hand poses via ARKit AnchorUpdates
- **ARKit anchors** — world anchors, image anchors, plane detection in the user's environment

## Before / After

**iOS SwiftUI app (2D only):**

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView() // flat 2D view
        }
    }
}

struct ContentView: View {
    var body: some View {
        Text("Hello, World!")
    }
}
```

**visionOS spatial app:**

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView() // still works as a flat 2D panel
        }

        ImmersiveSpace(id: "immersive") {
            ImmersiveView()
        }
    }
}

struct ImmersiveView: View {
    var body: some View {
        RealityView { content in
            // add 3D entities to the scene
            let sphere = ModelEntity(
                mesh: .generateSphere(radius: 0.15),
                materials: [SimpleMaterial(color: .cyan, isMetallic: false)]
            )
            content.add(sphere)
        }
    }
}
```

## Migration steps

1. **Add a visionOS target** — in Xcode, add a new visionOS destination to your existing project. Most SwiftUI views compile without changes and appear as floating 2D windows.
2. **Replace UIKit-only code** — visionOS does not support UIKit directly; use SwiftUI equivalents or `#if os(visionOS)` guards.
3. **Add 3D content with RealityView** — where you want spatial content, embed a `RealityView` inside your SwiftUI hierarchy and populate it with RealityKit entities.
4. **Declare an ImmersiveSpace scene** — for experiences that go beyond windows, declare `ImmersiveSpace` in your `App` body and open it via `@Environment(\.openImmersiveSpace)`.
5. **Adopt spatial audio** — attach `SpatialAudioComponent` to entities that should emit positional sound.
6. **Add hand tracking if needed** — use `ARKitSession` with `HandTrackingProvider` for skeletal hand poses; requires the `com.apple.developer.arkit.hand-tracking` entitlement.

## Compatibility notes

- visionOS 1.0+ required for all APIs covered here.
- RealityView and ImmersiveSpace are visionOS-exclusive; use `#if os(visionOS)` guards to share code with iOS/macOS targets.
- Hand tracking requires explicit user permission and the ARKit hand-tracking entitlement.
