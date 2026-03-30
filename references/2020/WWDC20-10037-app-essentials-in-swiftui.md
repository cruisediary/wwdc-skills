---
framework: SwiftUI
title: "App essentials in SwiftUI"
session: WWDC20-10037
year: 2020
applies_to: iOS 14+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/swiftui.md
---

# App essentials in SwiftUI — WWDC20

iOS 14 and macOS 11 introduced the `App` protocol and `Scene`-based lifecycle, replacing `UIApplicationDelegate` / `AppDelegate` as the primary app entry point for SwiftUI apps.

## What changed and why

Before iOS 14, a SwiftUI app still required an `AppDelegate` (or `SceneDelegate`) to bootstrap. iOS 14 introduced the `App` protocol so a pure SwiftUI app can declare its entry point without any UIKit scaffolding. The `Scene` abstraction also lets a single codebase support multiple windows on iPad and macOS without manual scene session management.

Key additions:
- `App` protocol — `@main` struct that replaces `AppDelegate`/`SceneDelegate`
- `WindowGroup` — a scene that manages one or more windows showing the same view hierarchy
- `Scene` — protocol for top-level application states (windows, document groups, settings)
- `@AppStorage` — `UserDefaults`-backed `@State` replacement
- `@SceneStorage` — per-scene state restoration storage
- `DocumentGroup` — scene type for document-based apps
- `Settings` — macOS-only scene for the Preferences window

## Mental model

```
App  (entry point, @main)
└── Scene  (window lifecycle unit)
    └── WindowGroup  (creates one or more windows)
        └── ContentView  (your root SwiftUI view)
```

`@AppStorage` sits between `@State` and `UserDefaults` — it reads/writes `UserDefaults` and triggers view updates just like `@State`.

`@SceneStorage` is similar but isolated per scene instance — ideal for restoring tab selection or scroll position when the app is relaunched.

## Usage

**Minimal app entry point:**
```swift
import SwiftUI

@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

**Injecting environment objects at the app level:**
```swift
@main
struct MyApp: App {
    @StateObject private var store = AppStore()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(store)
        }
    }
}
```

**@AppStorage — persisted preference:**
```swift
struct SettingsView: View {
    @AppStorage("fontSize") var fontSize: Double = 14.0

    var body: some View {
        Slider(value: $fontSize, in: 10...24)
    }
}
```

**@SceneStorage — per-scene state restoration:**
```swift
struct ContentView: View {
    @SceneStorage("selectedTab") var selectedTab: String = "home"

    var body: some View {
        TabView(selection: $selectedTab) {
            HomeView().tabItem { Label("Home", systemImage: "house") }.tag("home")
            ProfileView().tabItem { Label("Profile", systemImage: "person") }.tag("profile")
        }
    }
}
```

**Document-based app:**
```swift
@main
struct TextEditorApp: App {
    var body: some Scene {
        DocumentGroup(newDocument: TextDocument()) { file in
            TextEditorView(document: file.$document)
        }
    }
}
```

**macOS Settings scene:**
```swift
@main
struct MyMacApp: App {
    var body: some Scene {
        WindowGroup { ContentView() }

        #if os(macOS)
        Settings { PreferencesView() }
        #endif
    }
}
```

## Adopting this pattern

1. Delete `AppDelegate.swift` and `SceneDelegate.swift` if they exist and contain only boilerplate
2. Create a struct conforming to `App`, add `@main`
3. Move `UIApplicationDelegate` lifecycle hooks (`applicationDidFinishLaunching`, etc.) into `.onAppear` on the root view or use `UIApplicationDelegateAdaptor` for hooks that have no SwiftUI equivalent
4. Replace `UserDefaults.standard.set` / `.value(forKey:)` with `@AppStorage` where the value drives UI
5. Replace manual scene state restoration with `@SceneStorage`

```swift
// Keeping an AppDelegate for push notification registration:
@main
struct MyApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self) var appDelegate

    var body: some Scene {
        WindowGroup { ContentView() }
    }
}
```
