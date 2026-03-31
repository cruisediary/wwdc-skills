---
framework: UIKit
title: "Introducing Drag and Drop"
session: WWDC17-201
year: 2017
applies_to: iOS 11+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - 2017/WWDC17-213-drag-and-drop-with-collection-and-table-view.md
  - 2017/WWDC17-223-mastering-drag-and-drop.md
---

> **Reference-only (iOS 11+):** Drag and Drop APIs introduced in iOS 11 are unchanged in iOS 18. This session explains the conceptual model; see 213 and 223 for collection/table view integration.

## What changed and why

iOS 11 introduced system-level drag and drop across apps. The design centers on `NSItemProvider` (the data carrier) and interaction objects (`UIDragInteraction`, `UIDropInteraction`) added to any view. On iPad, drag operates across app boundaries; on iPhone, drag is within a single app.

## Mental model

```
User drag gesture
  → UIDragInteraction.delegate provides [UIDragItem]
       └── UIDragItem wraps NSItemProvider (lazy data provider)

User drop gesture
  → UIDropInteraction.delegate accepts/rejects via UIDropProposal
       └── UIDropSession delivers NSItemProvider to load data
```

## Usage

**Add drag to a view**

```swift
let dragInteraction = UIDragInteraction(delegate: self)
myView.addInteraction(dragInteraction)
myView.isUserInteractionEnabled = true

// UIDragInteractionDelegate
func dragInteraction(_ interaction: UIDragInteraction,
                     itemsForBeginning session: UIDragSession) -> [UIDragItem] {
    let provider = NSItemProvider(object: "Hello" as NSString)
    return [UIDragItem(itemProvider: provider)]
}
```

**Add drop to a view**

```swift
let dropInteraction = UIDropInteraction(delegate: self)
myView.addInteraction(dropInteraction)

func dropInteraction(_ interaction: UIDropInteraction,
                     performDrop session: UIDropSession) {
    session.loadObjects(ofClass: NSString.self) { items in
        guard let strings = items as? [String] else { return }
        print(strings.first ?? "")
    }
}

func dropInteraction(_ interaction: UIDropInteraction,
                     sessionDidUpdate session: UIDropSession) -> UIDropProposal {
    return UIDropProposal(operation: .copy)
}
```

## Adopting this pattern

- iPad supports cross-app drag; iPhone only supports within-app drag and drop.
- `NSItemProvider` is lazy — data is only loaded when `loadObjects(ofClass:)` is called.
- Use `UITableView`/`UICollectionView` built-in drag-drop support (WWDC17-213) for list reordering rather than raw `UIDragInteraction`.
