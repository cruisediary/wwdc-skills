---
framework: App Clips
session: WWDC20-10174
year: 2020
applies_to: iOS 14+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/app-clips.md
---

# App Clips — WWDC20 Introduction

App Clips were introduced at WWDC20 as lightweight, instantly-launchable app experiences.

## What's new

- App Clip target — separate Xcode target, subset of the full app
- Invocation via QR codes, NFC tags, App Clip Codes, Safari Smart App Banners, iMessage, Maps
- `NSUserActivity` with `NSUserActivityTypeBrowsingWeb` — carries the invocation URL
- `SKOverlay` — prompt to install the full app from within the App Clip
- App Groups — share data between App Clip and full app
- 10 MB initial size limit (raised to 50 MB later)
- `_XCAppClipURL` environment variable for testing

## Before / After

App Clips are a new capability, not a migration from a prior API. There is no direct predecessor — the alternative was requiring a full App Store install before providing any experience.

**New capability:**
```swift
// User scans QR code → App Clip launches instantly
// App Clip handles the URL:
struct ClipView: View {
    var body: some View {
        Text("App Clip Experience")
            .onContinueUserActivity(NSUserActivityTypeBrowsingWeb) { activity in
                let url = activity.webpageURL
                // load experience based on url
            }
    }
}
```

## Migration steps

1. Add a new "App Clip" target to your Xcode project
2. Share code/frameworks between main app and App Clip targets as needed
3. Add `NSAppClip` dictionary to App Clip's Info.plist with invocation URLs
4. Handle `NSUserActivity` in the App Clip's entry point to receive the URL
5. Add `SKOverlay` to prompt upgrade to full app
6. Configure App Groups if the App Clip needs to share data with the full app

## Compatibility notes

- Requires iOS 14+
- App Clip size: 50 MB limit (was 10 MB at launch)
- Cannot use: Push Notifications (directly), background refresh, certain entitlements
- App Clip card and invocation URLs must be configured in App Store Connect
