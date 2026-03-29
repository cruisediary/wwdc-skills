---
framework: Combine
status: current
applies_to: iOS 13+
shape: guide-first
superseded_by: null
history:
  - year: 2019
    file: 2019/combine.md
    summary: Combine introduction — Publisher, Subscriber, operators
---

# Combine

Apple's reactive streams framework (iOS 13+). Still valid and widely used — particularly in apps targeting iOS 13–16 or using `@Published` with `ObservableObject`. For new iOS 15+ code, `async/await` and `AsyncSequence` are simpler alternatives for most use cases.

## What changed and why

Combine provides a unified, declarative API for processing asynchronous events over time: network responses, user input, timer ticks, property changes. Before Combine, each async mechanism (NotificationCenter, KVO, URLSession callbacks) had a different API. Combine unifies them under `Publisher` → operators → `Subscriber`.

## Mental model

```
Publisher     = produces values over time (or an error, then completes)
Operator      = transforms, filters, or combines streams
Subscriber    = consumes values; must subscribe to start the stream
AnyCancellable = holds the subscription alive — store it or the stream cancels immediately
```

Key rule: **store your `AnyCancellable`**. Assigning to a local variable cancels when the variable goes out of scope.

## Usage

```swift
import Combine

// URLSession publisher
var cancellables = Set<AnyCancellable>()

URLSession.shared
    .dataTaskPublisher(for: url)
    .map(\.data)
    .decode(type: User.self, decoder: JSONDecoder())
    .receive(on: DispatchQueue.main)
    .sink(
        receiveCompletion: { completion in
            if case .failure(let error) = completion {
                print("Error:", error)
            }
        },
        receiveValue: { user in
            self.user = user
        }
    )
    .store(in: &cancellables)

// @Published property observation
class ViewModel: ObservableObject {
    @Published var searchText = ""
    var cancellables = Set<AnyCancellable>()

    init() {
        $searchText
            .debounce(for: .milliseconds(300), scheduler: DispatchQueue.main)
            .removeDuplicates()
            .sink { [weak self] query in
                self?.performSearch(query)
            }
            .store(in: &cancellables)
    }
}

// Combining publishers
Publishers.CombineLatest(usernamePublisher, passwordPublisher)
    .map { username, password in
        !username.isEmpty && password.count >= 8
    }
    .assign(to: \.isLoginEnabled, on: self)
    .store(in: &cancellables)
```

## Adopting this pattern

For new iOS 15+ code, consider `async/await` with `AsyncSequence` instead of Combine. The mental shift: replace `.sink { value in }` with `for await value in sequence`. See `canonical/swift-concurrency.md` for the modern approach. Combine remains the right choice when working with `@Published` properties in `ObservableObject` (iOS 13–16), SwiftUI bindings built around `ObservableObject`, or existing codebases heavily invested in Combine pipelines.
