---
framework: XCTest
title: "What's New in Testing"
session: WWDC17-405
year: 2017
applies_to: iOS 11+
status: reference-only
superseded_by: null
shape: code-first
related: []
---

> **Reference-only:** XCTest APIs shown here are still valid in Xcode 16. `measure()` performance testing and parallel testing remain current. For the modern replacement, see Swift Testing (`@Test`, `#expect`).

## Quick start

```swift
import XCTest

class MyTests: XCTestCase {
    func testExample() {
        let result = myFunction(42)
        XCTAssertEqual(result, 84)
    }

    func testPerformance() {
        measure {
            _ = (0..<10000).map { $0 * $0 }
        }
    }
}
```

## Key APIs

| API | Description |
|---|---|
| `XCTAssertEqual(_:_:)` | Value equality assertion |
| `XCTAssertNil(_:)` / `XCTAssertNotNil(_:)` | Nil checks |
| `XCTAssertThrowsError(_:)` | Asserts an expression throws |
| `measure { }` | Records average execution time over 10 runs |
| `XCTestExpectation` | Async test support via `wait(for:timeout:)` |
| `XCUIApplication` | Launch and interact with app in UI tests |

## Common patterns

**Async test (pre-async/await)**

```swift
func testAsyncOperation() {
    let exp = expectation(description: "network call completes")
    fetchData { result in
        XCTAssertNotNil(result)
        exp.fulfill()
    }
    wait(for: [exp], timeout: 5.0)
}
```

**Parallel testing**

Enable in Xcode scheme editor: Product → Scheme → Test → Options → Execute in parallel.
Parallel tests run in separate processes; shared mutable state causes flakiness.

## Gotchas

- `measure()` runs the block 10 times; the first run is often slower (cold caches). This is expected.
- UI tests run in a separate process; they cannot access app memory directly.
- For async/await tests in Swift 5.5+, use `async` test methods and `await` directly instead of `XCTestExpectation`.
