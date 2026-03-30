---
framework: SwiftUI
title: "What's new in SwiftUI"
session: WWDC24-10144
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/swiftui.md
---

# SwiftUI — What's New in SwiftUI (WWDC24)

iOS 18 brings custom containers, mesh gradients, zoom transitions, a new sidebar-adaptive TabView, and the `@Entry` macro for environment values.

## What's new

- **Custom containers** — `ForEach(subviewOf:)` lets you iterate over the subviews of a view builder, enabling reusable container components that wrap and restyle their children
- **`@Entry` macro** — replaces the `EnvironmentKey` boilerplate for declaring custom `@Environment` values; declare with a single line
- **Mesh gradients** — `MeshGradient` creates smooth multicolor gradients defined by a 2D grid of control points and colors
- **Zoom transitions** — `.transition(.zoom)` paired with `.matchedTransitionSource(id:in:)` and `.navigationTransitionStyle(.zoom(sourceID:in:))` provides hero-style zoom navigation without `matchedGeometryEffect` workarounds
- **Tab/Sidebar adaptive style** — `TabView` gains a `.sidebarAdaptable` style that renders as a bottom tab bar on iPhone and a collapsible sidebar on iPad/Mac
- **Enhanced scroll effects** — `.scrollTransition` and `.visualEffect` enable scroll-linked animations and per-frame geometry reads without UIKit

## Before / After

**Before (NavigationView + custom tab workaround):**
```swift
// iOS 17 and earlier: NavigationView deprecated but commonly used
// Custom sidebar required TabView + NavigationSplitView wiring by hand
NavigationView {
    SidebarView()
    ContentView()
}

// TabView had no sidebar mode — developers built separate iPad layouts
TabView(selection: $selection) {
    HomeView().tabItem { Label("Home", systemImage: "house") }.tag(0)
    SearchView().tabItem { Label("Search", systemImage: "magnifyingglass") }.tag(1)
}
```

**After (clean sidebarAdaptable TabView):**
```swift
// iOS 18: one declaration adapts to tab bar (iPhone) or sidebar (iPad/Mac)
TabView {
    Tab("Home", systemImage: "house") {
        HomeView()
    }
    Tab("Search", systemImage: "magnifyingglass") {
        SearchView()
    }
}
.tabViewStyle(.sidebarAdaptable)
```

**Before (EnvironmentKey boilerplate):**
```swift
private struct ThemeKey: EnvironmentKey {
    static let defaultValue: Theme = .default
}

extension EnvironmentValues {
    var theme: Theme {
        get { self[ThemeKey.self] }
        set { self[ThemeKey.self] = newValue }
    }
}
```

**After (`@Entry` macro):**
```swift
extension EnvironmentValues {
    @Entry var theme: Theme = .default
}
```

## Migration steps

1. Replace custom sidebar/tab hybrid layouts with `TabView { ... }.tabViewStyle(.sidebarAdaptable)` — the system handles both form factors automatically
2. Audit `NavigationStack` usages — add zoom transitions on drill-down rows with `.matchedTransitionSource(id:in:)` on the source and `.navigationTransitionStyle(.zoom(sourceID:in:))` on the destination
3. Replace `EnvironmentKey` declarations with `@Entry` in `EnvironmentValues` extensions
4. Replace complex `LinearGradient`/`RadialGradient` layering with `MeshGradient` for multicolor backgrounds
5. Migrate `matchedGeometryEffect` hero animations to the new zoom transition API where a zoom in/out gesture is the intended interaction

## Compatibility notes

- All new APIs require iOS 18+ / macOS 15+ / watchOS 11+ / tvOS 18+
- `@Entry` is a compile-time macro — it generates the same boilerplate as before; older OS targets are unaffected as long as `EnvironmentValues` extension compiles
- `.sidebarAdaptable` degrades gracefully: on iPhone it renders as a standard bottom tab bar
- `MeshGradient` requires iOS 18+ — wrap in `if #available(iOS 18, *)` for backward-compatible targets
- `ForEach(subviewOf:)` requires iOS 18+ and has no back-deployment equivalent
