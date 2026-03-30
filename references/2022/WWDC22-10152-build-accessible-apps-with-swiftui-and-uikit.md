---
framework: Accessibility
title: "Build accessible apps with SwiftUI and UIKit"
session: WWDC22-10152
year: 2022
applies_to: iOS 16+
status: reference-only
superseded_by: null
shape: guide-first
related: []
---

# Build accessible apps with SwiftUI and UIKit — WWDC22

A deep dive into VoiceOver customisation, accessibility rotor entries, and custom content in both SwiftUI and UIKit, targeting iOS 16 improvements.

## What changed and why

iOS 15–16 expanded the accessibility APIs to address two long-standing gaps: structured navigation (custom rotors for jumping between headings, errors, or any named category) and information density control (custom content that VoiceOver reads on demand rather than always). These additions give developers fine-grained control over the VoiceOver experience without requiring a parallel accessible view hierarchy.

## Mental model

Think of VoiceOver as reading a linearized version of your view hierarchy: it reads each accessible element in order, with its label, value, traits, and hint. Accessibility modifiers let you reshape that linearization — combining noisy child elements into one, appending secondary details behind a "more content" gesture, and adding rotor shortcuts so users can jump to the type of content they care about. The goal is to make the auditory experience as navigable and concise as the visual one.

## Usage example

### AccessibilityRotorEntry (SwiftUI)

The accessibility rotor allows VoiceOver users to jump between items of a specific type (headings, links, etc.). Custom rotors let you define your own categories.

```swift
struct ArticleView: View {
    let article: Article

    var body: some View {
        ScrollView {
            Text(article.body)
        }
        .accessibilityRotor("Headings") {
            ForEach(article.headings) { heading in
                AccessibilityRotorEntry(heading.text, id: heading.id)
            }
        }
    }
}
```

### .accessibilityCustomContent (SwiftUI)

Attach supplementary information that VoiceOver reads on demand (not by default, reducing noise):

```swift
struct ContactRow: View {
    let contact: Contact

    var body: some View {
        HStack {
            Text(contact.name)
        }
        .accessibilityElement(children: .combine)
        .accessibilityLabel(contact.name)
        .accessibilityCustomContent("Job Title", contact.jobTitle, importance: .default)
        .accessibilityCustomContent("Department", contact.department, importance: .high)
    }
}
```

- `.high` importance — read inline with the element
- `.default` importance — read when the user activates "More Content" in VoiceOver

### UIKit: accessibilityCustomContent

```swift
import Accessibility

class ContactCell: UITableViewCell {
    func configure(with contact: Contact) {
        accessibilityLabel = contact.name
        accessibilityCustomContent = [
            AXCustomContent(label: "Job Title", value: contact.jobTitle),
            AXCustomContent(label: "Department", value: contact.department, importance: .high)
        ]
    }
}
```

### Custom accessibility actions

```swift
// SwiftUI
Image(systemName: "heart")
    .accessibilityLabel("Like")
    .accessibilityAddTraits(.isButton)
    .accessibilityAction(named: "Like post") {
        likePost()
    }
    .accessibilityAction(named: "Share post") {
        sharePost()
    }
```

### Grouping elements

```swift
// Combine child elements into a single accessible element
HStack {
    Image(systemName: "person.fill")
    Text(user.name)
    Text(user.role)
}
.accessibilityElement(children: .combine)
.accessibilityLabel("\(user.name), \(user.role)")
```

### VoiceOver adjustable values

```swift
Slider(value: $volume, in: 0...1)
    .accessibilityLabel("Volume")
    .accessibilityValue("\(Int(volume * 100)) percent")
    .accessibilityAdjustableAction { direction in
        switch direction {
        case .increment: volume = min(1, volume + 0.1)
        case .decrement: volume = max(0, volume - 0.1)
        @unknown default: break
        }
    }
```

## UIKit: accessibilityRotor

```swift
override var accessibilityCustomRotors: [UIAccessibilityCustomRotor]? {
    get {
        let headingRotor = UIAccessibilityCustomRotor(name: "Headings") { predicate in
            // Return next/previous heading element based on predicate.searchDirection
            let direction = predicate.searchDirection
            // ... find next heading and return UIAccessibilityCustomRotorItemResult
            return nil
        }
        return [headingRotor]
    }
    set { }
}
```

## Adopting this pattern

- Always provide `.accessibilityLabel` for images and icons that convey meaning
- Use `.accessibilityCustomContent` for secondary details to keep the default read-out concise
- Add custom rotors for content types users need to navigate quickly (headings, errors, links)
- Test with VoiceOver on a real device — simulators don't fully replicate VoiceOver behaviour

## Compatibility notes

- `AccessibilityRotorEntry` and `.accessibilityCustomContent` in SwiftUI require iOS 15+
- `AXCustomContent` in UIKit (`import Accessibility`) requires iOS 14+
- `.accessibilityCustomContent` importance API requires iOS 15+
