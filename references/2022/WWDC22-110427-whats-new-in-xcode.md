---
framework: Xcode
title: "What's new in Xcode"
session: WWDC22-110427
year: 2022
applies_to: iOS 16+
status: reference-only
superseded_by: null
shape: guide-first
related: []
---

# What's new in Xcode — WWDC22

Xcode 14 introduced multi-platform targets (a single target builds for iOS, macOS, etc.), a build timeline visualiser, memory debugger improvements, and Swift Package plugins.

## What changed and why

- **Multi-platform targets** — a single app target can list multiple supported platforms instead of requiring separate targets per platform
- **Build timeline** — new build performance visualiser showing parallelism and bottlenecks (Product > Perform Action > Build with Timing Summary, or the build timeline view)
- **Memory Debugger improvements** — faster heap graph generation, better cycle detection
- **Swift Package plugins** — build tool plugins and command plugins; run arbitrary Swift code as part of the build or as on-demand commands
- **Parallel test execution** — run tests across multiple simulated devices simultaneously
- **Smaller iOS app binaries** — Xcode 14 reduces binary size via improved bitcode-free linking
- **Improved code completion** — faster and more accurate completions
- **Regex literals** — syntax highlighting and compile-time validation for `/pattern/` literals

## Mental model

Xcode 14's theme is reducing structural overhead: multi-platform targets collapse what used to be separate per-platform targets into one, Swift Package plugins bring code generation and formatting into the build graph rather than requiring external shell scripts, and parallel testing compresses the test-feedback loop. Think of the release as "same capabilities, less scaffolding" — the goal is fewer project-file changes when adding a platform or a new code-generation step.

## Multi-platform targets

Before Xcode 14, separate `MyApp-iOS` and `MyApp-macOS` targets were common. Xcode 14 allows:

```
Target "MyApp"
  Supported Destinations: iPhone, iPad, Mac (Designed for iPad), Mac
```

Conditions in build settings and `#if os(iOS)` / `#if os(macOS)` handle platform differences.

## Swift Package plugins

### Build tool plugin

```swift
// Package.swift
.plugin(
    name: "GenerateCode",
    capability: .buildTool()
)
```

```swift
// Plugin implementation
import PackagePlugin

@main struct GenerateCodePlugin: BuildToolPlugin {
    func createBuildCommands(context: PluginContext, target: Target) throws -> [Command] {
        let outputDir = context.pluginWorkDirectory.appending("Generated")
        return [
            .buildCommand(
                displayName: "Generate Swift code",
                executable: try context.tool(named: "codegen").path,
                arguments: [target.directory.string, outputDir.string],
                outputFiles: [outputDir.appending("Generated.swift")]
            )
        ]
    }
}
```

### Command plugin

```swift
@main struct FormatPlugin: CommandPlugin {
    func performCommand(context: PluginContext, arguments: [String]) throws {
        let swiftFormat = try context.tool(named: "swift-format")
        // run swift-format on source files
    }
}
```

Run via: `swift package <plugin-name>` or right-click target in Xcode.

## Compatibility notes

- Xcode 14 requires macOS 12.5+
- Multi-platform targets require Xcode 14; older Xcode requires separate targets
- Swift Package plugins are available from Swift 5.6+ but the plugin API was expanded in Xcode 14
- Build timeline viewer is a diagnostic tool; no code changes required to use it
