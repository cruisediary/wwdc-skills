---
framework: LLDB
title: 'LLDB: Beyond "po"'
session: WWDC17-401
year: 2017
applies_to: iOS 11+
status: reference-only
superseded_by: null
shape: guide-first
related: []
---

> **Reference-only:** LLDB debugging techniques shown here are still valid in Xcode 16. The `po`, `p`, `v`, and `expr` commands covered are unchanged.

## What changed and why

Xcode 9 / LLDB improvements focused on making the debugger output more accurate and the `po` command more predictable. The key insight: `po` calls `debugDescription`, which is user-overridable and may not show raw values. Use `p` or `v` for unadulterated output.

## Mental model

```
po  → calls CustomDebugStringConvertible.debugDescription (user code runs)
p   → calls LLDB's built-in formatter (no user code)
v   → uses the Swift runtime directly (fastest; no bridging)
expr <expr> → evaluates arbitrary Swift expression in current context
```

## Usage

**Common commands**

```lldb
(lldb) v self.items          # inspect variable without running user code
(lldb) p self.items.count    # evaluate expression with LLDB formatter
(lldb) po self               # call debugDescription (may execute user code)
(lldb) expr self.title = "debug"  # mutate state for testing
(lldb) bt                    # print backtrace
(lldb) frame variable        # show all variables in current frame
```

**Breakpoint with action**

```lldb
(lldb) breakpoint set --name viewDidLoad --one-shot true
(lldb) breakpoint set --file ViewController.swift --line 42 --condition "count > 10"
```

## Adopting this pattern

- Prefer `v` for quick value inspection; it is the lowest overhead command.
- Add `CustomDebugStringConvertible` conformances so `po` gives useful output in team contexts.
- Use `expr --` (double dash) to avoid ambiguity when the expression starts with a flag-like token.
