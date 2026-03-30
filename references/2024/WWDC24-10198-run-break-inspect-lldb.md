---
framework: LLDB
title: "Run, Break, Inspect: Explore effective debugging in LLDB"
session: WWDC24-10198
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: guide-first
related: []
---

## What changed and why

Xcode 16 unifies LLDB's expression evaluation commands behind a single `p` command that automatically chooses the best evaluation strategy. Previously developers had to choose between `po` (calls `debugDescription`), `p` (raw type output), and `expression` (full evaluator) based on context. The new `p` selects the right approach for the type at hand, reducing friction while still letting you drop into `po` or `expression` when needed.

## Mental model

Think of `p` as a smart dispatcher: it inspects the type, and if the type has a custom summary or `CustomDebugStringConvertible` conformance it surfaces that; otherwise it falls back to a structured type dump. `po` is now explicitly "call debugDescription" — use it only when you want the object's own description. `expression` (alias: `expr`) is the full REPL-style evaluator for side-effecting calls.

## Usage

```lldb
# Unified print — picks best representation automatically
(lldb) p someView
(lldb) p user.name

# Force object description (calls debugDescription / CustomDebugStringConvertible)
(lldb) po myModel

# Full expression evaluator — can call methods and mutate state
(lldb) expression myArray.append(42)

# Watchpoint: break when a variable's value changes
(lldb) watchpoint set variable self.count
(lldb) watchpoint list

# Raw memory inspection
(lldb) memory read --size 4 --format x --count 8 0x00000001008a4000

# Print a Swift struct's fields in one shot
(lldb) p -l swift -- import Foundation; print(Date())
```

```swift
// In code: add custom LLDB summary via CustomDebugStringConvertible
extension Order: CustomDebugStringConvertible {
    var debugDescription: String {
        "Order(id: \(id), total: \(total), items: \(items.count))"
    }
}
// (lldb) po order  →  Order(id: 42, total: 9.99, items: 3)
```

## Adopting this pattern

- Replace muscle-memory `po` calls with `p` for everyday inspection; reserve `po` for when you specifically want the description string
- Add `CustomDebugStringConvertible` to your domain models — `po` and Xcode's variable view both benefit
- Use `watchpoint set variable` instead of adding temporary `didSet { print(...) }` observers — no source change required
