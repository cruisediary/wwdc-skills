---
framework: Swift Concurrency
title: "Meet async/await in Swift"
session: WWDC21-10132
year: 2021
applies_to: iOS 15+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/swift-concurrency.md
---

# Meet async/await in Swift (WWDC21)

Introduced the `async`/`await` syntax in Swift 5.5, replacing completion-handler patterns with linear, readable asynchronous code.

## Quick start

- `async func` — declares a function that can suspend; caller must `await` it
- `await` — marks a suspension point; the thread is freed until the call resumes
- `try await` — combines error handling with async suspension
- `async let` — starts an async sub-task immediately; suspends when its value is first read
- Continuations — bridge callback-based APIs into the async world

## Key APIs

```swift
// Declaring an async function
func fetchImage(from url: URL) async throws -> UIImage {
    let (data, _) = try await URLSession.shared.data(from: url)
    guard let image = UIImage(data: data) else {
        throw ImageError.invalidData
    }
    return image
}

// Calling an async function
let image = try await fetchImage(from: url)

// async let — concurrent work, collected together
async let thumbnail = fetchImage(from: thumbnailURL)
async let fullSize  = fetchImage(from: fullSizeURL)
let (thumb, full) = try await (thumbnail, fullSize)

// withCheckedContinuation — wrapping a callback API
func fetchLegacyData(completion: @escaping (Data?) -> Void) { /* ... */ }

func fetchData() async -> Data? {
    await withCheckedContinuation { continuation in
        fetchLegacyData { data in
            continuation.resume(returning: data)
        }
    }
}

// withCheckedThrowingContinuation — wrapping a throwing callback
func fetchDataThrowing() async throws -> Data {
    try await withCheckedThrowingContinuation { continuation in
        fetchLegacyData { data in
            if let data {
                continuation.resume(returning: data)
            } else {
                continuation.resume(throwing: URLError(.badServerResponse))
            }
        }
    }
}
```

## Common patterns

**Before (nested completion handlers):**
```swift
func loadUserAvatar(id: String, completion: @escaping (UIImage?) -> Void) {
    fetchUser(id: id) { user in
        guard let user else { completion(nil); return }
        fetchImage(from: user.avatarURL) { image in
            completion(image)
        }
    }
}
```

**After (async/await):**
```swift
func loadUserAvatar(id: String) async -> UIImage? {
    guard let user = try? await fetchUser(id: id) else { return nil }
    return try? await fetchImage(from: user.avatarURL)
}
```

## Migration steps

1. Add `async throws` to any function that currently takes a completion handler and calls it once
2. Replace `completion(value)` with `return value`; replace `completion(.failure(error))` with `throw error`
3. At call sites, replace callback closures with `let result = try await func()`
4. Wrap legacy callback-only APIs with `withCheckedContinuation` or `withCheckedThrowingContinuation`
5. Replace `viewDidLoad` / `viewWillAppear` async kicks with `.task { }` modifier in SwiftUI or `Task { }` in UIKit

## Gotchas

- Requires iOS 15+, macOS 12+, Xcode 13+
- `async`/`await` is a compiler transformation — no runtime changes to threads
- Back-deploy to iOS 13/14 by wrapping `async` calls in `Task { }` inside a `DispatchQueue.main.async` call, or use `withCheckedContinuation` to bridge
- Completion-handler APIs remain available; migration is incremental
