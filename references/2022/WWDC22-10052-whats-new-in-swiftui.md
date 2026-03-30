---
framework: SwiftUI
title: "What's new in SwiftUI"
session: WWDC22-10052
year: 2022
applies_to: iOS 16+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/swiftui.md
  - canonical/navigation.md
  - canonical/swift-charts.md
---

# What's new in SwiftUI — WWDC22

SwiftUI iOS 16 / macOS 13 introduced overhauled navigation, native charts, new sharing primitives, layout customisation, and half-sheet presentation detents.

## What's new

### Navigation
- `NavigationStack` — replaces `NavigationView` for push navigation; type-safe path
- `NavigationPath` — heterogeneous, Codable navigation stack state
- `NavigationSplitView` — two- and three-column layouts for iPad and Mac

### Charts
- `Charts` framework integrated into SwiftUI — `Chart`, `BarMark`, `LineMark`, `PointMark`, `AreaMark`, `RuleMark`

### Presentation
- `.presentationDetents([.medium, .large])` — half-sheet (bottom sheet) support
- `.presentationDragIndicator(.visible)` — drag indicator visibility

### Sharing and export
- `ShareLink` — system share sheet from SwiftUI, works with `Transferable`
- `ImageRenderer` — render any SwiftUI view to a `UIImage`/`NSImage` or PDF

### Layout
- `Layout` protocol — custom layout algorithms composable with SwiftUI
- `Grid` and `GridRow` — table-like fixed layout

### Other
- `Charts` import — first-party chart framework
- `LabeledContent` — structured label + value rows
- `.bold()`, `.italic()`, `.fontWeight(_:)` directly on `Text`
- Multi-line text editing improvements in `TextField`
- `Table` on iPad (column sorting, multi-select)
- `SwiftUI Charts` accessibility automatic

## Key code examples

**NavigationStack with path:**
```swift
@State private var path = NavigationPath()

NavigationStack(path: $path) {
    List(items) { item in
        NavigationLink(item.title, value: item)
    }
    .navigationDestination(for: Item.self) { item in
        DetailView(item: item)
    }
}
```

**Half-sheet:**
```swift
.sheet(isPresented: $showSheet) {
    SheetContent()
        .presentationDetents([.medium, .large])
        .presentationDragIndicator(.visible)
}
```

**ShareLink:**
```swift
ShareLink(item: photoURL, preview: SharePreview("My Photo", image: Image("photo")))
```

**ImageRenderer:**
```swift
let renderer = ImageRenderer(content: MyChartView())
renderer.scale = displayScale
if let image = renderer.uiImage {
    // use image
}
```

**Layout protocol:**
```swift
struct MyEqualWidthHStack: Layout {
    func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) -> CGSize { ... }
    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) { ... }
}
```

## Migration steps

1. Replace `NavigationView` with `NavigationStack` (single column) or `NavigationSplitView` (multi-column)
2. Migrate `NavigationLink(destination:)` to `NavigationLink(value:)` + `.navigationDestination(for:)`
3. Replace custom sheet height hacks with `.presentationDetents`
4. Replace `UIActivityViewController` wrappers with `ShareLink`
5. Replace `AnyLayout` + alignment guides workarounds with the `Layout` protocol for custom layouts

## Compatibility notes

- All APIs require iOS 16+ / macOS 13+
- `NavigationView` is deprecated but still compiles
- `ImageRenderer` requires a main-thread context; use `@MainActor` or `await MainActor.run`
