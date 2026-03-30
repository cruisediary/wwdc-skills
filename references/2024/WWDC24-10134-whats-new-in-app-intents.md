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
- `UniversalLink` intent action opens a URL using the universal link routing mechanism rather than `OpenURLIntent`

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
// UniversalLink action — open a deep-link URL through universal link routing
import AppIntents

struct OpenItemIntent: AppIntent {
    static var title: LocalizedStringResource = "Open Item"
    @Parameter(title: "Item URL") var itemURL: URL

    func perform() async throws -> some OpensIntent {
        return .result(opensIntent: UniversalLink(url: itemURL))
    }
}
```

## Migration steps

1. Replace multiple `@AssistantIntent` declarations that share a type with a single `@AssistantSchemas(…)` macro call.
2. Set `AppShortcutsProvider.shortcutTileColor` to match your app's brand color.
3. Where you previously used `OpenURLIntent` for universal links, switch to `UniversalLink` to get proper app routing.
4. For entity parameters that should be filtered before Siri presents choices, add a predicate via the `IntentParameter` options — see Apple docs for the exact `EntityQueryPredicate` API.

## Compatibility notes

- `@AssistantSchemas` and `shortcutTileColor` require iOS 18 / macOS 15.
- `UniversalLink` is an iOS 18+ intent action; fall back to `OpenURLIntent` on earlier OS versions.
- `IntentParameter` predicate filtering requires iOS 18 and a conforming `EntityQuery` that adopts `EntityPropertyQuery`.
