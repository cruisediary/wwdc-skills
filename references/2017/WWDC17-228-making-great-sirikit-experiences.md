---
framework: SiriKit
title: "Making Great SiriKit Experiences"
session: WWDC17-228
year: 2017
applies_to: iOS 11+
status: deprecated
superseded_by: canonical/siri-shortcuts.md
shape: code-first
related: []
---

> **Deprecated:** Best-practice guidance for the SiriKit INIntent/INExtension model (iOS 10–15). Covers contact resolution, security, custom vocabulary, and UI. Superseded by App Intents framework (iOS 16+).

## Quick start

```swift
// Three-step intent lifecycle: resolve → confirm → handle
// Each step gives you a chance to gather info, validate state, and execute.
class SendMessageIntentHandler: NSObject, INSendMessageIntentHandling {

    func resolveRecipients(for intent: INSendMessageIntent,
                           with completion: @escaping ([INPersonResolutionResult]) -> Void) {
        guard let recipients = intent.recipients, !recipients.isEmpty else {
            completion([.needsValue()])
            return
        }
        // Disambiguate if multiple matches found
        completion(recipients.map { .success(with: $0) })
    }

    func confirm(intent: INSendMessageIntent,
                 completion: @escaping (INSendMessageIntentResponse) -> Void) {
        completion(INSendMessageIntentResponse(code: .ready, userActivity: nil))
    }

    func handle(intent: INSendMessageIntent,
                completion: @escaping (INSendMessageIntentResponse) -> Void) {
        // Perform the send, then report result
        completion(INSendMessageIntentResponse(code: .success, userActivity: nil))
    }
}
```

## Key APIs

| Type | Role |
|---|---|
| `INPersonResolutionResult` | Resolution outcome for a contact parameter (success, disambiguation, needsValue, unsupported) |
| `INSpeakableStringResolutionResult` | Resolution outcome for a free-form string |
| `INIntentResolutionResult` | Base class for all resolution results |
| `INVocabulary` | Register app-specific and user-specific terms Siri should recognize |
| `INVocabularyStringType` | Enum of vocabulary categories (contact names, workout names, payment method names, etc.) |
| `INUIHostedViewControlling` | Protocol for the custom Siri UI view controller in the IntentsUI extension |
| `INParameter` | Identifies a specific parameter within an intent for targeted UI customization |
| `LAContext` | Use with `evaluatePolicy(_:localizedReason:)` to require device authentication before handling sensitive intents |

## Common patterns

**Contact resolution with disambiguation**

```swift
func resolveRecipients(for intent: INSendMessageIntent,
                       with completion: @escaping ([INPersonResolutionResult]) -> Void) {
    var results: [INPersonResolutionResult] = []
    for recipient in intent.recipients ?? [] {
        let matches = lookUpContacts(matching: recipient)
        switch matches.count {
        case 0:
            results.append(.unsupported())
        case 1:
            results.append(.success(with: matches[0]))
        default:
            results.append(.disambiguation(with: matches))
        }
    }
    completion(results)
}
```

**Requiring device authentication for sensitive intents**

```swift
func confirm(intent: INSendPaymentIntent,
             completion: @escaping (INSendPaymentIntentResponse) -> Void) {
    let context = LAContext()
    context.evaluatePolicy(.deviceOwnerAuthentication,
                           localizedReason: "Authenticate to send payment") { success, _ in
        DispatchQueue.main.async {
            completion(INSendPaymentIntentResponse(
                code: success ? .ready : .failureRequiringAppLaunch,
                userActivity: nil))
        }
    }
}
```

**Registering custom vocabulary**

```swift
// Per-app vocabulary (same for all users) — set in AppIntentVocabulary.plist
// Per-user vocabulary — register at runtime:
INVocabulary.shared().setVocabularyStrings(
    NSOrderedSet(array: ["Checking", "Savings"]),
    of: .paymentAccountNickname
)
```

**Custom Siri UI (IntentsUI extension)**

```swift
class IntentViewController: UIViewController, INUIHostedViewControlling {
    func configureView(for parameters: Set<INParameter>,
                       of interaction: INInteraction,
                       interactiveBehavior: INUIInteractiveBehavior,
                       context: INUIHostedViewContext,
                       completion: @escaping (Bool, Set<INParameter>, CGSize) -> Void) {
        // Populate views from interaction.intent
        let desiredSize = CGSize(width: self.extensionContext!.hostedViewMaximumAllowedSize.width,
                                 height: 120)
        completion(true, parameters, desiredSize)
    }
}
```

## Gotchas

- Disambiguation presents a list to the user in Siri; keep displayed strings short and unambiguous.
- `INVocabularyStringType.contactName` vocabulary is scoped to the user and cleared when the user signs out — call `removeAllVocabulary()`.
- Authentication in `confirm` must complete quickly; Siri may time out if the biometric prompt takes too long.
- Custom Siri UI only displays for the `handle` phase; you cannot show UI during `resolve` or `confirm`.
- UI tests for SiriKit extensions can drive the Intents extension directly using `INInteraction` — faster than invoking Siri manually.
- The INIntent/INExtension approach is deprecated — prefer App Intents framework (iOS 16+) for new development.
