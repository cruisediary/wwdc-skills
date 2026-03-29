---
framework: Siri Shortcuts
session: WWDC18-211
year: 2018
applies_to: iOS 12+
status: deprecated
superseded_by: canonical/siri-shortcuts.md
shape: migration
related:
  - canonical/siri-shortcuts.md
---

## What's new

- **Siri Shortcuts** — new system that lets apps expose discrete actions to Siri and the Shortcuts app.
- **NSUserActivity donation** — simplest path: mark an `NSUserActivity` as eligible for prediction; Siri surfaces it as a suggestion.
- **Custom INIntent** — define rich, parameterized intents in an `.intentdefinition` file; an Intents Extension handles background execution.
- **Shortcuts app** — new first-party app (shipped with iOS 12) where users build automation workflows using donated shortcuts.
- **INVoiceShortcutButton** — system button that lets users add "Hey Siri, <phrase>" directly from your app.
- **Suggested invocation phrase** — app provides a hint phrase; user can customise it in the Shortcuts app.

## Before / After

**Before — no shortcut donation (iOS 11 and earlier)**

```swift
// Apps had no way to expose actions to Siri (except SiriKit domains)
// or let users invoke app features with a custom voice phrase.
// The only Siri integration was via predefined SiriKit intents
// (messaging, payments, etc.) with no custom phrases.
```

**After — NSUserActivity donation (iOS 12)**

```swift
import Intents

// Simplest form: donate via NSUserActivity
let activity = NSUserActivity(activityType: "com.example.app.viewRecipe")
activity.title = "View Chocolate Cake Recipe"
activity.isEligibleForSearch = true
activity.isEligibleForPrediction = true
activity.suggestedInvocationPhrase = "Show my recipe"
self.userActivity = activity
activity.becomeCurrent()
```

**After — custom INIntent with background handling (iOS 12)**

```swift
// 1. Define OrderSoupIntent in .intentdefinition
// 2. Intents Extension handler:
class OrderSoupIntentHandler: NSObject, OrderSoupIntentHandling {
    func handle(intent: OrderSoupIntent,
                completion: @escaping (OrderSoupIntentResponse) -> Void) {
        // Fulfill the order without opening the app
        completion(OrderSoupIntentResponse(code: .success, userActivity: nil))
    }
}

// 3. Donate the intent from the app
let intent = OrderSoupIntent()
intent.soup = "Tomato"
let interaction = INInteraction(intent: intent, response: nil)
interaction.donate(completion: nil)
```

## Migration steps

1. Update deployment target to iOS 12+.
2. Choose a donation strategy:
   - **NSUserActivity** (simpler): set `isEligibleForPrediction = true` and `suggestedInvocationPhrase` on existing activities.
   - **Custom INIntent** (richer): create an `.intentdefinition` file, add an Intents Extension target, implement the handler protocol.
3. Add `INVoiceShortcutButton` to relevant screens so users can add the shortcut to Siri.
4. Register your shortcuts in `Info.plist`: add `NSUserActivityTypes` (array of activity type strings) to the **main app's** `Info.plist` at the root level; add intent class names to the **Intents Extension's** `Info.plist` under the `NSExtension` → `NSExtensionAttributes` → `IntentsSupported` key.
5. Test in the Shortcuts app — donated shortcuts appear under your app in the Shortcuts gallery.

> For new projects targeting iOS 16+, use App Intents instead. See `canonical/siri-shortcuts.md`.

## Compatibility notes

- Siri Shortcuts require iOS 12+; the Shortcuts app is pre-installed on iOS 13+ and available as a free download on iOS 12.
- Custom `INIntent` background execution requires an Intents Extension (separate process); `NSUserActivity` shortcuts always open the app.
- Donated shortcuts persist across app updates but are cleared when the app is deleted.
- The App Intents framework (iOS 16+) is the strategic replacement — it requires no extension target and uses Swift concurrency for background execution.
