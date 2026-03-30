---
framework: SwiftUI
title: "Elevate your tab and sidebar experience in iPadOS"
session: WWDC24-10147
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/swiftui.md
---

# SwiftUI — Elevate Your Tab and Sidebar Experience in iPadOS (WWDC24)

iOS 18 introduces a new `Tab` type and `.sidebarAdaptable` tab view style that adapts between a bottom tab bar on iPhone and a collapsible sidebar on iPad and Mac.

## Quick start

```swift
import SwiftUI

struct RootView: View {
    var body: some View {
        TabView {
            Tab("Home", systemImage: "house") {
                HomeView()
            }
            Tab("Search", systemImage: "magnifyingglass") {
                SearchView()
            }
            Tab("Profile", systemImage: "person") {
                ProfileView()
            }
        }
        .tabViewStyle(.sidebarAdaptable)
    }
}
```

## Key APIs

| API | Purpose |
|---|---|
| `Tab(_:systemImage:) { }` | Declares a single tab with a label and content view |
| `TabSection(_:) { }` | Groups related tabs under a named section in the sidebar |
| `.tabViewStyle(.sidebarAdaptable)` | Adapts layout to sidebar (iPad/Mac) or tab bar (iPhone) |
| `.tabViewCustomization(_:)` | Binds a `TabViewCustomization` value, enabling user reordering and hiding of tabs |
| `@AppStorage` + `TabViewCustomization` | Persists the user's customization across launches |
| `Tab(..., role: .search)` | Designates the search tab; placed in the search field area on iPad |

## Common patterns

**Grouped tabs with `TabSection`:**
```swift
TabView {
    Tab("Inbox", systemImage: "tray") { InboxView() }

    TabSection("Library") {
        Tab("Books", systemImage: "books.vertical") { BooksView() }
        Tab("Audiobooks", systemImage: "headphones") { AudiobooksView() }
        Tab("Magazines", systemImage: "magazine") { MagazinesView() }
    }

    Tab("Settings", systemImage: "gear") { SettingsView() }
}
.tabViewStyle(.sidebarAdaptable)
```

**Programmatic tab selection:**
```swift
enum AppTab: String {
    case home, search, profile
}

struct RootView: View {
    @State private var selectedTab: AppTab = .home

    var body: some View {
        TabView(selection: $selectedTab) {
            Tab("Home", systemImage: "house", value: .home) { HomeView() }
            Tab("Search", systemImage: "magnifyingglass", value: .search) { SearchView() }
            Tab("Profile", systemImage: "person", value: .profile) { ProfileView() }
        }
        .tabViewStyle(.sidebarAdaptable)
    }
}
```

**User-customizable tabs:**
```swift
struct RootView: View {
    @AppStorage("tabCustomization")
    private var customization: TabViewCustomization

    var body: some View {
        TabView {
            Tab("Home", systemImage: "house") { HomeView() }
                .customizationID("home")
            Tab("Search", systemImage: "magnifyingglass") { SearchView() }
                .customizationID("search")
            Tab("Favorites", systemImage: "star") { FavoritesView() }
                .customizationID("favorites")
        }
        .tabViewStyle(.sidebarAdaptable)
        .tabViewCustomization($customization)
    }
}
```

## Gotchas

- **iOS 18+ only** — `Tab`, `TabSection`, and `.sidebarAdaptable` are not available before iOS 18. For backward compatibility, wrap in `if #available(iOS 18, *)` and provide a `.tabItem`-based fallback.
- **iPhone fallback** — on iPhone, `.sidebarAdaptable` renders as a standard bottom tab bar; the sidebar chrome is not shown. Test both form factors.
- **`TabSection` is sidebar-only** — section grouping is visible only in the sidebar on iPad/Mac. On iPhone, tabs from all sections appear flat in the tab bar.
- **`Tab` replaces `.tabItem`** — the new `Tab` initializer and the old `.tabItem` modifier are separate APIs and cannot be mixed in the same `TabView`.
- **Customization IDs must be stable** — if you change a `.customizationID`, the user's saved customization for that tab is lost. Treat them like accessibility identifiers.
