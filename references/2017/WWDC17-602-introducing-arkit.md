---
framework: ARKit
title: "Introducing ARKit: Augmented Reality for iOS"
session: WWDC17-602
year: 2017
applies_to: iOS 11+
status: deprecated
superseded_by: canonical/arkit.md
shape: code-first
related:
  - canonical/arkit.md
---

> **Deprecated:** ARKit 1.0 introduced in iOS 11. The ARAnchor/ARSession model remains in iOS 18, but new projects should use RealityKit + RealityComposerPro. See `canonical/arkit.md`.

## Quick start

```swift
import ARKit

class ViewController: UIViewController, ARSCNViewDelegate {
    @IBOutlet var sceneView: ARSCNView!

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        let configuration = ARWorldTrackingConfiguration()
        configuration.planeDetection = .horizontal
        sceneView.session.run(configuration)
    }

    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        sceneView.session.pause()
    }
}
```

## Key APIs

| Type | Role |
|---|---|
| `ARSession` | Central object that manages motion tracking and camera capture |
| `ARWorldTrackingConfiguration` | 6DOF tracking with plane detection and image anchors |
| `ARAnchor` | Named position+orientation in world space |
| `ARPlaneAnchor` | Detected horizontal surface; has `center` and `extent` |
| `ARFrame` | Snapshot of camera image + tracking state from `session.currentFrame` |
| `ARSCNView` | SceneKit view with AR camera feed; auto-maps ARAnchor → SCNNode |
| `ARSKView` | SpriteKit view with AR camera feed |

## Common patterns

**Add a virtual object on plane detection**

```swift
func renderer(_ renderer: SCNSceneRenderer, didAdd node: SCNNode, for anchor: ARAnchor) {
    guard let planeAnchor = anchor as? ARPlaneAnchor else { return }
    let plane = SCNPlane(width: CGFloat(planeAnchor.extent.x),
                         height: CGFloat(planeAnchor.extent.z))
    let planeNode = SCNNode(geometry: plane)
    planeNode.position = SCNVector3(planeAnchor.center.x, 0, planeAnchor.center.z)
    planeNode.eulerAngles.x = -.pi / 2
    node.addChildNode(planeNode)
}
```

**Hit-test for surface placement**

```swift
let results = sceneView.hitTest(tapLocation, types: .existingPlaneUsingExtent)
if let result = results.first {
    let transform = result.worldTransform
    let position = SCNVector3(transform.columns.3.x,
                              transform.columns.3.y,
                              transform.columns.3.z)
    // place anchor at position
}
```

## Gotchas

- `ARWorldTrackingConfiguration` requires an A9 chip or later. Check `ARWorldTrackingConfiguration.isSupported` before running.
- Plane detection only finds horizontal surfaces in ARKit 1.0. Vertical plane detection was added in ARKit 1.5 (iOS 11.3).
- Lighting estimation is opt-in: set `configuration.isLightEstimationEnabled = true`. Access via `frame.lightEstimate?.ambientIntensity`.
- Never mutate `ARFrame` data off the main thread; it is invalidated each frame.
