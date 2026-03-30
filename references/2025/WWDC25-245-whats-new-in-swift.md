---
framework: Swift
title: "What's new in Swift"
session: WWDC25-245
year: 2025
applies_to: iOS 26+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/swift-concurrency.md
  - 2025/swift-concurrency.md
  - 2024/WWDC24-10136-whats-new-in-swift.md
---

# Swift — What's New in Swift (WWDC25)

WWDC25 introduced default `@MainActor` isolation for types conforming to main-thread protocols, opt-out with `nonisolated`, refined typed throws, and continued improvements to `~Copyable` / `~Escapable` types.

## What's new

- **Default `@MainActor` isolation** — types conforming to `View`, `UIViewController`, and other explicitly `@MainActor`-annotated protocols are now implicitly `@MainActor`-isolated; no explicit annotation required. Note: `ObservableObject` does NOT confer `@MainActor` isolation — only protocols explicitly annotated `@MainActor` do.
- **`nonisolated` opt-out** — mark individual methods or stored properties `nonisolated` to run off the main actor without leaving the type's isolation domain
- **Typed throws improvements** — better inference of the thrown type in generic contexts; `rethrows` and typed throws interact more cleanly
- **`~Copyable` / `~Escapable` refinements** — expanded use in generics; conditional conformances involving `~Copyable` are now more expressible (see Apple docs for exact syntax)
- **`nonisolated(unsafe)` removal** — the `nonisolated(unsafe)` workaround is deprecated; proper `Sendable` design or `@unchecked Sendable` is the recommended path

## Before / After

**Before (WWDC24 — explicit `@MainActor` required on View-conforming types):**
```swift
// iOS 18: @MainActor annotation needed on every type/method
@MainActor
struct ProfileView: View {
    var body: some View { Text("Profile") }

    @MainActor
    func refresh() async { }
}
```

**After (WWDC25 — implicit `@MainActor` for View conformances):**
```swift
// iOS 26: isolation is inferred from the View conformance
struct ProfileView: View {
    var body: some View { Text("Profile") }

    // Implicitly @MainActor — no annotation needed
    func refresh() async { }

    // Opt out for background-safe utility work
    nonisolated func parsePayload(_ data: Data) -> Result { ... }
}
```

**Before (typed throws — extra `as?` cast required in generic code):**
```swift
func transform<T, E: Error>(_ value: T, using fn: (T) throws -> T) throws(E) -> T {
    // Complex — rethrows and typed throws didn't compose cleanly
}
```

**After (typed throws — cleaner generic composition):**
```swift
// iOS 26 / Swift 6.2: typed throws compose correctly with generic rethrows
// See Apple docs for exact syntax; inference is significantly improved
```

## Migration steps

1. Remove explicit `@MainActor` annotations from types that conform to `View`, `UIViewController`, or other main-actor-bound protocols — they are now implied
2. Audit `nonisolated(unsafe)` usages and replace with `nonisolated` (for truly isolation-free code) or proper `Sendable` conformance
3. For background utility functions on `@MainActor` types, add `nonisolated` to allow calling from non-main-actor contexts
4. Update `~Copyable` types to use refined generic syntax — run the Swift migrator in Xcode 26 to identify sites needing adjustment
5. Test incremental adoption: set per-target `Swift Language Version = 6` and verify that implicit isolation warnings resolve without annotation churn

## Compatibility notes

- Default actor isolation is a Swift 6.2 / Xcode 26 feature; deploying to iOS 26+ is required to use the full feature set
- Existing `@MainActor` annotations are not errors — they are redundant warnings; the Swift migrator can remove them in bulk
- `nonisolated(unsafe)` may be removed in a future Swift version — migrate proactively
- `~Copyable` / `~Escapable` API shape may shift before final release; consult Apple's Swift Evolution proposals and release notes
