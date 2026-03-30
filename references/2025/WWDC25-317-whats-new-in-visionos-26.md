---
framework: visionOS
title: "What's new in visionOS 26"
session: WWDC25-317
year: 2025
applies_to: visionOS 26+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/visionos.md
  - 2024/WWDC24-10101-whats-new-in-visionos.md
---

# visionOS — What's New in visionOS (WWDC25)

visionOS 26 refines the platform with Liquid Glass integration in spatial UI, updated immersive space APIs, and improvements to passthrough and scene understanding.

## What's new

- **Liquid Glass in spatial UI** — system UI elements (windows, ornaments, controls) adopt Liquid Glass material in visionOS 26; apps built against the visionOS 26 SDK receive this automatically
- **Immersive space improvements** — refined APIs for transitioning between progressive and full immersion; better handling of immersive space lifecycle events (see Apple docs)
- **Scene understanding updates** — expanded plane detection and mesh anchors for room-scale interactions; additional `ARKitSession` provider options
- **Passthrough improvements** — higher fidelity passthrough rendering; new API to control passthrough blend amount programmatically (see Apple docs)
- **Window and ornament updates** — ornament placement and sizing refined; additional `.windowStyle` and `.windowResizability` options

## Before / After

**Before (visionOS 2 — opening an immersive space):**
```swift
struct MyApp: App {
    @State private var immersionStyle: ImmersionStyle = .mixed

    var body: some Scene {
        WindowGroup {
            ContentView()
        }

        ImmersiveSpace(id: "mainSpace") {
            ImmersiveView()
        }
        .immersionStyle(selection: $immersionStyle, in: .mixed, .full)
    }
}
```

**After (visionOS 26 — same pattern, new lifecycle hooks available; see Apple docs):**
```swift
// Existing code continues to compile on visionOS 26.
// New: additional lifecycle modifiers for space transition events.
// Exact modifier names — refer to Xcode 26 visionOS documentation.
struct MyApp: App {
    @State private var immersionStyle: ImmersionStyle = .mixed

    var body: some Scene {
        WindowGroup {
            ContentView()
        }

        ImmersiveSpace(id: "mainSpace") {
            ImmersiveView()
        }
        .immersionStyle(selection: $immersionStyle, in: .mixed, .full)
        // New visionOS 26 lifecycle modifier — see Apple docs
    }
}
```

## Migration steps

1. Build with the visionOS 26 SDK and inspect system UI elements — Liquid Glass material is applied automatically; adjust tinting or backgrounds if contrast is impacted
2. Review `ImmersiveSpace` lifecycle handlers; new transition events may require explicit handling
3. Update scene understanding code if using plane detection — new anchor types may be available
4. Test passthrough rendering fidelity on physical hardware; simulator behavior may differ
5. Verify ornament placement; sizing behavior may have changed in visionOS 26

## Compatibility notes

- Liquid Glass on system UI is automatic for apps built against the visionOS 26 SDK
- Existing visionOS 2 apps continue to work without changes; new APIs require visionOS 26+
- Scene understanding additions require visionOS 26+ entitlements and device support
- Exact API names for new immersive space lifecycle and passthrough APIs should be confirmed against Xcode 26 release documentation
