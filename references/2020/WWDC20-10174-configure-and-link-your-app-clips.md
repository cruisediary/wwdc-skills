---
framework: App Clips
title: "Configure and link your app clips"
session: WWDC20-10174
year: 2020
applies_to: iOS 14+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/app-clips.md
---

# Configure and link your app clips

Covers the full invocation pipeline for App Clips: URL configuration, `NSUserActivity` handling, `SKOverlay`, and Sign in with Apple.

## Quick start

```swift
import SwiftUI

@main
struct MyAppClip: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .onContinueUserActivity(NSUserActivityTypeBrowsingWeb) { activity in
                    guard let url = activity.webpageURL else { return }
                    handleInvocation(url: url)
                }
        }
    }
}

func handleInvocation(url: URL) {
    // Parse the URL to determine which experience to show
    // e.g., url.path == "/order/42"
}
```

## Key APIs

| API | Description |
|---|---|
| `NSUserActivity` | Carries the invocation URL; activity type is `NSUserActivityTypeBrowsingWeb` |
| `activity.webpageURL` | The URL that triggered the App Clip launch |
| `SKOverlay` | Presents a non-modal banner to install the full app |
| `SKOverlay.AppClipConfiguration` | Configuration for the overlay within an App Clip |
| `SKOverlay(configuration:)` | Creates the overlay |
| `overlay.present(in:)` | Shows the overlay in a `UIWindow` / `SKScene` |
| `overlay.dismiss(animated:)` | Hides the overlay |
| `ASAuthorizationAppleIDButton` | Sign in with Apple button (usable in App Clips) |
| `NSAppClip` (Info.plist key) | Dictionary with `NSAppClipRequestEphemeralUserNotification` and `NSAppClipRequestLocationConfirmation` |

## Common patterns

**Showing SKOverlay to upgrade to full app:**
```swift
import StoreKit

func showUpgradeOverlay(in scene: UIWindowScene) {
    let config = SKOverlay.AppClipConfiguration(position: .bottom)
    let overlay = SKOverlay(configuration: config)
    overlay.present(in: scene)
}
```

**Dismissing the overlay on a specific action:**
```swift
func userCompletedPurchase(in scene: UIWindowScene) {
    SKOverlay.dismiss(in: scene)
}
```

**Sign in with Apple in SwiftUI (App Clip):**
```swift
import AuthenticationServices

struct SignInView: View {
    var body: some View {
        SignInWithAppleButton(
            .signIn,
            onRequest: { request in
                request.requestedScopes = [.fullName, .email]
            },
            onCompletion: { result in
                switch result {
                case .success(let auth):
                    // handle credential
                    break
                case .failure(let error):
                    print(error)
                }
            }
        )
        .frame(height: 44)
    }
}
```

**Testing invocation URL locally:**
```
# Set _XCAppClipURL in the scheme's environment variables
_XCAppClipURL = https://example.com/order/42
```

**Requesting ephemeral notification permission (Info.plist):**
```xml
<key>NSAppClip</key>
<dict>
    <key>NSAppClipRequestEphemeralUserNotification</key>
    <true/>
</dict>
```

## Gotchas

- App Clip invocation URLs must be registered in App Store Connect under "App Clip Experiences"
- The associated domain `appclips:` entitlement must be added to both the App Clip and the full app targets
- App Clips cannot use Push Notifications (only ephemeral notifications via `NSAppClipRequestEphemeralUserNotification`)
- App Clip size limit is 50 MB (was 10 MB at launch in iOS 14.0)
- `SKOverlay` is `StoreKit` — import it separately; it is not part of UIKit or SwiftUI
- Data sharing between App Clip and full app requires an App Group entitlement
- `NSUserActivityTypeBrowsingWeb` is the activity type for all App Clip invocations via URL
