---
framework: Swift Concurrency
title: "Meet distributed actors in Swift"
session: WWDC22-110356
year: 2022
applies_to: iOS 16+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/swift-concurrency.md
---

# Meet distributed actors in Swift — WWDC22

Distributed actors extend Swift's actor model to support cross-process and cross-network communication, allowing actor calls to transparently traverse process or machine boundaries.

## Core concepts

- `distributed actor` — an actor that may exist in another process or on another machine
- `DistributedActorSystem` protocol — pluggable transport layer (network, IPC, in-process)
- `distributed func` — marks a method as callable across the distribution boundary; callers always use `await try`
- `ActorID` — each distributed actor has a unique identity within its actor system
- `@Resolvable` — macro (or protocol-level mechanism) to resolve a remote actor reference from an ID
- Calls to distributed functions are `throws` because the remote call can fail for transport reasons

## Key APIs

```swift
// Define a distributed actor
distributed actor BankAccount {
    var balance: Double = 0

    distributed func deposit(amount: Double) {
        balance += amount
    }

    distributed func currentBalance() -> Double {
        balance
    }
}

// Resolve a remote reference (actor system provides the implementation)
let account = try BankAccount.resolve(id: knownID, using: actorSystem)
// Calling a distributed function is always async + throws
let bal = try await account.currentBalance()
```

## DistributedActorSystem

```swift
// Conform to DistributedActorSystem to provide a transport
protocol DistributedActorSystem {
    associatedtype ActorID: Sendable & Hashable & Codable
    associatedtype InvocationEncoder: DistributedTargetInvocationEncoder
    associatedtype InvocationDecoder: DistributedTargetInvocationDecoder
    associatedtype ResultHandler: DistributedTargetInvocationResultHandler
    associatedtype SerializationRequirement
    // ...
}
```

- Apple ships `LocalTestingDistributedActorSystem` for unit testing distributed actors in-process
- Third-party systems (e.g., Swift Distributed Actors cluster library) provide real network transport

## Design patterns

- **Location transparency** — caller code is identical whether actor is local or remote
- **Explicit failure surface** — all distributed calls are `throws`, making network failures visible at the type level
- **Codable boundary** — arguments and return values must satisfy `SerializationRequirement` (typically `Codable`)
- **Actor identity** — actors are resolved by `ActorID`; storing an ID allows later re-resolution

## Compatibility notes

- Distributed actors require Swift 5.7+ and Xcode 14
- `LocalTestingDistributedActorSystem` available for testing without a real transport
- Cluster transport library is a separate open-source Swift package, not bundled with the OS
- Available on iOS 16+, macOS 13+, but primarily a server/multi-process feature
