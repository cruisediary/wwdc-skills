---
framework: Swift Testing
session: WWDC24-10179
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/swift-testing.md
---

# Swift Testing — WWDC24 Introduction

Swift Testing was introduced at WWDC24 as a replacement for XCTest, providing a Swift-native, macro-based testing API.

## What's new

- `@Test` — marks any function as a test (no `XCTestCase` subclass required)
- `@Suite` — groups related tests; uses `init`/`deinit` instead of `setUp`/`tearDown`
- `#expect` — assertion macro that continues on failure (vs. `XCTAssert` which stops)
- `#require` — assertion macro that throws on failure (stops the test)
- `@Test(arguments:)` — parameterized tests with any `Collection` of arguments
- `.tags(...)` — categorize tests for filtering in Test Navigator
- `withKnownIssue { }` — mark expected failures
- Full async/await support — `@Test func` can be `async throws`
- Custom `Tag` definitions for project-level test organization

## Before / After

**Before (XCTest):**
```swift
import XCTest

class CalculatorTests: XCTestCase {
    var calc: Calculator!

    override func setUp() {
        super.setUp()
        calc = Calculator()
    }

    override func tearDown() {
        calc = nil
        super.tearDown()
    }

    func testAdd() {
        XCTAssertEqual(calc.add(2, 3), 5)
    }

    func testAddMultipleValues() {
        let cases = [(1, 2, 3), (0, 5, 5)]
        for (a, b, expected) in cases {
            XCTAssertEqual(calc.add(a, b), expected)
        }
    }
}
```

**After (Swift Testing):**
```swift
import Testing

@Suite struct CalculatorTests {
    let calc = Calculator()

    @Test func add() {
        #expect(calc.add(2, 3) == 5)
    }

    @Test("Add multiple values", arguments: [(1, 2, 3), (0, 5, 5)])
    func addTable(a: Int, b: Int, expected: Int) {
        #expect(calc.add(a, b) == expected)
    }
}
```

## Migration steps

1. Add `import Testing` alongside or instead of `import XCTest`
2. Replace `class FooTests: XCTestCase` with `@Suite struct FooTests`
3. Replace `func testFoo()` with `@Test func foo()` (drop the `test` prefix)
4. Replace `XCTAssertEqual(a, b)` with `#expect(a == b)`
5. Replace `XCTAssertThrowsError` with `#expect(throws: ErrorType.self) { }`
6. Replace `setUp`/`tearDown` with `init`/`deinit` on the `@Suite` struct
7. Replace manual test loops with `@Test(arguments:)` for parameterization

## Compatibility notes

- Swift Testing requires Xcode 16+
- Supports iOS 13+ deployment targets despite the `applies_to: iOS 18+` in frontmatter (18+ is when Apple shipped it as default; it works with earlier targets)
- XCTest continues to work — Swift Testing and XCTest can coexist in the same test target
- UI tests still require XCTest (`XCUIApplication`, etc.) — Swift Testing is for unit/integration tests
