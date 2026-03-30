---
framework: RealityKit
title: "Enhance your spatial computing app with RealityKit"
session: WWDC24-10104
year: 2024
applies_to: visionOS 2+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/visionos.md
---

# RealityKit — Enhance Your Spatial Computing App with RealityKit (WWDC24)

Deep-dive into `RealityView` attachments, building `Entity` hierarchies, and handling gestures with `.targetedToAnyEntity()` for interactive spatial experiences.

## Quick start

```swift
import RealityKit
import SwiftUI

struct SpatialScene: View {
    var body: some View {
        RealityView { content, attachments in
            // Build entity hierarchy
            let root = Entity()
            let sphere = ModelEntity(
                mesh: .generateSphere(radius: 0.1),
                materials: [SimpleMaterial(color: .blue, isMetallic: true)]
            )
            sphere.components.set(InputTargetComponent(allowedInputTypes: .indirect))
            sphere.components.set(CollisionComponent(shapes: [.generateSphere(radius: 0.1)]))
            root.addChild(sphere)
            content.add(root)

            // Attach a SwiftUI label to the sphere
            if let label = attachments.entity(for: "sphereLabel") {
                label.position = [0, 0.15, 0]
                sphere.addChild(label)
            }
        } attachments: {
            Attachment(id: "sphereLabel") {
                Text("Tap me")
                    .padding(8)
                    .glassBackgroundEffect()
            }
        }
        .gesture(
            TapGesture()
                .targetedToAnyEntity()
                .onEnded { value in
                    value.entity.components.set(
                        PhysicsBodyComponent(massProperties: .default,
                                             material: .default,
                                             mode: .dynamic)
                    )
                }
        )
    }
}
```

## Key APIs

| API | Purpose |
|---|---|
| `RealityView(make:update:attachments:)` | Creates a RealityKit scene with SwiftUI attachments |
| `RealityViewContent.add(_:)` | Adds a root entity to the scene |
| `Attachment(id:content:)` | Declares a named SwiftUI view to embed as a RealityKit entity |
| `attachments.entity(for:)` | Retrieves the attachment entity by ID inside `make` |
| `InputTargetComponent(allowedInputTypes:)` | Marks an entity as a gesture target |
| `CollisionComponent(shapes:)` | Required for hit-testing; must accompany `InputTargetComponent` |
| `.targetedToAnyEntity()` | Gesture modifier that routes spatial gestures to entity under the pointer |
| `.targetedToEntity(_:)` | Routes a gesture to a specific named entity |
| `Entity.addChild(_:)` | Attaches a child entity, inheriting parent's transform |
| `Entity.position` | Sets/gets local-space position as `SIMD3<Float>` |

## Common patterns

**Attachment anchored to an entity:**
```swift
RealityView { content, attachments in
    let model = try? await Entity(named: "Robot", in: .main)
    content.add(model ?? Entity())
    if let ui = attachments.entity(for: "controls") {
        ui.position = [0, 1.0, 0]          // 1 m above model root
        model?.addChild(ui)
    }
} attachments: {
    Attachment(id: "controls") {
        ControlPanel()
    }
}
```

**Drag gesture moving an entity in world space:**
```swift
.gesture(
    DragGesture()
        .targetedToAnyEntity()
        .onChanged { value in
            // Instead of: value.convert(value.location3D, from: .local, to: value.entity.parent ?? value.entity)
            // Use scene coordinate space:
            value.entity.position = value.convert(value.location3D, from: .local, to: .scene)
        }
)
```

**Updating entities in `update` closure:**
```swift
RealityView { content, _ in
    // initial setup
} update: { content, _ in
    // called when SwiftUI state driving the view changes
    guard let sphere = content.entities.first(where: { $0.name == "sphere" }) else { return }
    sphere.scale = isExpanded ? [2, 2, 2] : [1, 1, 1]
}
```

## Gotchas

- `InputTargetComponent` alone is not enough — an entity must also have a `CollisionComponent` for gestures to hit-test against it
- `attachments.entity(for:)` returns `nil` if the `Attachment` view is conditionally excluded; always guard the optional
- Entity transforms are in local (parent) space; use `convert(_:from:to:)` to translate between coordinate spaces
- The `update` closure fires on every SwiftUI state change — avoid heavy computation or entity rebuilding inside it; prefer mutating existing components
- `RealityView` does not automatically remove entities when the view disappears; use `content.remove(_:)` in a `onDisappear` or `update` to clean up
- Gesture modifiers like `.targetedToAnyEntity()` must be applied to the `RealityView`, not to child SwiftUI views inside attachments
