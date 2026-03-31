---
framework: UIKit
title: "Updating Your App for iOS 11"
session: WWDC17-810
year: 2017
applies_to: iOS 11+
status: deprecated
superseded_by: null
shape: migration
related: []
---

> **Deprecated:** iOS 11 migration guide from WWDC17. All migration steps described here are well past — any app targeting iOS 11+ has already addressed these. Preserved for historical context on when the safe area, large title, and content inset APIs were introduced.

## What's new

- `UIScrollView.contentInsetAdjustmentBehavior` replaces `automaticallyAdjustsScrollViewInsets` (deprecated)
- `safeAreaLayoutGuide` and `safeAreaInsets` replace `topLayoutGuide`/`bottomLayoutGuide` (deprecated)
- `UITableView` row height self-sizing enabled by default (`estimatedRowHeight = UITableView.automaticDimension`)
- `navigationItem.largeTitleDisplayMode` for large title bars
- Navigation bar behaviour changed with `extendedLayoutIncludesOpaqueBars`

## Before / After

**Scroll insets — before (iOS 10)**

```swift
self.automaticallyAdjustsScrollViewInsets = false
```

**Scroll insets — after (iOS 11)**

```swift
scrollView.contentInsetAdjustmentBehavior = .never
```

**Safe area — before (iOS 10)**

```swift
let topOffset = topLayoutGuide.length
```

**Safe area — after (iOS 11)**

```swift
view.safeAreaLayoutGuide.topAnchor
view.safeAreaInsets.top
```

## Migration steps

1. Remove all `automaticallyAdjustsScrollViewInsets` assignments; replace with `scrollView.contentInsetAdjustmentBehavior`.
2. Replace `topLayoutGuide`/`bottomLayoutGuide` constraints with `safeAreaLayoutGuide` anchors.
3. Remove explicit `estimatedRowHeight` assignments if using `UITableView.automaticDimension` — it is now the default.
4. Test navigation bars: if content appears under the nav bar, check `extendedLayoutIncludesOpaqueBars` and `edgesForExtendedLayout`.
5. Add `additionalSafeAreaInsets` on any view controller that draws custom chrome overlapping the scroll area.

## Compatibility notes

- `topLayoutGuide`/`bottomLayoutGuide` deprecated in iOS 11, removed in iOS 16.
- `automaticallyAdjustsScrollViewInsets` deprecated in iOS 11.
- `safeAreaInsets.bottom` is never zero on iPhone X or later.
