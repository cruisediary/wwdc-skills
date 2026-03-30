---
framework: Combine
title: "Introducing Combine"
session: WWDC19-722
year: 2019
applies_to: iOS 13+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/combine.md
---

# Introducing Combine (WWDC19)

Combine is Apple's unified reactive programming framework. This session introduces the Publisher/Subscriber/Operator model, key built-in publishers, and the foundation of reactive data pipelines.

## What changed and why

Before Combine, asynchronous event handling in Apple frameworks was fragmented: `NotificationCenter` for broadcasts, delegation for one-to-one callbacks, KVO for property observation, and completion closures for async work. Each pattern had its own composition and error handling story — or none at all.

Combine unifies all of these under a single protocol-based model:

- **Publisher** — emits a sequence of values over time, then either completes or fails
- **Subscriber** — receives and acts on values from a publisher
- **Operator** — transforms, filters, or combines publishers (they are themselves publishers)

## Mental model

```
Publisher<Output, Failure>
    ──operator──► Publisher (transformed)
    ──operator──► Publisher (transformed)
    ──sink/assign──► Subscriber
```

Every pipeline starts with a publisher, chains zero or more operators, and terminates with a subscriber. The subscription (`AnyCancellable`) must be retained — releasing it cancels the pipeline.

**Key types:**

| Type | Role |
|------|------|
| `Publisher` | Protocol — anything that emits values |
| `Subscriber` | Protocol — anything that receives values |
| `AnyPublisher<Output, Failure>` | Type-erased publisher for API boundaries |
| `AnyCancellable` | Subscription handle — release to cancel |
| `PassthroughSubject<Output, Failure>` | Imperatively send values |
| `CurrentValueSubject<Output, Failure>` | Stores the last-sent value; like a `@Published` you control |

## Usage

**`sink` — subscribe and handle values:**
```swift
let publisher = [1, 2, 3].publisher

let cancellable = publisher
    .map { $0 * 2 }
    .filter { $0 > 2 }
    .sink(
        receiveCompletion: { completion in
            switch completion {
            case .finished: print("Done")
            case .failure(let error): print("Error: \(error)")
            }
        },
        receiveValue: { value in print(value) }
    )
// Store cancellable or the pipeline is immediately cancelled
```

**`assign` — bind publisher output to a property:**
```swift
class ViewModel: ObservableObject {
    @Published var title = ""
    private var cancellables = Set<AnyCancellable>()

    init(service: TitleService) {
        service.titlePublisher
            .receive(on: DispatchQueue.main)
            .assign(to: &$title)  // iOS 14+ assign(to:) avoids retain cycle
    }
}
```

**`NotificationCenter.publisher` — observe notifications:**
```swift
NotificationCenter.default
    .publisher(for: UIApplication.didBecomeActiveNotification)
    .sink { _ in print("App became active") }
    .store(in: &cancellables)
```

**`URLSession.dataTaskPublisher` — network requests:**
```swift
URLSession.shared
    .dataTaskPublisher(for: url)
    .map(\.data)
    .decode(type: [Item].self, decoder: JSONDecoder())
    .receive(on: DispatchQueue.main)
    .sink(receiveCompletion: { _ in }, receiveValue: { items = $0 })
    .store(in: &cancellables)
```

**`PassthroughSubject` — imperative event bridge:**
```swift
let buttonTapped = PassthroughSubject<Void, Never>()

// Send an event imperatively
buttonTapped.send()

// Subscribe downstream
buttonTapped
    .debounce(for: .milliseconds(300), scheduler: DispatchQueue.main)
    .sink { handleTap() }
    .store(in: &cancellables)
```

## Adopting this pattern

1. Store all `AnyCancellable` values in a `Set<AnyCancellable>` on the owning object — releasing the set cancels all subscriptions.
2. Always call `.receive(on: DispatchQueue.main)` before UI-updating operators to ensure main-thread delivery.
3. Prefer `assign(to: &$publishedProperty)` (iOS 14+) over `assign(to:on:)` to avoid retain cycles in `ObservableObject`.
4. Use `AnyPublisher` as the return type of public publisher-returning methods to hide implementation details.
5. For new iOS 15+ code, consider `async/await` and `AsyncSequence` — they are simpler for request/response patterns; Combine remains useful for complex multi-stream composition.
