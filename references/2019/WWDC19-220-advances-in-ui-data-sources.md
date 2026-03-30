---
framework: UIKit
title: "Advances in UI Data Sources"
session: WWDC19-220
year: 2019
applies_to: iOS 13+
status: reference-only
superseded_by: null
shape: code-first
related: []
---

# Advances in UI Data Sources (WWDC19)

Diffable data sources for `UICollectionView` and `UITableView`: `UICollectionViewDiffableDataSource`, `UITableViewDiffableDataSource`, and `NSDiffableDataSourceSnapshot`.

## Quick start

```swift
// 1. Define your section and item identifiers (must be Hashable)
enum Section: Hashable { case main }
struct Item: Hashable { let id: UUID; let title: String }

// 2. Create the diffable data source
let dataSource = UICollectionViewDiffableDataSource<Section, Item>(
    collectionView: collectionView
) { collectionView, indexPath, item in
    let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "Cell", for: indexPath)
    cell.textLabel?.text = item.title
    return cell
}

// 3. Apply a snapshot to update the UI
var snapshot = NSDiffableDataSourceSnapshot<Section, Item>()
snapshot.appendSections([.main])
snapshot.appendItems(items)
dataSource.apply(snapshot, animatingDifferences: true)
```

## Key APIs

| API | Description |
|-----|-------------|
| `UICollectionViewDiffableDataSource<SectionIdentifier, ItemIdentifier>` | Diffable data source for `UICollectionView`; replaces `UICollectionViewDataSource` |
| `UITableViewDiffableDataSource<SectionIdentifier, ItemIdentifier>` | Same pattern for `UITableView` |
| `NSDiffableDataSourceSnapshot<SectionIdentifier, ItemIdentifier>` | Value-type snapshot of the data; describes what should be displayed |
| `snapshot.appendSections(_:)` | Adds section identifiers to the snapshot |
| `snapshot.appendItems(_:toSection:)` | Adds item identifiers to a section |
| `snapshot.deleteItems(_:)` | Removes specific items |
| `snapshot.reloadItems(_:)` | Marks items as needing reload (reconfigures cell) |
| `dataSource.apply(_:animatingDifferences:)` | Calculates diff and applies animated or instant updates |
| `dataSource.snapshot()` | Returns the current applied snapshot |

## Common patterns

**Filtering — reapply a new snapshot:**
```swift
func applyFilter(_ query: String) {
    let filtered = query.isEmpty ? allItems : allItems.filter { $0.title.contains(query) }
    var snapshot = NSDiffableDataSourceSnapshot<Section, Item>()
    snapshot.appendSections([.main])
    snapshot.appendItems(filtered)
    dataSource.apply(snapshot, animatingDifferences: true)
}
```

**Incremental update — delete and insert:**
```swift
var snapshot = dataSource.snapshot()
snapshot.deleteItems(itemsToRemove)
snapshot.appendItems(newItems, toSection: .main)
dataSource.apply(snapshot, animatingDifferences: true)
```

**Multiple sections:**
```swift
enum Section: Hashable { case featured, recent, all }

var snapshot = NSDiffableDataSourceSnapshot<Section, Item>()
snapshot.appendSections([.featured, .recent, .all])
snapshot.appendItems(featuredItems, toSection: .featured)
snapshot.appendItems(recentItems, toSection: .recent)
snapshot.appendItems(allItems, toSection: .all)
dataSource.apply(snapshot, animatingDifferences: false)
```

**Reload a single item (update cell content without delete/insert animation):**
```swift
var snapshot = dataSource.snapshot()
snapshot.reloadItems([updatedItem])
dataSource.apply(snapshot, animatingDifferences: true)
```

## Gotchas

- Item and section identifiers must be unique across the entire snapshot — duplicate identifiers cause a crash. Use stable unique IDs (e.g., `UUID`) rather than model values that can repeat.
- `apply` must be called on the main thread unless you pass `animatingDifferences: false` on a background thread (iOS 15+ allows background applies with `applySnapshotUsingReloadData`).
- `reloadItems` only reconfigures cells; it does not perform insert/delete animations. Use `deleteItems` + `appendItems` for position changes.
- `UICollectionViewDiffableDataSource` sets itself as the collection view's `dataSource` automatically — do not set a separate `dataSource` delegate.
- In iOS 15+, prefer `reconfigureItems(_:)` over `reloadItems(_:)` to update cell content without recreating the cell (better performance with custom cell configurations).
