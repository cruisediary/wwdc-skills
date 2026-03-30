---
framework: Swift Concurrency
title: "Meet AsyncSequence"
session: WWDC21-10058
year: 2021
applies_to: iOS 15+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/swift-concurrency.md
---

# Meet AsyncSequence (WWDC21)

Introduces the `AsyncSequence` protocol — the async counterpart to `Sequence`, enabling `for await in` loops over values that arrive over time.

## Core concepts

- `AsyncSequence` — like `Sequence` but each element is produced asynchronously; iteration suspends between elements
- `for await in` — the loop body runs once per element, suspending at the top of each iteration while waiting for the next
- `AsyncIteratorProtocol` — underlies `AsyncSequence`; `makeAsyncIterator()` returns the iterator; `next()` returns `Element?` asynchronously
- `AsyncStream` — a concrete `AsyncSequence` for bridging callback/delegate-based sources

## Key APIs

### for await in loop

```swift
// Reading lines from a URL
let url = URL(string: "https://example.com/data.txt")!
let (asyncBytes, _) = try await URLSession.shared.bytes(from: url)
for try await line in asyncBytes.lines {
    print(line)
}

// Notification stream (iOS 15+)
for await notification in NotificationCenter.default
    .notifications(named: UIApplication.didBecomeActiveNotification) {
    handleForeground(notification)
}
```

### AsyncStream — bridging callbacks

```swift
// Wrap a CLLocationManager delegate into an AsyncSequence
func locationStream() -> AsyncStream<CLLocation> {
    AsyncStream { continuation in
        let manager = CLLocationManager()
        let delegate = LocationDelegate(continuation: continuation)
        // delegate stores continuation and calls continuation.yield(location)
        // on each update, continuation.finish() when done
        objc_setAssociatedObject(manager, "delegate", delegate, .OBJC_ASSOCIATION_RETAIN)
        manager.startUpdatingLocation()
    }
}

for await location in locationStream() {
    updateMap(location)
}

// AsyncStream with a buffer policy
let stream = AsyncStream<Int>(bufferingPolicy: .bufferingNewest(10)) { continuation in
    Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { _ in
        continuation.yield(Int.random(in: 0..<100))
    }
}
```

### Operators

```swift
// map
let doubled = stream.map { $0 * 2 }

// filter
let evens = stream.filter { $0 % 2 == 0 }

// prefix — take only the first N elements
for await value in stream.prefix(5) {
    print(value)
}

// compactMap — skip nils
let validValues = stream.compactMap { optionalValue }

// Chaining
let result = stream
    .filter { $0 > 10 }
    .map { "Value: \($0)" }
    .prefix(3)

for await text in result {
    print(text)
}
```

### Implementing AsyncSequence manually

```swift
struct CountDown: AsyncSequence {
    typealias Element = Int
    let start: Int

    struct AsyncIterator: AsyncIteratorProtocol {
        var current: Int
        mutating func next() async -> Int? {
            guard current > 0 else { return nil }
            // simulate async work
            try? await Task.sleep(nanoseconds: 1_000_000_000)
            defer { current -= 1 }
            return current
        }
    }

    func makeAsyncIterator() -> AsyncIterator {
        AsyncIterator(current: start)
    }
}

for await count in CountDown(start: 3) {
    print(count)   // 3, 2, 1
}
```

## Before / After

**Before (delegate callbacks accumulating into an array):**
```swift
class LocationTracker: NSObject, CLLocationManagerDelegate {
    var locations: [CLLocation] = []
    func locationManager(_ manager: CLLocationManager,
                         didUpdateLocations locs: [CLLocation]) {
        locations.append(contentsOf: locs)
        NotificationCenter.default.post(name: .newLocation, object: nil)
    }
}
```

**After (AsyncStream):**
```swift
func makeLocationStream(manager: CLLocationManager) -> AsyncStream<CLLocation> {
    AsyncStream { continuation in
        // set up delegate that calls continuation.yield(_:)
    }
}
for await location in makeLocationStream(manager: manager) {
    process(location)
}
```

## Compatibility notes

- `AsyncSequence`, `AsyncStream`, and `for await in` require iOS 15+
- `AsyncThrowingStream` — throwing variant; iteration is `for try await in`
- `NotificationCenter.notifications(named:)` returns `AsyncSequence<Notification>` on iOS 15+
- `URLSession.bytes(from:).lines` returns `AsyncLineSequence<URLSession.AsyncBytes>` on iOS 15+
- Operators (`map`, `filter`, `prefix`, etc.) are defined in the standard library on `AsyncSequence`
