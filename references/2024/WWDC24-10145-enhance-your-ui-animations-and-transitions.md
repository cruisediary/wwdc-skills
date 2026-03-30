---
framework: SwiftUI
title: "Enhance your UI animations and transitions"
session: WWDC24-10145
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/swiftui.md
---

# SwiftUI — Enhance Your UI Animations and Transitions (WWDC24)

iOS 18 adds zoom transitions and custom animation completion callbacks, enabling coordinated enter/exit choreography without `matchedGeometryEffect` workarounds.

## What changed and why

Before iOS 18, hero-style zoom animations required `matchedGeometryEffect`, which couples source and destination views via a shared namespace and is fragile when used across navigation boundaries. Completion callbacks for animations were also unavailable in SwiftUI — developers had to estimate timing or use `DispatchQueue.asyncAfter`.

iOS 18 introduces:
- **Zoom transitions** — a first-class transition that zooms from a source element to a destination view, coordinated across navigation pushes
- **`withAnimation(_:completionCriteria:_:completion:)`** — a completion handler fires when the animation fully finishes (or when its logical model update is applied, depending on `completionCriteria`)
- **`matchedTransitionSource(id:in:)`** — marks a view as the origin of a zoom transition
- **`.navigationTransitionStyle(.zoom(sourceID:in:))`** — tells the navigation system to animate a pushed view using the zoom transition from the marked source

## Mental model

Think of transitions as coordinated enter/exit choreography: the source view "hands off" its frame to the incoming destination, which scales up from that origin. On dismissal the destination scales back down to return to the source.

The key insight: the zoom transition is a *navigation-level* concept, not a per-view modifier. The source registers its identity (`matchedTransitionSource`); the destination declares which source it zooms from (`.navigationTransitionStyle`). The system handles interpolation.

For animations with side effects after completion (e.g., triggering a network call once a card fully appears), `withAnimation` completion criteria let you fire code at the exact right moment rather than guessing with timers.

- `completionCriteria: .logicallyComplete` — fires when the model update is applied (fast)
- `completionCriteria: .removed` — fires when the animation is fully removed from the render tree (after the full duration)

## Usage

**Zoom transition between a list row and a detail view:**
```swift
import SwiftUI

struct ContentView: View {
    @Namespace private var zoomNamespace

    var body: some View {
        NavigationStack {
            List(items) { item in
                NavigationLink {
                    DetailView(item: item)
                        .navigationTransitionStyle(
                            .zoom(sourceID: item.id, in: zoomNamespace)
                        )
                } label: {
                    ItemRow(item: item)
                        .matchedTransitionSource(id: item.id, in: zoomNamespace)
                }
            }
        }
    }
}
```

**Animation with completion callback:**
```swift
withAnimation(.spring, completionCriteria: .removed) {
    isExpanded = true
} completion: {
    // Fires after the spring animation fully settles
    analyticsLogger.log(.cardExpanded)
}
```

**Explicit zoom transition on a sheet:**
```swift
Button("Open Profile") {
    showProfile = true
}
.matchedTransitionSource(id: "profile-button", in: zoomNamespace)
.sheet(isPresented: $showProfile) {
    ProfileView()
        .navigationTransitionStyle(
            .zoom(sourceID: "profile-button", in: zoomNamespace)
        )
}
```

## Adopting this pattern

Replace `matchedGeometryEffect` hero animations with the zoom transition API where a zoom in/out interaction is appropriate:

| Old pattern | Replacement |
|---|---|
| `matchedGeometryEffect(id:in:)` on both source and destination | `.matchedTransitionSource(id:in:)` on source + `.navigationTransitionStyle(.zoom(...))` on destination |
| `DispatchQueue.asyncAfter` to guess animation duration | `withAnimation(completionCriteria: .removed) { } completion: { }` |
| Custom `AnyTransition` with `.asymmetric` scale | `.transition(.zoom)` for standard zoom behavior |

**Minimal adoption — add zoom to an existing NavigationStack:**
```swift
// Before: plain NavigationLink, no zoom
NavigationLink { DetailView(item: item) } label: {
    ItemRow(item: item)
}

// After: add namespace + two modifiers
@Namespace private var ns

NavigationLink {
    DetailView(item: item)
        .navigationTransitionStyle(.zoom(sourceID: item.id, in: ns))
} label: {
    ItemRow(item: item)
        .matchedTransitionSource(id: item.id, in: ns)
}
```
