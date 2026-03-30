---
framework: SwiftUI Navigation
title: "The SwiftUI cookbook for navigation"
session: WWDC22-10054
year: 2022
applies_to: iOS 16+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/navigation.md
  - canonical/swiftui.md
---

# The SwiftUI cookbook for navigation — WWDC22

A deep-dive into the new navigation APIs introduced in iOS 16: `NavigationStack`, `NavigationPath`, and programmatic deep linking patterns.

## Core APIs

### NavigationStack

```swift
// Basic stack with implicit path
NavigationStack {
    RootView()
        .navigationDestination(for: Item.self) { item in
            DetailView(item: item)
        }
}
```

### navigationDestination(for:destination:)

The primary mechanism for data-driven destination resolution. Each type gets one destination closure per stack.

```swift
.navigationDestination(for: Recipe.self) { recipe in
    RecipeDetailView(recipe: recipe)
}
.navigationDestination(for: Ingredient.self) { ingredient in
    IngredientDetailView(ingredient: ingredient)
}
```

### NavigationPath — heterogeneous stack

```swift
@State private var path = NavigationPath()

// Push programmatically
path.append(someRecipe)    // Recipe must be Hashable
path.append(someIngredient)

// Pop to root
path.removeLast(path.count)

// Codable state restoration (all values must be Codable)
if let data = try? encoder.encode(path.codable) {
    UserDefaults.standard.set(data, forKey: "navPath")
}
```

### navigationDestination(isPresented:destination:)

Sheet-like programmatic push for a single boolean flag:

```swift
@State private var showDetail = false

Button("Open") { showDetail = true }
    .navigationDestination(isPresented: $showDetail) {
        DetailView()
    }
```

## Deep linking

```swift
// Handle incoming URL
.onOpenURL { url in
    if let destination = decode(url) {
        path.append(destination)
    }
}
```

## NavigationSplitView

```swift
// Two-column
NavigationSplitView {
    SidebarList(selection: $selectedItem)
} detail: {
    if let item = selectedItem {
        DetailView(item: item)
    }
}

// Three-column
NavigationSplitView {
    CategoryList(selection: $category)
} content: {
    ItemList(category: category, selection: $item)
} detail: {
    ItemDetail(item: item)
}
```

## Design patterns

- **Single source of truth** — store `NavigationPath` in `@State` or a view model; encode it for state restoration
- **Type-based routing** — each navigable type registers exactly one `.navigationDestination(for:)` in the stack
- **Avoid deep nesting** — `.navigationDestination` is picked up from any view in the stack, not just the root
- **Programmatic navigation** — append/remove from `path` instead of using boolean flags per destination

## Compatibility notes

- `NavigationStack` and `NavigationSplitView` require iOS 16+ / macOS 13+
- `NavigationPath` items must be `Hashable`; state restoration additionally requires `Codable`
- `NavigationView` is deprecated in iOS 16 — migrate to avoid future removal
