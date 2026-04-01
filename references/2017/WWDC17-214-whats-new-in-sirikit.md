---
framework: SiriKit
title: "What's New in SiriKit"
session: WWDC17-214
year: 2017
applies_to: iOS 11+
status: deprecated
superseded_by: canonical/siri-shortcuts.md
shape: code-first
related: []
---

> **Deprecated:** SiriKit INIntent/INExtension API introduced in iOS 10 and extended in iOS 11. This session covers new domains (Lists & Notes, visual codes) and new Payments intents. The INIntent/INExtension approach is superseded by App Intents framework (iOS 16+).

## Quick start

```swift
// iOS 11 SiriKit Intents extension entry point
import Intents

class IntentHandler: INExtension {
    override func handler(for intent: INIntent) -> Any {
        switch intent {
        case is INSendMessageIntent:
            return SendMessageIntentHandler()
        case is INCreateNoteIntent:
            return CreateNoteIntentHandler()
        default:
            fatalError("Unhandled intent type: \(intent)")
        }
    }
}
```

## Key APIs

| Type | Role |
|---|---|
| `INExtension` | App extension entry point; routes intents to handlers |
| `INIntent` | Base class for all Siri intents |
| `INIntentHandlerProviding` | Protocol the extension conforms to for routing |
| `INCreateNoteIntent` | New in iOS 11 — create a note via Siri (Lists & Notes domain) |
| `INAddTasksIntent` | New in iOS 11 — add tasks to a list |
| `INSearchForNotebookItemsIntent` | New in iOS 11 — search notes or reminders |
| `INSendPaymentIntent` | Payments domain — send money between accounts |
| `INRequestPaymentIntent` | Payments domain — request money from a contact |
| `INVisualCodeIntent` | New in iOS 11 — present a QR or contact code |
| `INStartWorkoutIntent` | Updated — can now launch workout app in background |
| `INVocabulary` | Register user-specific vocabulary (names, workout types, etc.) |

## Common patterns

**Resolve / Confirm / Handle lifecycle**

```swift
class CreateNoteIntentHandler: NSObject, INCreateNoteIntentHandling {

    func resolveTitle(for intent: INCreateNoteIntent,
                      with completion: @escaping (INSpeakableStringResolutionResult) -> Void) {
        if let title = intent.title {
            completion(.success(with: title))
        } else {
            completion(.needsValue())
        }
    }

    func confirm(intent: INCreateNoteIntent,
                 completion: @escaping (INCreateNoteIntentResponse) -> Void) {
        completion(INCreateNoteIntentResponse(code: .ready, userActivity: nil))
    }

    func handle(intent: INCreateNoteIntent,
                completion: @escaping (INCreateNoteIntentResponse) -> Void) {
        // Perform the actual note creation
        let activity = NSUserActivity(activityType: "com.example.createnote")
        completion(INCreateNoteIntentResponse(code: .success, userActivity: activity))
    }
}
```

**Registering custom vocabulary**

```swift
// Call once at app launch
INVocabulary.shared().setVocabularyStrings(
    NSOrderedSet(array: ["Morning Run", "Evening Yoga"]),
    of: .workoutActivityName
)
```

**Background workout launch (new in iOS 11)**

```swift
// Info.plist: add INStartWorkoutIntent to NSExtension > NSExtensionAttributes > IntentsSupported
// Handler can now complete without requiring the app to foreground
func handle(intent: INStartWorkoutIntent,
            completion: @escaping (INStartWorkoutIntentResponse) -> Void) {
    completion(INStartWorkoutIntentResponse(code: .handleInApp, userActivity: nil))
}
```

## Gotchas

- Add `NSSiriUsageDescription` to your main app's `Info.plist`; the system will prompt for permission before the first Siri interaction.
- Each supported intent must be declared under `NSExtension > NSExtensionAttributes > IntentsSupported` in the Intents extension's `Info.plist`.
- `INVocabulary` entries are per-user and stored on-device; call `removeAllVocabulary()` on sign-out.
- Background workout launch requires `IntentsRestrictedWhileLocked` to be absent or to explicitly allow the intent while locked.
- The INIntent/INExtension pattern is deprecated — prefer App Intents framework (iOS 16+) for new development.
