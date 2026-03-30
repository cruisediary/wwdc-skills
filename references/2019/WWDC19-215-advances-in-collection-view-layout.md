---
framework: UIKit
title: "Advances in Collection View Layout"
session: WWDC19-215
year: 2019
applies_to: iOS 13+
status: reference-only
superseded_by: null
shape: code-first
related: []
---

# Advances in Collection View Layout (WWDC19)

`UICollectionViewCompositionalLayout` — a new declarative layout system for `UICollectionView` that replaces `UICollectionViewFlowLayout` for complex, multi-section layouts.

## Quick start

```swift
let layout = UICollectionViewCompositionalLayout { sectionIndex, environment in
    // Item: the leaf element
    let itemSize = NSCollectionLayoutSize(
        widthDimension: .fractionalWidth(0.5),
        heightDimension: .fractionalHeight(1.0)
    )
    let item = NSCollectionLayoutItem(layoutSize: itemSize)
    item.contentInsets = NSDirectionalEdgeInsets(top: 4, leading: 4, bottom: 4, trailing: 4)

    // Group: a row or column of items
    let groupSize = NSCollectionLayoutSize(
        widthDimension: .fractionalWidth(1.0),
        heightDimension: .absolute(120)
    )
    let group = NSCollectionLayoutGroup.horizontal(layoutSize: groupSize, subitems: [item])

    // Section: contains groups
    let section = NSCollectionLayoutSection(group: group)
    section.contentInsets = NSDirectionalEdgeInsets(top: 8, leading: 16, bottom: 8, trailing: 16)
    return section
}

collectionView.collectionViewLayout = layout
```

## Key APIs

| API | Description |
|-----|-------------|
| `UICollectionViewCompositionalLayout` | Top-level layout object; takes a per-section closure |
| `NSCollectionLayoutItem` | Leaf cell descriptor; defines size and insets |
| `NSCollectionLayoutGroup.horizontal(layoutSize:subitems:)` | Horizontal row of items |
| `NSCollectionLayoutGroup.vertical(layoutSize:subitems:)` | Vertical column of items |
| `NSCollectionLayoutGroup.custom(layoutSize:itemProvider:)` | Fully custom item placement |
| `NSCollectionLayoutSection` | Contains one group; repeated to fill the section |
| `NSCollectionLayoutSize` | Width + height dimensions |
| `.fractionalWidth(_:)` | Fraction of the container's width |
| `.fractionalHeight(_:)` | Fraction of the container's height |
| `.absolute(_:)` | Fixed point value |
| `.estimated(_:)` | Self-sizing with an initial estimate |
| `NSCollectionLayoutBoundarySupplementaryItem` | Header or footer attached to a section |
| `section.orthogonalScrollingBehavior` | Enables horizontal scrolling within a vertically-scrolling section |

## Common patterns

**Horizontal scrolling section (carousel):**
```swift
let section = NSCollectionLayoutSection(group: group)
section.orthogonalScrollingBehavior = .continuous
// Or .groupPaging for snap-to-group, .groupPagingCentered for centered paging
```

**Section header:**
```swift
let headerSize = NSCollectionLayoutSize(
    widthDimension: .fractionalWidth(1.0),
    heightDimension: .estimated(44)
)
let header = NSCollectionLayoutBoundarySupplementaryItem(
    layoutSize: headerSize,
    elementKind: UICollectionView.elementKindSectionHeader,
    alignment: .top
)
section.boundarySupplementaryItems = [header]
```

**Full-width banner + grid below (different layout per section):**
```swift
let layout = UICollectionViewCompositionalLayout { sectionIndex, _ in
    if sectionIndex == 0 {
        // Banner: single full-width item
        let item = NSCollectionLayoutItem(layoutSize: .init(widthDimension: .fractionalWidth(1), heightDimension: .absolute(200)))
        let group = NSCollectionLayoutGroup.horizontal(layoutSize: .init(widthDimension: .fractionalWidth(1), heightDimension: .absolute(200)), subitems: [item])
        return NSCollectionLayoutSection(group: group)
    } else {
        // 3-column grid
        let item = NSCollectionLayoutItem(layoutSize: .init(widthDimension: .fractionalWidth(1/3), heightDimension: .fractionalHeight(1)))
        let group = NSCollectionLayoutGroup.horizontal(layoutSize: .init(widthDimension: .fractionalWidth(1), heightDimension: .absolute(100)), subitems: [item])
        return NSCollectionLayoutSection(group: group)
    }
}
```

**`UICollectionViewCompositionalLayout.list` (iOS 14+):**
```swift
// Shortcut for list-style layouts
let config = UICollectionLayoutListConfiguration(appearance: .insetGrouped)
let layout = UICollectionViewCompositionalLayout.list(using: config)
```

## Gotchas

- `NSCollectionLayoutGroup.horizontal(layoutSize:count:)` divides width evenly among N items — simpler than providing explicit subitems when all items are the same size.
- `orthogonalScrollingBehavior` only applies to the scroll direction perpendicular to the collection view's main scroll axis.
- `NSCollectionLayoutItem` size is relative to its containing group, not the collection view — nesting is additive.
- Unlike `FlowLayout`, supplementary views (headers/footers) must be declared in the layout, not just registered on the collection view.
- For iOS 14+, combine `UICollectionViewCompositionalLayout` with `UICollectionViewDiffableDataSource` + `UICollectionViewListCell` for table-like lists with full swipe action support.
