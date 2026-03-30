---
framework: Swift Concurrency
title: "Beyond the basics of structured concurrency"
session: WWDC23-10170
year: 2023
applies_to: iOS 17+
status: reference-only
superseded_by: null
shape: guide-first
related: []
---

# Beyond the Basics of Structured Concurrency (WWDC23)

Advanced Swift concurrency: `withTaskGroup` patterns, `AsyncStream`, the `Clock` protocol, and custom executors with `SerialExecutor`.

## What changed and why

WWDC21 introduced async/await and basic structured concurrency (Task, async let, TaskGroup). Swift 5.9 at WWDC23 deepens these foundations: `AsyncStream` provides a first-class bridge from callback/delegate APIs to `AsyncSequence`, the `Clock` protocol enables testable time-dependent code, and custom executors let library authors control where and how tasks run — enabling use cases like main-thread dispatch, single-threaded serial queues, and integration with existing threading models.

## Mental model

- **`withTaskGroup`** creates a dynamic set of child tasks whose results are collected; all children must complete before the group exits.
- **`AsyncStream`** is a `AsyncSequence` you produce imperatively via a `Continuation`; ideal for bridging delegate/callback APIs.
- **`Clock` protocol** abstracts time measurement; using `any Clock` instead of `Date`/`DispatchTime` makes code testable with `TestClock`.
- **Custom executors** (`SerialExecutor`, `TaskExecutor`) control where task continuations run — the runtime calls `enqueue(_:)` to schedule a job.

## Usage

**withTaskGroup — collecting heterogeneous results:**
```swift
func fetchAllData() async throws -> [String: Data] {
    try await withThrowingTaskGroup(of: (String, Data).self) { group in
        let urls = ["a": URL(string: "https://example.com/a")!,
                    "b": URL(string: "https://example.com/b")!]
        for (key, url) in urls {
            group.addTask {
                let (data, _) = try await URLSession.shared.data(from: url)
                return (key, data)
            }
        }
        var results: [String: Data] = [:]
        for try await (key, data) in group {
            results[key] = data
        }
        return results
    }
}
```

**AsyncStream — bridging a delegate:**
```swift
func locationUpdates() -> AsyncStream<CLLocation> {
    AsyncStream { continuation in
        let delegate = LocationDelegate { location in
            continuation.yield(location)
        }
        continuation.onTermination = { _ in
            delegate.stop()
        }
        delegate.start()
    }
}

// Consuming
for await location in locationUpdates() {
    updateUI(with: location)
}
```

**AsyncStream.makeStream (Swift 5.9 — separated continuation):**
```swift
let (stream, continuation) = AsyncStream.makeStream(of: Int.self)
// Producer
continuation.yield(1)
continuation.finish()
// Consumer
for await value in stream { print(value) }
```

**Clock protocol — testable sleep:**
```swift
// Production code parameterized on Clock
func poll<C: Clock>(every interval: C.Duration, clock: C) async {
    while true {
        try? await clock.sleep(for: interval)
        await refresh()
    }
}

// Production
await poll(every: .seconds(30), clock: ContinuousClock())

// Test (using a mock clock that advances instantly)
// Use swift-clocks library or implement a TestClock that calls sleep handlers immediately
```

**Custom SerialExecutor:**
```swift
final class MySerialExecutor: SerialExecutor {
    private let queue = DispatchQueue(label: "com.example.myQueue")

    func enqueue(_ job: consuming ExecutorJob) {
        let unownedJob = UnownedJob(job)
        queue.async { unownedJob.runSynchronously(on: self.asUnownedSerialExecutor()) }
    }

    func asUnownedSerialExecutor() -> UnownedSerialExecutor {
        UnownedSerialExecutor(ordinary: self)
    }
}

// Using with an actor
actor DataStore {
    nonisolated let unownedExecutor: UnownedSerialExecutor

    init(executor: MySerialExecutor) {
        self.unownedExecutor = executor.asUnownedSerialExecutor()
    }
}
```

**Cancellation propagation in task groups:**
```swift
await withTaskGroup(of: Void.self) { group in
    group.addTask { await doWork() }
    group.addTask { await doOtherWork() }
    // Cancelling the group cancels all children
    group.cancelAll()
}
```

## Adopting this pattern

- Replace `NotificationCenter`/delegate → `AsyncStream` at the boundary; keep the rest of the code using `for await`
- Parameterize time-sensitive functions on `any Clock` from the start — retrofitting is painful
- Prefer `withTaskGroup` over manually created `Task` arrays; structured lifetimes prevent leaks
- Use custom executors only for library code or specific threading constraints; application code should rely on actors and `@MainActor`
- Always implement `onTermination` in `AsyncStream.Continuation` to clean up underlying resources when the consumer cancels
