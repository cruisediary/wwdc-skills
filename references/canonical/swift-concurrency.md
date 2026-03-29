---
framework: Swift Concurrency
status: current
applies_to: iOS 15+
shape: guide-first
superseded_by: null
history:
  - year: 2021
    file: 2021/swift-concurrency.md
    summary: async/await, Task, async let, actors, @MainActor introduction
  - year: 2025
    file: 2025/swift-concurrency.md
    summary: Default actor isolation, Swift 6 strict concurrency
---

# Swift Concurrency

Swift's native concurrency model based on async/await, structured concurrency, and actors (iOS 15+, Swift 5.5+). The current standard for asynchronous code in Swift — prefer over DispatchQueue, completion handlers, and Combine for new code.

## What changed and why

Before Swift Concurrency, async code required completion handlers or Combine publishers, making it hard to read, error-prone to cancel, and difficult to reason about data races. `async/await` makes asynchronous code read like synchronous code. Structured concurrency (Task, async let) makes concurrent execution safe and cancellable by default. Actors eliminate data races through compiler-enforced serial access.

## Mental model

```
async func  = a function that can suspend without blocking the thread
await       = "this might suspend — let other work run until it resumes"
Task        = a unit of concurrent work with a lifetime and priority
async let   = run two async operations concurrently, collect results together
actor       = a class where only one caller can be inside at a time
@MainActor  = "this code always runs on the main thread"
```

Structured concurrency: child tasks cannot outlive their parent. Cancel the parent → all children cancel. This prevents the "fire and forget" memory leaks common with DispatchQueue.

## Usage

```swift
// Basic async/await
func fetchUser(id: String) async throws -> User {
    let url = URL(string: "https://api.example.com/users/\(id)")!
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(User.self, from: data)
}

// Calling async code
Task {
    do {
        let user = try await fetchUser(id: "123")
        print(user.name)
    } catch {
        print(error)
    }
}

// Concurrent execution with async let
func loadDashboard() async throws -> Dashboard {
    async let user = fetchUser(id: "123")
    async let posts = fetchPosts(userId: "123")
    return Dashboard(user: try await user, posts: try await posts)
}

// Actor for safe shared state
actor ImageCache {
    private var cache: [URL: UIImage] = [:]

    func image(for url: URL) -> UIImage? {
        cache[url]
    }

    func store(_ image: UIImage, for url: URL) {
        cache[url] = image
    }
}

let cache = ImageCache()
await cache.store(image, for: url)  // safe from any thread

// @MainActor for UI updates
@MainActor
func updateUI(with user: User) {
    nameLabel.text = user.name  // always on main thread
}
```

## Adopting this pattern

If you're migrating from completion handlers or DispatchQueue, see `2021/swift-concurrency.md` for a before/after migration guide. The key mental shift: instead of passing callbacks, `await` the result inline. Instead of `DispatchQueue.main.async { }`, mark functions `@MainActor`. Instead of `OperationQueue` with dependencies, use `async let` or `TaskGroup`.
