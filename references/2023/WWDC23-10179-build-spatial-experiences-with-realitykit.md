---
framework: RealityKit
title: "Build spatial experiences with RealityKit"
session: WWDC23-10179
year: 2023
applies_to: visionOS 1+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/visionos.md
---

# Build spatial experiences with RealityKit (WWDC23)

A comprehensive look at the RealityKit entity-component system, `RealityView`, physics, and gesture handling on visionOS.

## Quick start

```swift
import SwiftUI
import RealityKit

struct SpatialView: View {
    var body: some View {
        RealityView { content in
            // Create a box entity
            let box = ModelEntity(
                mesh: .generateBox(size: 0.2, cornerRadius: 0.01),
                materials: [SimpleMaterial(color: .systemBlue, isMetallic: true)]
            )
            box.position = [0, 1.5, -1]  // y=1.5m, z=1m forward
            box.generateCollisionShapes(recursive: false)
            box.components[InputTargetComponent.self] = InputTargetComponent()
            content.add(box)
        }
        .gesture(
            DragGesture()
                .targetedToAnyEntity()
                .onChanged { value in
                    value.entity.position = value.convert(value.location3D, from: .local, to: .scene)
                }
        )
    }
}
```

## Key APIs

| API | Purpose |
|---|---|
| `RealityView` | SwiftUI view hosting a RealityKit entity hierarchy |
| `RealityViewContent` | The content proxy — use `.add(_:)` to insert entities |
| `Entity` | Base class for all scene objects |
| `ModelEntity` | Convenience entity with `ModelComponent` pre-attached |
| `ModelComponent` | Holds a `MeshResource` and materials |
| `PhysicsBodyComponent` | Adds rigid-body physics simulation |
| `PhysicsMotionComponent` | Exposes linear/angular velocity for dynamic bodies |
| `CollisionComponent` | Required for physics and gesture hit-testing |
| `InputTargetComponent` | Marks an entity as a gesture interaction target |
| `generateCollisionShapes(recursive:)` | Auto-generates collision shapes from mesh bounds |
| `DragGesture().targetedToAnyEntity()` | Drag gesture scoped to any entity with `InputTargetComponent` |
| `TapGesture().targetedToEntity(_:)` | Tap gesture scoped to a specific entity |
| `value.convert(_:from:to:)` | Converts a 3D point between coordinate spaces |
| `AnchorEntity(.plane(.horizontal, …))` | Anchors the entity hierarchy to a detected plane |

## Common patterns

**Adding physics to an entity:**
```swift
let ball = ModelEntity(
    mesh: .generateSphere(radius: 0.05),
    materials: [SimpleMaterial(color: .red, isMetallic: false)]
)
ball.generateCollisionShapes(recursive: false)
ball.components[PhysicsBodyComponent.self] = PhysicsBodyComponent(
    shapes: ball.collision!.shapes,
    mass: 0.5,
    material: .generate(friction: 0.3, restitution: 0.8),
    mode: .dynamic
)
ball.components[PhysicsMotionComponent.self] = PhysicsMotionComponent(
    linearVelocity: [0, 2, -1]
)
```

**Gesture targeting a specific entity:**
```swift
@State private var cubeEntity: Entity?

RealityView { content in
    let cube = ModelEntity(mesh: .generateBox(size: 0.1),
                           materials: [SimpleMaterial()])
    cube.generateCollisionShapes(recursive: false)
    cube.components[InputTargetComponent.self] = InputTargetComponent()
    content.add(cube)
    cubeEntity = cube
}
.gesture(
    TapGesture()
        .targetedToEntity(cubeEntity ?? Entity())
        .onEnded { _ in
            cubeEntity?.isEnabled.toggle()
        }
)
```

**Subscribing to collision events:**
```swift
RealityView { content in
    let scene = content
    _ = content.subscribe(to: CollisionEvents.Began.self) { event in
        print("Collision: \(event.entityA.name) ↔ \(event.entityB.name)")
    }
}
```

**Attaching SwiftUI views to entities (attachments):**
```swift
RealityView { content, attachments in
    let sphere = ModelEntity(mesh: .generateSphere(radius: 0.1),
                             materials: [SimpleMaterial()])
    sphere.position = [0, 1.5, -1]
    if let label = attachments.entity(for: "label") {
        label.position = [0, 0.15, 0]
        sphere.addChild(label)
    }
    content.add(sphere)
} attachments: {
    Attachment(id: "label") {
        Text("Hello, RealityKit")
            .padding(8)
            .glassBackgroundEffect()
    }
}
```

## Gotchas

- `InputTargetComponent` requires a `CollisionComponent` — add both or gestures won't fire.
- `value.convert(_:from:to:)` in a `DragGesture` handler converts from SwiftUI local space to scene (world) space — always specify the coordinate space explicitly.
- Dynamic physics entities need both `PhysicsBodyComponent` (mode `.dynamic`) and `PhysicsMotionComponent` for velocity-driven motion.
- The RealityView coordinate origin is at the user's floor level; `y = 1.5` approximates eye height.
- Entity `.position` is in meters; objects placed at `z = 0` are at the user's standing position.
