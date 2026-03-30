---
framework: Swift Concurrency
title: "Swift concurrency: Behind the scenes"
session: WWDC21-10254
year: 2021
applies_to: iOS 15+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/swift-concurrency.md
---

# Swift Concurrency: Behind the Scenes (WWDC21)

Deep-dive into the Swift concurrency runtime — the cooperative thread pool, continuation semantics, how actors are scheduled, and how priority propagation works.

## Cooperative thread pool

- Swift creates a thread pool with **at most one thread per CPU core** (by default)
- Threads are never blocked — when a task suspends (`await`), the thread picks up another task
- This avoids context-switch overhead and thread explosion compared to GCD's unbounded thread creation
- Tasks are not tied to threads; they move between threads across suspension points

```
GCD model:           thread blocks waiting → OS creates more threads → thread explosion
Swift async model:   task suspends → thread runs other work → no new threads
```

## Continuation semantics

- Every `await` is a potential suspension point — the function saves its local state as a heap-allocated continuation
- The continuation resumes on the executor associated with the calling actor (or the cooperative pool)
- `withCheckedContinuation` / `withUnsafeContinuation` create continuations that bridge to callback code
  - Checked variant: runtime crashes if resume is called zero or more than once (safety net during development)
  - Unsafe variant: no runtime checks; slightly faster

```swift
// Safe bridge — checked continuation
func waitForCallback() async -> String {
    await withCheckedContinuation { continuation in
        someLegacyAPI { result in
            continuation.resume(returning: result)
        }
    }
}
```

## Actor execution model

- Each actor has a **serial executor** — its work queue
- When an async function hops to an actor (crossing an actor boundary), it suspends, enqueues itself on the actor's executor, and resumes when the actor is free
- `@MainActor` uses the main thread as its executor — equivalent to dispatching to `DispatchQueue.main`
- Custom actors use the cooperative pool's executor by default

```
Task calls actor method
  → task suspends
  → continuation enqueued on actor's serial executor
  → actor processes work serially
  → continuation resumes on actor's executor
  → result returned to caller
```

## Priority propagation and priority inversion avoidance

- Tasks carry a **priority** (`high`, `medium`, `low`, `background`, `utility`, `userInitiated`)
- When a high-priority task awaits a result from a lower-priority actor, the actor's priority is **temporarily elevated** (priority donation) to avoid priority inversion
- Task groups inherit the priority of their parent task
- `Task.detached` does NOT inherit priority — must set explicitly

```swift
// Priority donation example (conceptual)
// High-priority UI task awaiting a background actor
Task(priority: .userInitiated) {
    // The background actor's priority is raised while this task waits
    let result = await backgroundActor.compute()
    updateUI(result)
}
```

## Thread-safety model summary

| Mechanism | Thread safety | Blocking threads |
|---|---|---|
| `DispatchQueue` (serial) | Yes | Yes (sync), sometimes (async) |
| `DispatchQueue` (concurrent + barriers) | Yes | Yes (barriers block) |
| `actor` | Yes (compiler-enforced) | No — suspends instead |
| `@MainActor` | Yes (main thread) | No — suspends instead |
| `Task.detached` | Developer's responsibility | No |

## Compatibility notes

- The cooperative thread pool is managed entirely by the Swift runtime — developers cannot configure pool size
- Blocking a thread inside an async context (e.g., `Thread.sleep`, `DispatchSemaphore.wait`) defeats the cooperative model; use `try await Task.sleep(for:)` instead
- Instruments' "Swift Tasks" template (Xcode 13+) visualises task creation, suspension, and resumption
- `LIBDISPATCH_COOPERATIVE_POOL_STRICT=1` env var enforces strict pool limits in debug builds
