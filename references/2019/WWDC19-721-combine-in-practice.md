---
framework: Combine
title: "Combine in Practice"
session: WWDC19-721
year: 2019
applies_to: iOS 13+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/combine.md
---

# Combine in Practice (WWDC19)

Practical Combine patterns: `flatMap`, `zip`, `combineLatest`, `.receive(on:)`, `@Published` with `ObservableObject`, error handling, and form validation pipelines.

## Quick start

```swift
import Combine

class LoginViewModel: ObservableObject {
    @Published var username = ""
    @Published var password = ""
    @Published var isLoginEnabled = false

    private var cancellables = Set<AnyCancellable>()

    init() {
        Publishers.CombineLatest($username, $password)
            .map { username, password in
                !username.isEmpty && password.count >= 8
            }
            .assign(to: &$isLoginEnabled)
    }
}
```

## Key APIs

| API | Description |
|-----|-------------|
| `flatMap(maxPublishers:_:)` | Transforms each value into a new publisher, merging their outputs |
| `zip(_:)` | Pairs values from two publishers one-to-one; emits when both have emitted |
| `combineLatest(_:)` | Emits a tuple whenever either publisher emits; uses the latest value from the other |
| `receive(on:)` | Delivers downstream events on the specified scheduler (e.g., `DispatchQueue.main`) |
| `@Published` | Property wrapper; synthesizes a `Publisher` accessible via `$propertyName` |
| `ObservableObject` | Protocol; `objectWillChange` publisher fires before any `@Published` property changes |
| `tryMap(_:)` | Like `map`, but closure can throw; converts thrown errors to publisher failure |
| `catch(_:)` | Recovers from an upstream failure by substituting a new publisher |
| `retry(_:)` | Re-subscribes to the upstream publisher up to N times on failure |
| `debounce(for:scheduler:)` | Emits a value only after a quiet period; useful for search text fields |
| `removeDuplicates()` | Suppresses consecutive equal values |

## Common patterns

**`flatMap` — network request per user input:**
```swift
$searchText
    .debounce(for: .milliseconds(300), scheduler: DispatchQueue.main)
    .removeDuplicates()
    .flatMap { query -> AnyPublisher<[Result], Never> in
        guard !query.isEmpty else {
            return Just([]).eraseToAnyPublisher()
        }
        return searchService.search(query: query)
            .catch { _ in Just([]) }
            .eraseToAnyPublisher()
    }
    .assign(to: &$results)
```

**`zip` — wait for two requests to complete:**
```swift
let userPublisher = apiService.fetchUser(id: userID)
let ordersPublisher = apiService.fetchOrders(for: userID)

userPublisher.zip(ordersPublisher)
    .receive(on: DispatchQueue.main)
    .sink(
        receiveCompletion: { _ in },
        receiveValue: { user, orders in
            self.user = user
            self.orders = orders
        }
    )
    .store(in: &cancellables)
```

**`combineLatest` — form validation:**
```swift
Publishers.CombineLatest3($email, $password, $confirmPassword)
    .map { email, password, confirm in
        email.contains("@") && password.count >= 8 && password == confirm
    }
    .removeDuplicates()
    .assign(to: &$isSubmitEnabled)
```

**Error handling with `tryMap` + `catch`:**
```swift
URLSession.shared
    .dataTaskPublisher(for: url)
    .tryMap { data, response in
        guard let http = response as? HTTPURLResponse, http.statusCode == 200 else {
            throw URLError(.badServerResponse)
        }
        return data
    }
    .decode(type: [Item].self, decoder: JSONDecoder())
    .catch { error -> AnyPublisher<[Item], Never> in
        print("Error: \(error)")
        return Just([]).eraseToAnyPublisher()
    }
    .receive(on: DispatchQueue.main)
    .assign(to: &$items)
```

**`@Published` + `ObservableObject` in SwiftUI:**
```swift
class CartViewModel: ObservableObject {
    @Published var items: [CartItem] = []
    @Published var totalPrice: Decimal = 0

    private var cancellables = Set<AnyCancellable>()

    init() {
        $items
            .map { items in items.reduce(0) { $0 + $1.price } }
            .assign(to: &$totalPrice)
    }

    func add(_ item: CartItem) {
        items.append(item)
    }
}
```

## Gotchas

- `flatMap` creates a new publisher for every upstream value — use `maxPublishers: .max(1)` to cancel the in-flight publisher when a new value arrives (switch-map behaviour).
- `zip` buffers values — if one publisher is much faster, memory can grow. Use `combineLatest` when you want the latest rather than paired values.
- `@Published` fires `willChange` *before* the value changes — `didChange` requires subscribing to the `$property` publisher directly.
- Forgetting to store `AnyCancellable` values is a common bug — the subscription is immediately cancelled if the token is discarded.
- `assign(to:on:)` creates a retain cycle when the target is `self`; use `assign(to: &$property)` (iOS 14+) or `sink { [weak self] in ... }` instead.
