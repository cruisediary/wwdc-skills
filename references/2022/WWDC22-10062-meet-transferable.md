---
framework: SwiftUI
title: "Meet Transferable"
session: WWDC22-10062
year: 2022
applies_to: iOS 16+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/swiftui.md
---

# Meet Transferable — WWDC22

`Transferable` is a Swift protocol that lets your types participate in share sheets, drag-and-drop, copy-paste, and the Clipboard — replacing `UIActivityItemSource` and `NSItemProvider` wrappers.

## Core protocol

```swift
public protocol Transferable {
    associatedtype Representation: TransferRepresentation
    static var transferRepresentation: Representation { get }
}
```

## Built-in conformances

`String`, `Data`, `URL`, `Image`, and `AttributedString` already conform to `Transferable`.

## Representation types

### CodableRepresentation — for Codable types

```swift
struct Recipe: Codable, Transferable {
    var title: String
    var ingredients: [String]

    static var transferRepresentation: some TransferRepresentation {
        CodableRepresentation(contentType: .recipe)
    }
}

extension UTType {
    static let recipe = UTType(exportedAs: "com.example.recipe")
}
```

### ProxyRepresentation — reuse another type's transfer

```swift
struct Photo: Transferable {
    var url: URL

    static var transferRepresentation: some TransferRepresentation {
        ProxyRepresentation(exporting: \.url)
        // Also imports: the URL is used to reconstruct a Photo
    }
}
```

### DataRepresentation — raw data + UTType

```swift
struct Drawing: Transferable {
    var data: Data

    static var transferRepresentation: some TransferRepresentation {
        DataRepresentation(contentType: .png) { drawing in
            drawing.renderPNG()
        } importing: { data in
            try Drawing(pngData: data)
        }
    }
}
```

### Multiple representations

```swift
struct Note: Transferable {
    var title: String
    var body: String

    static var transferRepresentation: some TransferRepresentation {
        // Rich format first (preferred)
        CodableRepresentation(contentType: .note)
        // Fallback to plain text
        ProxyRepresentation(exporting: \.body)
    }
}
```

## ShareLink with Transferable

```swift
ShareLink(item: myRecipe, preview: SharePreview(myRecipe.title))

// With custom message
ShareLink(
    item: myRecipe,
    subject: Text("Check out this recipe"),
    message: Text("I thought you'd enjoy this."),
    preview: SharePreview(myRecipe.title, image: myRecipe.thumbnailImage)
)
```

## Drag-and-drop

```swift
// Drag source
Text(item.title)
    .draggable(item)   // item must be Transferable

// Drop target
List {
    ForEach(items) { item in Text(item.title) }
}
.dropDestination(for: Recipe.self) { droppedItems, location in
    items.append(contentsOf: droppedItems)
    return true
}
```

## Compatibility notes

- `Transferable`, `ShareLink`, `draggable`, `dropDestination` require iOS 16+ / macOS 13+
- `CodableRepresentation` requires a declared UTType (exported in Info.plist or via `UTType(exportedAs:)`)
- `ProxyRepresentation` is the lightest option when your type is backed by a standard type like `URL` or `String`
