---
framework: Accessibility
title: "What's new in accessibility for Apple platforms"
session: WWDC24-10191
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: migration
related: []
---

## What's new

- **Animated images pause** — system-level setting lets users pause animated images (GIFs, animated SF Symbols); apps can respect `UIAccessibility.isVideoAutoplayEnabled` and the new animated image pause signal
- **Dimming effects** — new per-app dimming control in accessibility settings; apps with custom brightness should respect `UIAccessibility.isDimFlashingLightsEnabled`
- **Personal Voice API improvements** — `AVSpeechSynthesizer` now provides better access to user-created Personal Voice voices for accessibility use cases
- **Keyboard navigation improvements** — full keyboard access gains new focus system hooks; SwiftUI views can participate via `focusable()` and `onKeyPress(_:)`

## Before / After

```swift
// BEFORE: checking for reduced motion was the primary motion preference
if UIAccessibility.isReduceMotionEnabled {
    // skip animation
}

// AFTER (iOS 18): also check video autoplay for animated content
if !UIAccessibility.isVideoAutoplayEnabled {
    // pause or skip animated image/GIF playback
}
```

```swift
// Personal Voice — use with AVSpeechSynthesizer (iOS 17+ for Personal Voice;
// iOS 18 improves entitlement and discovery)
import AVFoundation

func speakWithPersonalVoice(text: String) async {
    // Request access to Personal Voice
    let status = await AVSpeechSynthesizer.requestPersonalVoiceAuthorization()
    guard status == .authorized else { return }

    let voices = AVSpeechSynthesisVoice.speechVoices().filter { $0.voiceTraits.contains(.isPersonalVoice) }
    guard let personalVoice = voices.first else { return }

    let utterance = AVSpeechUtterance(string: text)
    utterance.voice = personalVoice
    AVSpeechSynthesizer().speak(utterance)
}
```

```swift
// Keyboard navigation — SwiftUI view participating in full keyboard access
import SwiftUI

struct FocusableCard: View {
    @FocusState private var isFocused: Bool
    let title: String
    let action: () -> Void

    var body: some View {
        Text(title)
            .padding()
            .background(isFocused ? Color.accentColor.opacity(0.2) : Color.clear)
            .focusable()
            .focused($isFocused)
            .onKeyPress(.return) {
                action()
                return .handled
            }
    }
}
```

## Migration steps

1. Audit any animated image rendering (GIF players, Lottie, animated SF Symbols) — gate autoplay on `UIAccessibility.isVideoAutoplayEnabled`.
2. If your app adjusts screen brightness or applies custom dimming overlays, check `UIAccessibility.isDimFlashingLightsEnabled` and yield to the system dimming preference.
3. For apps that use text-to-speech for accessibility purposes: update to use Personal Voice where available; call `AVSpeechSynthesizer.requestPersonalVoiceAuthorization()` and filter for `.isPersonalVoice` trait.
4. Review custom interactive components for keyboard navigability: add `focusable()`, `focused(_:)`, and `onKeyPress` where users might expect keyboard interaction under Full Keyboard Access.

## Compatibility notes

- `UIAccessibility.isVideoAutoplayEnabled` is available on iOS 14+.
- `AVSpeechSynthesizer.requestPersonalVoiceAuthorization()` requires iOS 17+ and a special entitlement — apply in your app's capabilities.
- `onKeyPress(_:)` is available on iOS 17+ / macOS 14+.
- Full Keyboard Access focus improvements in iOS 18 may change focus traversal order — test existing flows with Hardware Keyboard + Full Keyboard Access enabled.
