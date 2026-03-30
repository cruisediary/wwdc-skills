---
framework: Swift Concurrency
title: "Explore structured concurrency in Swift"
session: WWDC21-10134
year: 2021
applies_to: iOS 15+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/swift-concurrency.md
---

# Explore Structured Concurrency in Swift (WWDC21)

Covers structured concurrency — `async let`, `TaskGroup`, task trees, cancellation propagation, and task priorities.

## Mental model

```
Structured concurrency = tasks form a tree
Parent task outlives all its children
Cancellation flows down the tree
Errors propagate up the tree
```

## Key APIs

### async let — static concurrency

```swift
// Two tasks start immediately; both must complete before the function returns
func loadDashboard() async throws -> Dashboard {
    async let user    = fetchUser()
    async let metrics = fetchMetrics()
    // Suspension happens here — both are awaited together
    return Dashboard(user: try await user, metrics: try await metrics)
}
```

### withTaskGroup — dynamic concurrency

```swift
// Collect results from a dynamic number of tasks
func fetchAllThumbnails(for ids: [String]) async throws -> [String: UIImage] {
    try await withThrowingTaskGroup(of: (String, UIImage).self) { group in
        for id in ids {
            group.addTask {
                let image = try await fetchThumbnail(id: id)
                return (id, image)
            }
        }
        var results: [String: UIImage] = [:]
        for try await (id, image) in group {
            results[id] = image
        }
        return results
    }
}

// Non-throwing variant
func fetchAllNames(for ids: [String]) async -> [String] {
    await withTaskGroup(of: String.self) { group in
        for id in ids {
            group.addTask { await fetchName(id: id) }
        }
        var names: [String] = []
        for await name in group {
            names.append(name)
        }
        return names
    }
}
```

### Cancellation

```swift
// Check cancellation manually
func processItems(_ items: [Item]) async throws {
    for item in items {
        try Task.checkCancellation()   // throws CancellationError if cancelled
        await process(item)
    }
}

// Poll without throwing
func processItemsSoft(_ items: [Item]) async {
    for item in items {
        guard !Task.isCancelled else { break }
        await process(item)
    }
}

// Cancel a task from the outside
let task = Task {
    try await longRunningWork()
}
task.cancel()   // propagates to all child tasks
```

### Unstructured tasks

```swift
// Task — inherits actor context and priority
Task {
    await updateUI()
}

// Task.detached — no inherited context
Task.detached(priority: .background) {
    await expensiveWork()
}
```

## Structured vs unstructured

| | Structured (`async let`, `TaskGroup`) | Unstructured (`Task`, `Task.detached`) |
|---|---|---|
| Lifetime | Tied to enclosing scope | Independent |
| Cancellation | Automatic (parent cancels children) | Manual (`task.cancel()`) |
| Priority inheritance | Yes | `Task` inherits; `Task.detached` does not |
| Use case | Most async work | Bridging to non-async contexts, fire-and-forget |

## Compatibility notes

- `withTaskGroup` / `withThrowingTaskGroup` require iOS 15+
- Use `TaskGroup.addTask` to add child tasks; tasks run immediately and concurrently
- A `TaskGroup` child task that throws cancels all other children in the group (throwing variant only)
- `Task.isCancelled` and `Task.checkCancellation()` are static — they check the *current* task
