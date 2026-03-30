---
framework: Xcode
title: "Use Xcode for server-side development"
session: WWDC22-110360
year: 2022
applies_to: macOS 13+
status: reference-only
superseded_by: null
shape: guide-first
related: []
---

# Use Xcode for server-side development — WWDC22

This session demonstrates using Xcode 14 to build, debug, and document server-side Swift applications, including integration with the Swift Package Index and DocC for server projects.

## What's covered

- **Swift Package Index** — discovering and adding server-side packages (Vapor, Hummingbird, etc.) directly from Xcode's package search
- **Debugging server-side Swift** — attaching the Xcode debugger to a running server process, setting breakpoints in request handlers
- **DocC for server projects** — generating and hosting documentation for Swift server frameworks and libraries
- **Xcode Cloud for server** — CI/CD pipelines that build and test Linux-targeted Swift packages

## Key workflows

### Adding server packages via Xcode

```
File > Add Package Dependencies... → search Swift Package Index
```

Common server packages available:
- `swift-nio` — Apple's non-blocking I/O framework (foundation for Vapor, Hummingbird)
- `vapor/vapor` — full-featured web framework
- `hummingbird-project/hummingbird` — lightweight HTTP server framework

### Debugging a server process

```swift
// In a Vapor request handler — Xcode debugger attaches normally
app.get("hello") { req async -> String in
    // Set breakpoint here; Xcode pauses the server process
    let result = await computeResult()
    return result
}
```

Attach via: **Debug > Attach to Process by PID or Name...**

### DocC for server libraries

```swift
/// Processes an incoming request and returns a response.
///
/// - Parameter request: The incoming HTTP request.
/// - Returns: An `HTTPResponse` containing the result.
/// - Throws: `ServerError.notFound` if the resource does not exist.
public func handle(_ request: HTTPRequest) async throws -> HTTPResponse { ... }
```

Run `swift package generate-documentation` or use the **Product > Build Documentation** menu.

## Compatibility notes

- Xcode 14 on macOS 13 is required for the workflows shown
- Server-side Swift targets Linux; use Swift Package targets with `.executableTarget` and avoid AppKit/UIKit imports
- DocC-generated sites can be hosted on any static file server
- Xcode Cloud supports Linux cross-compilation for server projects as of Xcode 14
