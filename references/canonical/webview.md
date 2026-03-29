---
framework: WebView
status: current
applies_to: iOS 26+
shape: code-first
superseded_by: null
history:
  - year: 2025
    file: 2025/webview.md
    summary: "Native WebView — WebPage model, navigation API, find interaction"
---

## Quick start

```swift
import SwiftUI
import WebKit

struct BrowserView: View {
    let url = URL(string: "https://developer.apple.com")!

    var body: some View {
        WebView(url: url)
    }
}
```

No `UIViewRepresentable` wrapper needed — `WebView` is a native SwiftUI view.

## Key APIs

| API | Purpose |
|---|---|
| `WebView(url:)` | Display a URL in a SwiftUI-native web view |
| `WebView(webPage:)` | Display a URL using a shared `WebPage` model for state observation |
| `WebPage` | `@Observable` model representing a loaded page — URL, title, load progress, can go back/forward |
| `WebPage.load(_:)` | Programmatically navigate to a new URL |
| `WebPage.goBack()` / `goForward()` | Navigate the history stack |
| `.findInteraction(_:)` | Attach an in-page text search UI to the WebView |

## Common patterns

**Observable page state (title, progress, back/forward):**

```swift
@Observable
class BrowserModel {
    let page = WebPage()
}

struct BrowserView: View {
    @State private var model = BrowserModel()

    var body: some View {
        VStack {
            ProgressView(value: model.page.estimatedProgress)
                .opacity(model.page.isLoading ? 1 : 0)

            WebView(webPage: model.page)
                .navigationTitle(model.page.title ?? "Loading…")
        }
        .toolbar {
            ToolbarItem(placement: .navigationBarLeading) {
                Button("Back") { model.page.goBack() }
                    .disabled(!model.page.canGoBack)
            }
        }
        .task {
            model.page.load(URL(string: "https://developer.apple.com")!)
        }
    }
}
```

**In-page find interaction:**

```swift
struct SearchableWebView: View {
    @State private var findInteraction = WebPage.FindInteraction()

    var body: some View {
        WebView(url: URL(string: "https://example.com")!)
            .findInteraction($findInteraction)
        Button("Find in page") {
            findInteraction.presentFindNavigator(showingReplace: false)
        }
    }
}
```

## Gotchas

- `WebView` and `WebPage` require **iOS 26+**. For older OS versions, continue using `WKWebView` via `UIViewRepresentable`.
- `WebPage` is `@Observable` — use it with SwiftUI's observation system, not `@ObservableObject`.
- JavaScript evaluation and custom URL scheme handlers that previously went through `WKWebView` directly need to be re-routed through `WebPage` APIs or `WKWebViewConfiguration` if still required.
- App Transport Security (ATS) rules still apply — HTTP URLs require an `NSAppTransportSecurity` exception in `Info.plist`.
