---
framework: UIKit
title: "Drag and Drop with Collection and Table View"
session: WWDC17-213
year: 2017
applies_to: iOS 11+
status: reference-only
superseded_by: null
shape: code-first
related:
  - 2017/WWDC17-201-introducing-drag-and-drop.md
---

> **Reference-only (iOS 11+):** `UITableView`/`UICollectionView` built-in drag-drop APIs from iOS 11 are unchanged in iOS 18.

## Quick start

```swift
tableView.dragInteractionEnabled = true
tableView.dragDelegate = self
tableView.dropDelegate = self

// UITableViewDragDelegate
func tableView(_ tableView: UITableView,
               itemsForBeginning session: UIDragSession,
               at indexPath: IndexPath) -> [UIDragItem] {
    let provider = NSItemProvider(object: dataSource[indexPath.row].title as NSString)
    return [UIDragItem(itemProvider: provider)]
}

// UITableViewDropDelegate
func tableView(_ tableView: UITableView,
               performDropWith coordinator: UITableViewDropCoordinator) {
    coordinator.session.loadObjects(ofClass: NSString.self) { items in
        // insert items into data source and tableView
    }
}
```

## Key APIs

| Type | Role |
|---|---|
| `UITableView.dragDelegate` | `UITableViewDragDelegate` — provides drag items per index path |
| `UITableView.dropDelegate` | `UITableViewDropDelegate` — accepts/performs drop |
| `UICollectionView.dragDelegate` | `UICollectionViewDragDelegate` |
| `UICollectionView.dropDelegate` | `UICollectionViewDropDelegate` |
| `UITableViewDropCoordinator` | Coordinates animated drop into table; use `drop(_:toRowAt:)` for animated insertion |
| `UICollectionViewDropCoordinator` | Same for collection views |

## Common patterns

**Animated row insertion during drop**

```swift
func tableView(_ tableView: UITableView,
               performDropWith coordinator: UITableViewDropCoordinator) {
    let dest = coordinator.destinationIndexPath
        ?? IndexPath(row: tableView.numberOfRows(inSection: 0), section: 0)
    coordinator.session.loadObjects(ofClass: NSString.self) { items in
        let strings = items as? [String] ?? []
        self.dataSource.insert(contentsOf: strings, at: dest.row)
        tableView.insertRows(at: [dest], with: .automatic)
    }
    coordinator.drop(coordinator.items.first!.dragItem, toRowAt: dest)
}
```

## Gotchas

- Set `tableView.dragInteractionEnabled = true` on iPhone (disabled by default on iPhone, enabled by default on iPad).
- The drop coordinator's `destinationIndexPath` is nil when dropping below all rows — always provide a fallback.
