---
framework: StoreKit
title: "Meet StoreKit for SwiftUI"
session: WWDC23-10013
year: 2023
applies_to: iOS 17+
status: reference-only
superseded_by: null
shape: code-first
related: []
---

# Meet StoreKit for SwiftUI (WWDC23)

iOS 17 adds native SwiftUI views for in-app purchases: `ProductView`, `StoreView`, and `SubscriptionStoreView` — reducing boilerplate for common IAP UI patterns.

## Quick start

```swift
import StoreKit
import SwiftUI

// Display a single product with purchase button
struct UpgradeView: View {
    let productID = "com.example.premium"

    var body: some View {
        ProductView(id: productID) { _ in
            // Custom icon
            Image(systemName: "crown.fill")
                .foregroundStyle(.yellow)
        }
        .productViewStyle(.large)
    }
}
```

## Key APIs

| API | Purpose |
|---|---|
| `ProductView(id:)` | Single product display + purchase button |
| `StoreView(ids:)` | Grid/list of multiple products with purchase buttons |
| `SubscriptionStoreView(groupID:)` | Full subscription purchase UI for a subscription group |
| `.productViewStyle(_:)` | Style: `.automatic`, `.compact`, `.large`, `.regular` |
| `.storeButton(_:for:)` | Customise the visibility of auxiliary buttons (restore, redeem) |
| `Product.purchase()` | Programmatic purchase (existing async API) |
| `Transaction.updates` | Async sequence of transaction updates |
| `AppStore.sync()` | Syncs purchases with the App Store server |

## Common patterns

**Store view for a list of consumables/non-consumables:**
```swift
let productIDs = [
    "com.example.coins.100",
    "com.example.coins.500",
    "com.example.coins.1000"
]

StoreView(ids: productIDs) { product in
    // Custom icon per product
    Label(product.displayName, systemImage: "bitcoinsign.circle")
}
.productViewStyle(.regular)
```

**Subscription store view:**
```swift
// Use the subscription group ID from App Store Connect
SubscriptionStoreView(groupID: "com.example.pro.group") {
    // Marketing content above the subscription options
    VStack {
        Image(systemName: "crown.fill").font(.largeTitle)
        Text("Go Pro").font(.title.bold())
        Text("Unlock all features")
    }
    .containerBackground(.blue.gradient, for: .subscriptionStoreFullHeight)
}
.subscriptionStoreButtonLabel(.multiline)
.subscriptionStorePickerItemBackground(.thinMaterial)
```

**Listening for transaction updates:**
```swift
.task {
    for await update in Transaction.updates {
        if case .verified(let transaction) = update {
            // Deliver content
            await transaction.finish()
        }
    }
}
```

**Restore purchases button:**
```swift
Button("Restore Purchases") {
    Task { try? await AppStore.sync() }
}
```

**Custom purchase flow with Product.purchase():**
```swift
Button("Buy for \(product.displayPrice)") {
    Task {
        do {
            let result = try await product.purchase()
            switch result {
            case .success(let verification):
                if case .verified(let transaction) = verification {
                    unlockContent(for: transaction.productID)
                    await transaction.finish()
                }
            case .userCancelled, .pending:
                break
            @unknown default:
                break
            }
        } catch {
            print("Purchase error: \(error)")
        }
    }
}
```

## Gotchas

- `ProductView`, `StoreView`, and `SubscriptionStoreView` require iOS 17+.
- These views handle loading, purchase, and error states automatically — use them when you don't need custom loading UI.
- Always call `transaction.finish()` after delivering content, or the purchase stays in a pending state.
- Test purchases in StoreKit Testing in Xcode (use a `StoreKit Configuration` file) before testing on a real device with a Sandbox account.
- `SubscriptionStoreView` requires a subscription group configured in App Store Connect.
