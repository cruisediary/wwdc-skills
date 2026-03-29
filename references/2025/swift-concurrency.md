---
framework: Swift Concurrency
session: null
year: 2025
applies_to: iOS 26+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/swift-concurrency.md
  - 2021/swift-concurrency.md
---

# Swift Concurrency — WWDC25 Updates

WWDC25 introduced default actor isolation (Swift 6.2) and additional strict concurrency improvements.

## What's new

- **Default actor isolation** — `@MainActor` is now the default isolation for types conforming to `View`, `UIViewController`, and other main-thread types. Opt out with `nonisolated`.
- Swift 6 strict concurrency is now default in new projects; upgrade path is `SWIFT_STRICT_CONCURRENCY = complete`
- Improved `Sendable` inference for actor-isolated types

## Before / After

**Before (pre-WWDC25 — explicit @MainActor everywhere):**
```swift
@MainActor
class MyViewModel: ObservableObject {
    @Published var title = ""
}

@MainActor
func updateTitle(_ title: String) { ... }
```

**After (WWDC25 — default isolation on View-conforming types):**
```swift
// SwiftUI Views are implicitly @MainActor — no annotation needed
struct MyView: View {
    var body: some View { Text("Hello") }

    func handleTap() {
        // Implicitly @MainActor — no annotation required
    }
}

// Opt out with nonisolated for background work
nonisolated func parseData(_ data: Data) -> ParsedResult { ... }
```

## Migration steps

1. Run build with `SWIFT_STRICT_CONCURRENCY = complete` to surface isolation warnings
2. Remove redundant `@MainActor` annotations on `View` types (now implicit)
3. Add `nonisolated` to functions that don't need main-actor isolation
4. Replace `nonisolated(unsafe)` with proper `Sendable` design
5. Use `@preconcurrency` import for third-party code not yet Swift 6 compatible

## Compatibility notes

- Default actor isolation applies to types that conform to protocols already marked `@MainActor`
- Existing code continues to compile — changes are warnings, not errors, unless `SWIFT_STRICT_CONCURRENCY = complete`
- Requires Swift 6.2 / Xcode 26
