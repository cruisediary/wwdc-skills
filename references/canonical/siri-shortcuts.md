---
framework: Siri Shortcuts
status: deprecated
applies_to: iOS 12+
shape: code-first
superseded_by: null
history:
  - year: 2018
    file: 2018/siri-shortcuts.md
    summary: "Initial introduction — NSUserActivity, INIntent, Shortcuts app"
---

## Quick start

```swift
import Intents

// Donate an NSUserActivity-based shortcut
let activity = NSUserActivity(activityType: "com.example.app.viewOrder")
activity.title = "View My Order"
activity.isEligibleForSearch = true
activity.isEligibleForPrediction = true
activity.persistentIdentifier = NSUserActivityPersistentIdentifier("viewOrder-42")
activity.suggestedInvocationPhrase = "Check my order"

// Attach to a view controller or view
self.userActivity = activity
activity.becomeCurrent()
```

> **Deprecated:** Siri Shortcuts via `NSUserActivity` / `INIntent` is superseded by the **App Intents** framework (iOS 16+). App Intents provides the same capability with a fully Swift-native API and no extension target required. See `canonical/app-intents.md` (once added to this repo).

## Key APIs

| API | Purpose |
|---|---|
| `NSUserActivity` | Signals an in-app action that can become a Siri shortcut |
| `INIntent` | Base class for custom intents defined in a `.intentdefinition` file |
| `INInteraction` | Donates an intent interaction to Siri for suggestion |
| `INVoiceShortcutButton` | System-provided UI button to add a shortcut to Siri |
| `INShortcut` | Wraps either an `NSUserActivity` or `INIntent` for donation |
| `INVoiceShortcutCenter` | Queries and manages donated shortcuts |

## Common patterns

```swift
// Donate an INIntent interaction
let intent = OrderCoffeeIntent()
intent.drink = "Flat White"
intent.suggestedInvocationPhrase = "Order my coffee"

let interaction = INInteraction(intent: intent, response: nil)
interaction.donate { error in
    if let error { print("Donation failed: \(error)") }
}

// Show the "Add to Siri" button
let shortcut = INShortcut(intent: intent)
let button = INVoiceShortcutButton(style: .whiteOutline)
button.shortcut = shortcut
button.delegate = self
view.addSubview(button)
```

## Gotchas

- App Intents (iOS 16+) is the modern replacement — no `.intentdefinition` file, no extension target, pure Swift structs conforming to `AppIntent`. Migrate when your deployment target allows.
- `INIntent`-based shortcuts require a separate Intents Extension target, which adds build complexity.
- `NSUserActivity` shortcuts are simpler but can only open the app; `INIntent` shortcuts can run in the background.
- Donated shortcuts appear in Siri Suggestions and the Shortcuts app; they require user trust before Siri can invoke them automatically.
- Siri phrase recognition quality depends on the `suggestedInvocationPhrase` — keep it short and natural-sounding.
