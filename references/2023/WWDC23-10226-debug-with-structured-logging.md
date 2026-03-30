---
framework: OSLog
title: "Debug with structured logging"
session: WWDC23-10226
year: 2023
applies_to: iOS 17+
status: reference-only
superseded_by: null
shape: guide-first
related: []
---

# Debug with structured logging (WWDC23)

How to use `os.Logger` for structured, privacy-aware log messages, and how to read and filter them in Instruments and the Console app.

## What changed and why

`print()` is unstructured and disappears in production builds. `os_log` has an awkward C-style API. `Logger` (from `os` framework) — introduced in iOS 14 — provides a Swift-native API with string interpolation, log levels, categories, and privacy annotations. iOS 17 / Xcode 15 improve Console's filtering UI and Instruments integration.

## Mental model

- **Logger** — Create one (or a few) `Logger` instances with a subsystem (your bundle ID) and a category (module/feature name). Reuse them; they are cheap value types.
- **Log levels** — `.debug` (development only, never persisted), `.info` (persisted briefly), `.error` (persisted longer), `.fault` (critical; persisted until device reboot). Use the lowest level that fits.
- **Privacy** — String interpolation values are redacted by default in production (`<private>`). Mark values explicitly: `\(value, privacy: .public)` or `\(value, privacy: .sensitive)`.
- **Structured data** — Log integers, floats, booleans, and `OSLogMessage` with type-safe formatting.
- **OSLogStore** — Retrieve logs programmatically at runtime for in-app log export or crash reporter integration.
- **Console + Instruments** — Filter by subsystem and category; inspect log levels and timestamps; use the logging Instrument for timeline visualisation.

## Usage

**Creating a logger:**
```swift
import OSLog

// Create at file/module scope or in a type
let logger = Logger(subsystem: "com.example.MyApp", category: "Networking")

// Per-type logger pattern
extension Logger {
    static let network = Logger(subsystem: "com.example.MyApp", category: "Networking")
    static let ui = Logger(subsystem: "com.example.MyApp", category: "UI")
}
```

**Logging at different levels:**
```swift
Logger.network.debug("Fetching URL: \(url, privacy: .public)")
Logger.network.info("Response received: \(statusCode)")
Logger.network.error("Request failed: \(error.localizedDescription, privacy: .public)")
Logger.network.fault("Unrecoverable state: \(description, privacy: .public)")
```

**Privacy annotations:**
```swift
let userID = "user-12345"
let email = "user@example.com"

// Default: <private> in production, value visible in debug
logger.info("User logged in: \(userID)")

// Explicitly public — always visible
logger.info("App version: \(Bundle.main.appVersion, privacy: .public)")

// Sensitive — extra protection hint (treated like private)
logger.info("Email: \(email, privacy: .sensitive)")
```

**Formatted numeric values:**
```swift
let bytes = 1_048_576
logger.info("Downloaded \(bytes, format: .byteCount(style: .file)) bytes")
// Output: "Downloaded 1 MB bytes"
```

**Reading logs programmatically with OSLogStore:**
```swift
do {
    let store = try OSLogStore(scope: .currentProcessIdentifier)
    let position = store.position(timeIntervalSinceLatestBoot: -3600)  // last hour
    let entries = try store.getEntries(at: position)
        .compactMap { $0 as? OSLogEntryLog }
        .filter { $0.subsystem == "com.example.MyApp" }
    for entry in entries {
        print("\(entry.date): [\(entry.category)] \(entry.composedMessage)")
    }
} catch {
    print("Log store error: \(error)")
}
```

## Adopting this pattern

1. Replace `print()` calls with `Logger` at the appropriate level — `debug` for development traces, `error`/`fault` for real failures.
2. Create one `Logger` extension with static properties per subsystem/category; share them across files.
3. Mark sensitive data as `.private` (default) and only elevate to `.public` when the value is safe to expose in crash logs.
4. Filter logs in Console.app by your app's bundle-ID subsystem to see only your messages.
5. Use `OSLogStore` to pull recent logs for in-app diagnostics or to attach to feedback reports.
