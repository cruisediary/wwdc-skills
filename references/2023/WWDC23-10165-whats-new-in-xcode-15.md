---
framework: Xcode
title: "What's new in Xcode 15"
session: WWDC23-10165
year: 2023
applies_to: iOS 17+
status: reference-only
superseded_by: null
shape: migration
related: []
---

# What's new in Xcode 15 (WWDC23)

Xcode 15 ships with the `#Preview` macro, a bookmark navigator, asset catalog improvements, an enhanced test navigator, and documentation enhancements.

## What's new

- **`#Preview` macro** — Replace `PreviewProvider` structs with a `#Preview { }` freestanding macro in SwiftUI and UIKit files
- **Bookmark navigator** — A new navigator pane for bookmarking source locations (breakpoints, interests, TODOs) with annotations
- **Asset catalog improvements** — Symbol variants, darkening, and multiplatform asset management improvements; new `.symbolEffect` modifiers visible in previews
- **Test navigator** — Redesigned; shows test plan, runs history, and per-test timing; integrates with Swift Testing's `@Test` / `@Suite` in Xcode 15
- **Documentation** — DocC gains a static site generator that can be hosted on GitHub Pages; `\(SPI:)` and article improvements
- **String catalog (`.xcstrings`)** — New localisation format replacing `.strings` / `.stringsdict`; plural rules and device-specific strings in a single JSON file; Xcode validates completeness
- **#Preview for UIKit** — `#Preview { MyViewController() }` works in UIKit files
- **Improved diagnostics** — Fix-it suggestions for common mistakes; better concurrency diagnostics with Swift 5.9

## Before / After

**Previews:**
```swift
// Before (Xcode 14)
struct MyView_Previews: PreviewProvider {
    static var previews: some View {
        MyView()
    }
}

// After (Xcode 15 — #Preview macro)
#Preview {
    MyView()
}

// With name and traits
#Preview("Dark mode", traits: .sizeThatFitsLayout) {
    MyView()
        .preferredColorScheme(.dark)
}
```

**UIKit preview:**
```swift
#Preview {
    let vc = MyViewController()
    vc.loadViewIfNeeded()
    return vc
}
```

**String catalog localisation:**
```swift
// Before: "greeting" = "Hello"; in Localizable.strings (one file per language)
// After: Localizable.xcstrings contains all languages as structured JSON,
//        managed in Xcode's string catalog editor.
//
// Usage in code is identical:
Text("greeting")  // or NSLocalizedString("greeting", comment: "")
```

## Migration steps

1. Replace `PreviewProvider` structs with `#Preview { }` — Xcode provides a refactoring action.
2. Migrate `.strings` / `.stringsdict` files to `.xcstrings` via Xcode > Editor > Convert to String Catalog.
3. Add bookmarks to frequently-visited code locations via Editor > Bookmark menu.
4. Review the new test navigator for your project's test plans — Swift Testing tests appear alongside XCTest tests.

## Compatibility notes

- `#Preview` macro requires Xcode 15+ but the generated code targets iOS 17+ / macOS 14+ for live previews.
- `.xcstrings` files require Xcode 15+ for editing; the runtime behavior is compatible with older OS versions.
- String catalog migration is opt-in; old `.strings` files continue to work.
