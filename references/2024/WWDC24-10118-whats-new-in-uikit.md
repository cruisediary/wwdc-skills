---
framework: UIKit
title: "What's new in UIKit"
session: WWDC24-10118
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: migration
related: []
---

## What's new

- `UIUpdateLink`: display-synchronized animation driver replacing `CADisplayLink` for precise frame-aligned updates
- `UITabBarController.Mode.tabSidebar`: automatic tab/sidebar adaptive layout on iPad — tab bar collapses into a sidebar when space allows
- `UIListContentConfiguration.textProperties.maximumNumberOfLines`: per-cell line-limit control in list configurations
- Document launch improvements: `UIDocumentViewController` gains a built-in launch experience replacing custom launch screens
- Sheet presentation improvements: `UISheetPresentationController` gains `prefersPageSizing` and automatic keyboard-avoidance refinements
- `UITraitCollection` additions for `UIUserInterfaceIdiom.vision` and dynamic type improvements
- Symbol animations: `UIImageView` and `UIButton` support `.symbolEffect` attribute for animated SF Symbols
- `UIControl.isSymbolAnimationEnabled` to toggle symbol animation per-control

## Before / After

### Display-linked animation (CADisplayLink → UIUpdateLink)

```swift
// Before (iOS 17 and earlier)
class AnimationDriver {
    var displayLink: CADisplayLink?

    func start() {
        displayLink = CADisplayLink(target: self, selector: #selector(tick))
        displayLink?.add(to: .main, forMode: .common)
    }

    @objc func tick(link: CADisplayLink) {
        let timestamp = link.timestamp
        // update animation at timestamp
    }

    func stop() {
        displayLink?.invalidate()
        displayLink = nil
    }
}

// After (iOS 18+)
class AnimationDriver {
    var updateLink: UIUpdateLink?

    func start(in view: UIView) {
        updateLink = UIUpdateLink(view: view, actionTarget: self, selector: #selector(tick))
        updateLink?.isEnabled = true
    }

    @objc func tick(updateLink: UIUpdateLink, updateInfo: UIUpdateInfo) {
        let timestamp = updateInfo.modelTime
        // update animation at modelTime — automatically phase-aligned with display
    }
}
```

### Tab bar with sidebar (iPadOS 18)

```swift
// Before (iOS 17 and earlier)
let tabBarController = UITabBarController()
tabBarController.viewControllers = [homeVC, searchVC, profileVC]
// No automatic sidebar — required manual UISplitViewController setup

// After (iOS 18+)
let tabBarController = UITabBarController()
tabBarController.mode = .tabSidebar          // enables adaptive tab/sidebar
tabBarController.sidebar.isHidden = false    // control sidebar visibility
tabBarController.viewControllers = [homeVC, searchVC, profileVC]
// Automatically shows sidebar on iPad when horizontal space allows
```

### List cell line limit

```swift
// Before
var content = cell.defaultContentConfiguration()
content.text = item.title
// No per-cell line limit — had to subclass or use custom cell

// After (iOS 18+)
var content = cell.defaultContentConfiguration()
content.text = item.title
content.textProperties.maximumNumberOfLines = 2   // new in iOS 18
cell.contentConfiguration = content
```

## Migration steps

1. **UIUpdateLink**: Replace `CADisplayLink` with `UIUpdateLink` where animation must stay in sync with the display's refresh cadence; pass the driving `UIView` on init.
2. **Tab/sidebar on iPad**: Set `tabBarController.mode = .tabSidebar` and remove any manual sidebar workarounds; test compact/regular size-class transitions.
3. **List line limits**: Replace custom cell subclasses used only for line-limiting with `textProperties.maximumNumberOfLines` on `UIListContentConfiguration`.
4. **Document launch**: Migrate custom document-picker launch screens to `UIDocumentViewController`'s built-in launch experience (see WWDC24-10132).
5. **Symbol animations**: Adopt `.symbolEffect` on `UIImageView`/`UIButton` instead of frame-by-frame GIF or Lottie for SF Symbol animations.
6. **Sheet sizing**: Remove manual `preferredContentSize` hacks; adopt `prefersPageSizing` on `UISheetPresentationController` for standard page-height sheets.

## Compatibility notes

- `UIUpdateLink` requires iOS 18+; keep `CADisplayLink` fallback for iOS 17 and earlier.
- `UITabBarController.Mode.tabSidebar` is iOS 18+ only; existing `.automatic` mode is unchanged on iOS 17.
- `UIListContentConfiguration.textProperties.maximumNumberOfLines` is iOS 18+; guard with `#available(iOS 18, *)` or set a deployment target.
- Symbol effect APIs (`symbolEffect`) were introduced in iOS 17 for SwiftUI but UIKit support via `UIImageView.addSymbolEffect` arrived in iOS 17 — no new version gate for basic effects; advanced per-control toggle `isSymbolAnimationEnabled` is iOS 18+.
