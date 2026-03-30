---
framework: Foundation
title: "What's new in Foundation"
session: WWDC21-10109
year: 2021
applies_to: iOS 15+
status: reference-only
superseded_by: null
shape: migration
related: []
---

# What's New in Foundation (WWDC21)

iOS 15 Foundation additions: `AttributedString` (Swift-native), `FormatStyle` for type-safe formatting, `Locale.Language` hierarchy, and `Duration`/date-interval improvements.

## What's new

- **`AttributedString`** — Swift-native value type replacing `NSAttributedString`; Codable, diffable, localizable
- **`FormatStyle`** — type-safe, locale-aware formatting for numbers, dates, lists, and more
- **`Locale` improvements** — structured `Locale.Language`, `Locale.Region`, `Locale.Script` types
- **`AttributedString` with Markdown** — parse inline Markdown directly into `AttributedString`
- **`URL` improvements** — `URL(string:relativeTo:)` improvements; `URL` formatted with `FormatStyle`
- **Grammar agreement** — automatic grammatical agreement for inflected strings (`.inflected`)

## Key APIs

### AttributedString

```swift
// Creating an AttributedString
var attributed = AttributedString("Hello, World!")

// Setting attributes on a range
let range = attributed.range(of: "World")!
attributed[range].foregroundColor = .red
attributed[range].font = .boldSystemFont(ofSize: 17)

// Markdown parsing
let mdString = try! AttributedString(
    markdown: "**Bold** and *italic* text with a [link](https://example.com)"
)

// Converting to/from NSAttributedString
let nsAttr = NSAttributedString(attributed)
let backToSwift = AttributedString(nsAttr)

// Localizable attributed string with Markdown in .strings
// Key: "greeting" = "Hello, **%@**!"
var localized = AttributedString(localized: "greeting")
```

### FormatStyle

```swift
// Number formatting
let formatted = 1234567.89.formatted(.number.grouping(.automatic).precision(.fractionLength(2)))
// "1,234,567.89"

let percent = 0.75.formatted(.percent)
// "75%"

let currency = 42.50.formatted(.currency(code: "USD"))
// "$42.50"

// Date formatting
let date = Date.now
let dateStr = date.formatted(date: .abbreviated, time: .shortened)
// "Oct 15, 2021 at 2:30 PM"

let customDate = date.formatted(.dateTime.weekday(.wide).month().day())
// "Friday, October 15"

// List formatting
let items = ["apples", "oranges", "bananas"]
let list = items.formatted(.list(type: .and, width: .standard))
// "apples, oranges, and bananas"

// Relative date formatting
let relative = Date.now.addingTimeInterval(-3600).formatted(.relative(presentation: .named))
// "1 hour ago"

// Parsing with FormatStyle (round-trip)
let number = try? Double("1,234.56", format: .number)
let parsedDate = try? Date("Oct 15, 2021", strategy: .dateTime.month().day().year())
```

### Locale improvements

```swift
// Structured locale components (iOS 16+ for full Language type; iOS 15 adds Locale improvements)
let locale = Locale(identifier: "en-US")
let languageCode = locale.language.languageCode?.identifier  // "en"
let regionCode = locale.region?.identifier                   // "US"

// Current locale
let current = Locale.current
print(current.identifier)           // e.g., "en_US"
```

## Before / After

**Before (NSAttributedString — verbose, Objective-C API):**
```swift
let nsAttr = NSMutableAttributedString(string: "Hello, World!")
let range = (nsAttr.string as NSString).range(of: "World")
nsAttr.addAttribute(.foregroundColor, value: UIColor.red, range: range)
nsAttr.addAttribute(.font, value: UIFont.boldSystemFont(ofSize: 17), range: range)
label.attributedText = nsAttr
```

**After (AttributedString — Swift value type):**
```swift
var attributed = AttributedString("Hello, World!")
let range = attributed.range(of: "World")!
attributed[range].foregroundColor = .red
attributed[range].font = .boldSystemFont(ofSize: 17)
label.attributedText = NSAttributedString(attributed)
// Or directly in SwiftUI: Text(attributed)
```

**Before (DateFormatter):**
```swift
let formatter = DateFormatter()
formatter.dateStyle = .medium
formatter.timeStyle = .short
let str = formatter.string(from: date)
```

**After (FormatStyle):**
```swift
let str = date.formatted(date: .abbreviated, time: .shortened)
```

## Migration steps

1. Replace `NSMutableAttributedString` + `addAttribute` with `AttributedString` and subscript-based attribute setting
2. Replace `DateFormatter`, `NumberFormatter`, `ByteCountFormatter` with `.formatted()` and `FormatStyle`
3. Use Markdown in localizable `.strings` files — Foundation parses inline Markdown automatically with `AttributedString(localized:)`
4. Replace `NSLocale.current.languageCode` with `Locale.current.language.languageCode?.identifier`

## Compatibility notes

- `AttributedString` requires iOS 15+; `NSAttributedString` continues to work on all versions
- `FormatStyle` requires iOS 15+; `DateFormatter`/`NumberFormatter` continue to work
- `AttributedString` is Codable — can be serialised to JSON or Plist
- SwiftUI `Text` accepts `AttributedString` directly (no `NSAttributedString` bridge needed)
