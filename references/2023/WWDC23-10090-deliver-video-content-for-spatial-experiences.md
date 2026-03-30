---
framework: RealityKit
title: "Deliver video content for spatial experiences"
session: WWDC23-10090
year: 2023
applies_to: visionOS 1+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/visionos.md
---

# Deliver video content for spatial experiences (WWDC23)

How to play 2D and spatial (3D) video on visionOS using `VideoPlayerComponent`, `AVPlayer`, and spatial audio.

## What changed and why

visionOS introduces a new `VideoPlayerComponent` in RealityKit that lets you attach an `AVPlayer` to an entity and play video in 3D space. The system handles rendering into the RealityKit scene with correct depth and lighting. For fully immersive playback in a virtual environment, use `AVPlayerViewController` inside an `ImmersiveSpace`.

## Mental model

- **Inline spatial video** — Attach `VideoPlayerComponent` to a `ModelEntity` (a flat plane) to embed video in your 3D scene. The video renders as a texture on the entity.
- **Immersive playback** — Use `AVPlayerViewController` inside an `ImmersiveSpace` for cinema-style experiences. The system renders the video filling a virtual screen in the user's space.
- **Spatial audio** — visionOS renders audio sources in 3D space. Attach audio to an entity position so sound comes from where the video appears. Use `AVAudioSession` for spatial mixing preferences.
- **Video formats** — Standard H.264/HEVC for 2D; MV-HEVC (Multi-View HEVC) for spatial (3D) video.

## Usage

**Attaching video to a plane entity:**
```swift
import RealityKit
import AVFoundation

// Create a flat plane entity for the video screen
let screenMesh = MeshResource.generatePlane(width: 1.6, height: 0.9)  // 16:9
let screenMaterial = VideoMaterial(avPlayer: player)
let screenEntity = ModelEntity(mesh: screenMesh, materials: [screenMaterial])
screenEntity.position = [0, 1.5, -2]  // 2m forward, eye height

// Alternatively use VideoPlayerComponent
var videoPlayer = VideoPlayerComponent(avPlayer: player)
screenEntity.components[VideoPlayerComponent.self] = videoPlayer
content.add(screenEntity)

// Start playback
player.play()
```

**Setting up an AVPlayer:**
```swift
let url = Bundle.main.url(forResource: "intro", withExtension: "mp4")!
let player = AVPlayer(url: url)
```

**Immersive video playback (AVPlayerViewController):**
```swift
// In a SwiftUI view inside an ImmersiveSpace
struct ImmersiveVideoView: View {
    let player: AVPlayer

    var body: some View {
        VideoPlayer(player: player)
            .frame(width: 1920, height: 1080)
    }
}
```

**Spatial audio from the video entity:**
```swift
// Audio from a VideoMaterial is automatically spatialized at the entity's position.
// For additional spatial audio cues, attach a SpatialAudioComponent:
var spatialAudio = SpatialAudioComponent()
spatialAudio.gain = 0  // 0 dB
screenEntity.components[SpatialAudioComponent.self] = spatialAudio
```

**Controlling playback rate and looping:**
```swift
player.rate = 1.0
// Loop via NotificationCenter
NotificationCenter.default.addObserver(forName: .AVPlayerItemDidPlayToEndTime,
                                       object: player.currentItem, queue: .main) { _ in
    player.seek(to: .zero)
    player.play()
}
```

## Adopting this pattern

1. Use `VideoMaterial(avPlayer:)` to render video as a texture on any `ModelEntity` plane.
2. Use `VideoPlayerComponent` for more control over playback state and to receive playback events from RealityKit.
3. For full-screen immersive cinema playback, add an `AVPlayerViewController` or SwiftUI `VideoPlayer` inside an `ImmersiveSpace`.
4. Let the system spatialize audio automatically — audio from a `VideoMaterial` entity is rendered at the entity's world position.
5. Use MV-HEVC-encoded video for true spatial (3D) content on visionOS.
