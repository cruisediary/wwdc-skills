---
framework: UIKit
title: "A Tour of UICollectionView"
session: WWDC18-225
year: 2018
applies_to: iOS 12+
status: deprecated
superseded_by: null
shape: guide-first
related: []
---

> **Deprecated:** This session covers `UICollectionView` fundamentals from WWDC18. The patterns here remain valid on iOS 12+, but the preferred data source is now `UICollectionViewDiffableDataSource` (iOS 13+) and the preferred layout system is `UICollectionViewCompositionalLayout` (iOS 13+). Use this as historical context only.

## What changed and why

Before iOS 13, `UICollectionView` required a manual `UICollectionViewDataSource` with index-path arithmetic and explicit `performBatchUpdates` calls. WWDC18 session 225 documented the authoritative patterns for this era — still the foundation you need to understand before adopting the diffable/compositional APIs.

## Mental model

```
UICollectionView
  └── UICollectionViewLayout  (describes geometry)
        └── UICollectionViewFlowLayout  (linear grid; rows/columns)
  └── UICollectionViewDataSource  (provides cells and supplementary views)
  └── UICollectionViewDelegate    (handles selection, display events)
```

**Cells** are dequeued and reused; register them before the view appears. **Supplementary views** (headers/footers) follow the same register/dequeue pattern. **Batch updates** group insertions, deletions, and moves so the collection view animates them as a unit.

## Usage

**Register and dequeue**

```swift
collectionView.register(MyCell.self, forCellWithReuseIdentifier: "cell")
collectionView.register(HeaderView.self,
    forSupplementaryViewOfKind: UICollectionView.elementKindSectionHeader,
    withReuseIdentifier: "header")

// In cellForItemAt:
let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "cell", for: indexPath) as! MyCell
```

**Flow layout sizing**

```swift
let layout = UICollectionViewFlowLayout()
layout.itemSize = CGSize(width: 100, height: 100)
layout.minimumInteritemSpacing = 8
layout.minimumLineSpacing = 12
layout.sectionInset = UIEdgeInsets(top: 16, left: 16, bottom: 16, right: 16)
layout.headerReferenceSize = CGSize(width: 0, height: 44)
```

**Batch updates**

```swift
collectionView.performBatchUpdates({
    collectionView.insertItems(at: [IndexPath(item: 0, section: 0)])
    collectionView.deleteItems(at: [IndexPath(item: 3, section: 0)])
    collectionView.moveItem(at: IndexPath(item: 1, section: 0),
                            to: IndexPath(item: 2, section: 0))
}, completion: nil)
```

## Adopting this pattern

- Always update the data model **inside** `performBatchUpdates` before calling insert/delete/move so the data source and the view stay in sync.
- For iOS 13+, replace `performBatchUpdates` with `UICollectionViewDiffableDataSource` and `NSDiffableDataSourceSnapshot` to eliminate manual index tracking.
- For complex layouts (sticky headers, orthogonal sections), replace `UICollectionViewFlowLayout` with `UICollectionViewCompositionalLayout` (iOS 13+).
- `UICollectionViewFlowLayout` with `estimatedItemSize = UICollectionViewFlowLayout.automaticSize` enables self-sizing cells via Auto Layout — still relevant on iOS 12.
