---
framework: StoreKit
title: "What's new in StoreKit 2 and StoreKit Testing in Xcode"
session: WWDC22-10039
year: 2022
applies_to: iOS 16+
status: reference-only
superseded_by: null
shape: guide-first
related: []
---

# What's new in StoreKit 2 and StoreKit Testing in Xcode — WWDC22

iOS 16 and Xcode 14 brought improvements to StoreKit 2's in-app purchase APIs and the StoreKit testing framework, enabling more thorough test coverage of purchase flows.

## What changed and why in StoreKit 2

- `Transaction.currentEntitlements` — async sequence of all active entitlements
- `Product.SubscriptionInfo.Status` — detailed subscription state (active, expired, in billing retry, etc.)
- `AppTransaction` — verify the app purchase itself (not just IAP) for apps distributed outside the App Store
- `Transaction.unfinished` — async sequence of transactions awaiting `finish()`
- Improved `Product.purchase(options:)` with additional purchase options

## What changed and why in StoreKit Testing

- `StoreKitTest` framework — `SKTestSession` for controlling the test environment
- Control subscription renewal rate, trigger billing issues, approve/decline transactions in tests
- `SKTestTransaction` — inspect and manage simulated transactions

## Mental model

StoreKit 2 replaces the delegate-and-callback pattern of SKPaymentQueue with async sequences: you iterate `Transaction.updates` to receive live purchase events and `Transaction.currentEntitlements` to reconstruct the full entitlement state at any point. Think of entitlements as a stream, not a snapshot — your app should be able to rebuild its access gates from that sequence at launch, after a restore, or after a subscription status change. The StoreKit testing framework mirrors this model by giving tests programmatic control over the same async sequences.

## Key testing APIs

```swift
import StoreKitTest
import XCTest

class PurchaseTests: XCTestCase {
    var session: SKTestSession!

    override func setUp() async throws {
        session = try SKTestSession(configurationFileNamed: "Configuration")
        session.disableDialogs = true
        session.resetToDefaultState()
    }

    func testSuccessfulPurchase() async throws {
        // Simulate a purchase
        let products = try await Product.products(for: ["com.example.premium"])
        let result = try await products.first!.purchase()

        switch result {
        case .success(let verification):
            let transaction = try verification.payloadValue
            XCTAssertEqual(transaction.productID, "com.example.premium")
            await transaction.finish()
        default:
            XCTFail("Expected successful purchase")
        }
    }

    func testExpiredSubscription() async throws {
        // Force expire all subscriptions in the test session
        session.expireSubscriptions()

        // Verify entitlements reflect expired state
        for await result in Transaction.currentEntitlements {
            // Should be empty or expired
        }
    }
}
```

## Transaction management

```swift
// Listen for transactions (e.g. at app launch)
for await result in Transaction.updates {
    if case .verified(let transaction) = result {
        // Deliver content
        await transaction.finish()
    }
}

// Check current entitlements
for await result in Transaction.currentEntitlements {
    if case .verified(let transaction) = result {
        // Grant access to purchased content
    }
}
```

## Adopting this pattern

1. Replace `SKPaymentQueue` and `SKPaymentTransactionObserver` with StoreKit 2 `Transaction.updates` listener
2. Replace receipt validation with `Transaction.currentEntitlements` iteration
3. Add `SKTestSession` to test targets; create a `Configuration.storekit` file in the project
4. Use `session.disableDialogs = true` to suppress purchase sheets in tests

## Compatibility notes

- StoreKit 2 APIs (`Product`, `Transaction`, `SKTestSession`) require iOS 15+; all WWDC22 additions require iOS 16+
- `SKTestSession` is test-only (StoreKitTest framework); do not import in production targets
- Original StoreKit 1 (`SKPaymentQueue`) still functions on iOS 16 but is not recommended for new code
