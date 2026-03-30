---
framework: UIKit
title: "What's new in UIKit"
session: WWDC25-243
year: 2025
applies_to: iOS 26+
status: reference-only
superseded_by: null
shape: migration
related: []
---

# UIKit — What's New in UIKit (WWDC25)

iOS 26 updates UIKit to align with the Liquid Glass design system, introduces fluid visual transitions, and brings default actor isolation to UIViewController and UIView subclasses.

## What's new

- **Liquid Glass in UIKit** — system chrome (navigation bars, tab bars, toolbars) automatically adopts Liquid Glass material when built against the iOS 26 SDK; no explicit opt-in required
- **Default `@MainActor` isolation** — `UIViewController` and `UIView` conformances are implicitly main-actor-isolated in Swift 6.2; explicit `@MainActor` annotations on subclasses can be removed
- **Fluid visual transitions** — new transition APIs for presenting and dismissing view controllers with Liquid Glass-compatible animations (see Apple docs for specific API names)
- **Updated `UITabBarController` styles** — tab bar appearance refined to match iOS 26 Liquid Glass styling; existing `.tabSidebar` mode from iOS 18 continues
- **Toolbar and navigation bar material APIs** — new customization points to control blur intensity and tinting for Liquid Glass surfaces (see Apple docs)

## Before / After

**Before (iOS 18 — explicit `@MainActor` on UIViewController subclass):**
```swift
@MainActor
class ProfileViewController: UIViewController {
    @MainActor
    func reloadData() {
        tableView.reloadData()
    }
}
```

**After (iOS 26 / Swift 6.2 — implicit isolation via UIViewController conformance):**
```swift
// @MainActor is implicit for UIViewController subclasses in Swift 6.2
class ProfileViewController: UIViewController {
    func reloadData() {
        // Still runs on main thread — no annotation needed
        tableView.reloadData()
    }

    // Opt out for background-safe utilities
    nonisolated func buildSnapshot(from items: [Item]) -> NSDiffableDataSourceSnapshot<Section, Item> {
        var snapshot = NSDiffableDataSourceSnapshot<Section, Item>()
        snapshot.appendSections([.main])
        snapshot.appendItems(items, toSection: .main)
        return snapshot
    }
}
```

**Before (iOS 18 — custom navigation bar appearance):**
```swift
let appearance = UINavigationBarAppearance()
appearance.configureWithOpaqueBackground()
appearance.backgroundColor = .systemBackground
navigationController?.navigationBar.standardAppearance = appearance
```

**After (iOS 26 — Liquid Glass appearance applied automatically):**
```swift
// Building against iOS 26 SDK: system chrome uses Liquid Glass by default.
// Customizing blur or tinting — see Apple docs for updated UINavigationBarAppearance APIs.
// Existing UINavigationBarAppearance code continues to compile; visual output will differ.
```

## Migration steps

1. Build with the iOS 26 SDK and run the app on a simulator or device to review how Liquid Glass affects custom navigation bars, tab bars, and toolbars — adjust `UINavigationBarAppearance` where needed
2. Remove explicit `@MainActor` annotations from `UIViewController` and `UIView` subclasses (now implicit via Swift 6.2 protocol inference); use Xcode 26 fix-its for bulk removal
3. Add `nonisolated` to view controller methods that construct data snapshots or perform parsing without touching UIKit APIs
4. Audit any `nonisolated(unsafe)` usages and migrate to actor-based or `Sendable`-conforming designs
5. Test `UITabBarController` visuals on iOS 26 — the Liquid Glass material may require adjusting tint colors or custom backgrounds

## Compatibility notes

- Liquid Glass appearance on system chrome is automatic when the app is built against the iOS 26 SDK; apps built against older SDKs retain legacy appearance
- `nonisolated` on UIKit methods is backward-compatible (Swift 5.5+) but the implicit-isolation feature requires Swift 6.2 / Xcode 26
- Exact API names for fluid transition and Liquid Glass customization should be verified against Xcode 26 release notes before shipping
