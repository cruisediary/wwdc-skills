---
framework: Swift Testing
title: "Go further with Swift Testing"
session: WWDC24-10195
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/swift-testing.md
---

# Swift Testing — Go Further with Swift Testing (WWDC24)

Advanced Swift Testing features: parameterized tests for data-driven coverage, tags for organizing and filtering test runs, and custom traits for reusable test configuration.

## What changed and why

XCTest's approach to data-driven testing requires writing one `func test...()` per input case or manually looping inside a single test — both approaches either inflate the test count or collapse multiple logical cases into one opaque failure. There is also no built-in way to categorize tests across suites for selective execution (e.g., run only performance tests or only networking tests).

Swift Testing addresses both problems:

- **`@Test(arguments:)`** — declare a parameterized test once; the framework runs it as a separate, independently reported test case for each argument value
- **Tags** — attach semantic labels to tests with `@Test(.tags(...))` and filter test runs by tag in Xcode or `swift test --filter`
- **Custom traits** — implement the `TestTrait` protocol to encapsulate shared preconditions, timeouts, or configuration that applies to multiple tests

## Mental model

Think of `@Test(arguments:)` as a `for` loop promoted to the test runner level. Each argument becomes an independent test invocation with its own pass/fail result, its own failure message, and the ability to re-run just that one failing case.

```
@Test(arguments: [1, 2, 3])
func isPositive(_ n: Int) { ... }

// Runner sees:
// ✓  isPositive(1)
// ✓  isPositive(2)
// ✓  isPositive(3)
// — not one test with three iterations
```

Tags are orthogonal to suite structure. A test in `NetworkTests` and a test in `DatabaseTests` can both carry `.integration`, letting you run or exclude all integration tests regardless of where they live.

## Usage

**Parameterized tests with a value array:**
```swift
import Testing

@Test(arguments: [1, 2, 3, 100])
func isPositive(_ n: Int) {
    #expect(n > 0)
}
```

**Parameterized tests with named enum cases:**
```swift
enum Locale: CaseIterable {
    case en, fr, de, ja
}

@Test(arguments: Locale.allCases)
func formatterProducesOutput(for locale: Locale) throws {
    let formatter = DateFormatter(locale: locale)
    let result = formatter.string(from: .now)
    try #require(!result.isEmpty)
}
```

**Two-argument parameterization (cartesian product):**
```swift
@Test(arguments: [2, 4, 6], [3, 5, 7])
func sum(even: Int, odd: Int) {
    #expect((even + odd) % 2 != 0)
}
// Runs 9 combinations: (2,3), (2,5), (2,7), (4,3), ...
```

**Defining and using tags:**
```swift
// Declare tags in an extension — one place, reused everywhere
extension Tag {
    @Tag static var performance: Tag
    @Tag static var networking: Tag
    @Tag static var integration: Tag
}

@Suite
struct APIClientTests {
    @Test(.tags(.networking, .integration))
    func fetchUserSucceeds() async throws {
        let user = try await APIClient.shared.fetchUser(id: 1)
        #expect(user != nil)
    }

    @Test(.tags(.performance))
    func fetchLatencyIsAcceptable() async throws {
        let start = Date()
        _ = try await APIClient.shared.fetchUser(id: 1)
        #expect(Date().timeIntervalSince(start) < 2.0)
    }
}
```

**Running only tagged tests (command line):**
```bash
swift test --filter performance
```

**Custom trait for shared setup:**
```swift
struct NetworkUnavailable: Error {}

struct RequiresNetworkTrait: TestTrait {
    func prepare(for test: Test) async throws {
        guard isNetworkAvailable() else {
            throw NetworkUnavailable()
        }
    }
}

extension Trait where Self == RequiresNetworkTrait {
    static var requiresNetwork: RequiresNetworkTrait { .init() }
}

@Test(.requiresNetwork)
func liveEndpointReturnsData() async throws {
    // Only runs when network is available
}
```

## Adopting this pattern

Replace repetitive XCTest methods with parameterized `@Test`:

| Before (XCTest) | After (Swift Testing) |
|---|---|
| `func testPositive1() { XCTAssert(1 > 0) }` `func testPositive2() { XCTAssert(2 > 0) }` | `@Test(arguments: [1, 2]) func isPositive(_ n: Int) { #expect(n > 0) }` |
| Manual `for` loop in a single test function | `@Test(arguments: collection)` — each element is an independent test |
| Comment-based grouping (`// MARK: - Performance`) | `@Tag static var performance: Tag` + `@Test(.tags(.performance))` |
| Shared `setUp` logic duplicated across test classes | Custom `TestTrait` with a `prepare(for:)` implementation |

Migration checklist:
1. Identify test methods that loop over inputs or are duplicated with minor variations — convert to `@Test(arguments:)`
2. Identify logical categories across your test suite — declare `@Tag` extensions and annotate tests
3. In CI, add per-tag test jobs: `swift test --filter integration` for integration suites, `swift test --filter unit` for fast unit tests
4. Extract shared preconditions (network, auth, database seeding) into custom `TestTrait` conformances
