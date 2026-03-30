---
framework: SwiftUI
title: "Integrating SwiftUI"
session: WWDC19-231
year: 2019
applies_to: iOS 13+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/swiftui.md
---

# Integrating SwiftUI (WWDC19)

How to embed SwiftUI views into UIKit apps (`UIHostingController`) and wrap existing UIKit/AppKit views for use inside SwiftUI (`UIViewRepresentable`, `UIViewControllerRepresentable`).

## What changed and why

Full rewrites are rarely practical. SwiftUI was designed from day one to coexist with UIKit: you can adopt SwiftUI incrementally, one screen or component at a time.

Three integration points:
- **`UIHostingController`** — wraps a SwiftUI `View` as a `UIViewController`; use it to push/present SwiftUI screens from UIKit
- **`UIViewRepresentable`** — wraps a `UIView` for use inside SwiftUI (e.g. `UITextView`, `MKMapView`, `WKWebView`)
- **`UIViewControllerRepresentable`** — wraps a `UIViewController` for use inside SwiftUI (e.g. `UIImagePickerController`, `MFMailComposeViewController`)

## Mental model

```
UIKit app
  └─ UIViewController
       └─ UIHostingController(rootView: MySwiftUIView())  ← SwiftUI island

SwiftUI app
  └─ MySwiftUIView
       └─ UIViewRepresentable              ← UIKit island (single view)
       └─ UIViewControllerRepresentable    ← UIKit island (full controller)
```

The `Coordinator` pattern bridges delegate/data-source callbacks from UIKit back into SwiftUI bindings.

## Usage

**`UIHostingController` — embed SwiftUI in UIKit:**
```swift
// Push a SwiftUI view from a UIViewController
let hostingVC = UIHostingController(rootView: SettingsView())
navigationController?.pushViewController(hostingVC, animated: true)

// Or present modally
let hostingVC = UIHostingController(rootView: OnboardingView())
present(hostingVC, animated: true)
```

**`UIViewRepresentable` — wrap `UITextView`:**
```swift
struct MultilineTextField: UIViewRepresentable {
    @Binding var text: String

    func makeUIView(context: Context) -> UITextView {
        let textView = UITextView()
        textView.delegate = context.coordinator
        return textView
    }

    func updateUIView(_ uiView: UITextView, context: Context) {
        if uiView.text != text {
            uiView.text = text
        }
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(text: $text)
    }

    class Coordinator: NSObject, UITextViewDelegate {
        @Binding var text: String
        init(text: Binding<String>) { _text = text }

        func textViewDidChange(_ textView: UITextView) {
            text = textView.text
        }
    }
}
```

**`UIViewControllerRepresentable` — wrap `UIImagePickerController`:**
```swift
struct ImagePicker: UIViewControllerRepresentable {
    @Binding var selectedImage: UIImage?
    @Environment(\.dismiss) private var dismiss

    func makeUIViewController(context: Context) -> UIImagePickerController {
        let picker = UIImagePickerController()
        picker.delegate = context.coordinator
        return picker
    }

    func updateUIViewController(_ uiViewController: UIImagePickerController, context: Context) {}

    func makeCoordinator() -> Coordinator {
        Coordinator(selectedImage: $selectedImage, dismiss: dismiss)
    }

    class Coordinator: NSObject, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
        @Binding var selectedImage: UIImage?
        let dismiss: DismissAction

        init(selectedImage: Binding<UIImage?>, dismiss: DismissAction) {
            _selectedImage = selectedImage
            self.dismiss = dismiss
        }

        func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey: Any]) {
            selectedImage = info[.originalImage] as? UIImage
            dismiss()
        }
    }
}
```

## Adopting this pattern

1. Use `UIHostingController` to adopt SwiftUI screen-by-screen without touching the rest of the app.
2. Implement `UIViewRepresentable` for any `UIView` that has no direct SwiftUI equivalent (rich text, maps, web views, cameras).
3. Always implement a `Coordinator` when the UIKit view has delegate callbacks you need to bridge back to SwiftUI bindings.
4. Call `context.coordinator` in `makeUIView`/`makeUIViewController` to set delegates — do not capture `self` from the representable struct, which is a value type that may be recreated.
5. `updateUIView` / `updateUIViewController` is called on every SwiftUI re-render — guard against no-op updates to avoid feedback loops.
