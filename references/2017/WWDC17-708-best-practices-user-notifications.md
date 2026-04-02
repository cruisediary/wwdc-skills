---
framework: UserNotifications
title: "Best Practices and What's New in User Notifications"
session: WWDC17-708
year: 2017
applies_to: iOS 11+
status: reference-only
superseded_by: null
shape: code-first
related: []
---

> **Reference-only (iOS 11+):** UserNotifications APIs shown here remain current in iOS 18. This session covers notification management, grouped notifications groundwork, and best practices for the `UNUserNotificationCenter` model introduced in iOS 10.

## Quick start

```swift
import UserNotifications

// Request authorization
UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .sound, .badge]) { granted, error in
    guard granted else { return }
    DispatchQueue.main.async {
        UIApplication.shared.registerForRemoteNotifications()
    }
}

// Schedule a local notification
let content = UNMutableNotificationContent()
content.title = "Reminder"
content.body = "Don't forget your meeting."
content.sound = .default

let trigger = UNTimeIntervalNotificationTrigger(timeInterval: 60, repeats: false)
let request = UNNotificationRequest(identifier: "meeting-reminder", content: content, trigger: trigger)
UNUserNotificationCenter.current().add(request)
```

## Key APIs

| Type | Role |
|---|---|
| `UNUserNotificationCenter` | Central object for managing notification permissions, delivery, and handling |
| `UNNotificationRequest` | Combines content + trigger into a schedulable unit |
| `UNMutableNotificationContent` | Configurable notification payload (title, body, sound, badge, userInfo, attachments) |
| `UNNotificationTrigger` | Abstract base; concrete types: `UNTimeIntervalNotificationTrigger`, `UNCalendarNotificationTrigger`, `UNLocationNotificationTrigger` |
| `UNNotificationAction` | Actionable button shown in the notification (foreground or background) |
| `UNNotificationCategory` | Groups a set of actions and registers them with the notification center |
| `UNNotificationAttachment` | Attaches media (image, audio, video) to a notification |
| `UNNotificationServiceExtension` | App extension that can modify a remote notification payload before delivery |
| `UNNotificationContentExtension` | App extension that provides a custom notification UI |
| `UNUserNotificationCenterDelegate` | Callbacks for foreground delivery and action handling |

## Common patterns

**Actionable notifications**

```swift
// Register a category with actions
let replyAction = UNTextInputNotificationAction(
    identifier: "REPLY_ACTION",
    title: "Reply",
    options: [],
    textInputButtonTitle: "Send",
    textInputPlaceholder: "Type a message…"
)
let category = UNNotificationCategory(
    identifier: "MESSAGE_CATEGORY",
    actions: [replyAction],
    intentIdentifiers: [],
    options: []
)
UNUserNotificationCenter.current().setNotificationCategories([category])

// On the remote notification payload, set: "category": "MESSAGE_CATEGORY"
```

**Handling foreground notifications**

```swift
class AppDelegate: UIResponder, UIApplicationDelegate, UNUserNotificationCenterDelegate {
    func userNotificationCenter(_ center: UNUserNotificationCenter,
                                willPresent notification: UNNotification,
                                withCompletionHandler completionHandler: @escaping (UNNotificationPresentationOptions) -> Void) {
        // Show banner + play sound even when app is in foreground
        completionHandler([.banner, .sound])
    }
}
```

**Notification Service Extension (modify remote payload)**

```swift
class NotificationService: UNNotificationServiceExtension {
    override func didReceive(_ request: UNNotificationRequest,
                             withContentHandler contentHandler: @escaping (UNNotificationContent) -> Void) {
        guard let mutable = request.content.mutableCopy() as? UNMutableNotificationContent,
              let urlString = mutable.userInfo["attachment-url"] as? String,
              let url = URL(string: urlString) else {
            contentHandler(request.content)
            return
        }
        // Download and attach media
        downloadAttachment(from: url) { attachment in
            if let attachment { mutable.attachments = [attachment] }
            contentHandler(mutable)
        }
    }
}
```

**Cancelling and updating pending notifications**

```swift
// Remove specific pending requests
UNUserNotificationCenter.current().removePendingNotificationRequests(withIdentifiers: ["meeting-reminder"])

// Update by re-adding with same identifier
let updatedRequest = UNNotificationRequest(identifier: "meeting-reminder", content: newContent, trigger: newTrigger)
UNUserNotificationCenter.current().add(updatedRequest)
```

## Gotchas

- `UNNotificationServiceExtension` only runs for remote notifications that include `"mutable-content": 1` in the APNs payload.
- The service extension has a limited execution window (~30 seconds); call `contentHandler` as early as possible and implement `serviceExtensionTimeWillExpire` for cleanup.
- `UNNotificationContentExtension` requires the notification's category identifier to match the extension's declared category in `Info.plist`.
- Notification attachments must be downloaded to disk before being passed to `UNNotificationAttachment(identifier:url:options:)`.
- Requesting `.criticalAlert` authorization (added in iOS 12) requires a special entitlement from Apple.
- Always check the `authorizationStatus` via `getNotificationSettings` before scheduling — the user may have denied permission after initial grant.
