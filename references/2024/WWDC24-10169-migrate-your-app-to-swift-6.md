---
framework: Swift
title: "Migrate your app to Swift 6"
session: WWDC24-10169
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: migration
related: []
---

# Swift — Migrate Your App to Swift 6 (WWDC24)

A step-by-step guide to adopting Swift 6 strict concurrency, incrementally and without breaking existing code.

## What's new

- **Swift 6 language mode** — enables strict data isolation; all data-race conditions become compile-time errors
- **`SWIFT_STRICT_CONCURRENCY` build setting** — controls how aggressively the compiler checks concurrency (`minimal`, `targeted`, `complete`)
- **`Sendable` requirement enforcement** — values crossing actor/task boundaries must conform to `Sendable`
- **`@preconcurrency` import** — suppresses Sendable warnings for modules not yet updated for Swift 6
- **`nonisolated(unsafe)`** — temporary escape hatch for properties that are manually safe but can't be proven so by the compiler

## Before / After

**Before (Swift 5 — concurrency warnings, no errors):**
```swift
// Swift 5: this compiles with warnings under targeted checking
class UserCache {
    var users: [User] = []  // Not Sendable — shared mutable state
}

actor DataManager {
    let cache = UserCache()

    func storeUser(_ user: User) {
        cache.users.append(user)  // Warning: mutation of non-isolated state
    }
}
```

**After (Swift 6 — strict isolation, errors resolved):**
```swift
// Option 1: Make UserCache an actor
actor UserCache {
    var users: [User] = []

    func append(_ user: User) {
        users.append(user)
    }
}

// Option 2: Make User and UserCache Sendable with value semantics
struct User: Sendable { var id: Int; var name: String }

final class UserCache: Sendable {
    private let lock = NSLock()
    private var _users: [User] = []

    var users: [User] {
        lock.withLock { _users }
    }

    func append(_ user: User) {
        lock.withLock { _users.append(user) }
    }
}
```

## Migration steps

1. **Enable minimal checking** — set `SWIFT_STRICT_CONCURRENCY = targeted` in your main app target; this shows concurrency warnings only for code you've annotated with `async`/`await` or actors
2. **Fix Sendable violations** — for each warning, choose a strategy: make the type a value type (`struct`), conform to `Sendable`, use an `actor`, or apply `@unchecked Sendable` as a bridge
3. **Enable complete checking** — set `SWIFT_STRICT_CONCURRENCY = complete`; this surfaces all potential data races across the entire module
4. **Enable Swift 6 mode** — set `Swift Language Version = 6`; warnings become errors
5. **Repeat per module** — migrate each Swift package target independently; use `@preconcurrency import` for unmigrated dependencies

## Compatibility notes

- Modules can be migrated independently — a Swift 6 module can depend on a Swift 5 module
- `@preconcurrency import SomeModule` suppresses Sendable warnings from that module until it is updated
- `nonisolated(unsafe)` is a valid interim tool for global constants that are effectively immutable after initialization
- Swift 6 mode does not require iOS 18+ at runtime — it is a compiler enforcement level only; the same app binary runs on older OS versions
- Third-party packages that are not Swift 6 ready will emit warnings, not errors, when imported with `@preconcurrency`
