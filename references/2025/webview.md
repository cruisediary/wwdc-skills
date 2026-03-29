---
framework: WebView
session: null
year: 2025
applies_to: iOS 26+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/webview.md
---

## What's new

iOS 26 introduces a SwiftUI-native `WebView` and an observable `WebPage` model, eliminating the need for `UIViewRepresentable` wrappers around `WKWebView`:

- **`WebView` SwiftUI view** — drop-in SwiftUI view that accepts a URL or a `WebPage` model; no UIKit bridging required
- **`WebPage` observable model** — `@Observable` class exposing page state: current URL, title, load progress, canGoBack/canGoForward, isLoading
- **Declarative navigation** — `WebPage.load(_:)`, `goBack()`, `goForward()` replace `WKWebView` imperative navigation calls
- **`WKNavigationDelegate` replacement** — navigation events surface as properties on `WebPage` rather than delegate callbacks
- **Find interaction** — `WebPage.FindInteraction` and `.findInteraction(_:)` modifier bring in-page search to SwiftUI without accessing the underlying `WKWebView`

## Before / After

**Before — WKWebView via UIViewRepresentable (iOS 14–17 style):**

```swift
struct LegacyWebView: UIViewRepresentable {
    let url: URL

    func makeUIView(context: Context) -> WKWebView {
        let webView = WKWebView()
        webView.navigationDelegate = context.coordinator
        return webView
    }

    func updateUIView(_ webView: WKWebView, context: Context) {
        let request = URLRequest(url: url)
        webView.load(request)
    }

    func makeCoordinator() -> Coordinator {
        Coordinator()
    }

    class Coordinator: NSObject, WKNavigationDelegate {
        func webView(_ webView: WKWebView,
                     didFinish navigation: WKNavigation!) {
            print("Loaded: \(webView.url?.absoluteString ?? "")")
        }
    }
}

// Usage
struct ContentView: View {
    var body: some View {
        LegacyWebView(url: URL(string: "https://example.com")!)
    }
}
```

**After — native WebView with WebPage model (iOS 26+):**

```swift
struct ContentView: View {
    @State private var page = WebPage()

    var body: some View {
        WebView(webPage: page)
            .navigationTitle(page.title ?? "")
            .task {
                page.load(URL(string: "https://example.com")!)
            }
    }
}
```

## Migration steps

1. **Remove `UIViewRepresentable` wrapper** — delete the struct conforming to `UIViewRepresentable` and its `Coordinator`.
2. **Replace with `WebView(url:)`** for simple cases where you don't need to observe page state.
3. **Introduce a `WebPage` instance** (`@State private var page = WebPage()`) when you need title, progress, or navigation controls.
4. **Switch to `WebView(webPage:)`** and drive navigation with `page.load(_:)`, `page.goBack()`, `page.goForward()`.
5. **Migrate `WKNavigationDelegate` callbacks** — replace delegate methods with reactive reads of `WebPage` properties (`page.isLoading`, `page.estimatedProgress`, `page.canGoBack`).
6. **Replace find-in-page UIKit calls** with `WebPage.FindInteraction` and the `.findInteraction(_:)` modifier.

## Compatibility notes

- `WebView` and `WebPage` require **iOS 26+**.
- For apps targeting iOS 17 or earlier, keep the `UIViewRepresentable` + `WKWebView` approach. You can use `if #available(iOS 26, *) { WebView(url: url) } else { LegacyWebView(url: url) }` to adopt gradually.
- `WKWebView` itself is not deprecated — it remains available for advanced use cases (custom URL scheme handling, JavaScript injection, `WKWebViewConfiguration`) that `WebPage` does not yet cover.
