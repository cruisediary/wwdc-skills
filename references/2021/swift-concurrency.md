---
framework: Swift Concurrency
session:
  - WWDC21-10132
  - WWDC21-10134
  - WWDC21-10133
year: 2021
applies_to: iOS 15+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/swift-concurrency.md
---

# Swift Concurrency — WWDC21 Introduction

async/await, structured concurrency, and actors were introduced at WWDC21 (Swift 5.5).

## What's new

- `async`/`await` keywords for asynchronous functions
- `Task { }` — creates a new top-level concurrent task
- `async let` — runs two async operations concurrently
- `TaskGroup` — dynamic number of concurrent child tasks
- `actor` type — compiler-enforced serial access to mutable state
- `@MainActor` — constrains code to the main actor (UI thread)
- `AsyncSequence` protocol — async iteration with `for await`
- Cooperative thread pool — Swift manages threads, not the developer

## Before / After

**Before (completion handlers):**
```swift
func loadUser(id: String, completion: @escaping (Result<User, Error>) -> Void) {
    URLSession.shared.dataTask(with: url) { data, _, error in
        if let error = error { completion(.failure(error)); return }
        do {
            let user = try JSONDecoder().decode(User.self, from: data!)
            completion(.success(user))
        } catch { completion(.failure(error)) }
    }.resume()
}

// Nested callbacks ("callback hell")
loadUser(id: "1") { result in
    switch result {
    case .success(let user):
        loadPosts(userId: user.id) { postsResult in
            // ...
        }
    case .failure(let error):
        handleError(error)
    }
}
```

**After (async/await):**
```swift
func loadUser(id: String) async throws -> User {
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(User.self, from: data)
}

// Linear, readable
let user = try await loadUser(id: "1")
let posts = try await loadPosts(userId: user.id)
```

**Before (DispatchQueue for thread hopping):**
```swift
DispatchQueue.global().async {
    let result = expensiveComputation()
    DispatchQueue.main.async {
        self.label.text = result
    }
}
```

**After (@MainActor):**
```swift
let result = await Task.detached { expensiveComputation() }.value
await MainActor.run { label.text = result }
// or mark the function @MainActor
```

## Migration steps

1. Add `async throws` to functions that use completion handlers; return value instead of calling completion
2. Replace `URLSession.dataTask` with `try await URLSession.shared.data(from:)`
3. Replace `DispatchQueue.main.async { }` with `@MainActor` annotation or `await MainActor.run { }`
4. Replace `DispatchQueue.global().async { }` with `Task.detached(priority: .background) { }`
5. Replace shared mutable state protected by locks/serial queues with `actor`
6. Replace `NotificationCenter` observation with `AsyncStream` or `AsyncChannel`

## Compatibility notes

- Requires iOS 15+, macOS 12+. For iOS 13/14 back-deployment, wrap async APIs in `withCheckedContinuation`
- Xcode provides automatic migration for some URLSession and CoreData APIs
- DispatchQueue and completion-handler APIs continue to work — migration is incremental
