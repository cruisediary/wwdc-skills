---
framework: visionOS
title: "Develop your first immersive app"
session: WWDC23-10203
year: 2023
applies_to: visionOS 1+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/visionos.md
---

# Develop your first immersive app (WWDC23)

A hands-on guide to building a visionOS immersive experience using `RealityView`, `Entity`, and `ImmersiveSpace`.

## Quick start

```swift
import SwiftUI
import RealityKit

// 1. Declare the ImmersiveSpace scene
@main
struct HelloSpatialApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }

        ImmersiveSpace(id: "solar") {
            SolarSystemView()
        }
    }
}

// 2. Build the immersive content with RealityView
struct SolarSystemView: View {
    var body: some View {
        RealityView { content in
            // Load a reality file or build entities in code
            if let sun = try? await Entity(named: "Sun", in: realityKitContentBundle) {
                content.add(sun)
            }
        }
    }
}

// 3. Open the immersive space from the 2D window
struct ContentView: View {
    @Environment(\.openImmersiveSpace) private var openImmersiveSpace
    @Environment(\.dismissImmersiveSpace) private var dismissImmersiveSpace
    @State private var isImmersive = false

    var body: some View {
        Button(isImmersive ? "Exit" : "Enter Solar System") {
            Task {
                if isImmersive {
                    await dismissImmersiveSpace()
                } else {
                    await openImmersiveSpace(id: "solar")
                }
                isImmersive.toggle()
            }
        }
    }
}
```

## Key APIs

| API | Purpose |
|---|---|
| `ImmersiveSpace(id:content:)` | Scene type for a full-environment experience |
| `RealityView` | SwiftUI view that hosts a RealityKit entity hierarchy |
| `RealityView { content in }` | Make closure — add initial entities to `content` |
| `RealityView(make:update:)` | Update closure — called when SwiftUI state changes |
| `Entity(named:in:)` | Async load a named entity from a Reality Composer Pro bundle |
| `content.add(_:)` | Add an entity to the RealityView scene |
| `ModelComponent` | Component that holds a 3D mesh + materials |
| `Entity()` | Create an empty entity to attach components to |
| `openImmersiveSpace(id:)` | Environment action to open a declared `ImmersiveSpace` |
| `dismissImmersiveSpace()` | Environment action to close the active immersive space |

## Common patterns

**Building an entity in code (no RC Pro file):**
```swift
RealityView { content in
    let sphere = ModelEntity(
        mesh: .generateSphere(radius: 0.1),
        materials: [SimpleMaterial(color: .blue, isMetallic: true)]
    )
    sphere.position = [0, 1.5, -1]  // 1.5m up, 1m in front
    content.add(sphere)
}
```

**Updating entities when SwiftUI state changes:**
```swift
@State private var color: Color = .red

RealityView { content in
    let box = ModelEntity(mesh: .generateBox(size: 0.2),
                          materials: [SimpleMaterial()])
    box.name = "box"
    content.add(box)
} update: { content in
    if let box = content.entities.first(where: { $0.name == "box" }),
       var model = box.components[ModelComponent.self] {
        model.materials = [SimpleMaterial(color: UIColor(color), isMetallic: false)]
        box.components[ModelComponent.self] = model
    }
}
```

**Handling tap gestures on entities:**
```swift
RealityView { content in
    let cube = ModelEntity(mesh: .generateBox(size: 0.1),
                           materials: [SimpleMaterial(color: .orange, isMetallic: false)])
    cube.generateCollisionShapes(recursive: false)
    cube.components[InputTargetComponent.self] = InputTargetComponent()
    content.add(cube)
}
.gesture(TapGesture().targetedToAnyEntity().onEnded { value in
    value.entity.isEnabled.toggle()
})
```

## Gotchas

- `Entity(named:in:)` is async — always use it inside an `async` context (the make closure runs asynchronously).
- Entities require a `CollisionComponent` + `InputTargetComponent` to receive gestures; adding collision shapes via `generateCollisionShapes(recursive:)` is the quick path.
- The RealityView coordinate system places the origin at the floor level in front of the user; +Y is up, -Z is forward.
- `ImmersiveSpace` scenes must be declared at the App level — you cannot open an immersive space from another immersive space.
- Use `openImmersiveSpace` asynchronously and check its result to handle failures (e.g., user denied permission).
