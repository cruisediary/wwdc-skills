---
framework: App Intents
title: "Bring your app to Siri"
session: WWDC24-10133
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/siri-shortcuts.md
---

## Quick start

```swift
import AppIntents

// 1. Conform your intent to a domain-specific AssistantSchema
@AssistantIntent(schema: .photos.search)
struct SearchPhotosIntent: AppIntent {
    static var title: LocalizedStringResource = "Search Photos"

    @Parameter(title: "Query") var searchQuery: String

    func perform() async throws -> some ReturnsValue<[PhotoEntity]> {
        let results = try await PhotoLibrary.search(query: searchQuery)
        return .result(value: results)
    }
}

// 2. Expose a SiriTip in your UI to teach users the phrase
import SwiftUI

struct PhotoSearchView: View {
    var body: some View {
        VStack {
            // Shows the canonical Siri phrase for this intent
            SiriTipView(intent: SearchPhotosIntent())
                .padding()
            PhotoGrid()
        }
    }
}
```

## Key APIs

| API | Purpose |
|---|---|
| `@AssistantIntent(schema:)` | Binds an `AppIntent` to an Apple-defined domain schema so Siri understands it without custom utterances |
| `AssistantSchema` | Namespace of pre-defined domain schemas (`.photos`, `.mail`, `.browser`, `.files`, etc.) |
| `SiriTipView` | SwiftUI view that displays the canonical Siri phrase for an intent, educating users |
| `SiriTipUIView` (UIKit) | UIKit view that displays the canonical Siri phrase for an intent; use `SiriTipUIView(intent:)` and add to the view hierarchy directly |
| `AppEntity` | Protocol for domain objects Siri can reference (e.g., a photo, a contact) |
| `@Parameter` | Declares an intent input that Siri can fill through voice or follow-up questions |
| `AppShortcutsProvider` | Conform to this protocol to expose shortcuts; App Intents handles donation automatically — no manual donation call needed |

## Common patterns

```swift
// Pattern 1: Multi-parameter intent with an AppEntity result
@AssistantIntent(schema: .mail.sendMessage)
struct SendMailIntent: AppIntent {
    @Parameter(title: "Recipient") var recipient: PersonEntity
    @Parameter(title: "Subject")   var subject: String
    @Parameter(title: "Body")      var body: String

    func perform() async throws -> some ProvidesDialog {
        try await MailComposer.send(to: recipient, subject: subject, body: body)
        return .result(dialog: "Message sent to \(recipient.name).")
    }
}

// Pattern 2: UIKit — show a SiriTip in a view controller
import AppIntents

class PhotoViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        let tipView = SiriTipUIView(intent: SearchPhotosIntent())
        view.addSubview(tipView)
    }
}
```

## Gotchas

- `@AssistantIntent` requires the intent to exactly satisfy the schema's required parameters — missing a required `@Parameter` causes a compile-time error
- Domain schemas are curated by Apple; you cannot define custom schemas — pick the closest built-in domain or fall back to a plain `AppIntent`
- `SiriTipView` (SwiftUI) and `SiriTipUIView` (UIKit) only render when the system determines the tip is relevant; they may show nothing in certain conditions (e.g., the user has already added the shortcut)
- Donation is automatic when you conform to `AppShortcutsProvider` — do not call any manual donation API; there is no `IntentDonationManager` in App Intents
- Test Siri integration on a real device with a signed-in Apple ID; the Simulator has limited Siri support
- `AppEntity` objects must implement `defaultQuery` returning an `EntityQuery` — omitting this prevents Siri from resolving entity references by voice
