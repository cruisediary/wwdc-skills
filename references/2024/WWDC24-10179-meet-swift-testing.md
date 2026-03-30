---
framework: Swift Testing
title: "Meet Swift Testing"
session: WWDC24-10179
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/swift-testing.md
---

# Swift Testing — Meet Swift Testing (WWDC24)

Swift Testing is a new first-party testing framework introduced in Xcode 16 / iOS 18. It replaces XCTest with a macro-based API that is more expressive, composable, and Swift-native.

## Quick start

```swift
import Testing

@Test func addition() {
    #expect(1 + 1 == 2)
}

@Suite struct MathTests {
    @Test func subtraction() {
        #expect(5 - 3 == 2)
    }

    @Test func multiplicationByZero() {
        #expect(5 * 0 == 0)
    }
}
```

Run with `swift test` or in Xcode's Test navigator — no subclassing or naming conventions required.

## Key APIs

| API | Purpose |
|---|---|
| `@Test` | Marks a function as a test case; replaces `func test...()` convention |
| `@Suite` | Groups related `@Test` functions; can be a `struct`, `class`, or `enum`; replaces `XCTestCase` |
| `#expect(_:)` | Asserts a condition is true; records a failure and **continues** the test if false |
| `#require(_:)` | Asserts a condition is true; **throws** on failure, stopping the current test immediately |
| `#require(throws:)` | Asserts that an expression throws a specific error type |
| `Issue.record(_:)` | Manually records a test failure with a custom message, without a Boolean condition |
| `@Test(.disabled("reason"))` | Marks a test as unconditionally disabled with an explanatory message |
| `@Test(.bugReport("url"))` | Associates a test with a known bug; marks it as an expected failure |

## Common patterns

**Grouping tests with `@Suite`:**
```swift
@Suite("Article model")
struct ArticleTests {
    @Test func titleIsNonEmpty() {
        let article = Article(title: "Hello", body: "World")
        #expect(!article.title.isEmpty)
    }

    @Test func bodyIsNonEmpty() {
        let article = Article(title: "Hello", body: "World")
        #expect(!article.body.isEmpty)
    }
}
```

**Expected failures with `.bugReport`:**
```swift
@Test(.bugReport("https://github.com/org/repo/issues/42", "Parser crashes on empty input"))
func parserHandlesEmptyInput() {
    let result = Parser.parse("")
    #expect(result != nil)  // Currently fails — tracked in bug report
}
```

**Async tests:**
```swift
@Test func fetchUserReturnsName() async throws {
    let user = try await UserService.fetch(id: 1)
    #expect(user.name == "Alice")
}
```

**Using `#require` to stop a test early:**
```swift
@Test func firstElementExists() throws {
    let items = fetchItems()
    let first = try #require(items.first)  // Stops test if items is empty
    #expect(first.isValid)
}
```

**Recording a manual failure:**
```swift
@Test func customValidation() {
    let value = computeValue()
    if value < 0 {
        Issue.record("Expected non-negative value, got \(value)")
    }
}
```

## Gotchas

- **`#require` throws on failure** — it stops the current test immediately. Use it only when subsequent assertions are meaningless if the requirement is unmet (e.g., unwrapping an optional). Use `#expect` when you want to collect all failures in one run.
- **`#expect` continues on failure** — all `#expect` calls in a test body run regardless of earlier failures, giving a complete picture of what went wrong.
- **`@Suite` initializers replace `setUp`** — `init()` and `deinit` (for class-based suites) replace `setUpWithError`/`tearDownWithError`. Each `@Test` function gets a fresh suite instance.
- **No `XCTestCase` subclass needed** — `@Suite` works with structs, which means no class inheritance or `override` boilerplate.
- **Swift Testing and XCTest coexist** — both frameworks can be used in the same test target. Migrate incrementally.
- **`@Test` functions must be non-mutating in structs** — if a test modifies suite-level state, use a `class` or `actor` suite.
