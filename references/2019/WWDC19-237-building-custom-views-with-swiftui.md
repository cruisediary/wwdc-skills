---
framework: SwiftUI
title: "Building Custom Views with SwiftUI"
session: WWDC19-237
year: 2019
applies_to: iOS 13+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/swiftui.md
---

# Building Custom Views with SwiftUI (WWDC19)

Advanced layout and drawing: `GeometryReader`, `PreferenceKey`, `alignmentGuide`, custom layout with `Path`, and the `Shape` protocol.

## What changed and why

UIKit relied on `layoutSubviews`, Auto Layout constraints, and `drawRect` for custom layouts and drawing. SwiftUI provides higher-level primitives:

- **`GeometryReader`** — reads parent-offered geometry (size and coordinate spaces) inside a view
- **`PreferenceKey`** — lets child views communicate data (like their size) back up to ancestors
- **`alignmentGuide`** — overrides the default alignment position for a view inside a stack
- **`Path` / `Shape`** — draw 2D vector graphics with explicit coordinates, similar to `CGPath`

## Mental model

SwiftUI layout is a three-step negotiation:
1. **Parent proposes** a size to the child
2. **Child chooses** its own size (it can ignore the proposal)
3. **Parent places** the child at a position within itself

`GeometryReader` participates in step 1 — it fills the proposed size and gives you a `GeometryProxy` to read dimensions.

`PreferenceKey` reverses the data flow: children set preference values, and ancestors collect them via `.onPreferenceChange`.

## Usage

**`GeometryReader` — size-relative layout:**
```swift
struct RelativeWidthBar: View {
    var fraction: CGFloat  // 0.0 – 1.0

    var body: some View {
        GeometryReader { proxy in
            Rectangle()
                .fill(Color.blue)
                .frame(width: proxy.size.width * fraction, height: 20)
        }
        .frame(height: 20)
    }
}
```

**`PreferenceKey` — child reports its height to parent:**
```swift
struct HeightKey: PreferenceKey {
    static let defaultValue: CGFloat = 0
    static func reduce(value: inout CGFloat, nextValue: () -> CGFloat) {
        value = max(value, nextValue())
    }
}

struct ReportingView: View {
    var body: some View {
        Text("Hello")
            .background(
                GeometryReader { proxy in
                    Color.clear.preference(key: HeightKey.self, value: proxy.size.height)
                }
            )
    }
}

struct ParentView: View {
    @State private var childHeight: CGFloat = 0

    var body: some View {
        ReportingView()
            .onPreferenceChange(HeightKey.self) { childHeight = $0 }
    }
}
```

**`alignmentGuide` — custom alignment in HStack:**
```swift
HStack(alignment: .custom) {
    Text("Label")
        .alignmentGuide(.custom) { d in d[.bottom] }
    Image(systemName: "star.fill")
        .alignmentGuide(.custom) { d in d[VerticalAlignment.center] }
}
```

**`Path` — drawing lines and shapes:**
```swift
struct DiagonalLine: View {
    var body: some View {
        Path { path in
            path.move(to: CGPoint(x: 0, y: 0))
            path.addLine(to: CGPoint(x: 200, y: 200))
        }
        .stroke(Color.red, lineWidth: 2)
    }
}
```

**Custom `Shape`:**
```swift
struct Triangle: Shape {
    func path(in rect: CGRect) -> Path {
        var path = Path()
        path.move(to: CGPoint(x: rect.midX, y: rect.minY))
        path.addLine(to: CGPoint(x: rect.maxX, y: rect.maxY))
        path.addLine(to: CGPoint(x: rect.minX, y: rect.maxY))
        path.closeSubpath()
        return path
    }
}

// Usage:
Triangle()
    .fill(Color.orange)
    .frame(width: 100, height: 100)
```

## Adopting this pattern

1. Avoid `GeometryReader` unless you truly need parent size — it breaks the layout contract by always filling its container.
2. Use `PreferenceKey` to communicate child sizes or positions upward when you cannot pass them via bindings.
3. Implement `Shape` instead of using `Path` directly when the geometry needs to be reusable and scalable.
4. For custom alignment guides in `HStack`/`VStack`, define a custom `AlignmentID` and use `.alignmentGuide` to position views precisely.
5. `GeometryReader` coordinates are in the parent's coordinate space by default — use `proxy.frame(in:)` to convert to other spaces.
