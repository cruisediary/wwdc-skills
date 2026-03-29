---
framework: Swift Testing
status: current
applies_to: iOS 18+
shape: code-first
superseded_by: null
history:
  - year: 2024
    file: 2024/swift-testing.md
    summary: Swift Testing introduction — @Test, #expect, @Suite, parameterized tests
---

# Swift Testing

Apple's modern testing framework (Xcode 16+, iOS 18+), replacing XCTest with a Swift-native, macro-based API. XCTest continues to work — migration is incremental.

## Quick start

```swift
import Testing

// Basic tests — no subclass required
@Test func additionWorks() {
    #expect(2 + 2 == 4)
}

@Test func stringContains() throws {
    let result = "Hello, World"
    #expect(result.contains("World"))
    try #require(result.contains("Hello"))  // stops test if false
}

// Grouped in a suite
@Suite("Calculator Tests")
struct CalculatorTests {
    let calc = Calculator()

    @Test func add() {
        #expect(calc.add(2, 3) == 5)
    }

    @Test func divide() throws {
        try #require(calc.denominator != 0)
        #expect(calc.divide(10, by: 2) == 5)
    }
}

// Parameterized tests
@Test("Addition", arguments: [(1, 2, 3), (0, 5, 5), (-1, 1, 0)])
func additionTable(a: Int, b: Int, expected: Int) {
    #expect(a + b == expected)
}

// Async tests
@Test func asyncFetch() async throws {
    let result = try await fetchUser(id: "1")
    #expect(result.name == "Alice")
}
```

## Key APIs

| API | Purpose |
|---|---|
| `@Test` | Marks a function as a test case |
| `@Suite` | Groups related tests; optional but useful for shared state |
| `#expect` | Assertion — records failure but continues the test |
| `#require` | Assertion — throws on failure, stopping the test immediately |
| `@Test(arguments:)` | Parameterized test — runs once per argument |
| `@Test(.enabled(if:))` | Conditionally enables a test |
| `@Test(.tags(...))` | Tag a test for filtering |
| `Issue.record(_:)` | Record a failure manually |
| `withKnownIssue { }` | Mark code expected to fail (like `XCTExpectFailure`) |
| `#expect(throws:)` | Assert a specific error is thrown |

## Common patterns

```swift
// Testing throws
@Test func invalidInput() {
    #expect(throws: ValidationError.self) {
        try validate(input: "")
    }
}

// Known failure
@Test func knownBrokenFeature() {
    withKnownIssue {
        #expect(buggyFunction() == expectedValue)
    }
}

// setUp/tearDown equivalent — use init/deinit on @Suite struct
@Suite struct DatabaseTests {
    let db: TestDatabase

    init() async throws {
        db = try await TestDatabase.create()
    }

    deinit {
        db.close()
    }

    @Test func queryReturnsResults() async throws {
        let results = try await db.query("SELECT * FROM users")
        #expect(!results.isEmpty)
    }
}

// Tags for filtering
extension Tag {
    @Tag static var networking: Self
    @Tag static var persistence: Self
}

@Test(.tags(.networking)) func apiCallSucceeds() async throws { ... }
```

## Gotchas

- `#expect` does not stop the test on failure — use `#require` when subsequent steps depend on the result
- `@Suite` is a struct or class — `init`/`deinit` replace `setUp`/`tearDown`
- Swift Testing and XCTest can coexist in the same target — migration is incremental
- `@Test` functions can be top-level (no wrapping type required)
- Parameterized test arguments are `Sendable` — they must be copyable across concurrency boundaries
- Requires Xcode 16+ even for iOS 17 and earlier deployment targets
