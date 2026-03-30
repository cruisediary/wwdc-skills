---
framework: Swift
title: "Consume noncopyable types in Swift"
session: WWDC24-10170
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: guide-first
related: []
---

# Swift — Consume Noncopyable Types in Swift (WWDC24)

How to use `~Copyable` to express exclusive ownership of a value, preventing accidental copies of resource-owning types.

## What changed and why

By default, every Swift value type is copyable — assigning a value or passing it to a function silently creates a duplicate. For types that wrap system resources (file descriptors, locks, network connections), silent copying is dangerous: two copies can both try to close the same file handle or release the same lock.

Swift 5.9 introduced `~Copyable` as a constraint that suppresses the implicit copy. A `~Copyable` type has exactly one owner at any point in time. Ownership transfers explicitly via the `consume` operator; the compiler enforces that you do not use a variable after its ownership has been consumed.

## Mental model

Think of a `~Copyable` value as an exclusive ownership token — like a physical key. You can lend the key to someone (`borrowing`), or permanently hand it over (`consuming`). After you hand it over, you no longer have it. The compiler enforces this: attempting to use a variable after consuming it is a compile-time error.

- **`borrowing` parameter** — the callee reads the value; the caller retains ownership after the call
- **`consuming` parameter** — the callee takes ownership; the caller cannot use the variable after the call
- **`consume` expression** — explicitly transfers ownership of a local variable, making it invalid after that point
- **`deinit`** — runs when the last owner drops the value; ideal for resource cleanup

## Usage

**Defining a noncopyable type:**
```swift
struct FileHandle: ~Copyable {
    private let fd: Int32

    init(path: String) throws {
        fd = open(path, O_RDONLY)
        guard fd >= 0 else { throw POSIXError(.ENOENT) }
    }

    deinit {
        close(fd)  // Runs exactly once — no accidental double-close
    }

    borrowing func read(count: Int) -> Data {
        // Read without consuming ownership
        var buffer = [UInt8](repeating: 0, count: count)
        _ = Darwin.read(fd, &buffer, count)
        return Data(buffer)
    }
}
```

**Consuming ownership explicitly:**
```swift
func processFile(handle: consuming FileHandle) {
    // We own `handle` — it will be deinitialized when this function returns
    let data = handle.read(count: 1024)
    process(data)
    // `handle` destroyed here — `close(fd)` called once
}

var myHandle = try FileHandle(path: "/tmp/data.bin")
processFile(handle: consume myHandle)
// `myHandle` is invalid here — compiler error if accessed
```

**Borrowing without transferring ownership:**
```swift
func inspect(handle: borrowing FileHandle) -> String {
    // Caller retains ownership after this call
    let data = handle.read(count: 64)
    return data.hexString
}

let handle = try FileHandle(path: "/tmp/data.bin")
let preview = inspect(handle: handle)  // handle still valid here
```

## Adopting this pattern

Use `~Copyable` for types that:

- **Wrap file descriptors, socket handles, or OS resources** — prevents double-close bugs
- **Implement locks or semaphores** — ensures unlock is called by the same logical owner that locked
- **Model unique network connections** — prevents two parts of code from both writing to the same socket
- **Represent one-shot operations** — cryptographic nonces, write-once tokens

Adoption checklist:
1. Add `~Copyable` to the type's protocol list: `struct MyResource: ~Copyable { }`
2. Add a `deinit` for cleanup (structs support `deinit` when `~Copyable`)
3. Annotate function parameters with `borrowing` (read-only access) or `consuming` (ownership transfer)
4. Use `consume varName` at call sites where you intend to transfer ownership
5. For generic code, use `~Copyable` as a constraint: `func process<T: ~Copyable>(_ value: consuming T)`
