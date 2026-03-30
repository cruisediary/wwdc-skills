---
framework: Swift
title: "Demystify explicitly built modules"
session: WWDC24-10171
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: guide-first
related: []
---

# Swift — Demystify Explicitly Built Modules (WWDC24)

How Xcode 16's explicit module build system eliminates redundant compilation and speeds up clean and incremental builds.

## What changed and why

Before Xcode 16, modules were built *implicitly*: each compiler invocation would discover and compile the modules it needed on the fly. This meant the same module (e.g., `Foundation`, `UIKit`, or a shared framework) could be compiled redundantly across multiple targets in the same build, wasting time and memory.

Xcode 16 introduces *explicitly built modules*: modules are pre-compiled once as a separate build phase, cached, and reused across all targets that need them. The compiler receives an explicit list of pre-built module artifacts rather than discovering them at compile time.

This change is enabled automatically in Xcode 16 — no code changes are required.

## Mental model

Think of explicitly built modules like pre-compiled headers (PCH) from earlier Xcode eras, but applied uniformly to every Swift and Clang module in the project.

- **Implicit modules (old)**: each compiler job compiles the modules it needs, possibly duplicating work across N parallel jobs
- **Explicit modules (new)**: a module scanning phase runs first, builds a dependency graph, pre-compiles each module once, then all compiler jobs consume the cached artifacts

The result: cleaner parallelism, better cache reuse across builds (even between CI runs when the cache is warmed), and earlier detection of module-level incompatibilities.

## Usage

No code changes are required. Explicit modules are automatically enabled for new and existing projects in Xcode 16.

To verify the setting is active:
- In Xcode 16: **Build Settings** → search for `Explicitly Built Modules` → should be `Yes` for new projects
- The build log will show a **Scan dependencies** phase before compilation begins

For Swift Packages, explicit modules apply automatically when built via Xcode. Command-line `swift build` uses a separate implementation that also benefits from module caching.

**Reading the build log:**
```
Scan dependencies for Target 'MyApp'
Build module 'Foundation' (cached)
Build module 'UIKit'
Build module 'MyFramework'
Compile Swift source files for Target 'MyApp'
```

The `(cached)` label indicates a module was reused from a previous build.

## Gotchas

- **Module fingerprinting surfaces binary incompatibilities earlier** — explicitly built modules include a fingerprint of their build configuration. If a dependency is built with a different deployment target, SDK, or compiler flags than the consuming target, you will see a module mismatch error at build time rather than a subtle runtime bug. Fix: ensure all targets in a project use consistent SDK and deployment target settings.

- **Header ordering issues become errors** — implicit modules were tolerant of certain header include-order bugs because they rebuilt modules on demand. With explicit modules, a header that depends on another header being included first will now produce an error if the ordering is not declared correctly. Fix: add the missing `#include` or `@import` to the header that needs it.

- **`ENABLE_EXPLICIT_MODULE_BUILDS` build setting** — if you need to opt out temporarily (e.g., for a third-party SDK that does not yet support explicit modules), set `ENABLE_EXPLICIT_MODULE_BUILDS = NO` for that target. Report the issue to the SDK vendor.

- **Clean build cache invalidation** — the first clean build after enabling explicit modules may be slower because all modules must be compiled and cached. Subsequent builds are faster.
