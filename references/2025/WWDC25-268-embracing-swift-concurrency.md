---
framework: Swift Concurrency
title: "Embracing Swift concurrency"
session: WWDC25-268
year: 2025
applies_to: iOS 26+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/swift-concurrency.md
  - 2025/swift-concurrency.md
  - 2025/WWDC25-245-whats-new-in-swift.md
  - 2024/WWDC24-10169-migrate-your-app-to-swift-6.md
---

# Swift Concurrency — Adopt Default Actor Isolation (WWDC25)

This session provides a step-by-step guide for migrating existing codebases to Swift 6.2's default `@MainActor` isolation model, removing redundant annotations and leveraging `nonisolated` for background work.

## What changed and why

Swift 6.2 introduced a more approachable concurrency model by making `@MainActor` isolation implicit for types conforming to main-actor protocols like `View` and `UIViewController`, removing the need for boilerplate annotations that developers had added during the Swift 6 migration. The change acknowledges that most app code naturally belongs on the main actor, and `nonisolated` is the explicit opt-out for the minority of code that should run on a background executor.

## Mental model

Think of Swift 6.2's model as "main actor by default, opt out where needed": if a type conforms to a protocol that is already `@MainActor` (like `View`), every method and property is implicitly main-actor-isolated without any annotation. The `nonisolated` keyword is the escape hatch for pure logic that has no UI dependencies and can safely run on any thread. The migration workflow is to remove redundant annotations that the compiler no longer needs, then add `nonisolated` to the methods that genuinely should not touch the main actor.

## Concept

In Swift 6.2 (Xcode 26), types that conform to protocols already annotated `@MainActor` (such as `View`, `UIViewController`, `UIView`) are implicitly main-actor-isolated. This eliminates the need to annotate every type and method individually.

> **Note:** `ObservableObject` does NOT confer `@MainActor` isolation — only protocols explicitly annotated `@MainActor` do.

The key operations are:
- **Remove** redundant `@MainActor` on types/methods where isolation is implied by a protocol conformance
- **Add `nonisolated`** to methods that perform background-safe work and don't need the main actor
- **Eliminate `nonisolated(unsafe)`** — replace with correct `Sendable` design

## Step-by-step guide

### Step 1 — Enable complete concurrency checking

Set `SWIFT_STRICT_CONCURRENCY = complete` in your target's build settings. This surfaces all isolation warnings as errors (in Swift 6 mode) or warnings (Swift 5 mode). Fix warnings before enabling Swift 6 mode.

### Step 2 — Identify redundant `@MainActor` annotations

```swift
// Before: explicit annotation on a View-conforming type (redundant in Swift 6.2)
@MainActor
struct SettingsView: View {
    @State private var username = ""

    @MainActor
    func save() {
        UserDefaults.standard.set(username, forKey: "username")
    }

    var body: some View {
        TextField("Username", text: $username)
            .onSubmit { save() }
    }
}
```

Run Xcode 26's "Remove redundant @MainActor" fix-its to strip these automatically.

### Step 3 — Add `nonisolated` to background-safe functions

```swift
// After: isolation is implicit; background-safe utilities opt out
struct SettingsView: View {
    @State private var username = ""

    // Implicit @MainActor — still runs on main thread
    func save() {
        UserDefaults.standard.set(username, forKey: "username")
    }

    // Opt out: this pure transformation doesn't touch the UI
    nonisolated func validate(_ input: String) -> Bool {
        !input.trimmingCharacters(in: .whitespaces).isEmpty
    }

    var body: some View {
        TextField("Username", text: $username)
            .onSubmit { save() }
    }
}
```

### Step 4 — Remove `nonisolated(unsafe)`

```swift
// Before (workaround — was needed to satisfy Sendable for shared mutable state)
class SharedConfig {
    nonisolated(unsafe) var apiKey: String = ""
}

// After: use an actor or structure as Sendable value types instead
actor SharedConfig {
    var apiKey: String = ""

    func setAPIKey(_ key: String) {
        apiKey = key
    }
}

// Or, if truly read-only after init, use a struct or let:
struct AppConfig: Sendable {
    let apiKey: String
}
```

### Step 5 — Handle `@preconcurrency` imports

For third-party code not yet updated to Swift 6, annotate imports with `@preconcurrency` to silence warnings while the ecosystem catches up:

```swift
@preconcurrency import SomeLegacyFramework
```

## Key APIs

| Annotation | Purpose |
|---|---|
| `nonisolated func` | Declares a function that runs without any actor isolation; callable from any context |
| `nonisolated let` | Declares a stored property accessible from any isolation context (must be `Sendable`) |
| `@MainActor` (implicit) | Applied automatically to types conforming to main-actor protocols in Swift 6.2 |
| `@preconcurrency import` | Suppresses strict concurrency warnings from a pre-Swift-6 module |

## Gotchas

- `nonisolated func` can only access `nonisolated` or `Sendable` state — any main-actor-isolated property access inside a `nonisolated` function is a compile error
- Removing `@MainActor` from a type that does NOT conform to a main-actor protocol changes its isolation — verify this is intentional
- `nonisolated(unsafe)` is deprecated; using it in Swift 6.2 generates a warning; it may be removed in a future Swift version
- Implicit `@MainActor` isolation applies only to direct conformances to main-actor protocols, not to classes that merely subclass them (check Apple documentation for exact inheritance rules)
- Test the migration incrementally: enable Swift 6 mode one target at a time

## Compatibility notes

- Requires Swift 6.2 / Xcode 26; apps with iOS 26+ deployment target
- Existing explicit `@MainActor` annotations remain valid — they are now redundant but not errors
- The `nonisolated` keyword has existed since Swift 5.5; adding it to existing methods is backward-compatible for iOS 15+ targets
