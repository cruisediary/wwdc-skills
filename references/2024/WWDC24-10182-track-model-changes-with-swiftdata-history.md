---
framework: SwiftData
title: "Track model changes with SwiftData history"
session: WWDC24-10182
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/swiftdata.md
---

# SwiftData — Track Model Changes with SwiftData History (WWDC24)

iOS 18 adds a history API to SwiftData that lets you fetch an ordered record of inserts, updates, and deletes on your model types, enabling sync engines, undo stacks, and audit logs.

## Quick start

```swift
import SwiftData

// Fetch all changes since the last persisted token
let lastToken: HistoryToken? = loadTokenFromStorage()

let historyDescriptor = HistoryDescriptor<DefaultHistoryTransaction>(
    predicate: #Predicate { _ in true }
)

let transactions = try context.fetchHistory(historyDescriptor)

for transaction in transactions {
    for change in transaction.changes {
        switch change {
        case .insert(let inserted):
            print("Inserted: \(inserted.persistentModelID)")
        case .update(let updated):
            print("Updated: \(updated.persistentModelID)")
        case .delete(let deleted):
            print("Deleted id: \(deleted.persistentModelID)")
        @unknown default:
            break
        }
    }
}

// Persist the latest token so the next launch starts where this one left off
if let latest = transactions.last?.token {
    saveTokenToStorage(latest)
}
```

## Key APIs

| API | Purpose |
|---|---|
| `ModelContext.fetchHistory(_:)` | Returns `[DefaultHistoryTransaction]` matching the descriptor |
| `HistoryDescriptor<T>` | Configures the history query — can filter by model type or time range |
| `HistoryToken` | Opaque cursor representing a point in history; pass to the next fetch to get only newer changes |
| `DefaultHistoryTransaction` | A batch of changes committed together; contains `changes: [HistoryChange]` and a `token` |
| `HistoryChange` | Enum with cases `.insert`, `.update`, `.delete`; each case carries the model or its ID |
| `DefaultHistoryInsert` | Payload of a `.insert` change; provides `persistentModelID` and model property values |
| `DefaultHistoryUpdate` | Payload of a `.update` change; provides `persistentModelID` and changed property values |
| `DefaultHistoryDelete` | Payload of a `.delete` change; provides only `persistentModelID` (model is gone) |

## Common patterns

**Syncing changes to a remote server:**
```swift
func syncPendingChanges(context: ModelContext) async throws {
    let token: HistoryToken? = UserDefaults.standard.historyToken
    let descriptor = HistoryDescriptor<DefaultHistoryTransaction>()

    let transactions = try context.fetchHistory(descriptor)
    var latestToken: HistoryToken?

    for tx in transactions {
        for change in tx.changes {
            switch change {
            case .insert(let insert):
                try await remoteAPI.create(id: insert.persistentModelID, data: insert.changedValues)
            case .update(let update):
                try await remoteAPI.update(id: update.persistentModelID, data: update.changedValues)
            case .delete(let delete):
                try await remoteAPI.delete(id: delete.persistentModelID)
            @unknown default: break
            }
        }
        latestToken = tx.token
    }

    if let latestToken {
        UserDefaults.standard.historyToken = latestToken
    }
}
```

**Building a lightweight undo history:**
```swift
// Store tokens at each save point to enable undo
struct SavePoint {
    let description: String
    let token: HistoryToken
}

var savePoints: [SavePoint] = []

func saveWithUndo(context: ModelContext, description: String) throws {
    try context.save()
    // Capture the current token as an undo marker
    let descriptor = HistoryDescriptor<DefaultHistoryTransaction>()
    if let latest = try context.fetchHistory(descriptor).last?.token {
        savePoints.append(SavePoint(description: description, token: latest))
    }
}
```

**Filtering history to a specific model type:**
```swift
// Only fetch history for Article changes
let descriptor = HistoryDescriptor<DefaultHistoryTransaction>(
    predicate: #Predicate<DefaultHistoryTransaction> { transaction in
        transaction.changes.contains { change in
            change.persistentModelID.entityName == "Article"
        }
    }
)
let articleTransactions = try context.fetchHistory(descriptor)
```

## Gotchas

- **History is retained for a limited window** — SwiftData purges old history after a system-defined period. Do not rely on history being available indefinitely; process it promptly after launch.
- **Persist tokens between launches** — `HistoryToken` is `Codable`; store it in `UserDefaults` or a dedicated model property. Losing the token means you cannot determine what changed since the last run.
- **Delete payloads are ID-only** — `DefaultHistoryDelete` provides only `persistentModelID`; the deleted model's properties are gone. If you need property values at delete time, capture them before deletion or listen for changes synchronously.
- **History requires iOS 18+** — the API is unavailable on earlier OS versions. Guard with `if #available(iOS 18, *)` when deploying to mixed targets.
- **Context isolation** — `fetchHistory` reflects changes committed to the persistent store, not in-flight context changes. Call `context.save()` before fetching history if you want to include the latest session's changes.
