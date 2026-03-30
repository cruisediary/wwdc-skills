---
framework: Accessibility
title: "Catch up on accessibility in SwiftUI"
session: WWDC24-10190
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: guide-first
related: []
---

## What changed and why

This session is a catch-up guide — not a list of new WWDC24 APIs — covering SwiftUI accessibility modifiers that many apps underuse. The goal is to help developers properly support VoiceOver, Switch Control, and Voice Control without reaching for UIKit accessibility APIs.

## Mental model

**SwiftUI accessibility works by composing semantic annotations onto views.** The render tree and the accessibility tree are separate; SwiftUI builds the accessibility tree from your modifiers. Three principles:

1. **Grouping** — combine related visual elements into one accessibility element so VoiceOver reads them as a unit.
2. **Labeling** — every interactive and informational element needs a clear, concise label that makes sense read aloud without visual context.
3. **Traits and actions** — declare what an element *is* (button, header, image) and what a user can *do* with it.

## Usage

### Grouping elements

```swift
// Combine a label and value into one VoiceOver element
HStack {
    Text("Battery")
    Spacer()
    Text("82%")
}
.accessibilityElement(children: .combine)
// VoiceOver reads: "Battery, 82%"
```

### Labels and hints

```swift
Button(action: deleteItem) {
    Image(systemName: "trash")
}
.accessibilityLabel("Delete item")
.accessibilityHint("Removes this item from your list")
// Without .accessibilityLabel, VoiceOver reads "trash" (the SF Symbol name)
```

### Traits

```swift
Text("Getting Started")
    .font(.title2)
    .accessibilityAddTraits(.isHeader)
// VoiceOver announces it as a heading; users can jump between headings with the rotor

Image("profile-photo")
    .accessibilityAddTraits(.isImage)
    .accessibilityLabel("Profile photo of Maria")

// Mark a view as selected (e.g., a custom tab)
myTabView
    .accessibilityAddTraits(isSelected ? .isSelected : [])
```

### Custom content with accessibilityCustomContent

```swift
// Provides additional detail that VoiceOver can surface on demand
// (user must enable "Custom Content" in VoiceOver rotor)
struct FlightRow: View {
    let flight: Flight

    var body: some View {
        VStack(alignment: .leading) {
            Text(flight.destination)
            Text(flight.departureTime)
        }
        .accessibilityElement(children: .combine)
        .accessibilityLabel(flight.destination)
        .accessibilityCustomContent("Departure", flight.departureTime)
        .accessibilityCustomContent("Gate", flight.gate, importance: .high)
    }
}
```

### Rotor customization

```swift
// Add a custom rotor so VoiceOver users can quickly navigate to specific items
struct ArticleView: View {
    let paragraphs: [Paragraph]

    var body: some View {
        ScrollView {
            ForEach(paragraphs) { paragraph in
                Text(paragraph.text).id(paragraph.id)
            }
        }
        .accessibilityRotor("Paragraphs") {
            ForEach(paragraphs) { paragraph in
                AccessibilityRotorEntry(paragraph.summary, id: paragraph.id)
            }
        }
    }
}
```

## Adopting this pattern

| Pattern | When to use |
|---|---|
| `.accessibilityElement(children: .combine)` | Visual groupings (icon + label, key-value pairs) |
| `.accessibilityElement(children: .ignore)` | Decorative containers whose children are independently accessible |
| `.accessibilityLabel` | Any view whose default description is wrong or missing |
| `.accessibilityAddTraits` | Custom interactive elements (custom buttons, headers, toggles) |
| `.accessibilityCustomContent` | Rich data rows where not all detail should be in the primary label |
| `.accessibilityRotor` | Long lists where users benefit from category-based navigation |
