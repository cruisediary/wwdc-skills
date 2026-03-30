---
framework: App Intents
title: "What's new in App Intents"
session: WWDC25-10134
year: 2025
applies_to: iOS 26+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/siri-shortcuts.md
  - 2024/WWDC24-10134-whats-new-in-app-intents.md
---

# App Intents — What's New in App Intents (WWDC25)

WWDC25 expands App Intents with deeper Siri and Apple Intelligence integration, new domain schemas, and improved entity querying for iOS 26.

## What's new

- **Apple Intelligence integration** — new `@AssistantSchemas` domains for Apple Intelligence actions; Siri can invoke intents in multi-step AI workflows (see Apple docs for new schema domains)
- **Expanded domain schemas** — additional `AssistantSchema` domains beyond WWDC24's initial set; broader coverage of app categories
- **Improved entity resolution** — `EntityQuery` gains new filtering and sorting capabilities; entities can be resolved more accurately in multi-turn conversations
- **`IntentParameter` updates** — new parameter types for structured data; improved dynamic option lists (see Apple docs)
- **Shortcuts app improvements** — new visual action blocks in Shortcuts for App Intent actions; improved parameter editing UI

## Before / After

**Before (iOS 18 — intent with basic AssistantSchema):**
```swift
@AssistantIntent(schema: .photos.search)
struct SearchPhotosIntent: AppIntent {
    static var title: LocalizedStringResource = "Search Photos"
    @Parameter(title: "Query") var searchQuery: String

    func perform() async throws -> some ReturnsValue<[PhotoEntity]> {
        let results = try await PhotoLibrary.search(query: searchQuery)
        return .result(value: results)
    }
}
```

**After (iOS 26 — new Apple Intelligence schema domains; existing intents unchanged):**
```swift
// Existing @AssistantIntent code continues to work unchanged on iOS 26.
// New: additional schema domains for Apple Intelligence multi-step workflows.
// Example (schema name illustrative — verify against Xcode 26 docs):
// @AssistantIntent(schema: .productivity.createTask)
// struct CreateTaskIntent: AppIntent { ... }
```

## Migration steps

1. Review new `AssistantSchema` domains in Xcode 26 — map your app's actions to any newly available schemas for better Siri/Apple Intelligence discoverability
2. Update `EntityQuery` implementations to use new filtering capabilities if Xcode 26 flags deprecations
3. Test multi-turn Siri conversations with your intents on an iOS 26 device with Apple Intelligence enabled
4. Verify `AppShortcutsProvider` phrases — new Siri capabilities may surface intents in new contexts, requiring phrase review

## Compatibility notes

- New `AssistantSchema` domains require iOS 26+; existing domains from iOS 18 continue to work
- Apple Intelligence integration requires devices supporting Apple Intelligence; intents remain available in Siri/Shortcuts on all devices
- Exact new schema domain names should be verified against Xcode 26 App Intents documentation
