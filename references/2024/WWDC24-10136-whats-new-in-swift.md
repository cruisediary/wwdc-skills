---
framework: Swift
title: "What's new in Swift"
session: WWDC24-10136
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: migration
related: []
---

# Swift — What's New in Swift (WWDC24)

WWDC24 introduced Swift 5.10 and previewed the Swift 6 transition, with typed throws, noncopyable types, and complete concurrency checking.

## What's new

- **Typed throws** — `throws(MyError)` annotates the exact error type a function can throw; callers can catch without `as?` casting
- **Noncopyable types** (`~Copyable`) — suppress the implicit copy of a value type, enabling exclusive ownership semantics
- **`consume` operator** — explicitly moves ownership of a noncopyable value, preventing further use of the original binding
- **Global actor isolation improvements** — cleaner inference of `@MainActor` on types conforming to main-thread protocols
- **Complete concurrency checking** — `SWIFT_STRICT_CONCURRENCY = complete` surfaces all data-race warnings as errors in Swift 6 mode
- **Swift 6 language mode** — opt-in per-module via `Swift Language Version = 6` build setting

## Before / After

**Before (untyped throws — requires `as?` at call site):**
```swift
enum NetworkError: Error {
    case timeout
    case unauthorized
}

func fetchUser(id: Int) throws -> User {
    // Could throw any Error — caller must cast
    throw NetworkError.timeout
}

do {
    let user = try fetchUser(id: 42)
} catch let e as NetworkError {
    // Explicit cast needed
    print(e)
} catch {
    // Catch-all required even though only NetworkError is possible
}
```

**After (typed throws — exhaustive catch, no casting):**
```swift
func fetchUser(id: Int) throws(NetworkError) -> User {
    throw NetworkError.timeout
}

do {
    let user = try fetchUser(id: 42)
} catch {
    // `error` is inferred as NetworkError — no cast needed
    switch error {
    case .timeout: print("Timed out")
    case .unauthorized: print("Unauthorized")
    }
}
```

## Migration steps

1. Start with `SWIFT_STRICT_CONCURRENCY = targeted` to see concurrency warnings without blocking the build
2. Fix `Sendable` violations surfaced by targeted checking — mark types `Sendable` or use `@unchecked Sendable` as a short-term bridge
3. Move to `SWIFT_STRICT_CONCURRENCY = complete` and resolve remaining warnings
4. Set `Swift Language Version = 6` in build settings to enable Swift 6 mode; treat remaining warnings as errors
5. Migrate module-by-module — each Swift package target can adopt Swift 6 independently
6. Adopt typed throws (`throws(MyError)`) in new code; existing untyped `throws` code continues to compile

## Compatibility notes

- Typed throws require Swift 6.0+ toolchain; can be used with iOS 18+ deployment targets
- Noncopyable types (`~Copyable`) require Swift 5.9+; full generics support requires Swift 6
- `SWIFT_STRICT_CONCURRENCY = complete` is a warning-only change until `Swift Language Version = 6` is set
- Swift 6 mode is per-module — dependent packages remain on Swift 5 until individually upgraded
