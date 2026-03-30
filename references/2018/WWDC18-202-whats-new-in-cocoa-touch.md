---
framework: Cocoa Touch
title: "What's New in Cocoa Touch"
session: WWDC18-202
year: 2018
applies_to: iOS 12+
status: deprecated
superseded_by: null
shape: migration
related: []
---

> **Deprecated:** This session covers WWDC18 APIs. Siri Shortcuts has been superseded by App Intents (iOS 16+); notifications and NLP improvements are part of the stable iOS 12+ baseline. Consult current Apple documentation for best practices.

## What's new

- **Siri Shortcuts** — donate `INInteraction` or `NSUserActivity` to surface app actions in Siri; users can create voice shortcuts in Settings. Full custom intents via `INIntent` subclasses with an `IntentsExtension`.
- **Grouped notifications** — `UNNotificationContent.threadIdentifier` groups related notifications in Notification Center. `UNNotificationCategory` summary format string controls the collapsed group label.
- **Natural Language framework preview** — `NLLanguageRecognizer`, `NLTokenizer`, and `NLTagger` replace `NSLinguisticTagger` with a cleaner Swift API.
- **Automatic strong passwords** — `UITextContentType.newPassword` triggers the system password generator; `.username` and `.password` enable AutoFill from iCloud Keychain.
- **Notifications improvements** — `UNNotificationRequest` with rich attachments, provisional authorization (`UNAuthorizationOptions.provisional`) delivers quietly with no prompt.
- **Performance** — scroll hitching reductions, auto-scaled rendering (`CAMetalLayer` improvements), memory footprint tooling additions.

## Before / After

**Donating a shortcut (iOS 12)**

```swift
// Donate via NSUserActivity
let activity = NSUserActivity(activityType: "com.example.viewOrder")
activity.title = "View Order #42"
activity.isEligibleForSearch = true
activity.isEligibleForPrediction = true
activity.persistentIdentifier = NSUserActivityPersistentIdentifier("order-42")
self.userActivity = activity
activity.becomeCurrent()
```

**Grouped notifications thread identifier**

```swift
let content = UNMutableNotificationContent()
content.title = "New message from Alice"
content.threadIdentifier = "chat-alice"   // groups in Notification Center
content.summaryArgument = "Alice"
```

## Migration steps

1. Replace `NSLinguisticTagger` usage with `NLTagger` / `NLLanguageRecognizer`.
2. Add `threadIdentifier` to notification content to enable grouping.
3. To adopt Siri Shortcuts, start with `NSUserActivity` donation — requires no extension; escalate to `INIntent` subclass for parameterized shortcuts.
4. Set `UITextContentType.newPassword` on password fields for automatic strong password generation.
5. Consider `UNAuthorizationOptions.provisional` to ship notifications without an upfront permission prompt.

## Compatibility notes

- Siri Shortcuts (`INIntent` + shortcut donation) requires iOS 12+. The App Intents replacement requires iOS 16+.
- `NSLinguisticTagger` is still available on iOS 12 but soft-deprecated; `NLTagger` is the preferred path.
- Grouped notifications with `threadIdentifier` work on iOS 12+ with no additional entitlement.
