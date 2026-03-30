---
framework: Swift Concurrency
title: "Protect mutable state with Swift actors"
session: WWDC21-10133
year: 2021
applies_to: iOS 15+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/swift-concurrency.md
---

# Protect Mutable State with Swift Actors (WWDC21)

Introduces the `actor` type — a reference type that serializes access to its own mutable state, eliminating data races at the language level.

## Core concepts

- `actor` — like a `class`, but the compiler enforces that mutable state is only accessed from within the actor's executor
- Actor isolation — the actor's own body can access state directly (synchronously); callers from outside must `await`
- `@MainActor` — a global actor that runs on the main thread; use on UI-facing code
- `nonisolated` — opts a method or property out of actor isolation (must not touch mutable actor state)
- Reentrancy — actors can interleave work between suspension points; guard invariants across awaits

## Key APIs

```swift
// Declaring an actor
actor ImageCache {
    private var cache: [URL: UIImage] = [:]

    func image(for url: URL) -> UIImage? {
        cache[url]
    }

    func store(_ image: UIImage, for url: URL) {
        cache[url] = image
    }
}

// Accessing an actor from outside — must await
let cache = ImageCache()
if let img = await cache.image(for: url) {
    // use img
}
await cache.store(downloaded, for: url)

// nonisolated — safe because it reads only immutable state
actor ProfileStore {
    let id: UUID = UUID()           // let — safe to access without await

    nonisolated var description: String {
        "ProfileStore(\(id))"       // no mutable access, so nonisolated is valid
    }
}

// @MainActor on a class — all methods/properties run on the main thread
@MainActor
class ViewModel: ObservableObject {
    @Published var title: String = ""

    func refresh() async {
        let value = await fetchTitle()
        title = value   // safe — already on main actor
    }
}

// @MainActor on individual methods
class MyViewController: UIViewController {
    @MainActor
    func updateLabel(_ text: String) {
        label.text = text
    }
}

// Calling @MainActor code from a background context
Task.detached {
    let result = await computeOffMainThread()
    await MainActor.run {
        label.text = result
    }
}
```

## Reentrancy — key pattern

```swift
actor BankAccount {
    var balance: Double = 0

    // WRONG — balance may change between the await and the mutation
    func transferUnsafe(amount: Double, to other: BankAccount) async {
        guard balance >= amount else { return }
        await other.deposit(amount)   // actor suspends here — balance can change!
        balance -= amount             // might overdraft
    }

    // RIGHT — re-check invariants after suspension
    func transfer(amount: Double, to other: BankAccount) async throws {
        guard balance >= amount else { throw BankError.insufficientFunds }
        balance -= amount             // mutate BEFORE suspending
        await other.deposit(amount)
    }

    func deposit(_ amount: Double) {
        balance += amount
    }
}
```

## Before / After

**Before (serial DispatchQueue for thread safety):**
```swift
class ThreadSafeCache {
    private var store: [URL: UIImage] = [:]
    private let queue = DispatchQueue(label: "cache")

    func image(for url: URL) -> UIImage? {
        queue.sync { store[url] }
    }
    func store(_ image: UIImage, for url: URL) {
        queue.async { self.store[url] = image }
    }
}
```

**After (actor):**
```swift
actor ImageCache {
    private var store: [URL: UIImage] = [:]
    func image(for url: URL) -> UIImage? { store[url] }
    func store(_ image: UIImage, for url: URL) { store[url] = image }
}
```

## Compatibility notes

- `actor` requires Swift 5.5 / iOS 15+
- Global actors (`@MainActor`, custom `@MyActor`) require Swift 5.5+
- Actors are reference types — do not need to be `Sendable` themselves, but their isolated state must be `Sendable` when crossing actor boundaries
- `nonisolated` methods can be called without `await`; they must not read or write mutable isolated storage
