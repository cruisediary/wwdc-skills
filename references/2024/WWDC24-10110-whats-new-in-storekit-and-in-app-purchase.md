---
framework: StoreKit
title: "What's new in StoreKit and In-App Purchase"
session: WWDC24-10110
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: migration
related: []
---

## What's new

- `Product.SubscriptionInfo.RenewalInfo.gracePeriodExpirationDate` — lets you check whether a subscriber is in a billing grace period and when it ends
- `StoreView` and `ProductView` now support custom styles for richer in-app purchase UI
- `Product.purchase(options:)` accepts `appAccountToken` in the options set to associate purchases with your backend user accounts
- Win-back offers for lapsed subscribers

## Before / After

```swift
// BEFORE (iOS 17): checking grace period required raw transaction fields
// and there was no first-class gracePeriodExpirationDate property

// AFTER (iOS 18): read grace period expiry directly from RenewalInfo
import StoreKit

func checkGracePeriod(for productID: String) async {
    guard let statuses = try? await Product.SubscriptionInfo.status(for: productID) else { return }
    for status in statuses {
        if case .verified(let renewalInfo) = status.renewalInfo {
            if let graceExpiry = renewalInfo.gracePeriodExpirationDate {
                // User is in grace period — continue granting access until graceExpiry
                print("Grace period ends: \(graceExpiry)")
            }
        }
    }
}
```

```swift
// BEFORE: ProductView had limited built-in styling
ProductView(id: "com.example.premium")

// AFTER (iOS 18): ProductView with a custom style via ProductViewStyle conformance
struct SubscriptionProductStyle: ProductViewStyle {
    func makeBody(configuration: Configuration) -> some View {
        if let product = configuration.product {
            // Product loaded — show full UI
            VStack {
                Text(product.displayName)
                    .font(.headline)
                Text(product.displayPrice)
                    .foregroundStyle(.secondary)
                configuration.buyButton
                    .buttonStyle(.borderedProminent)
            }
        } else {
            // Product still loading
            ProgressView()
        }
    }
}

// Usage:
ProductView(id: "com.example.premium") {
    // product image
    Image(systemName: "star.fill")
}
.productViewStyle(SubscriptionProductStyle())
```

```swift
// Associating a purchase with a backend account token
import StoreKit

func purchaseWithAccount(_ product: Product, accountToken: UUID) async throws {
    let result = try await product.purchase(options: [
        .appAccountToken(accountToken)
    ])
    // handle result
}
```

## Migration steps

1. Audit grace-period handling: replace any custom date calculation logic with `renewalInfo.gracePeriodExpirationDate`.
2. Update `StoreView` and `ProductView` usages to take advantage of custom styles for brand consistency — review `ProductViewStyle` protocol.
3. If you track users across devices, pass `appAccountToken` on every `Product.purchase(options:)` call to ensure server-side receipt validation can correlate transactions.
4. Review win-back offer eligibility in App Store Connect and expose them via `Product.SubscriptionInfo` win-back offer APIs (see Apple docs for exact type names).

## Compatibility notes

- `gracePeriodExpirationDate` requires iOS 18+ / macOS 15+.
- Custom `ProductViewStyle` requires iOS 17+ (check availability for earlier style options).
- `appAccountToken` purchase option has been available since iOS 15 via `Product.PurchaseOption.appAccountToken(_:)` — iOS 18 does not change this API, but it is highlighted in context with new server-side reconciliation features.
- Win-back offers require iOS 18+ on-device and corresponding App Store Connect configuration.
