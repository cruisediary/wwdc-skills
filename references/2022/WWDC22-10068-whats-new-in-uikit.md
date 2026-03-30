---
framework: UIKit
title: "What's new in UIKit"
session: WWDC22-10068
year: 2022
applies_to: iOS 16+
status: reference-only
superseded_by: null
shape: migration
related: []
---

# What's new in UIKit — WWDC22

iOS 16 brought several new UIKit components and enhancements: a native calendar picker view, improved sheet presentation detents, list separator customisation, and a paste control.

## What's new

- `UICalendarView` — fully customisable calendar picker with multi-date and range selection
- `UISheetPresentationController` detents — custom fractional and absolute detents, not just `.medium`/`.large`
- `UIListSeparatorConfiguration` — per-cell separator insets and visibility
- `UIPasteControl` — privacy-friendly paste button that avoids triggering the pasteboard permission banner
- `UINavigationItem.style` — `.browser`, `.editor` styles for document-centric apps
- SF Symbols in `UIButton.Configuration` — symbol animations
- `UIPageControl` with custom indicator images
- `UIFindInteraction` — in-app find-and-replace (like Safari)
- Stage Manager awareness APIs for macOS / iPadOS 16

## Key code examples

**UICalendarView:**
```swift
let calendarView = UICalendarView()
calendarView.calendar = .current
calendarView.locale = .current
calendarView.delegate = self

// Single date selection
let singleSelection = UICalendarSelectionSingleDate(delegate: self)
calendarView.selectionBehavior = singleSelection

// Multi-date selection
let multiSelection = UICalendarSelectionMultiDate(delegate: self)
calendarView.selectionBehavior = multiSelection
```

**Custom sheet detent:**
```swift
let sheet = viewController.sheetPresentationController
let customDetent = UISheetPresentationController.Detent.custom(identifier: .init("preview")) { context in
    return context.maximumDetentValue * 0.4   // 40% of screen height
}
sheet?.detents = [customDetent, .large()]
sheet?.prefersGrabberVisible = true
present(viewController, animated: true)
```

**UIListSeparatorConfiguration:**
```swift
// In UICollectionLayoutListConfiguration
var config = UICollectionLayoutListConfiguration(appearance: .insetGrouped)
config.itemSeparatorHandler = { indexPath, sectionSeparatorConfiguration in
    var separatorConfig = sectionSeparatorConfiguration
    separatorConfig.bottomSeparatorInsets = .init(top: 0, leading: 56, bottom: 0, trailing: 0)
    return separatorConfig
}
```

**UIPasteControl:**
```swift
let pasteControl = UIPasteControl(configuration: .init())
pasteControl.target = self   // Must implement UIPasteConfigurationSupporting
view.addSubview(pasteControl)
```

## Migration steps

1. Replace custom calendar pickers (date wheels, third-party) with `UICalendarView` on iOS 16+
2. Replace hardcoded `.medium`/`.large` sheet detents with `Detent.custom` for precise heights
3. Apply `UIListSeparatorConfiguration` instead of hiding cells or using section headers for separator control
4. Replace `UIPasteboard.general` read-on-tap patterns with `UIPasteControl` to avoid privacy prompts

## Compatibility notes

- All listed APIs require iOS 16+
- `UICalendarView` does not replace `UIDatePicker` — use `UIDatePicker` when you only need date+time input
- `UIPasteControl` is the preferred way to access clipboard on iOS 16+ to avoid the system banner
