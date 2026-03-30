---
framework: ARKit
title: "Meet ARKit for spatial computing"
session: WWDC23-10082
year: 2023
applies_to: visionOS 1+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/arkit.md
  - canonical/visionos.md
---

# Meet ARKit for spatial computing (WWDC23)

visionOS ships a redesigned ARKit with a Swift-async session/provider API replacing the `ARSession` delegate pattern from iOS.

## Quick start

```swift
import ARKit
import RealityKit

// 1. Declare required capabilities in Info.plist:
//    NSWorldSensingUsageDescription (plane detection, scene reconstruction)
//    NSHandsTrackingUsageDescription (hand tracking)

// 2. Start an ARKit session with providers
let session = ARKitSession()
let worldTracking = WorldTrackingProvider()
let planeDetection = PlaneDetectionProvider(alignments: [.horizontal, .vertical])

Task {
    do {
        try await session.run([worldTracking, planeDetection])
    } catch {
        print("ARKit session failed: \(error)")
    }
}

// 3. Consume plane anchor updates
Task {
    for await update in planeDetection.anchorUpdates {
        handlePlaneUpdate(update)
    }
}

func handlePlaneUpdate(_ update: AnchorUpdate<PlaneAnchor>) {
    let anchor = update.anchor
    switch update.event {
    case .added:
        print("Plane added: \(anchor.geometry)")
    case .updated:
        print("Plane updated")
    case .removed:
        print("Plane removed")
    }
}
```

## Key APIs

| API | Purpose |
|---|---|
| `ARKitSession` | The entry point; manages running data providers |
| `ARKitSession.run(_:)` | Starts the session with an array of `DataProvider` instances |
| `WorldTrackingProvider` | Provides 6-DOF device tracking and world anchors |
| `PlaneDetectionProvider` | Detects horizontal and vertical surfaces |
| `HandTrackingProvider` | Streams hand skeleton joint data for both hands |
| `SceneReconstructionProvider` | Streams a mesh of the surrounding environment |
| `AnchorUpdate<T>` | An async update containing the anchor and the event type (added/updated/removed) |
| `PlaneAnchor` | An anchor describing a detected planar surface |
| `HandAnchor` | An anchor containing `HandSkeleton` with per-joint transforms |
| `WorldAnchor` | A persistent anchor placed at a specific world position |
| `deviceAnchor(atTimestamp:)` | Queries the device's pose at a given timestamp from `WorldTrackingProvider` |

## Common patterns

**Querying device pose:**
```swift
if let deviceAnchor = worldTracking.queryDeviceAnchor(atTimestamp: CACurrentMediaTime()) {
    let transform = deviceAnchor.originFromAnchorTransform
    // use 4x4 transform to position content relative to device
}
```

**Hand tracking:**
```swift
let handTracking = HandTrackingProvider()
try await session.run([handTracking])

Task {
    for await update in handTracking.anchorUpdates {
        let hand = update.anchor
        if hand.chirality == .right,
           let indexTip = hand.handSkeleton?.joint(.indexFingerTip) {
            let tipTransform = hand.originFromAnchorTransform * indexTip.anchorFromJointTransform
            // use tipTransform to position content at fingertip
        }
    }
}
```

**Scene reconstruction:**
```swift
let reconstruction = SceneReconstructionProvider()
try await session.run([reconstruction])

Task {
    for await update in reconstruction.anchorUpdates {
        let meshAnchor = update.anchor
        // meshAnchor.geometry gives vertices and faces for occlusion
    }
}
```

## Gotchas

- Authorization is required before starting session — check `ARKitSession.requestAuthorization(for:)` and handle `.denied` state.
- `WorldTrackingProvider` and `PlaneDetectionProvider` require **world sensing** authorization; `HandTrackingProvider` requires **hands tracking** authorization.
- All provider updates are delivered as `AsyncSequence` streams — consume them in `Task` blocks; cancelling the task stops consumption.
- Unlike iOS `ARSession`, there is no passthrough camera feed accessible to the app; the system renders passthrough internally.
- ARKit on visionOS does not expose `ARFrame` or `ARCamera` — use `WorldTrackingProvider.queryDeviceAnchor` for device pose.
