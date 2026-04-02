---
framework: UIKit
title: "What's New in Cocoa Touch"
session: WWDC17-203
year: 2017
applies_to: iOS 11+
status: deprecated
superseded_by: null
shape: guide-first
related: []
---

> **Deprecated:** iOS 11 overview session. Most features covered (safe area, drag & drop, large title navigation bars) are now baseline iOS behavior. Use as historical context for when these APIs were introduced.

## What changed and why

iOS 11 was a major UIKit refactoring release. Key changes: safe area APIs replaced `topLayoutGuide`/`bottomLayoutGuide`, `UINavigationBar` added large titles, `UITableView` got drag-and-drop and swipe actions, and `UIScrollView` got a new `contentInsetAdjustmentBehavior` system.

## Mental model

```
Safe area layout:
  Old: topLayoutGuide.length / bottomLayoutGuide.length (deprecated)
  New: view.safeAreaInsets / view.safeAreaLayoutGuide

Navigation bar:
  prefersLargeTitles = true  →  first vc shows large title
  navigationItem.largeTitleDisplayMode  →  .always / .never / .automatic (default)

Scroll insets:
  scrollView.contentInsetAdjustmentBehavior
    .automatic (default) — system adjusts for safe area + keyboard
    .never              — no automatic adjustment
```

## Usage

**Safe area constraints**

```swift
NSLayoutConstraint.activate([
    label.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: 16),
    label.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor)
])
```

**Large title navigation bar**

```swift
navigationController?.navigationBar.prefersLargeTitles = true
navigationItem.largeTitleDisplayMode = .always
```

## Adopting this pattern

- Replace all `topLayoutGuide`/`bottomLayoutGuide` references with `safeAreaLayoutGuide`. The old guides were deprecated in iOS 11.
- `UIScrollView.contentInsetAdjustmentBehavior = .never` is needed when you manage insets manually (e.g., custom keyboard avoidance).
