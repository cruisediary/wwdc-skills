---
framework: Foundation
title: "Modernizing Grand Central Dispatch Usage"
session: WWDC17-706
year: 2017
applies_to: iOS 11+
status: reference-only
superseded_by: null
shape: guide-first
related: []
---

> **Reference-only (iOS 11+):** Covers GCD best practices introduced and codified with iOS 11 and macOS High Sierra. The patterns shown — serial queues for mutual exclusion, avoiding thread explosion, and using `DispatchSource` — remain the recommended approach. Swift Concurrency (`async`/`await`) introduced in iOS 15 supersedes many manual GCD patterns for new code.

## What changed and why

iOS 11 and macOS High Sierra introduced quality-of-service (QoS) propagation improvements and formalized guidance on preventing thread explosion. The session replaced the old "one concurrent queue per subsystem" pattern with a model built around a small number of serial queues and explicit QoS classes, reducing context-switch overhead and improving energy efficiency.

Key shifts:
- Use serial queues (not concurrent) as the primary synchronization primitive.
- Avoid creating many concurrent queues, which can starve the thread pool and cause thread explosion.
- Use `DispatchSource` for I/O and timer events rather than spinning threads.
- Leverage `DispatchSemaphore` and `DispatchGroup` for coordination, not busy-waiting.

## Mental model

GCD maps work onto a finite thread pool. When too many concurrent queues block on I/O or locks, GCD creates new threads to keep work moving — this "thread explosion" wastes memory and causes priority inversion. The modern model uses:

- **Serial queues** — one per independent subsystem; cheap to create, guarantee ordering.
- **QoS classes** — `.userInteractive`, `.userInitiated`, `.utility`, `.background` signal importance to the scheduler.
- **Global concurrent queues** — for truly independent, CPU-bound work only.

## Usage

**Serial queue for mutual exclusion**

```swift
let queue = DispatchQueue(label: "com.example.mysubsystem")

queue.async {
    // safe to mutate shared state here
}

// Synchronous access when you need a return value
let result = queue.sync { sharedState.value }
```

**Targeting a queue to inherit QoS**

```swift
let serialQueue = DispatchQueue(label: "com.example.serial",
                                target: DispatchQueue.global(qos: .utility))
```

**DispatchGroup for fan-out / fan-in**

```swift
let group = DispatchGroup()

for item in items {
    group.enter()
    processAsync(item) {
        group.leave()
    }
}

group.notify(queue: .main) {
    // all items processed
    updateUI()
}
```

**DispatchSource timer (replaces Timer on background queues)**

```swift
let timer = DispatchSource.makeTimerSource(queue: DispatchQueue.global(qos: .utility))
timer.schedule(deadline: .now(), repeating: .seconds(5))
timer.setEventHandler {
    performPeriodicWork()
}
timer.resume()
```

## Adopting this pattern

1. Audit existing `DispatchQueue.global()` + `async` call sites — replace with a dedicated serial queue if the work mutates shared state.
2. Remove concurrent queues created with `.concurrent` attribute unless the workload is truly embarrassingly parallel.
3. Assign a QoS class that matches the work's priority, not just `.userInitiated` everywhere.
4. Consider migrating to Swift Concurrency (`async`/`await` actors) for new code — actors model serial queue isolation at the language level.
