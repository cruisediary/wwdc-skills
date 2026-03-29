---
framework: ARKit
status: deprecated
applies_to: iOS 11+
shape: code-first
superseded_by: null  # no in-repo successor — superseded by RealityKit/RealityView (see canonical/visionos.md)
history:
  - year: 2018
    file: 2018/arkit-2.md
    summary: "ARKit 2 — multi-user sessions, image/object tracking, environment texturing"
---

## Quick start

```swift
import ARKit
import SceneKit

class ViewController: UIViewController, ARSCNViewDelegate {
    @IBOutlet var sceneView: ARSCNView!

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        let configuration = ARWorldTrackingConfiguration()
        configuration.planeDetection = [.horizontal, .vertical]
        sceneView.session.run(configuration)
    }

    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        sceneView.session.pause()
    }
}
```

> **Deprecated:** ARKit with ARSCNView/ARSKView is still available but the modern path is RealityKit + RealityView. For new projects — especially targeting visionOS — use `references/canonical/visionos.md`.

## Key APIs

| API | Purpose |
|---|---|
| `ARSession` | Manages the AR session lifecycle — starts, pauses, resets |
| `ARWorldTrackingConfiguration` | 6DOF world tracking with plane and image detection |
| `ARSCNView` | SceneKit overlay on AR camera feed |
| `ARAnchor` | A real-world position/orientation anchor attached to the session |
| `ARPlaneAnchor` | Subclass of ARAnchor for detected horizontal/vertical planes |
| `ARFrame` | Single captured frame — camera image, tracking state, anchors |

## Common patterns

```swift
// Add a SceneKit node when a plane is detected
func renderer(_ renderer: SCNSceneRenderer, didAdd node: SCNNode, for anchor: ARAnchor) {
    guard let planeAnchor = anchor as? ARPlaneAnchor else { return }
    // extent.z maps to height for horizontal planes; adapt for vertical ARPlaneAnchor.alignment
    let plane = SCNPlane(width: CGFloat(planeAnchor.extent.x),
                         height: CGFloat(planeAnchor.extent.z))
    let planeNode = SCNNode(geometry: plane)
    planeNode.eulerAngles.x = -.pi / 2
    node.addChildNode(planeNode)
}

// Reset session
sceneView.session.run(ARWorldTrackingConfiguration(),
                      options: [.resetTracking, .removeExistingAnchors])
```

## Gotchas

- ARKit is still present in iOS 18, but Apple's strategic direction is RealityKit + RealityView.
- visionOS does not support ARSCNView — use RealityView exclusively there.
- `ARWorldTrackingConfiguration` requires an A9 chip or later; always check `ARWorldTrackingConfiguration.isSupported`.
- Session interruptions (e.g., phone calls) require re-running the configuration to restore tracking.
- The modern replacement for complex AR is RealityKit; see `canonical/visionos.md` for spatial computing coverage.
