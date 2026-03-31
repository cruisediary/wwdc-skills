---
framework: PDFKit
title: "Introducing PDFKit on iOS"
session: WWDC17-207
year: 2017
applies_to: iOS 11+
status: reference-only
superseded_by: null
shape: code-first
related: []
---

> **Reference-only (iOS 11+):** PDFKit was ported from macOS to iOS 11. APIs are stable and unchanged through iOS 18. This is the primary framework for PDF rendering and annotation in iOS apps.

## Quick start

```swift
import PDFKit

let pdfView = PDFView(frame: view.bounds)
pdfView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
view.addSubview(pdfView)

if let url = Bundle.main.url(forResource: "document", withExtension: "pdf"),
   let document = PDFDocument(url: url) {
    pdfView.document = document
    pdfView.autoScales = true
}
```

## Key APIs

| Type | Role |
|---|---|
| `PDFDocument` | Loads and represents a PDF file; access pages, metadata |
| `PDFPage` | A single page; can render to `CGContext` or provide `PDFAnnotation` objects |
| `PDFView` | UIView subclass that displays a `PDFDocument` with scroll/zoom |
| `PDFThumbnailView` | Displays page thumbnails; syncs with a `PDFView` |
| `PDFAnnotation` | Highlight, underline, ink, text annotations |
| `PDFSelection` | Represents selected text; used for search results |

## Common patterns

**Search and highlight**

```swift
let results = document.findString("swift", withOptions: .caseInsensitive)
for selection in results {
    selection.pages.forEach { page in
        let highlight = PDFAnnotation(bounds: selection.bounds(for: page),
                                      forType: .highlight, withProperties: nil)
        highlight.color = UIColor.yellow.withAlphaComponent(0.5)
        page.addAnnotation(highlight)
    }
}
```

**Render page to image**

```swift
let page = document.page(at: 0)!
let thumbnail = page.thumbnail(of: CGSize(width: 200, height: 280), for: .mediaBox)
```

## Gotchas

- `PDFDocument` loading is synchronous — load on a background queue and assign `pdfView.document` on the main queue.
- `PDFAnnotation` bounds use PDF coordinate space (origin bottom-left). Convert from `PDFView` screen coordinates using `pdfView.convert(_:to:)`.
- Password-protected documents: check `document.isLocked` and call `document.unlock(withPassword:)` before accessing pages.
