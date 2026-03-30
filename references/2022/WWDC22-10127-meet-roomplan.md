---
framework: RoomPlan
title: "Meet RoomPlan"
session: WWDC22-10127
year: 2022
applies_to: iOS 16+
status: reference-only
superseded_by: null
shape: code-first
related: []
---

# Meet RoomPlan — WWDC22

RoomPlan is introduced as a new ARKit-backed framework for scanning and capturing the 3D structure of interior rooms, detecting walls, doors, windows, and furniture.

## Core APIs

### RoomCaptureSession

The central object that drives room capture using ARKit and LiDAR.

```swift
import RoomPlan

let captureSession = RoomCaptureSession()
captureSession.delegate = self

// Start capturing
let config = RoomCaptureSession.Configuration()
captureSession.run(configuration: config)

// Stop and get result
captureSession.stop()
```

### RoomCaptureView

A ready-made view for displaying the live capture UI (walls, detected surfaces shown in AR):

```swift
import RoomPlan
import UIKit

class ScanViewController: UIViewController {
    var roomCaptureView: RoomCaptureView!

    override func viewDidLoad() {
        super.viewDidLoad()
        roomCaptureView = RoomCaptureView(frame: view.bounds)
        roomCaptureView.captureSession.delegate = self
        view.addSubview(roomCaptureView)
    }

    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)
        let config = RoomCaptureSession.Configuration()
        roomCaptureView.captureSession.run(configuration: config)
    }
}
```

### RoomCaptureSessionDelegate

```swift
extension ScanViewController: RoomCaptureSessionDelegate {
    func captureSession(_ session: RoomCaptureSession,
                        didUpdate room: CapturedRoom) {
        // Called incrementally as the scan progresses
        // room.walls, room.doors, room.windows, room.objects updated here
    }

    func captureSession(_ session: RoomCaptureSession,
                        didEndWith room: CapturedRoom,
                        error: Error?) {
        // Final result after stop()
        if let error { print("Scan error: \(error)"); return }
        // Export the captured room
        try? room.export(to: outputURL)
    }
}
```

### CapturedRoom

```swift
let room: CapturedRoom = ...

// Detected surfaces
let walls: [CapturedRoom.Surface] = room.walls
let doors: [CapturedRoom.Surface] = room.doors
let windows: [CapturedRoom.Surface] = room.windows
let openings: [CapturedRoom.Surface] = room.openings

// Detected objects (furniture categories)
let objects: [CapturedRoom.Object] = room.objects

// Each surface has:
let surface = walls.first!
let transform = surface.transform    // simd_float4x4 — position + orientation
let dimensions = surface.dimensions  // simd_float3 — width, height, depth
let confidence = surface.confidence  // .low / .medium / .high
```

### Exporting

```swift
// Export as USDZ for use in Reality Composer, Quick Look, etc.
let outputURL = FileManager.default.temporaryDirectory
    .appendingPathComponent("room.usdz")
try room.export(to: outputURL)
```

## Compatibility notes

- RoomPlan requires **iPhone with LiDAR Scanner** (iPhone 12 Pro and later, iPad Pro with LiDAR)
- Requires iOS 16+
- `RoomCaptureView` provides a complete capture UI; use it unless you need a fully custom experience
- Exported USDZ files are compatible with Reality Composer Pro and AR Quick Look
