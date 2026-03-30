---
framework: GroupActivities
title: "Customize spatial Persona templates in SharePlay"
session: WWDC24-10108
year: 2024
applies_to: visionOS 2+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/visionos.md
---

# GroupActivities — Customize Spatial Persona Templates in SharePlay (WWDC24)

Control where participants' spatial Personas appear in a SharePlay session using custom `SpatialTemplate` layouts and `GroupSessionMessenger` for coordinated state.

## Quick start

```swift
import GroupActivities
import RealityKit

// 1. Define a custom spatial template
struct SideBySideTemplate: SpatialTemplate {
    // Declare participant seats in the shared coordinate space
    var elements: [any SpatialTemplateElement] {
        SpatialTemplateSeatElement(position: .init(x: -0.6, y: 0, z: 0))
        SpatialTemplateSeatElement(position: .init(x:  0.6, y: 0, z: 0))
    }
}

// 2. Attach the template when creating a GroupSession
struct DrawingActivity: GroupActivity {
    static let activityIdentifier = "com.example.drawing"

    var metadata: GroupActivityMetadata {
        var meta = GroupActivityMetadata()
        meta.title = "Collaborative Drawing"
        meta.type = .generic
        meta.spatialExperienceInfo = .init(
            scene: .init(configuration: .init(template: SideBySideTemplate()))
        )
        return meta
    }
}

// 3. Use GroupSessionMessenger to sync shared state
actor DrawingSession {
    let messenger: GroupSessionMessenger

    init(session: GroupSession<DrawingActivity>) {
        messenger = GroupSessionMessenger(session: session)
    }

    func sendStroke(_ stroke: DrawingStroke) async throws {
        try await messenger.send(stroke)
    }

    func receiveStrokes() -> AsyncStream<(DrawingStroke, Participant)> {
        AsyncStream { continuation in
            Task {
                for await (stroke, context) in messenger.messages(of: DrawingStroke.self) {
                    continuation.yield((stroke, context.source))
                }
            }
        }
    }
}
```

## Key APIs

| API | Purpose |
|---|---|
| `SpatialTemplate` | Protocol defining participant seat layout in shared space |
| `SpatialTemplateSeatElement` | A single seat position within a `SpatialTemplate` |
| `SpatialTemplateSeatElement.position` | `SIMD3<Float>` position in the shared coordinate space |
| `GroupActivityMetadata.spatialExperienceInfo` | Attaches spatial configuration (template) to the activity |
| `SystemCoordinator` | Coordinates the shared immersive space among participants |
| `SystemCoordinator.localParticipantState` | The local user's current spatial state (seat, immersion) |
| `GroupSessionMessenger` | Sends/receives `Codable` messages between participants |
| `GroupSessionMessenger.messages(of:)` | `AsyncSequence` of typed incoming messages |
| `CoordinateSpaceMapping` | Maps between local and shared coordinate spaces |
| `GroupSession.systemCoordinator` | Access the coordinator for a running session |

## Common patterns

**Assigning seats based on join order:**
```swift
let coordinator = await session.systemCoordinator
var config = SystemCoordinator.Configuration()
config.spatialTemplatePreference = .specific(SideBySideTemplate())
await coordinator.configure(config)
```

**Converting shared coordinates to local RealityKit space:**
```swift
// CoordinateSpaceMapping translates between participants' local spaces
if let mapping = await coordinator.localParticipantState.coordinateSpaceMapping {
    let sharedPoint = SIMD3<Float>(0, 0, -1)  // 1 m in front in shared space
    let localPoint = mapping.converting(sharedPoint, from: .shared, to: .local)
    entity.position = localPoint
}
```

**Receiving typed messages:**
```swift
Task {
    for await (stroke, context) in messenger.messages(of: DrawingStroke.self) {
        await applyStroke(stroke, from: context.source)
    }
}
```

## Gotchas

- `SpatialTemplate` seat positions are in the *shared* coordinate space, not local device space — use `CoordinateSpaceMapping` to convert before positioning RealityKit entities
- `GroupSessionMessenger.messages(of:)` delivers messages on a background actor; always marshal UI or RealityKit updates to `@MainActor`
- The system places the local participant in the nearest available seat — you cannot force a specific participant into a specific seat; design templates to be seat-order-agnostic
- `spatialExperienceInfo` must be set before the activity is presented; it cannot be changed after the session starts
- `SystemCoordinator` is only available while the session is in the `.joined` state; check `session.state` before accessing it
- Custom templates must declare at least as many seats as the expected maximum participant count; extra participants overflow to system-default positions
