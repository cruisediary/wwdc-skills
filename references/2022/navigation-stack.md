---
framework: SwiftUI Navigation
session: WWDC22-10054
year: 2022
applies_to: iOS 16+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/navigation.md
---

# NavigationStack — WWDC22 Introduction

`NavigationStack` and `NavigationSplitView` were introduced at WWDC22, replacing the deprecated `NavigationView`.

## What's new

- `NavigationStack` — manages a path of pushed views with a type-safe API
- `NavigationSplitView` — two- and three-column layouts for iPad and Mac
- `.navigationDestination(for:)` — data-driven destination resolution replacing `NavigationLink(destination:)`
- `NavigationPath` — heterogeneous, `Codable` path for programmatic and deep-link navigation
- `NavigationLink(value:)` — pushes a value, resolved lazily by `.navigationDestination`

## Before / After

**Before (NavigationView — deprecated):**
```swift
NavigationView {
    List(items) { item in
        NavigationLink(destination: DetailView(item: item)) {
            Text(item.title)
        }
    }
    .navigationTitle("Items")
}
```

**After (NavigationStack):**
```swift
NavigationStack {
    List(items) { item in
        NavigationLink(item.title, value: item)
    }
    .navigationTitle("Items")
    .navigationDestination(for: Item.self) { item in
        DetailView(item: item)
    }
}
```

## Migration steps

1. Replace `NavigationView { }` with `NavigationStack { }`
2. Replace `NavigationLink(destination:) { label }` with `NavigationLink(title, value: item)`
3. Move destination view construction into `.navigationDestination(for: Type.self) { }`
4. For programmatic navigation: add `@State private var path = NavigationPath()` and pass `path: $path` to `NavigationStack`
5. For iPad: replace `NavigationView` with two-column style with `NavigationSplitView`

## Compatibility notes

- `NavigationStack` requires iOS 16+
- `NavigationView` still compiles but is deprecated — triggers warnings in Xcode
- `NavigationLink(destination:)` still works inside `NavigationStack` but data-driven style is preferred
- `NavigationPath` items must be `Hashable`; `Codable` items enable state restoration
