---
framework: visionOS
status: current
applies_to: visionOS 1+
shape: guide-first
superseded_by: null
history:
  - year: 2023
    file: 2023/visionos.md
    summary: "Initial introduction — RealityView, ImmersiveSpace, WindowGroup"
---

## What changed and why

visionOS is Apple's spatial computing platform where apps exist in a shared space and can display 2D windows, 3D volumes, and fully immersive experiences. Unlike iOS, the display surface is the user's physical environment — apps must account for depth, scale, and the user's surroundings.

## Mental model

Think of visionOS as SwiftUI extended into 3D space. The same declarative view system applies, but you gain a third axis and new scene types. A `WindowGroup` works exactly like on iOS (a flat 2D panel floating in space). A `RealityView` is a SwiftUI view that hosts a RealityKit 3D scene. An `ImmersiveSpace` takes over the user's full field of view.

```
WindowGroup     →  flat 2D panel (familiar SwiftUI)
RealityView     →  3D content embedded in a window or volume
ImmersiveSpace  →  full environment, replaces the passthrough world
```

## Usage

**Minimal RealityView with a sphere entity:**

```swift
import SwiftUI
import RealityKit

struct SphereView: View {
    var body: some View {
        RealityView { content in
            let mesh = MeshResource.generateSphere(radius: 0.1)
            let material = SimpleMaterial(color: .blue, isMetallic: true)
            let entity = ModelEntity(mesh: mesh, materials: [material])
            content.add(entity)
        }
    }
}
```

**Declaring scene types in the App struct:**

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }

        ImmersiveSpace(id: "immersive") {
            ImmersiveView()
        }
    }
}
```

**Opening an ImmersiveSpace from a button:**

```swift
struct ContentView: View {
    @Environment(\.openImmersiveSpace) private var openImmersiveSpace
    @Environment(\.dismissImmersiveSpace) private var dismissImmersiveSpace

    var body: some View {
        Button("Enter Immersive Experience") {
            Task {
                await openImmersiveSpace(id: "immersive")
            }
        }
    }
}
```

## Adopting this pattern

If you have an existing iOS SwiftUI app, the main adaptation steps are:

1. Add a visionOS target in Xcode — most SwiftUI views compile as-is and appear as 2D windows.
2. Introduce `RealityView` where you want 3D content alongside existing 2D UI.
3. Add an `ImmersiveSpace` scene for fully spatial experiences.
4. Use `#if os(visionOS)` guards for platform-specific APIs (spatial audio, hand tracking, ARKit anchors).
