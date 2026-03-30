---
framework: visionOS
title: "What's new in visionOS"
session: WWDC24-10101
year: 2024
applies_to: visionOS 2+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/visionos.md
---

# visionOS — What's New in visionOS (WWDC24)

visionOS 2 introduces volumetric window styles, new ornament APIs, `.glassBackgroundEffect()`, and significant passthrough improvements for mixed-reality experiences.

## What's new

- **Volumetric window style** — `WindowGroup` can now be styled with `.volumetric` to create 3D windows that exist in the user's space with a defined bounding box
- **Window push/pop ornaments** — `ornament(visibility:attachmentAnchor:contentAlignment:content:)` places UI panels that float alongside a window without occluding its content
- **`.glassBackgroundEffect()`** — applies the system glass material to any SwiftUI view, consistent with the visionOS design language; replaces manual blur + tint layering
- **Passthrough improvements** — visionOS 2 enhances the mixed-reality passthrough compositor with improved color accuracy and reduced latency; `.mixed` immersion style benefits most
- **New `ImmersionStyle` options** — `.progressive` immersion style lets users dial between passthrough and full immersion using the Digital Crown
- **`Model3D` async loading** — `Model3D(url:)` and `Model3D(named:)` gain improved loading state callbacks and placeholder support

## Before / After

**Before (visionOS 1 glass background workaround):**
```swift
// visionOS 1: manual layering to approximate glass material
ZStack {
    RoundedRectangle(cornerRadius: 16)
        .fill(.regularMaterial)
    content
}
```

**After (visionOS 2 `.glassBackgroundEffect()`):**
```swift
// visionOS 2: system-provided glass material in one modifier
content
    .glassBackgroundEffect(in: .rect(cornerRadius: 16))
```

**Before (visionOS 1 flat WindowGroup):**
```swift
WindowGroup {
    ContentView()
}
```

**After (visionOS 2 volumetric window):**
```swift
WindowGroup {
    ContentView()
}
.windowStyle(.volumetric)
.defaultSize(width: 0.5, height: 0.5, depth: 0.5, in: .meters)
```

**Before (visionOS 1 ornament — manual RealityView overlay):**
```swift
// Ornaments had to be placed manually via RealityKit attachments
```

**After (visionOS 2 ornament modifier):**
```swift
ContentView()
    .ornament(attachmentAnchor: .scene(.bottom)) {
        HStack { /* toolbar buttons */ }
            .glassBackgroundEffect()
    }
```

## Migration steps

1. Replace manual glass-material layering (`RoundedRectangle + .regularMaterial`) with `.glassBackgroundEffect(in:)`
2. Move toolbar/panel UI that floats beside windows into `.ornament(attachmentAnchor:content:)` instead of embedding it in RealityKit attachments
3. Adopt `.windowStyle(.volumetric)` with `.defaultSize(width:height:depth:in:)` for any window that displays 3D content
4. Audit `ImmersionStyle` usage — offer `.progressive` as an option so users can choose their preferred immersion level via Digital Crown
5. Remove `#available(visionOS 2, *)` guards once the minimum deployment target is raised to visionOS 2

## Compatibility notes

- All new APIs require visionOS 2+; visionOS 1 builds must wrap with `#available(visionOS 2, *)`
- `.glassBackgroundEffect()` is visionOS-only; use `#if os(visionOS)` to guard platform-specific code
- `.progressive` immersion style requires visionOS 2 and the user's Digital Crown; not available on Simulator
- `ornament(attachmentAnchor:)` is available on visionOS 2+ only; fall back to toolbar or overlay UI on visionOS 1
