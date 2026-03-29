---
framework: App Clips
status: current
applies_to: iOS 14+
shape: code-first
superseded_by: null
history:
  - year: 2020
    file: 2020/app-clips.md
    summary: App Clips introduction
---

# App Clips

Lightweight, on-demand app experiences that launch from QR codes, NFC tags, App Clip Codes, Safari banners, or Maps (iOS 14+). An App Clip is a subset of your full app, delivered instantly without a full App Store install.

## Quick start

```swift
// AppClip target's @main App entry point
import SwiftUI

@main
struct MyAppClip: App {
    @UIApplicationDelegateAdaptor private var delegate: AppDelegate

    var body: some Scene {
        WindowGroup {
            AppClipContentView()
        }
        .handlesExternalEvents(preferring: ["*"], allowing: ["*"])
    }
}

// Handle the invocation URL
struct AppClipContentView: View {
    @State private var invocationURL: URL?

    var body: some View {
        VStack {
            if let url = invocationURL {
                Text("Launched with: \(url.absoluteString)")
            }
            // Prompt to install full app
            AppClipUpgradeView()
        }
        .onContinueUserActivity(NSUserActivityTypeBrowsingWeb) { activity in
            invocationURL = activity.webpageURL
        }
    }
}

// Prompt to install the full app
import StoreKit

struct AppClipUpgradeView: View {
    var body: some View {
        Button("Get Full App") {
            let config = SKOverlay.AppClipConfiguration(position: .bottom)
            if let scene = UIApplication.shared.connectedScenes.first as? UIWindowScene {
                SKOverlay(configuration: config).present(in: scene)
            }
        }
    }
}
```

## Key APIs

| API | Purpose |
|---|---|
| App Clip target | Separate Xcode target; subset of full app, max 50 MB |
| `NSUserActivityTypeBrowsingWeb` | Receive invocation URL via `NSUserActivity` |
| `onContinueUserActivity(_:perform:)` | SwiftUI handler for incoming user activities |
| `SKOverlay.AppClipConfiguration` | Prompt to upgrade to full app |
| `SKOverlay.present(in:)` | Display the overlay in a window scene |
| App Groups | Share data between App Clip and full app via shared container |
| `_XCAppClipURL` | Environment variable for testing invocation URLs in Xcode |

## Common patterns

```swift
// Share data with full app via App Group
let defaults = UserDefaults(suiteName: "group.com.example.myapp")
defaults?.set(savedValue, forKey: "key")

// Test with a specific invocation URL in Xcode
// Edit Scheme → Run → Arguments → Environment Variables:
// _XCAppClipURL = https://example.com/clip?item=123
```

## Gotchas

- App Clips have a 50 MB size limit — only include essential assets
- Cannot use push notifications, background modes, or some entitlements in App Clips
- App Clip data is deleted after 30 days of inactivity or when the full app is installed
- Adoption has been limited — evaluate whether the user experience benefit justifies the maintenance overhead of a separate target
