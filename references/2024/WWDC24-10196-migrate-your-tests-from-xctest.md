---
framework: Swift Testing
title: "Migrate your tests from XCTest"
session: WWDC24-10196
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/swift-testing.md
---

# Swift Testing — Migrate Your Tests from XCTest (WWDC24)

A practical guide to incrementally migrating an existing XCTest suite to Swift Testing, including direct API mappings and coexistence rules.

## What's new

- **Swift Testing runs alongside XCTest** — both frameworks coexist in the same test target; migrate test by test without a big-bang rewrite
- **Incremental migration** — XCTest and Swift Testing tests are discovered and reported separately in Xcode's Test navigator; there is no conflict between them
- **Direct API mappings** — every common `XCTAssert*` function has a Swift Testing equivalent; the assertion model is more expressive with `#expect` and `#require`
- **Lifecycle simplification** — `setUp`/`tearDown` are replaced by `init`/`deinit` on the suite type, aligning with standard Swift value-type semantics

## Before / After

**Simple test class:**
```swift
// XCTest
import XCTest

class MathTests: XCTestCase {
    func testAddition() {
        XCTAssertEqual(1 + 1, 2)
    }

    func testDivisionByZero() {
        XCTAssertNil(safeDivide(10, by: 0))
    }
}

// Swift Testing
import Testing

@Suite struct MathTests {
    @Test func addition() {
        #expect(1 + 1 == 2)
    }

    @Test func divisionByZero() {
        #expect(safeDivide(10, by: 0) == nil)
    }
}
```

**Setup and teardown:**
```swift
// XCTest
class DatabaseTests: XCTestCase {
    var db: Database!

    override func setUpWithError() throws {
        db = try Database(inMemory: true)
    }

    override func tearDownWithError() throws {
        try db.close()
    }

    func testInsert() throws {
        try db.insert(record: .sample)
        XCTAssertEqual(db.count, 1)
    }
}

// Swift Testing — init/deinit replace setUp/tearDown
// Note: requires a class (not struct) to use deinit
@Suite final class DatabaseTests {
    let db: Database

    init() throws {
        db = try Database(inMemory: true)
    }

    deinit {
        try? db.close()
    }

    @Test func insert() throws {
        try db.insert(record: .sample)
        #expect(db.count == 1)
    }
}
```

**Throwing tests:**
```swift
// XCTest
func testFetchSucceeds() throws {
    let result = try fetchData()
    XCTAssertNotNil(result)
}

// Swift Testing
@Test func fetchSucceeds() throws {
    let result = try fetchData()
    #expect(result != nil)
}
```

## Migration steps

1. **Add `import Testing`** — keep `import XCTest` in files that still use XCTest; both can coexist in the same file during migration
2. **Change `XCTestCase` class to `@Suite` struct** — `@Suite` does not require class inheritance; prefer `struct` unless `deinit` is needed for cleanup
3. **Replace `func test...()` with `@Test func`** — remove the `test` prefix naming convention; give functions descriptive names
4. **Replace `XCTAssert*` calls with `#expect` or `#require`:**

| XCTest | Swift Testing |
|---|---|
| `XCTAssertEqual(a, b)` | `#expect(a == b)` |
| `XCTAssertNotEqual(a, b)` | `#expect(a != b)` |
| `XCTAssertTrue(x)` | `#expect(x)` |
| `XCTAssertFalse(x)` | `#expect(!x)` |
| `XCTAssertNil(x)` | `#expect(x == nil)` |
| `XCTAssertNotNil(x)` | `#expect(x != nil)` |
| `XCTAssertThrowsError(try f())` | `#expect(throws: (any Error).self) { try f() }` |
| `XCTAssertNoThrow(try f())` | `#expect(throws: Never.self) { try f() }` |
| `XCTFail("message")` | `Issue.record("message")` |
| `try XCTUnwrap(optional)` | `try #require(optional)` |

5. **Replace `setUp`/`tearDown` with `init`/`deinit`** — if the suite needs `deinit`, use a `final class` instead of a `struct`; if setup only (no teardown), a `struct` with a throwing `init()` works

## Compatibility notes

- Both test frameworks run in the same test target — no separate targets or schemes required
- XCTest and Swift Testing test results appear together in Xcode's Test navigator and are reported separately in test result bundles
- `XCTestCase` subclasses and `@Suite` types can both exist in the same `.swift` file
- UI tests (`XCUITest`) have no Swift Testing equivalent yet — continue using `XCTestCase` for UI automation
- Performance tests (`measure { }`) have no Swift Testing equivalent yet — keep those in `XCTestCase`
- Swift Testing requires Swift 6 toolchain (Xcode 16+) and runs on iOS 18+, macOS 15+, watchOS 11+, tvOS 18+; XCTest remains available for earlier deployment targets
