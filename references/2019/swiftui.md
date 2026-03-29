---
framework: SwiftUI
session: WWDC19-204
year: 2019
applies_to: iOS 13+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/swiftui.md
---

# SwiftUI — WWDC19 Introduction

SwiftUI was introduced at WWDC19, replacing UIKit as the recommended framework for new Apple platform UI development.

## What's new

- `View` protocol — declare UI as a function of state, not a sequence of mutations
- `@State` — local mutable state owned by a view
- `@Binding` — two-way reference to a parent's state
- `@EnvironmentObject` — dependency injection through the view hierarchy
- Layout containers: `VStack`, `HStack`, `ZStack`
- `List` with `ForEach` for dynamic collections
- `NavigationView` with `NavigationLink` (deprecated in iOS 16 — use `NavigationStack`)
- `PreviewProvider` (deprecated in Xcode 15 — use `#Preview`)
- Live Previews in Xcode — see changes without running the simulator

## Before / After

**Before (UIKit):**
```swift
class CounterViewController: UIViewController {
    private let label = UILabel()
    private var count = 0

    override func viewDidLoad() {
        super.viewDidLoad()
        let stack = UIStackView(arrangedSubviews: [label, makeButton()])
        stack.axis = .vertical
        view.addSubview(stack)
        // ... layout constraints
        updateLabel()
    }

    @objc private func increment() {
        count += 1
        updateLabel()
    }

    private func updateLabel() {
        label.text = "Count: \(count)"
    }
}
```

**After (SwiftUI WWDC19):**
```swift
struct CounterView: View {
    @State private var count = 0

    var body: some View {
        VStack {
            Text("Count: \(count)")
            Button("Increment") { count += 1 }
        }
    }
}
```

## Migration steps

1. Start with leaf views (no child view controllers) — convert to `View` structs first
2. Use `UIHostingController` to embed SwiftUI views in existing UIKit hierarchy
3. Replace `IBOutlet` properties with `@State` or `@Binding`
4. Replace `IBAction` methods with Button action closures
5. Replace `UITableView`/`UICollectionView` with `List` + `ForEach`
6. Migrate navigation last — `NavigationView` → `NavigationStack` (iOS 16+)

## Compatibility notes

- Requires iOS 13+, macOS 10.15+
- `NavigationView` introduced in iOS 13 is deprecated in iOS 16 — use `NavigationStack`
- `PreviewProvider` deprecated in Xcode 15 — use `#Preview { }` macro
- UIKit and SwiftUI can coexist — use `UIHostingController` (UIKit hosting SwiftUI) or `UIViewRepresentable` (SwiftUI hosting UIKit)
