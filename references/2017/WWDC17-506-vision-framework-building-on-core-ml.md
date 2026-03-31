---
framework: Vision
title: "Vision Framework: Building on Core ML"
session: WWDC17-506
year: 2017
applies_to: iOS 11+
status: reference-only
superseded_by: null
shape: code-first
related:
  - 2017/WWDC17-703-introducing-core-ml.md
---

> **Reference-only (iOS 11+):** Vision introduced in iOS 11 remains the primary framework for on-device image analysis. APIs are stable and widely used in production. The core request/handler pattern is unchanged in iOS 18.

## Quick start

```swift
import Vision

let request = VNDetectFaceRectanglesRequest { request, error in
    guard let faces = request.results as? [VNFaceObservation] else { return }
    for face in faces {
        print(face.boundingBox)   // normalized CGRect (origin bottom-left)
    }
}
let handler = VNImageRequestHandler(cgImage: cgImage, orientation: .up, options: [:])
try? handler.perform([request])
```

## Key APIs

| Type | Role |
|---|---|
| `VNImageRequestHandler` | Processes one or more requests on a single image |
| `VNSequenceRequestHandler` | Processes tracking requests across a sequence of frames |
| `VNRequest` | Base class for all vision requests |
| `VNObservation` | Base class for results; has `confidence` and `uuid` |
| `VNFaceObservation` | Detected face; `boundingBox` in normalized coords (0–1, origin bottom-left) |
| `VNFaceLandmarkRegion2D` | Points for facial features (eyes, nose, mouth) |
| `VNRectangleObservation` | Detected rectangle with four corner points |
| `VNTextObservation` | Detected text region (character boxes as `VNRectangleObservation`) |
| `VNCoreMLRequest` | Runs a Core ML model; produces `VNClassificationObservation` or `VNPixelBufferObservation` |

## Common patterns

**Face landmarks**

```swift
let landmarkRequest = VNDetectFaceLandmarksRequest { request, _ in
    guard let faces = request.results as? [VNFaceObservation] else { return }
    for face in faces {
        if let landmarks = face.landmarks {
            let leftEye = landmarks.leftEye?.normalizedPoints ?? []
            _ = leftEye   // points are relative to face.boundingBox
        }
    }
}
```

**Batch multiple requests on one image**

```swift
let faceRequest = VNDetectFaceRectanglesRequest()
let rectRequest = VNDetectRectanglesRequest()
let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
try? handler.perform([faceRequest, rectRequest])
```

## Gotchas

- `boundingBox` uses a **flipped coordinate system** (origin at bottom-left). Convert to UIKit: `y_uikit = 1.0 - boundingBox.origin.y - boundingBox.size.height`.
- Pass `orientation` matching the image's EXIF orientation, or detections will be rotated.
- `VNSequenceRequestHandler` is not thread-safe; use one instance per thread.
- Vision requests are expensive — dispatch off the main queue.
