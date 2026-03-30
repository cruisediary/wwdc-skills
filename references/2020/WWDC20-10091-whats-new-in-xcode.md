---
framework: Xcode
title: "What's new in Xcode"
session: WWDC20-10091
year: 2020
applies_to: iOS 14+
status: reference-only
superseded_by: null
shape: migration
related: []
---

# What's new in Xcode — WWDC20 (Xcode 12)

Xcode 12 shipped with iOS 14 SDK support, multiplatform targets, StoreKit testing, and the new App Clips target type.

## What's new

- **Multiplatform target** — single target that builds for iOS, iPadOS, and macOS (Mac Catalyst or native) from one codebase
- **App Clips target** — new target type for App Clip extensions
- **StoreKit Testing framework** — `SKTestSession`, `StoreKitTest`, local StoreKit configuration files for in-app purchase testing without a sandbox account
- **Mac Catalyst improvements** — menu bar customization, `UISceneActivationConditions`, toolbar support
- **Document tabs** — code editor and canvas side-by-side improvements
- **Simulator improvements** — better performance, temperature indicator
- **Swift package index** — search for packages in the "Add Package Dependency" sheet
- **Build timeline** — build performance visualization in the build report
- **Code completion improvements** — faster, more accurate completions

## Before / After

**StoreKit testing (before — sandbox account required):**
```
// Had to sign in to a sandbox account on device/simulator
// No programmatic control of purchase flow in unit tests
```

**StoreKit testing (after — StoreKitTest framework):**
```swift
import StoreKitTest
import XCTest

class PurchaseTests: XCTestCase {
    var session: SKTestSession!

    override func setUp() async throws {
        session = try SKTestSession(configurationFileNamed: "Products")
        session.disableDialogs = true
        session.clearTransactions()
    }

    func testPurchase() async throws {
        let products = try await Product.products(for: ["com.example.premium"])
        let result = try await products.first!.purchase()
        // assert result
    }
}
```

**App Clips target (new in Xcode 12):**
```
// In Xcode: File > New > Target > App Clip
// Results in:
//   MyApp (main app target)
//   MyAppClip (App Clip target)
// Both share code via embedded frameworks or copy file build phases
```

**Multiplatform target (new concept):**
```
// Single SwiftUI app target builds for iPhone, iPad, Mac
// Conditional compilation for platform-specific code:
#if os(iOS)
    // iOS-only view
#elseif os(macOS)
    // macOS-only view
#endif
```

## Migration steps

1. Update to Xcode 12 to get iOS 14 SDK and Swift 5.3
2. For in-app purchase testing, create a StoreKit Configuration file (`File > New > File > StoreKit Configuration`) and enable it in the scheme's Options tab
3. Add an App Clip target if shipping an App Clip experience; configure associated domains in both targets
4. Consider consolidating iOS/macOS targets using multiplatform targets for pure SwiftUI apps
5. Review build timeline to identify slow build phases after migrating

## Compatibility notes

- Xcode 12 requires macOS 10.15.4 (Catalina) or later
- StoreKit testing (`StoreKitTest`) is an Xcode 12 / iOS 14 addition; requires a `.storekit` configuration file
- Multiplatform targets use Mac Catalyst by default for macOS; native macOS requires `SUPPORTS_MACCATALYST = NO`
- App Clips require Xcode 12 to create the target template; the entitlement (`com.apple.developer.on-demand-install-capable`) must be added manually or via Signing & Capabilities
- Swift Package Manager resolution is now shown in the Xcode build log
