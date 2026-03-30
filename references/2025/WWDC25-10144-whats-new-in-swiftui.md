---
framework: SwiftUI
title: "What's new in SwiftUI"
session: WWDC25-10144
year: 2025
applies_to: iOS 26+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/swiftui.md
  - canonical/liquid-glass.md
  - canonical/webview.md
  - 2024/WWDC24-10144-whats-new-in-swiftui.md
---

# SwiftUI — What's New in SwiftUI (WWDC25)

iOS 26 brings Liquid Glass material to SwiftUI, a redesigned tab bar with fluid visual styles, updated toolbar APIs, and a native `WebView` type replacing `WKWebViewRepresentable` workarounds.

## What's new

- **Liquid Glass integration** — system containers (tab bars, navigation bars, sheets) automatically adopt Liquid Glass material; custom surfaces can use `GlassEffect` modifier (see `canonical/liquid-glass.md`)
- **New tab bar styles** — `TabView` gains additional style options for the iOS 26 fluid tab bar; the `.sidebarAdaptable` style introduced in iOS 18 continues and is enhanced
- **Updated toolbar APIs** — toolbar placement and material customization aligned with the Liquid Glass design system; see Apple docs for specific modifier names
- **`WebView` in SwiftUI** — native `WebView` type replaces `WKWebViewRepresentable` wrappers; uses a `WebPage` model object (`WebView(webPage:)`) for loading and navigation (see `canonical/webview.md`)
- **Continued `@Observable` and `@Environment` improvements** — reduced boilerplate, better compile-time diagnostics

## Before / After

**Before (WWDC24 — WKWebView in SwiftUI required UIViewRepresentable wrapper):**
```swift
struct WebWrapper: UIViewRepresentable {
    let url: URL

    func makeUIView(context: Context) -> WKWebView {
        WKWebView()
    }

    func updateUIView(_ webView: WKWebView, context: Context) {
        webView.load(URLRequest(url: url))
    }
}

// Usage
WebWrapper(url: URL(string: "https://example.com")!)
```

**After (iOS 26 — native `WebView` with `WebPage` model):**
```swift
import SwiftUI
import WebKit

// WebPage is the model object; WebView renders it
let page = WebPage()
page.load(URLRequest(url: URL(string: "https://example.com")!))

// In a view:
WebView(webPage: page)

// See canonical/webview.md for full WebPage API
```

**Before (iOS 18 tab bar — manual style configuration):**
```swift
TabView {
    Tab("Home", systemImage: "house") { HomeView() }
    Tab("Search", systemImage: "magnifyingglass") { SearchView() }
}
.tabViewStyle(.sidebarAdaptable)
```

**After (iOS 26 — Liquid Glass tab bar applied automatically):**
```swift
// The system applies Liquid Glass material to the tab bar automatically.
// No additional modifier needed for the default fluid appearance.
TabView {
    Tab("Home", systemImage: "house") { HomeView() }
    Tab("Search", systemImage: "magnifyingglass") { SearchView() }
}
// Opt into specific style if needed — see Apple docs for new style identifiers
```

## Migration steps

1. Adopt `WebView(webPage:)` with a `WebPage` model — remove `UIViewRepresentable` wrappers around `WKWebView`; create a `WebPage`, call `page.load(_:)`, and pass it to `WebView(webPage:)` (see `canonical/webview.md`)
2. Remove manual `GlassEffect` customizations on standard containers (tab bars, sheets) — the system provides them automatically on iOS 26
3. Audit custom toolbar modifiers; some placement values may have changed — test with Xcode 26 and verify visual results on device
4. For custom surfaces that need Liquid Glass: apply the `.glassEffect()` modifier (see `canonical/liquid-glass.md`)
5. Verify `@Observable` types — redundant `@Published` annotations produce warnings in Xcode 26; remove them

## Compatibility notes

- All new iOS 26 APIs require `#available(iOS 26, *)` guards for apps with lower deployment targets
- `WebView` is a new type — old `UIViewRepresentable` wrappers continue to compile unchanged
- Liquid Glass on system chrome is automatic on iOS 26; apps built against the iOS 26 SDK will display it without code changes
- Exact modifier and type names for new toolbar APIs should be confirmed against Xcode 26 documentation before shipping
