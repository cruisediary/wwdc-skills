---
framework: Accessibility
title: "Build accessible apps with SwiftUI and UIKit"
session: WWDC23-10036
year: 2023
applies_to: iOS 17+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/swiftui.md
---

# Build accessible apps with SwiftUI and UIKit (WWDC23)

Practical guidance for making iOS apps accessible using SwiftUI and UIKit accessibility APIs — covering labels, traits, rotors, Dynamic Type, and testing.

## What changed and why

iOS 17 introduces no single landmark accessibility API change, but this session consolidates best practices for building fully accessible apps with both SwiftUI and UIKit — covering the full accessibility stack that VoiceOver, Switch Control, and Full Keyboard Access depend on.

## Mental model

- **Labels and values** — Every interactive and informative element needs an `.accessibilityLabel`. Use `.accessibilityValue` for mutable state (e.g., "On" / "Off", "3 of 5 stars").
- **Traits** — `.accessibilityAddTraits` and `.accessibilityRemoveTraits` tell assistive technologies what kind of element this is (`.isButton`, `.isHeader`, `.isSelected`, etc.).
- **Grouping** — `.accessibilityElement(children: .combine)` merges a group into one focusable element with a combined label. Use `.ignore` to hide decorative sub-elements.
- **Rotor** — `AccessibilityRotor` provides quick-navigation categories for VoiceOver's rotor gesture (e.g., "Headings", "Links", custom categories).
- **Dynamic Type** — Support all text sizes by using `Font` text styles (`.body`, `.title`, `.caption`) and `@ScaledMetric` for custom spacing/sizes. Set `minimumScaleFactor` only as a last resort.
- **Focus order** — Use `.accessibilitySortPriority` (SwiftUI) or `accessibilityActivationPoint` (UIKit) to fix non-obvious reading order.

## Usage

**Label, value, and hint:**
```swift
Toggle(isOn: $notificationsEnabled) {
    Text("Notifications")
}
.accessibilityLabel("Enable notifications")
.accessibilityValue(notificationsEnabled ? "On" : "Off")
.accessibilityHint("Double tap to toggle")
```

**Traits:**
```swift
Text("Section Header")
    .accessibilityAddTraits(.isHeader)

Image(systemName: "checkmark")
    .accessibilityHidden(true)   // Decorative — hide from VoiceOver
```

**Grouping child elements:**
```swift
HStack {
    Image(systemName: "star.fill").foregroundStyle(.yellow)
    Text("4.5")
    Text("(128 reviews)")
}
.accessibilityElement(children: .combine)
.accessibilityLabel("4.5 stars, 128 reviews")
```

**Custom rotor:**
```swift
.accessibilityRotor("Bookmarks") {
    ForEach(bookmarks) { bookmark in
        AccessibilityRotorEntry(bookmark.title, id: bookmark.id)
    }
}
```

**Dynamic Type support:**
```swift
// Always use text styles
Text("Welcome").font(.headline)

// @ScaledMetric scales a custom dimension with type size
@ScaledMetric(relativeTo: .body) private var iconSize: CGFloat = 24

Image(systemName: "star")
    .frame(width: iconSize, height: iconSize)
```

**UIKit — label and traits:**
```swift
myButton.accessibilityLabel = "Add to favourites"
myButton.accessibilityTraits = [.button]
myButton.accessibilityHint = "Adds this item to your favourites list"
```

**UIKit — custom rotor:**
```swift
let bookmarksRotor = UIAccessibilityCustomRotor(name: "Bookmarks") { predicate in
    // Return the next/previous bookmark based on predicate.searchDirection
    // Return nil when no more items
    return nil  // replace with actual logic
}
view.accessibilityCustomRotors = [bookmarksRotor]
```

**Testing accessibility:**
```swift
// Use Accessibility Inspector (Xcode > Open Developer Tool > Accessibility Inspector)
// Run VoiceOver in Simulator via Settings > Accessibility > VoiceOver
// Use XCTest to verify labels:
let element = app.buttons["Add to favourites"]
XCTAssertTrue(element.exists)
```

## Adopting this pattern

1. Audit every custom interactive view — add `.accessibilityLabel` and appropriate traits.
2. Hide purely decorative images with `.accessibilityHidden(true)`.
3. Group related label/value pairs with `.accessibilityElement(children: .combine)`.
4. Add `AccessibilityRotor` entries for navigable content categories (headings, links, bookmarks).
5. Use `.font(.body)` and other text styles everywhere; use `@ScaledMetric` for any size constant that should scale.
6. Test with VoiceOver in Simulator and with Accessibility Inspector's audit feature before shipping.
