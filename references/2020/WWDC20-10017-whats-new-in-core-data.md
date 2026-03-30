---
framework: Core Data
title: "What's new in Core Data"
session: WWDC20-10017
year: 2020
applies_to: iOS 14+
status: reference-only
superseded_by: null
shape: migration
related: []
---

# What's new in Core Data — WWDC20 (iOS 14)

iOS 14 brought persistent history tracking improvements, CloudKit sync enhancements via `NSPersistentCloudKitContainer`, and batch operation refinements.

## What's new

- `NSPersistentCloudKitContainer` — history tracking enabled by default for CloudKit-backed stores
- `NSPersistentHistoryTransaction` / `NSPersistentHistoryChange` — track and merge remote changes
- `NSPersistentCloudKitContainerOptions` — configure per-store CloudKit database scope (`.private`, `.shared`, `.public`)
- `NSPersistentCloudKitContainer.eventChangedNotification` — monitor sync events
- `NSCoreDataCoreSpotlightDelegate` — index Core Data objects in Spotlight
- Batch insert improvements — `NSBatchInsertRequest` with dictionary or managed object handler
- `NSFetchedResultsController` diffable data source integration enhancements

## Before / After

**CloudKit container with shared database (before — private only):**
```swift
// iOS 13 — only private database scope supported easily
let container = NSPersistentCloudKitContainer(name: "MyModel")
container.loadPersistentStores { _, error in }
```

**CloudKit container with shared database (after — explicit scope):**
```swift
let container = NSPersistentCloudKitContainer(name: "MyModel")

guard let privateDescription = container.persistentStoreDescriptions.first else { return }
privateDescription.cloudKitContainerOptions = NSPersistentCloudKitContainerOptions(
    containerIdentifier: "iCloud.com.example.myapp"
)
// scope defaults to .private; set explicitly:
privateDescription.cloudKitContainerOptions?.databaseScope = .private

container.loadPersistentStores { _, error in }
```

**Batch insert with dictionary array:**
```swift
let request = NSBatchInsertRequest(
    entityName: "Item",
    objects: [
        ["title": "First", "createdAt": Date()],
        ["title": "Second", "createdAt": Date()]
    ]
)
request.resultType = .objectIDs
let result = try context.execute(request) as? NSBatchInsertResult
```

**Batch insert with managed object handler:**
```swift
let request = NSBatchInsertRequest(entity: Item.entity()) { (managedObject: NSManagedObject) -> Bool in
    guard let item = managedObject as? Item, let data = dataIterator.next() else { return true }
    item.title = data.title
    item.createdAt = data.date
    return false  // return true when done
}
```

**Monitoring CloudKit sync events:**
```swift
NotificationCenter.default.addObserver(
    forName: NSPersistentCloudKitContainer.eventChangedNotification,
    object: container,
    queue: .main
) { notification in
    guard let event = notification.userInfo?[NSPersistentCloudKitContainer.eventNotificationUserInfoKey]
        as? NSPersistentCloudKitContainer.Event else { return }
    // event.type: .setup, .import, .export
    // event.succeeded, event.error
}
```

**Spotlight indexing:**
```swift
let delegate = NSCoreDataCoreSpotlightDelegate(
    forStoreWith: storeDescription,
    coordinator: container.persistentStoreCoordinator
)
delegate.startSpotlightIndexing()
```

## Migration steps

1. To use CloudKit sync, add the CloudKit entitlement and set `cloudKitContainerOptions` on the store description
2. Enable persistent history tracking if merging remote changes manually: `storeDescription.setOption(true as NSNumber, forKey: NSPersistentHistoryTrackingKey)`
3. Migrate bulk inserts from individual `context.insert` loops to `NSBatchInsertRequest` for performance
4. Replace manual `NSFetchedResultsControllerDelegate` diff logic with the diffable data source integration

## Compatibility notes

- `NSPersistentCloudKitContainer` requires iCloud capability and a CloudKit container
- `NSBatchInsertRequest` with dictionary handler is iOS 14+; object handler is also iOS 14+
- `NSCoreDataCoreSpotlightDelegate` requires iOS 14+
- Persistent history tracking (`NSPersistentHistoryTrackingKey`) is available from iOS 13 but more automated in iOS 14 with CloudKit container
- Batch operations bypass `NSManagedObjectContext` — call `mergeChanges(fromRemoteContextSave:into:)` or listen for `NSManagedObjectContextDidSave` to update in-memory contexts
