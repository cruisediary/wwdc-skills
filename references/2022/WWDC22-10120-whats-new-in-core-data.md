---
framework: Core Data
title: "What's new in Core Data"
session: WWDC22-10120
year: 2022
applies_to: iOS 16+
status: reference-only
superseded_by: null
shape: migration
related: []
---

# What's new in Core Data — WWDC22

iOS 16 and macOS 13 brought CloudKit sync improvements to `NSPersistentCloudKitContainer`, better history tracking via `NSPersistentHistoryTransaction`, and staged migration support.

## What's new

- **CloudKit sync conflict resolution** — improved merge policy handling in `NSPersistentCloudKitContainer`
- **`NSPersistentHistoryTransaction`** — track fine-grained changes for UI refresh and sync reconciliation
- **Staged migration** — break large schema migrations into sequential lightweight stages
- **`NSManagedObjectContext` improvements** — `performAndWait` async/await version (`perform`)
- **SwiftUI integration** — `@FetchRequest` with `SectionedFetchRequest` improvements

## Key APIs

### NSPersistentHistoryTransaction

```swift
// Fetch recent history transactions to find what changed
let request = NSPersistentHistoryChangeRequest.fetchHistory(after: lastToken)
let result = try context.execute(request) as! NSPersistentHistoryResult
let transactions = result.result as! [NSPersistentHistoryTransaction]

for transaction in transactions {
    for change in transaction.changes ?? [] {
        switch change.changeType {
        case .insert: handleInsert(change.changedObjectID)
        case .update: handleUpdate(change.changedObjectID, change.updatedProperties)
        case .delete: handleDelete(change.tombstone)
        default: break
        }
    }
}
// Save token for next fetch
lastToken = transactions.last?.token
```

### Async perform

```swift
// New in iOS 15/16 — async version of performAndWait
await context.perform {
    let object = MyEntity(context: context)
    object.name = "Example"
    try context.save()
}
```

### Staged migration

```swift
// Define migration stages that execute sequentially
// Each stage is either lightweight or requires a mapping model
// Configure on NSPersistentStoreDescription before loading stores
let description = NSPersistentStoreDescription(url: storeURL)
// Staged migration is configured through NSPersistentStoreStagedMigrationManager
// (see Core Data migration documentation for full setup)
```

### NSPersistentCloudKitContainer sync

```swift
let container = NSPersistentCloudKitContainer(name: "MyModel")
container.persistentStoreDescriptions.first?.setOption(
    true as NSNumber,
    forKey: NSPersistentHistoryTrackingKey
)
container.persistentStoreDescriptions.first?.setOption(
    true as NSNumber,
    forKey: NSPersistentStoreRemoteChangeNotificationPostOptionKey
)
container.loadPersistentStores { _, error in
    if let error { fatalError(error.localizedDescription) }
}
```

## Migration steps

1. Enable persistent history tracking (`NSPersistentHistoryTrackingKey`) on all stores that use CloudKit sync
2. Observe `NSPersistentStoreRemoteChangeNotification` to merge remote changes into the UI context
3. Replace multi-step heavyweight migrations with staged lightweight migration where possible
4. Adopt `context.perform { }` (async) instead of `performAndWait` in async code paths

## Compatibility notes

- `NSPersistentHistoryTransaction` is available from iOS 13+ but recommended usage pattern improved in iOS 16
- CloudKit sync requires iCloud entitlement and `NSPersistentCloudKitContainer`
- Staged migration API details evolved across iOS 16–17; see WWDC23 SwiftData sessions for the modern approach
