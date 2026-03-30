---
framework: visionOS
title: "Build great games for spatial computing"
session: WWDC23-10093
year: 2023
applies_to: visionOS 1+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/visionos.md
---

# Build great games for spatial computing (WWDC23)

Guidance and patterns for building games on visionOS using RealityKit, the game loop, collision, input, and Metal.

## What changed and why

visionOS is a new platform for games — spatial computing lets players interact with game content placed in their real environment. Games can run in a shared space (window/volume), a fully immersive space, or a mix. The platform's input model (eye gaze + hand gestures) and rendering pipeline (composited via the system compositor) require adapting traditional game-loop patterns.

## Mental model

- **Space choice** — Casual games fit in a `WindowGroup` or volumetric window. Fully immersive action games use `ImmersiveSpace` with `.immersionStyle(.full)`.
- **Game loop** — RealityKit drives the render loop. Use `RealityView` and subscribe to scene events (`SceneEvents.Update`) instead of building a manual `CADisplayLink`-based loop.
- **Input** — visionOS input is driven by eye gaze (pointing) and pinch gestures. Attach `InputTargetComponent` + `CollisionComponent` to entities to receive SwiftUI gesture hits. Game controllers (MFi) are fully supported.
- **Collision and physics** — Add `PhysicsBodyComponent` and `PhysicsMotionComponent` to entities; RealityKit's physics engine handles collision response. Subscribe to `CollisionEvents.Began` for game logic.
- **Metal** — For custom rendering, use a `CompositorServices` layer renderer with a `LayerRenderer` (Metal-based). This bypasses RealityKit for the draw call but still composites correctly in the visionOS system compositor.
- **Fully immersive rendering** — Use `.immersionStyle(selection:in:)` with `.full` or `.progressive` for AR/MR passthrough control.

## Usage

**Subscribing to the game update tick:**
```swift
struct GameView: View {
    @State private var score = 0

    var body: some View {
        RealityView { content, attachments in
            // set up entities
        } update: { content, attachments in
            // respond to SwiftUI state changes
        }
        .onReceive(NotificationCenter.default.publisher(for: .init("GameTick"))) { _ in
            // custom tick logic
        }
    }
}

// Subscribe to RealityKit scene update events
func setupGameLoop(in content: RealityViewContent) {
    content.subscribe(to: SceneEvents.Update.self) { event in
        let deltaTime = event.deltaTime
        // update game entities
    }
}
```

**Collision detection:**
```swift
func setupCollision(scene: RealityKit.Scene) {
    scene.subscribe(to: CollisionEvents.Began.self) { event in
        let entityA = event.entityA
        let entityB = event.entityB
        // handle collision between A and B
    }
}
```

**Adding physics to an entity:**
```swift
let ball = ModelEntity(mesh: .generateSphere(radius: 0.05),
                       materials: [SimpleMaterial(color: .red, isMetallic: false)])
ball.generateCollisionShapes(recursive: false)
ball.components[PhysicsBodyComponent.self] = PhysicsBodyComponent(
    shapes: ball.collision!.shapes,
    mass: 1.0,
    material: .generate(friction: 0.5, restitution: 0.7),
    mode: .dynamic
)
ball.components[PhysicsMotionComponent.self] = PhysicsMotionComponent()
```

**Input via gesture on entities:**
```swift
RealityView { content in
    let target = makeTargetEntity()
    target.components[InputTargetComponent.self] = InputTargetComponent()
    target.generateCollisionShapes(recursive: false)
    content.add(target)
}
.gesture(TapGesture().targetedToAnyEntity().onEnded { value in
    handleTap(on: value.entity)
})
```

## Adopting this pattern

1. Choose your space: `WindowGroup` + `.windowStyle(.volumetric)` for casual experiences; `ImmersiveSpace` for fully immersive games.
2. Use `SceneEvents.Update` subscription for per-frame game logic instead of a custom run loop.
3. Add `InputTargetComponent` and collision shapes to any entity the player can interact with.
4. Use RealityKit physics (`PhysicsBodyComponent`) for collision response; subscribe to `CollisionEvents` for game logic triggers.
5. For custom Metal rendering, explore `CompositorServices` and `LayerRenderer` for direct GPU access within the visionOS compositor.
6. Support MFi game controllers via `GCController` — the same `GameController` framework works on visionOS.
