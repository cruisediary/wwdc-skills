---
framework: Swift Concurrency
title: "A Swift Tour: Explore Swift's concurrency"
session: WWDC24-10164
year: 2024
applies_to: iOS 15+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/swift-concurrency.md
---

# Swift Concurrency — A Swift Tour: Explore Swift's Concurrency (WWDC24)

A beginner-friendly walkthrough of Swift Concurrency concepts: async/await, actors, and structured concurrency.

## What changed and why

Traditional iOS concurrency relied on threads, locks, and `DispatchQueue`. These APIs are error-prone: threads are expensive, locks can deadlock, and callback-based code is hard to read and reason about.

Swift Concurrency replaces this model with:
- **`async`/`await`** — functions that can pause without blocking a thread
- **`Task`** — a unit of asynchronous work with a clear lifetime
- **Actors** — reference types that serialize access to their state, eliminating data races
- **`@MainActor`** — ensures UI updates always happen on the main thread

The compiler enforces correct usage at compile time: you cannot accidentally access actor-isolated state from the wrong context.

## Mental model

An `async` function is like a regular function that can "pause and resume" at `await` points. When it pauses, the underlying thread is released and can do other work. When the awaited result is ready, the function resumes — possibly on a different thread, but always with the correct isolation context.

- `await` = "I'm willing to suspend here"
- `async let` = "start this work in parallel; I'll collect the result later"
- `TaskGroup` = "fan out N parallel tasks whose count I don't know at compile time"
- `actor` = "a class whose methods are automatically serialized — no explicit locks needed"
- `@MainActor` = "this code must run on the main thread"

## Usage

**Basic async/await:**
```swift
func fetchAvatar(for userID: String) async throws -> UIImage {
    let url = URL(string: "https://api.example.com/avatars/\(userID)")!
    let (data, _) = try await URLSession.shared.data(from: url)
    return UIImage(data: data) ?? UIImage(systemName: "person")!
}
```

**`async let` for parallel work:**
```swift
func loadDashboard() async throws -> Dashboard {
    async let profile = fetchProfile()
    async let feed = fetchFeed()
    async let notifications = fetchNotifications()
    // All three requests run concurrently; we collect results here
    return Dashboard(
        profile: try await profile,
        feed: try await feed,
        notifications: try await notifications
    )
}
```

**`TaskGroup` for dynamic concurrency:**
```swift
func fetchAllAvatars(userIDs: [String]) async throws -> [UIImage] {
    try await withThrowingTaskGroup(of: UIImage.self) { group in
        for id in userIDs {
            group.addTask { try await fetchAvatar(for: id) }
        }
        var images: [UIImage] = []
        for try await image in group {
            images.append(image)
        }
        return images
    }
}
```

**`@MainActor` for UI updates:**
```swift
@MainActor
class ProfileViewModel: ObservableObject {
    @Published var avatar: UIImage?

    func loadAvatar(userID: String) async {
        do {
            // Fetch happens off the main thread automatically
            let image = try await fetchAvatar(for: userID)
            // Assignment is on @MainActor — safe to update Published property
            avatar = image
        } catch {
            print("Failed:", error)
        }
    }
}
```

**Actor for shared mutable state:**
```swift
actor ImageCache {
    private var cache: [String: UIImage] = [:]

    func image(for key: String) -> UIImage? {
        cache[key]
    }

    func store(_ image: UIImage, for key: String) {
        cache[key] = image  // Serialized — no data race possible
    }
}
```

## Adopting this pattern

Replace callback/DispatchQueue patterns with Swift Concurrency equivalents:

| Old pattern | Replacement |
|---|---|
| `DispatchQueue.main.async { }` | `await MainActor.run { }` or mark the function `@MainActor` |
| `DispatchQueue.global().async { }` | `Task { }` or `Task.detached { }` |
| Completion handler `(Result<T, Error>) -> Void` | `async throws -> T` |
| `DispatchGroup` | `async let` (fixed count) or `TaskGroup` (dynamic count) |
| `NSLock` / `DispatchQueue` serial queue for shared state | `actor` |

**Minimal migration — wrap a call site:**
```swift
// Before
DispatchQueue.global().async {
    let data = expensiveComputation()
    DispatchQueue.main.async {
        self.label.text = data
    }
}

// After
Task {
    let data = await Task.detached { expensiveComputation() }.value
    await MainActor.run { label.text = data }
}
```
