---
framework: SwiftUI
title: "Bring your iOS app to the Mac"
session: WWDC22-10076
year: 2022
applies_to: macOS 13+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/swiftui.md
---

# Bring your iOS app to the Mac — WWDC22

A guide to running iOS apps on macOS using Mac Catalyst and native Mac SwiftUI, covering when to use each approach and key APIs for Mac-idiomatic UI.

## What changed and why

WWDC22 consolidated guidance on the three Mac deployment paths — Mac Catalyst, Designed for iPad, and native SwiftUI multiplatform — that had accumulated across several releases, making the trade-offs explicit. Xcode 14's multi-platform targets reduced the per-platform target overhead, encouraging a single codebase that conditionally adapts, rather than maintaining parallel app targets.

## Mental model

Think of the three paths as a spectrum of fidelity versus effort: Designed for iPad requires zero Mac-specific code but delivers an iOS UI at a fixed scale, Mac Catalyst runs UIKit on macOS with optional Mac-style chrome, and native SwiftUI multiplatform gives the highest Mac fidelity by using platform-adaptive components. The key decision driver is how much of your app depends on touch-specific interactions versus data and business logic — the more logic you have and the less touch-specific your UI, the more a full multiplatform target pays off.

## Approaches

| Approach | When to use |
|---|---|
| **Mac Catalyst** | Existing UIKit app; want Mac without rewrite |
| **Designed for iPad** | Quick availability on Apple Silicon Mac; no Mac work needed |
| **Native Mac (SwiftUI multiplatform)** | Best Mac experience; new or SwiftUI-based apps |

## Key SwiftUI APIs for Mac

### Window style

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .windowStyle(.hiddenTitleBar)   // Unified toolbar + content area
    }
}
```

### Commands and menu bar

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup { ContentView() }
            .commands {
                CommandMenu("Format") {
                    Button("Bold") { formatBold() }
                        .keyboardShortcut("b")
                    Button("Italic") { formatItalic() }
                        .keyboardShortcut("i")
                }
                CommandGroup(replacing: .newItem) {
                    Button("New Document") { newDocument() }
                        .keyboardShortcut("n")
                }
            }
    }
}
```

### Settings scene

```swift
Settings {
    SettingsView()
}
```

Adds **App Name > Preferences...** (⌘,) menu item automatically.

### Menu

```swift
Menu("Actions") {
    Button("Duplicate") { duplicate() }
    Button("Delete", role: .destructive) { delete() }
}
```

## Mac Catalyst tips

```swift
// Increase Mac Catalyst tap target size to be closer to macOS norms
#if targetEnvironment(macCatalyst)
// Use larger button insets, avoid touch-specific gestures
#endif

// Scale UI for Mac
UIUserInterfaceIdiom.mac  // available in Mac Catalyst apps
```

### Toolbar customisation (Mac Catalyst)

```swift
// In UIScene setup — enable toolbar for Mac Catalyst
#if targetEnvironment(macCatalyst)
windowScene.titlebar?.titleVisibility = .hidden
windowScene.titlebar?.toolbar = toolbar
#endif
```

## Conditional compilation

```swift
#if os(macOS)
    // macOS-specific code
#elseif os(iOS)
    // iOS-specific code
#endif

#if targetEnvironment(macCatalyst)
    // Catalyst-specific code (iOS code running on Mac)
#endif
```

## Adopting this pattern

- Mac apps use menus, not swipe actions — add `.contextMenu` and `CommandMenu` entries
- Prefer `.toolbar` with `ToolbarItem(placement: .primaryAction)` for primary actions
- Use `Settings { }` scene instead of a settings screen inside the main navigation
- `.windowStyle(.hiddenTitleBar)` gives a modern unified look; avoid if the app needs a visible title

## Compatibility notes

- `CommandMenu`, `Settings` scene, `.windowStyle` require macOS 11+
- `Designed for iPad` mode on Apple Silicon Mac does not require any code changes but limits Mac UI fidelity
- Mac Catalyst requires `SUPPORTS_MACCATALYST = YES` in build settings
