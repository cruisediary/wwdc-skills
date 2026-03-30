---
framework: CloudKit
title: "What's new in CloudKit"
session: WWDC20-10650
year: 2020
applies_to: iOS 14+
status: reference-only
superseded_by: null
shape: migration
related: []
---

# What's new in CloudKit — WWDC20 (iOS 14)

iOS 14 expanded CloudKit with encrypted fields, shared database improvements, and refined record zone APIs.

> **Note:** `CKSyncEngine` was introduced in a later OS release (iOS 17). Content here is limited to what was confirmed available in iOS 14.

## What's new

- Encrypted `CKRecord` field values — per-field end-to-end encryption using `encryptedValues` subscript
- `CKRecord.Reference` — unchanged API but expanded documentation around deletion rules
- `CKRecordZone` listing improvements — `CKFetchRecordZonesOperation` for enumerating all zones
- Shared database (`CKDatabase.DatabaseScope.shared`) — subscribe to and fetch shared records
- `CKShare` participant management — accept/decline share invitations
- `CloudKit Console` tooling improvements (developer-facing, no API changes)

## Before / After

**Encrypted field values (before — no built-in encryption):**
```swift
// iOS 13 — all field values stored in plaintext on CloudKit servers
let record = CKRecord(recordType: "Note")
record["sensitiveContent"] = "Secret text" as CKRecordValue
```

**Encrypted field values (after — encryptedValues):**
```swift
// iOS 14 — encrypt specific fields end-to-end
let record = CKRecord(recordType: "Note")
// Standard (unencrypted) field:
record["title"] = "My Note" as CKRecordValue
// Encrypted field — stored encrypted on CloudKit servers:
record.encryptedValues["sensitiveContent"] = "Secret text" as CKRecordValue
```

**Fetching all record zones:**
```swift
let fetchZonesOp = CKFetchRecordZonesOperation.fetchAllRecordZonesOperation()
fetchZonesOp.fetchRecordZonesResultBlock = { result in
    switch result {
    case .success(let zonesByID):
        for (zoneID, zone) in zonesByID {
            print("Zone: \(zoneID.zoneName)")
        }
    case .failure(let error):
        print("Error: \(error)")
    }
}
CKContainer.default().privateCloudDatabase.add(fetchZonesOp)
```

**Saving a record with a reference:**
```swift
let parentRecord = CKRecord(recordType: "Post")
let childRecord = CKRecord(recordType: "Comment")

let reference = CKRecord.Reference(record: parentRecord, action: .deleteSelf)
childRecord["post"] = reference
```

**Subscribing to shared database changes:**
```swift
let subscription = CKDatabaseSubscription(subscriptionID: "shared-changes")
let notificationInfo = CKSubscription.NotificationInfo()
notificationInfo.shouldSendContentAvailable = true
subscription.notificationInfo = notificationInfo

CKContainer.default().sharedCloudDatabase.save(subscription) { _, error in
    // handle result
}
```

## Migration steps

1. Identify fields containing sensitive user data and migrate them to `record.encryptedValues[key]`
2. Test encrypted field reads — `record.encryptedValues["key"]` returns `nil` on devices without the user's iCloud key material
3. To enumerate all zones in a database, use `CKFetchRecordZonesOperation.fetchAllRecordZonesOperation()` instead of building zone IDs manually
4. For shared database access, ensure the app handles `CKShare` accept flow via `UIApplicationDelegate`/`App.userActivity`

## Compatibility notes

- `encryptedValues` requires iOS 15+ / macOS 12+ — despite this session being at WWDC20, the encrypted values subscript shipped in the following year's OS
- `CKSyncEngine` is **not** an iOS 14 API — it was introduced later; do not reference it for iOS 14 targets
- Encrypted fields are only accessible on devices signed in to the same iCloud account with valid key material; plan for nil reads
- `CKRecord.Reference` deletion rules (`.deleteSelf` vs `.none`) are enforced server-side in CloudKit
