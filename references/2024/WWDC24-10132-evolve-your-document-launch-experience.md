---
framework: UIKit
title: "Evolve your document launch experience"
session: WWDC24-10132
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: code-first
related: []
---

## Quick start

```swift
import UIKit

// 1. Subclass UIDocumentViewController — iOS 18's built-in document host
class DocumentViewController: UIDocumentViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        // document is available via self.document once opened
    }

    // Called when the user opens or creates a document
    override func documentDidOpen() {
        guard let doc = document as? MyDocument else { return }
        // populate your UI from doc.content
    }
}

// 2. Configure the launch experience in SceneDelegate / app entry point
class SceneDelegate: UIResponder, UIWindowSceneDelegate {

    var window: UIWindow?

    func scene(_ scene: UIScene,
               willConnectTo session: UISceneSession,
               options connectionOptions: UIScene.ConnectionOptions) {
        guard let windowScene = scene as? UIWindowScene else { return }

        let launchVC = UIDocumentLaunchViewController()
        launchVC.allowedContentTypes = [.myDocumentType]  // UTType
        launchVC.delegate = self

        window = UIWindow(windowScene: windowScene)
        window?.rootViewController = launchVC
        window?.makeKeyAndVisible()
    }
}

extension SceneDelegate: UIDocumentLaunchViewControllerDelegate {
    func documentLaunchViewController(
        _ vc: UIDocumentLaunchViewController,
        didPickDocumentAt url: URL
    ) {
        let doc = MyDocument(fileURL: url)
        let docVC = DocumentViewController(document: doc)
        window?.rootViewController = docVC
    }
}
```

## Key APIs

| API | Purpose |
|---|---|
| `UIDocumentViewController` | Base class for a document-editing view controller; manages open/close lifecycle |
| `UIDocumentViewController.document` | The currently open `UIDocument` instance |
| `UIDocumentViewController.documentDidOpen()` | Override point called after the document has been read from disk |
| `UIDocumentLaunchViewController` | System-provided launch screen with recents, templates, and file picker |
| `UIDocumentLaunchViewController.allowedContentTypes` | `[UTType]` restricting which files appear in the picker |
| `UIDocumentLaunchViewControllerDelegate` | Callbacks for document selection and new-document creation |
| `UIDocumentLaunchViewController.additionalButton` | Inject a custom `UIButton` into the launch screen action area |
| Background extension icons | Declare `UIDocumentExtensionIcons` in Info.plist for per-extension thumbnail backgrounds |

## Common patterns

### Providing new-document templates

```swift
// Implement the delegate method to create a blank document
func documentLaunchViewController(
    _ vc: UIDocumentLaunchViewController,
    didRequestNewDocumentWithTemplate template: URL?
) {
    // template is nil for blank, or a URL to a bundled template file
    let newURL = FileManager.default
        .urls(for: .documentDirectory, in: .userDomainMask)[0]
        .appendingPathComponent("Untitled.\(MyDocument.fileExtension)")

    if let template {
        try? FileManager.default.copyItem(at: template, to: newURL)
    } else {
        MyDocument(fileURL: newURL).save(to: newURL, for: .forCreating) { _ in }
    }

    let doc = MyDocument(fileURL: newURL)
    let docVC = DocumentViewController(document: doc)
    window?.rootViewController = docVC
}
```

### Adding a custom action button to the launch screen

```swift
let launchVC = UIDocumentLaunchViewController()

var config = UIButton.Configuration.borderedProminent()
config.title = "Import from Camera"
launchVC.additionalButton = UIButton(configuration: config, primaryAction: UIAction { _ in
    // present camera picker
})
```

### Declaring background extension icons (Info.plist)

```xml
<key>UIDocumentExtensionIcons</key>
<dict>
    <!-- key = file extension, value = asset catalog image name -->
    <key>mydoc</key>
    <string>DocumentThumbnailBackground</string>
</dict>
```

### UIDocumentViewController lifecycle

```swift
class DocumentViewController: UIDocumentViewController {

    // Document is opened — safe to access document.content
    override func documentDidOpen() {
        renderContent()
    }

    // Respond to external changes (e.g., iCloud sync conflict)
    override func documentStateChanged() {
        if document?.documentState.contains(.inConflict) == true {
            resolveConflict()
        }
    }

    private func renderContent() {
        guard let doc = document as? MyDocument else { return }
        textView.text = doc.content
    }
}
```

## Gotchas

- `UIDocumentViewController` is iOS 18+ only — existing `UIDocumentBrowserViewController` remains available for iOS 16/17 deployments; guard with `#available(iOS 18, *)`.
- `UIDocumentLaunchViewController` replaces custom launch screens but does not replace `UIDocumentBrowserViewController` for file-manager-style UIs; use the browser when you need folder navigation.
- `documentDidOpen()` is called on the main thread after `UIDocument.open(completionHandler:)` succeeds; do not call `open` manually — `UIDocumentViewController` manages this.
- Set `allowedContentTypes` before the view loads; changing it afterward has no effect.
- Background extension icons defined in `UIDocumentExtensionIcons` must reference image assets in the main app bundle, not an extension bundle.
- When the user picks a document from iCloud, `didPickDocumentAt` may return a security-scoped URL — call `startAccessingSecurityScopedResource()` before reading and `stopAccessingSecurityScopedResource()` when done.
