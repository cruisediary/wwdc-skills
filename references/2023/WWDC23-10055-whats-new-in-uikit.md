---
framework: UIKit
title: "What's new in UIKit"
session: WWDC23-10055
year: 2023
applies_to: iOS 17+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/swiftui.md
---

# What's new in UIKit (WWDC23)

UIKit iOS 17 adds `UIContentUnavailableView`, `viewIsAppearing(_:)`, SF Symbols effect APIs, and various collection/table view improvements.

## What's new

- `UIContentUnavailableView` — standard empty-state view with image, title, and subtitle (mirrors SwiftUI `ContentUnavailableView`)
- `UIViewController.viewIsAppearing(_:)` — new lifecycle callback called after `viewWillAppear` but after the view is added to the hierarchy and has a valid trait collection / geometry; ideal for first-layout adjustments
- Symbol effects — `UIImageView.addSymbolEffect(_:)`, `.removeSymbolEffect(ofType:)`, `UIImage.applyingSymbolConfiguration(_:)` with new animation effects
- `UIContentConfiguration` improvements — `UIListContentConfiguration` picks up new decoration options
- Spring animations — `UIView.animate(springDuration:bounce:initialSpringVelocity:delay:options:animations:completion:)` mirrors the SwiftUI spring API
- `UITraitCollection` changes — traits are now defined as `UITraitDefinition` protocol types; custom traits use `UIMutableTraits`
- `UIViewController` preview macro — `#Preview` macro works in UIKit files for in-canvas UIViewController previews

## Before / After

**Empty state view:**
```swift
// Before (iOS 16)
func showEmptyState() {
    let label = UILabel()
    label.text = "No Results"
    label.textAlignment = .center
    view.addSubview(label)
    // ... layout constraints
}

// After (iOS 17)
var contentUnavailableConfiguration: UIContentUnavailableConfiguration {
    var config = UIContentUnavailableConfiguration.empty()
    config.image = UIImage(systemName: "magnifyingglass")
    config.text = "No Results"
    config.secondaryText = "Try a different search."
    return config
}

// Or use the built-in search variant:
contentUnavailableConfiguration = UIContentUnavailableConfiguration.search()
```

**View controller lifecycle — first geometry pass:**
```swift
// Before: using viewDidAppear (too late) or viewWillAppear (no geometry yet)
override func viewWillAppear(_ animated: Bool) {
    super.viewWillAppear(animated)
    // view.bounds.size may not yet reflect final layout
}

// After (iOS 17)
override func viewIsAppearing(_ animated: Bool) {
    super.viewIsAppearing(animated)
    // Safe to use view.bounds, safeAreaInsets, traitCollection here
    scrollToInitialPosition()
}
```

**Symbol animation:**
```swift
// Before: no built-in animation for symbol changes
imageView.image = UIImage(systemName: "heart.fill")

// After (iOS 17)
imageView.addSymbolEffect(.pulse)
imageView.addSymbolEffect(.bounce, options: .repeating)
imageView.setSymbolImage(UIImage(systemName: "heart.fill")!,
                         contentTransition: .replace.offUp)
```

**Spring animation:**
```swift
// Before
UIView.animate(withDuration: 0.5, delay: 0,
               usingSpringWithDamping: 0.7, initialSpringVelocity: 0, ...) { }

// After (iOS 17)
UIView.animate(springDuration: 0.5, bounce: 0.3) {
    view.transform = .identity
}
```

## Migration steps

1. Replace custom empty-state views in `UITableViewController` / `UICollectionViewController` with `contentUnavailableConfiguration`.
2. Move first-layout code from `viewWillAppear` or `viewDidAppear` to `viewIsAppearing` for accurate geometry.
3. Replace `usingSpringWithDamping:initialSpringVelocity:` animations with `springDuration:bounce:`.
4. Use `#Preview { MyViewController() }` in UIKit files instead of `PreviewProvider`.

## Compatibility notes

- `UIContentUnavailableView` and `viewIsAppearing(_:)` are iOS 17+ only.
- `viewIsAppearing(_:)` is back-deployable to iOS 13 via the SDK (the method exists as a no-op stub on older OS versions), making it safe to override without a version check.
- Symbol effects require iOS 17+.
