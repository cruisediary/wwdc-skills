---
framework: SwiftUI
title: "Accessibility in SwiftUI"
session: WWDC19-238
year: 2019
applies_to: iOS 13+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/swiftui.md
---

# Accessibility in SwiftUI (WWDC19)

SwiftUI ships with built-in accessibility support. This session covers the modifier API for labeling, hinting, hiding, and describing UI elements for VoiceOver and other assistive technologies.

## What changed and why

In UIKit, accessibility required explicit property assignment (`accessibilityLabel`, `accessibilityHint`) on `UIView` subclasses. SwiftUI makes accessibility declarative — modifiers like `.accessibilityLabel()` read and compose automatically, and most standard views (Text, Button, Toggle, Slider) have sensible defaults without any extra work.

The system automatically:
- Uses the label text of `Text` and `Button` as the accessibility label
- Groups `HStack`/`VStack` children into a single accessibility element when appropriate
- Announces state changes for `Toggle` and `Slider`

## Mental model

Accessibility modifiers layer on top of the view tree identically to visual modifiers. They are not separate — they are part of the same `View` value.

```
Button("Delete", action: delete)
    .accessibilityLabel("Delete item")      // overrides the default "Delete"
    .accessibilityHint("Removes the item from your list")
    .accessibilityAddTraits(.isDestructive) // communicates danger
```

## Usage

**`.accessibilityLabel` — human-readable name:**
```swift
Image(systemName: "heart.fill")
    .accessibilityLabel("Liked")
// Without this, VoiceOver would say "heart fill" (the system name)
```

**`.accessibilityHint` — describes what happens when activated:**
```swift
Button("Buy") { purchase() }
    .accessibilityHint("Completes the purchase using Apple Pay")
```

**`.accessibilityValue` — current value of a control:**
```swift
// Useful for custom controls where the value isn't obvious from the label
Text("Volume")
    .accessibilityValue("\(Int(volume * 100)) percent")
```

**`.accessibilityHidden` — remove from accessibility tree:**
```swift
Image(systemName: "chevron.right")
    .accessibilityHidden(true)  // decorative only
```

**`.accessibilityElement(children:)` — merge group into one element:**
```swift
VStack(alignment: .leading) {
    Text("John Appleseed")
    Text("Engineering")
}
.accessibilityElement(children: .combine)
// VoiceOver reads: "John Appleseed, Engineering"
```

**`.accessibilityAddTraits` / `.accessibilityRemoveTraits`:**
```swift
Text("Selected")
    .accessibilityAddTraits(.isSelected)

Button("Submit") { submit() }
    .accessibilityAddTraits(.isDestructive)
```

**`.accessibilityAction` — custom actions in the VoiceOver rotor:**
```swift
ArticleRow(article: article)
    .accessibilityAction(named: "Share") { share(article) }
    .accessibilityAction(named: "Save for Later") { save(article) }
```

## Adopting this pattern

1. Run your app with VoiceOver enabled after every major UI change — the simulator supports VoiceOver.
2. Always provide `.accessibilityLabel` for `Image` views that are not purely decorative.
3. Use `.accessibilityHidden(true)` for purely decorative images and separator views.
4. Use `.accessibilityElement(children: .combine)` to group related labels (name + role, date + time) into a single readable element.
5. Use `.accessibilityValue` for custom controls (progress, ratings, sliders with custom UI) to communicate numeric or descriptive state.
6. Test with VoiceOver on a physical device — simulator behavior can differ for complex gestures.
