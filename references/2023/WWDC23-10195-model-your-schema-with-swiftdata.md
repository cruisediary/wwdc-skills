---
framework: SwiftData
title: "Model your schema with SwiftData"
session: WWDC23-10195
year: 2023
applies_to: iOS 17+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/swiftdata.md
---

# Model your schema with SwiftData (WWDC23)

This session covers advanced schema modeling: relationships, deletion rules, uniqueness constraints, and schema migrations using `VersionedSchema` and `SchemaMigrationPlan`.

## What changed and why

SwiftData moves schema definition entirely into Swift source code using macros. Rather than editing an `.xcdatamodel` file in a GUI, you express the full schema — including relationships and deletion rules — as annotations on Swift classes. Migrations are expressed as versioned schemas with explicit migration stages, making them diffable and testable in source control.

## Mental model

- Each `@Model` class maps to a database table.
- Properties become columns automatically; no registration step needed.
- `@Relationship` controls what happens to related objects when the owner is deleted.
- `VersionedSchema` snapshots a schema at a point in time; `SchemaMigrationPlan` sequences the upgrade path.
- `MigrationStage.lightweight` handles renames and additions automatically; `MigrationStage.custom` lets you write migration logic in Swift.

## Usage

**Defining a relationship with a delete rule:**
```swift
@Model
class Trip {
    var name: String
    // When a Trip is deleted, all its BucketListItems are also deleted
    @Relationship(deleteRule: .cascade)
    var bucketList: [BucketListItem] = []

    // When a Trip is deleted, its LivingAccommodation reference is set to nil
    @Relationship(deleteRule: .nullify)
    var livingAccommodation: LivingAccommodation?
}
```

**Delete rules:**

| Rule | Behavior |
|---|---|
| `.nullify` (default) | Sets the inverse relationship to nil on the related objects |
| `.cascade` | Deletes all related objects when the owner is deleted |
| `.deny` | Prevents deletion if related objects exist |
| `.noAction` | Takes no action on related objects |

**Unique constraints:**
```swift
@Model
class Person {
    // Ensures no two Person records share the same email
    // Note: Use @Attribute(.unique) for per-property uniqueness
    @Attribute(.unique) var email: String
    var name: String
}
```

**Schema versioning and migration:**
```swift
enum TripSchemaV1: VersionedSchema {
    static var versionIdentifier = Schema.Version(1, 0, 0)
    static var models: [any PersistentModel.Type] { [Trip.self] }

    @Model
    class Trip {
        var name: String
        var destination: String
    }
}

enum TripSchemaV2: VersionedSchema {
    static var versionIdentifier = Schema.Version(2, 0, 0)
    static var models: [any PersistentModel.Type] { [Trip.self] }

    @Model
    class Trip {
        var name: String
        var destination: String
        var startDate: Date  // new property added
    }
}

enum TripMigrationPlan: SchemaMigrationPlan {
    static var schemas: [any VersionedSchema.Type] {
        [TripSchemaV1.self, TripSchemaV2.self]
    }

    static var stages: [MigrationStage] {
        [migrateV1toV2]
    }

    // Lightweight migration: SwiftData infers the schema change automatically
    static let migrateV1toV2 = MigrationStage.lightweight(
        fromVersion: TripSchemaV1.self,
        toVersion: TripSchemaV2.self
    )
}
```

**Using the migration plan:**
```swift
let container = try ModelContainer(
    for: Trip.self,
    migrationPlan: TripMigrationPlan.self
)
```

**Custom migration stage:**
```swift
static let migrateV1toV2 = MigrationStage.custom(
    fromVersion: TripSchemaV1.self,
    toVersion: TripSchemaV2.self,
    willMigrate: { context in
        // Runs before migration — use old schema types
    },
    didMigrate: { context in
        // Runs after migration — use new schema types
        let trips = try context.fetch(FetchDescriptor<TripSchemaV2.Trip>())
        for trip in trips {
            trip.startDate = .distantPast
        }
        try context.save()
    }
)
```

## Adopting this pattern

If your app already uses SwiftData from WWDC23 without versioning:

1. Wrap your current model types in a `VersionedSchema` enum (e.g. `AppSchemaV1`)
2. Set `versionIdentifier` to `Schema.Version(1, 0, 0)`
3. Create a `SchemaMigrationPlan` with that single version in `schemas` and an empty `stages` array
4. Pass `migrationPlan:` to `ModelContainer`
5. For future changes, add `V2`, `V3`, etc. and append `MigrationStage` entries
