---
framework: App Intents
title: "Design App Intents for system experiences"
session: WWDC24-10176
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/siri-shortcuts.md
---

## What changed and why

Before iOS 18, App Intents adoption was largely optional and app-centric — intents lived inside the app's own Shortcuts configuration. iOS 18 expands the surface area to the Action button, Apple Intelligence, and the Shortcuts widget, which means poorly designed intents become prominently visible to users. This session is a design guide for building intents that feel native across all system entry points.

## Mental model

**An App Intent is a contract, not a function call.** The system (Siri, Shortcuts, Action button) may invoke it at any time with minimal context. Design around three questions:

1. **When should this be an intent?** Only actions the user would plausibly initiate without opening the app. Avoid intents that require prior navigation state.
2. **What is the right granularity?** One intent per discrete user goal — not one intent per screen. Combine related parameters rather than splitting into many narrow intents.
3. **What does the user understand?** Titles and parameter names must be plain language. Avoid technical or internal terminology.

## Usage

### Choosing when to use App Intents

| Use App Intents when… | Avoid App Intents when… |
|---|---|
| The action has a clear, stateless trigger | The action requires sequential UI navigation |
| The result is immediately meaningful to the user | The action is primarily configuration or settings |
| The action can be expressed in one imperative phrase | Multiple prior decisions are required |

### Naming conventions

```swift
// Good: verb + noun, plain language
struct CreateNoteIntent: AppIntent {
    static var title: LocalizedStringResource = "Create Note"
}

// Bad: internal name, unclear scope
struct NoteComposerLaunchIntent: AppIntent {
    static var title: LocalizedStringResource = "Launch Note Composer"
}
```

### Entity design

- Entity display names should be what the user calls the thing, not what the data model calls it.
- Provide a `defaultQuery` that returns results fast — Siri shows a loading state if entity resolution is slow.
- Limit entity parameters to the minimum needed; Siri will ask follow-up questions for optional ones.

```swift
// Entity with a human-readable display representation
struct NoteEntity: AppEntity {
    static var typeDisplayRepresentation: TypeDisplayRepresentation = "Note"
    var displayRepresentation: DisplayRepresentation {
        DisplayRepresentation(title: "\(title)")
    }
    // see Apple docs for EntityQuery conformance details
    static var defaultQuery = NoteQuery()
    var id: UUID
    var title: String
}
```

### Action button integration

- Register intents for the Action button by adding them to `AppShortcutsProvider.appShortcuts`.
- Keep Action button intents to single, instant actions — the Action button has no follow-up UI by default.
- Use `.openAppWhenRun = false` where possible so the action completes without launching the app.

```swift
struct MyShortcuts: AppShortcutsProvider {
    static var appShortcuts: [AppShortcut] {
        AppShortcut(
            intent: CreateNoteIntent(),
            phrases: ["Create a note in \(.applicationName)"],
            shortTitle: "Create Note",
            systemImageName: "square.and.pencil"
        )
    }
    static var shortcutTileColor: ShortcutTileColor = .green
}
```

## Adopting this pattern

If you have existing `INIntent` (SiriKit) intents:

1. Map each `INIntent` to an `AppIntent` with an equivalent schema or plain title.
2. Replace `INInteraction.donate(_:)` calls with `AppShortcutsProvider` — donation is automatic.
3. Audit parameter titles: replace any snake_case or camelCase titles with sentence-style plain language.
4. Test each intent from Shortcuts, the Action button settings screen, and via Siri voice — these three surfaces have different UI constraints.
