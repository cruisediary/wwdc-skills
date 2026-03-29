---
framework: Combine
session: WWDC19-722
year: 2019
applies_to: iOS 13+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/combine.md
---

# Combine — WWDC19 Introduction

Combine was introduced at WWDC19 as Apple's unified reactive streams framework.

## What's new

- `Publisher` protocol — emits values, errors, and a completion event
- `Subscriber` protocol — receives values from a publisher
- `Subject` types: `PassthroughSubject`, `CurrentValueSubject` — imperatively send values
- `AnyPublisher` / `AnyCancellable` — type-erased publisher and subscription handle
- Built-in publishers: `URLSession.dataTaskPublisher`, `NotificationCenter.publisher`, `Timer.publish`
- `@Published` property wrapper — wraps a property as a publisher
- Operators: `map`, `filter`, `flatMap`, `combineLatest`, `merge`, `zip`, `debounce`, `throttle`, `receive(on:)`, `sink`, `assign`

## Before / After

**Before (NotificationCenter + callbacks):**
```swift
NotificationCenter.default.addObserver(
    self,
    selector: #selector(handleChange),
    name: UITextField.textDidChangeNotification,
    object: textField
)

@objc private func handleChange(_ notification: Notification) {
    guard let text = (notification.object as? UITextField)?.text else { return }
    performSearch(text)
}
```

**After (Combine):**
```swift
NotificationCenter.default
    .publisher(for: UITextField.textDidChangeNotification, object: textField)
    .compactMap { ($0.object as? UITextField)?.text }
    .debounce(for: .milliseconds(300), scheduler: DispatchQueue.main)
    .sink { [weak self] text in self?.performSearch(text) }
    .store(in: &cancellables)
```

## Migration steps

1. Add `import Combine`
2. Replace `NotificationCenter.addObserver` with `NotificationCenter.publisher(for:)` + `.sink`
3. Replace KVO with `NSObject.publisher(for:)` or `@Published`
4. Replace completion-handler patterns with custom `Publisher` or `Future`
5. Store all subscriptions in `Set<AnyCancellable>` on the owning object

## Compatibility notes

- Requires iOS 13+, macOS 10.15+
- `@Published` is a Combine concept — requires `ObservableObject`
- For iOS 15+: consider `async/await` and `AsyncSequence` for new code
