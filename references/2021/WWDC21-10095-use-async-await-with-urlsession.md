---
framework: Swift Concurrency
title: "Use async/await with URLSession"
session: WWDC21-10095
year: 2021
applies_to: iOS 15+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/swift-concurrency.md
---

# Use async/await with URLSession (WWDC21)

Covers the new `async`/`await`-native URLSession APIs introduced in iOS 15 — `data(from:)`, `upload(for:from:)`, `download(from:)`, and the `bytes(from:)` streaming API.

## Key APIs

### Fetching data

```swift
// Basic data fetch — replaces dataTask(with:completionHandler:)
let (data, response) = try await URLSession.shared.data(from: url)
let httpResponse = response as? HTTPURLResponse
// data is Data, response is URLResponse

// With a URLRequest
var request = URLRequest(url: url)
request.httpMethod = "POST"
request.httpBody = payload
let (data, response) = try await URLSession.shared.data(for: request)

// With a delegate for progress / auth challenge
let (data, response) = try await URLSession.shared.data(
    for: request,
    delegate: myDelegate
)
```

### Uploading

```swift
// Upload a file
let (data, response) = try await URLSession.shared.upload(
    for: request,
    fromFile: fileURL
)

// Upload raw Data
let (data, response) = try await URLSession.shared.upload(
    for: request,
    from: bodyData
)
```

### Downloading

```swift
// Download to a temp file URL
let (tempURL, response) = try await URLSession.shared.download(from: url)
// Move the file before the function returns — temp file is deleted after
let destination = FileManager.default.temporaryDirectory
    .appendingPathComponent(UUID().uuidString)
try FileManager.default.moveItem(at: tempURL, to: destination)
```

### Streaming bytes — URLSession.bytes

```swift
// Line-by-line streaming of a large response
let (asyncBytes, response) = try await URLSession.shared.bytes(from: url)
for try await line in asyncBytes.lines {
    process(line)   // process each line as it arrives
}

// Byte-by-byte streaming
let (asyncBytes, _) = try await URLSession.shared.bytes(from: url)
var buffer = Data()
for try await byte in asyncBytes {
    buffer.append(byte)
    if buffer.count >= chunkSize {
        await processChunk(buffer)
        buffer.removeAll()
    }
}
```

## Quick start

**Before (dataTask with completion handler):**
```swift
func fetchUser(id: Int, completion: @escaping (Result<User, Error>) -> Void) {
    let url = URL(string: "https://api.example.com/users/\(id)")!
    URLSession.shared.dataTask(with: url) { data, response, error in
        if let error { completion(.failure(error)); return }
        do {
            let user = try JSONDecoder().decode(User.self, from: data!)
            completion(.success(user))
        } catch {
            completion(.failure(error))
        }
    }.resume()
}
```

**After (async/await):**
```swift
func fetchUser(id: Int) async throws -> User {
    let url = URL(string: "https://api.example.com/users/\(id)")!
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(User.self, from: data)
}
```

## Common patterns

```swift
// Wrap in a Task to support cancellation
func loadImage(from url: URL) async throws -> UIImage {
    let task = Task {
        let (data, _) = try await URLSession.shared.data(from: url)
        guard let image = UIImage(data: data) else {
            throw URLError(.cannotDecodeContentData)
        }
        return image
    }
    return try await task.value
}

// Cancelling the Task automatically cancels the underlying URLSession task
```

## Gotchas

- `URLSession.data(from:)`, `URLSession.data(for:)`, `URLSession.bytes(from:)` require iOS 15+
- `URLSession.download(from:)` requires iOS 15+
- `URLSession.upload(for:from:)` and `URLSession.upload(for:fromFile:)` require iOS 15+
- The `delegate:` parameter on all these methods allows per-request delegate callbacks alongside async/await
- For iOS 13/14 back-deployment, wrap `dataTask` in `withCheckedThrowingContinuation`
