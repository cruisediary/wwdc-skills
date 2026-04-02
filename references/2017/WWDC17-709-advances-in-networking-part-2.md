---
framework: URLSession
title: "Advances in Networking, Part 2"
session: WWDC17-709
year: 2017
applies_to: iOS 11+
status: reference-only
superseded_by: null
shape: code-first
related: []
---

> **Reference-only (iOS 11+):** URLSession APIs covered here remain current in iOS 18. This session focuses on adaptive connectivity, background task scheduling, and `URLSessionTask` scheduling properties introduced in iOS 11.

## Quick start

```swift
import Foundation

// Wait for connectivity instead of failing immediately (new in iOS 11)
let config = URLSessionConfiguration.default
config.waitsForConnectivity = true

let session = URLSession(configuration: config, delegate: self, delegateQueue: nil)
let task = session.dataTask(with: URL(string: "https://api.example.com/data")!) { data, response, error in
    guard let data, error == nil else { return }
    // process data
}
task.resume()
```

## Key APIs

| Type | Role |
|---|---|
| `URLSessionConfiguration.waitsForConnectivity` | When `true`, tasks wait for connectivity instead of failing with `NSURLErrorNotConnectedToInternet` |
| `URLSessionTaskDelegate.urlSession(_:taskIsWaitingForConnectivity:)` | Called when a task is waiting; use to update UI (e.g., show offline banner) |
| `URLSessionTask.earliestBeginDate` | Schedule a task to start no earlier than a given date (background sessions) |
| `URLSessionTask.countOfBytesClientExpectsToSend` | Hint to the system about expected upload size for scheduling |
| `URLSessionTask.countOfBytesClientExpectsToReceive` | Hint to the system about expected download size for scheduling |
| `URLSessionConfiguration.background(withIdentifier:)` | Creates a background session; tasks run out-of-process |
| `URLSessionDownloadTask` | Downloads a file to disk; survives app suspension in background sessions |
| `URLSessionUploadTask` | Uploads data or a file; supports background sessions |
| `URLSession.shared` | Convenience singleton for simple, foreground requests |

## Common patterns

**Adaptive connectivity — wait instead of fail**

```swift
let config = URLSessionConfiguration.default
config.waitsForConnectivity = true
let session = URLSession(configuration: config, delegate: self, delegateQueue: .main)

// Delegate callback to update UI while waiting
func urlSession(_ session: URLSession, taskIsWaitingForConnectivity task: URLSessionTask) {
    showOfflineBanner()
}
```

**Scheduled background download with date hint**

```swift
let config = URLSessionConfiguration.background(withIdentifier: "com.myapp.nightly-sync")
let session = URLSession(configuration: config, delegate: self, delegateQueue: nil)

var request = URLRequest(url: URL(string: "https://api.example.com/sync")!)
let task = session.downloadTask(with: request)

// Don't start before 2 AM
var components = Calendar.current.dateComponents([.year, .month, .day], from: Date())
components.hour = 2
task.earliestBeginDate = Calendar.current.date(from: components)

// Give the system sizing hints for smarter scheduling
task.countOfBytesClientExpectsToReceive = 5 * 1024 * 1024  // ~5 MB
task.resume()
```

**Background session completion handler (AppDelegate)**

```swift
// In AppDelegate
func application(_ application: UIApplication,
                 handleEventsForBackgroundURLSession identifier: String,
                 completionHandler: @escaping () -> Void) {
    // Recreate the session with the same identifier
    backgroundCompletionHandler = completionHandler
}

// In URLSessionDelegate
func urlSessionDidFinishEvents(forBackgroundURLSession session: URLSession) {
    DispatchQueue.main.async {
        self.backgroundCompletionHandler?()
        self.backgroundCompletionHandler = nil
    }
}
```

**Multipath TCP (MPTCP) for seamless Wi-Fi/cellular handoff**

```swift
let config = URLSessionConfiguration.default
config.multipathServiceType = .handover  // seamless fallback to cellular
let session = URLSession(configuration: config)
// Requires com.apple.developer.networking.multipath entitlement
```

## Gotchas

- `waitsForConnectivity` does not apply to background sessions (they always wait by nature); set it on default or ephemeral configurations.
- `earliestBeginDate` is a hint, not a guarantee; the system may start the task later based on battery, CPU, and network conditions.
- Background sessions must be recreated with the same identifier each app launch to reconnect to in-flight tasks.
- Always implement `urlSessionDidFinishEvents(forBackgroundURLSession:)` and call the stored completion handler, or iOS may not grant additional background time.
- Multipath TCP (`multipathServiceType`) requires a special entitlement; `.handover` is the most common mode (falls back to cellular only when Wi-Fi is lost).
- Sizing hints (`countOfBytesClientExpectsToSend/Receive`) use `NSURLSessionTransferSizeUnknown` as the default — provide estimates when known for better scheduling.
