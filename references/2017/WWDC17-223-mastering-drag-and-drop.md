---
framework: UIKit
title: "Mastering Drag and Drop"
session: WWDC17-223
year: 2017
applies_to: iOS 11+
status: reference-only
superseded_by: null
shape: code-first
related:
  - 2017/WWDC17-201-introducing-drag-and-drop.md
  - 2017/WWDC17-213-drag-and-drop-with-collection-and-table-view.md
---

> **Reference-only (iOS 11+):** Advanced drag and drop patterns from WWDC17 remain valid in iOS 18. Covers custom preview, progress tracking, and multi-item drag.

## Quick start

```swift
func dragInteraction(_ interaction: UIDragInteraction,
                     previewForLifting item: UIDragItem,
                     session: UIDragSession) -> UITargetedDragPreview? {
    let parameters = UIDragPreviewParameters()
    parameters.visiblePath = UIBezierPath(roundedRect: myView.bounds, cornerRadius: 12)
    return UITargetedDragPreview(view: myView, parameters: parameters)
}
```

## Key APIs

| Type | Role |
|---|---|
| `UIDragPreviewParameters` | Controls visible region, shadow, background during lift |
| `UITargetedDragPreview` | Associates a preview with a target point in a container view |
| `UIDragInteraction.allowsMoveOperation` | Whether the drag source allows `.move` (default true) |
| `NSItemProvider.registerObject(_:visibility:)` | Register lazy data for multiple UTI types |
| `UIDragSession.hasItemsConforming(toTypeIdentifiers:)` | Check accepted types before accepting a drop |

## Common patterns

**Multi-item drag**

```swift
func dragInteraction(_ interaction: UIDragInteraction,
                     itemsForAddingTo session: UIDragSession,
                     withTouchAt point: CGPoint) -> [UIDragItem] {
    return additionalItems(for: point).map { UIDragItem(itemProvider: NSItemProvider(object: $0)) }
}
```

**Progress tracking**

```swift
let progress = item.itemProvider.loadObject(ofClass: UIImage.self) { image, error in
    DispatchQueue.main.async { /* handle loaded image */ }
}
// progress.fractionCompleted for large cross-app transfers
_ = progress
```

## Gotchas

- `UITargetedDragPreview` target must be a view in the window's view hierarchy at the time the preview is requested.
- Cross-app drops use `NSItemProvider` with UTI types; always register both a primary type and fallbacks.
- `allowsMoveOperation = false` prevents the source app from removing the original; use when sharing (not moving) data.
