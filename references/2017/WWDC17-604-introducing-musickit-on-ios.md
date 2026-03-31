---
framework: MusicKit
title: "Introducing MusicKit on iOS"
session: WWDC17-604
year: 2017
applies_to: iOS 11+
status: reference-only
superseded_by: null
shape: code-first
related: []
---

> **Reference-only (iOS 11+):** The original StoreKit-based MusicKit APIs from iOS 11. In WWDC21, Apple introduced a Swift-native MusicKit framework. For new projects use the Swift MusicKit framework; this session documents `SKCloudServiceController` and `MPMusicPlayerController`.

## Quick start

```swift
import StoreKit

SKCloudServiceController.requestAuthorization { status in
    guard status == .authorized else { return }
    let controller = SKCloudServiceController()
    controller.requestCapabilities { capabilities, error in
        if capabilities.contains(.musicCatalogPlayback) {
            // user has Apple Music subscription
        }
    }
}
```

## Key APIs

| Type | Role |
|---|---|
| `SKCloudServiceController` | Request authorization and check Apple Music capabilities |
| `SKCloudServiceCapability` | Bitmask: `.musicCatalogPlayback`, `.addToCloudMusicLibrary` |
| `MPMusicPlayerController` | System music player; `systemMusicPlayer` plays in Apple Music queue |
| `SKCloudServiceSetupViewController` | Presents Apple Music subscription offer |

## Common patterns

**Play a catalog item**

```swift
let player = MPMusicPlayerController.systemMusicPlayer
player.setQueue(with: ["catalogTrackID"])
player.play()
```

## Gotchas

- `SKCloudServiceController.requestAuthorization` must be called before any capability check; authorization persists across app launches.
- Add `NSAppleMusicUsageDescription` to `Info.plist`.
- The Swift-native `MusicKit` framework (WWDC21+) provides a completely different, more ergonomic API — prefer it for new development.
