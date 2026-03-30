---
framework: App Intents
title: "What's new in App Intents"
session: WWDC24-10134
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/siri-shortcuts.md
---

## What's new

- `@AssistantSchemas` macro applies multiple schema bindings to an `AppIntent` at once
- `AppShortcutsProvider.shortcutTileColor` lets you tint the shortcut tile in the Shortcuts app
- `IntentParameter` supports predicate filters so Siri can narrow entity queries before presenting options
- `OpenURLIntent` opens a URL from within an `AppIntent`, replacing any need for a hypothetical `UniversalLink` action

## Before / After

```swift
// BEFORE (iOS 17): bind one schema at a time, no tile color
@AssistantIntent(schema: .photos.search)
struct SearchPhotosIntent: AppIntent { … }

struct MyShortcuts: AppShortcutsProvider {
    static var appShortcuts: [AppShortcut] { … }
    // No tile color customization available
}

// AFTER (iOS 18): bind multiple schemas with @AssistantSchemas, add tile color
@AssistantSchemas(.photos.search, .files.search)
struct SearchContentIntent: AppIntent {
    static var title: LocalizedStringResource = "Search Content"
    @Parameter(title: "Query") var query: String

    func perform() async throws -> some ReturnsValue<[ContentEntity]> {
        // see Apple docs for exact return type usage
        let results = try await ContentStore.search(query: query)
        return .result(value: results)
    }
}

struct MyShortcuts: AppShortcutsProvider {
    static var appShortcuts: [AppShortcut] { … }
    static var shortcutTileColor: ShortcutTileColor = .blue
}
```

```swift
// Opening a URL from an AppIntent: use the system-provided OpenURLIntent
// which handles routing correctly in Siri/Shortcuts extension contexts
// Note: UIApplication.shared is unavailable in intent extensions — use OpenURLIntent instead
// See Apple docs: https://developer.apple.com/documentation/appintents/openurlintent
```

## Migration steps

1. Replace multiple `@AssistantIntent` declarations that share a type with a single `@AssistantSchemas(…)` macro call.
2. Set `AppShortcutsProvider.shortcutTileColor` to match your app's brand color.
3. To open a URL from an intent, use the system-provided `OpenURLIntent` — do not use `UIApplication.shared.open()`, which is unavailable in Siri/Shortcuts extension contexts. See Apple docs for `OpenURLIntent`.
4. For entity parameters that should be filtered before Siri presents choices, add a predicate via the `IntentParameter` options — see Apple docs for the exact `EntityQueryPredicate` API.

## Compatibility notes

- `@AssistantSchemas` and `shortcutTileColor` require iOS 18 / macOS 15.
- The system-provided `OpenURLIntent` is available across supported iOS versions for URL routing from intent context.
- `IntentParameter` predicate filtering requires iOS 18 and a conforming `EntityQuery` that adopts `EntityPropertyQuery`.
