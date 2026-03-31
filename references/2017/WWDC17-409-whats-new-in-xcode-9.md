---
framework: Xcode
title: "What's New in Xcode 9"
session: WWDC17-409
year: 2017
applies_to: iOS 11+
status: deprecated
superseded_by: null
shape: guide-first
related: []
---

> **Deprecated:** Covers Xcode 9 features. Xcode 16 has superseded all of these workflows. Useful as historical context for understanding when specific features were introduced.

## What changed and why

Xcode 9 introduced wireless debugging, a refactored source editor with cross-file rename, GitHub source control integration, and Swift playground environment on iOS. These features normalized practices (wireless device deployment, inline rename) that are now standard.

## Mental model

```
Wireless debugging      → Device must be on the same Wi-Fi network; pair once via USB
Source editor refactor  → All navigation uses the jump bar
Rename                  → Right-click symbol → Refactor → Rename; renames across Swift and Obj-C
GitHub integration      → Xcode manages clone/commit/PR via built-in SCM panel
```

## Usage

**Wireless deployment**
1. Connect device via USB → trust → Devices & Simulators window → check "Connect via network".
2. Unplug USB. Device appears with network icon in the device toolbar.

**Cross-language rename**
1. Click on a symbol → Editor menu → Refactor → Rename (or right-click → Refactor).
2. Edit the inline field; preview shows all affected locations.
3. Press Return to apply.

## Adopting this pattern

- Wireless debugging requires both Mac and device on the same subnet; corporate Wi-Fi with client isolation will block it.
- The refactored source editor moved some keyboard shortcuts; use Help → Keyboard Shortcuts to find them.
