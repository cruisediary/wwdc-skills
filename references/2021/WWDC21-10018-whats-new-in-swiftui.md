---
framework: SwiftUI
title: "What's new in SwiftUI"
session: WWDC21-10018
year: 2021
applies_to: iOS 15+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/swiftui.md
---

# What's New in SwiftUI (WWDC21)

iOS 15 / SwiftUI 3 additions: `AsyncImage`, `.searchable`, `.refreshable`, `.task`, swipe actions, Focus API, `FocusState`, `AttributedString` rendering, and `.badge`.

## What's new

- **`AsyncImage`** — declarative async image loading with placeholder support
- **`.searchable`** — adds a search bar to `NavigationView` or `List`
- **`.refreshable`** — pull-to-refresh on `List` and `ScrollView`
- **`.task`** — async task tied to the view's lifetime; auto-cancelled on disappear
- **`.swipeActions`** — custom leading/trailing swipe actions on `List` rows
- **`FocusState`** — programmatic focus control for text fields and focusable views
- **`AttributedString`** — Swift-native attributed string rendered directly in `Text`
- **`.badge`** — count/string badge on `TabView` tabs and `List` rows
- **`refreshable` on `List`** — async handler called when user pulls to refresh
- **`Canvas`** — immediate-mode 2D drawing with `GraphicsContext`
- **`TimelineView`** — view that updates on a schedule (replaces `Timer` hacks)

## Key APIs

```swift
// AsyncImage — with placeholder and phase
AsyncImage(url: URL(string: "https://example.com/photo.jpg")) { phase in
    switch phase {
    case .empty:
        ProgressView()
    case .success(let image):
        image.resizable().aspectRatio(contentMode: .fit)
    case .failure:
        Image(systemName: "photo").foregroundColor(.secondary)
    @unknown default:
        EmptyView()
    }
}

// .searchable — search bar in navigation
NavigationView {
    List(results) { item in Text(item.name) }
        .searchable(text: $searchText, prompt: "Search items")
        .navigationTitle("Items")
}

// .refreshable — pull to refresh
List(items) { item in
    Text(item.title)
}
.refreshable {
    await viewModel.reload()
}

// .task — async work tied to view lifetime
struct ContentView: View {
    @State private var user: User?

    var body: some View {
        Text(user?.name ?? "Loading…")
            .task {
                user = try? await fetchUser()
            }
    }
}

// .swipeActions — custom swipe on List rows
List(messages) { message in
    Text(message.subject)
        .swipeActions(edge: .trailing) {
            Button(role: .destructive) {
                delete(message)
            } label: {
                Label("Delete", systemImage: "trash")
            }
        }
        .swipeActions(edge: .leading) {
            Button { markRead(message) } label: {
                Label("Read", systemImage: "envelope.open")
            }
            .tint(.blue)
        }
}

// FocusState — programmatic focus
struct LoginView: View {
    @FocusState private var focusedField: Field?
    @State private var username = ""
    @State private var password = ""

    enum Field { case username, password }

    var body: some View {
        VStack {
            TextField("Username", text: $username)
                .focused($focusedField, equals: .username)
            SecureField("Password", text: $password)
                .focused($focusedField, equals: .password)
            Button("Login") { submit() }
        }
        .onAppear { focusedField = .username }
    }
}

// AttributedString in Text
var attributed = AttributedString("Hello, World!")
attributed[attributed.startIndex..<attributed.endIndex].foregroundColor = .red
Text(attributed)

// .badge on TabView tab
TabView {
    InboxView()
        .tabItem { Label("Inbox", systemImage: "envelope") }
        .badge(unreadCount)   // Int badge

    SettingsView()
        .tabItem { Label("Settings", systemImage: "gear") }
        .badge("New")         // String badge
}

// TimelineView — updates on schedule
TimelineView(.periodic(from: .now, by: 1.0)) { context in
    ClockFaceView(date: context.date)
}

// Canvas — 2D drawing
Canvas { context, size in
    context.fill(
        Path(ellipseIn: CGRect(origin: .zero, size: size)),
        with: .color(.blue)
    )
}
```

## Before / After

### Async image loading

```swift
// BEFORE — manual URLSession + @State
struct AvatarView: View {
    let url: URL
    @State private var image: UIImage?

    var body: some View {
        Group {
            if let image {
                Image(uiImage: image).resizable()
            } else {
                ProgressView()
            }
        }
        .onAppear {
            URLSession.shared.dataTask(with: url) { data, _, _ in
                if let data { DispatchQueue.main.async { image = UIImage(data: data) } }
            }.resume()
        }
    }
}

// AFTER — AsyncImage (iOS 15+)
AsyncImage(url: url) { phase in
    switch phase {
    case .success(let image): image.resizable().aspectRatio(contentMode: .fill)
    case .failure:            Image(systemName: "photo").foregroundColor(.secondary)
    default:                  ProgressView()
    }
}
```

### Pull-to-refresh

```swift
// BEFORE — UIRefreshControl bridged via UIViewRepresentable
struct RefreshableScrollView<Content: View>: UIViewControllerRepresentable {
    var onRefresh: () -> Void
    var content: Content
    // … dozens of lines of boilerplate coordinator / UIScrollView setup …
}

// AFTER — .refreshable (iOS 15+)
List(items) { item in
    Text(item.title)
}
.refreshable {
    await viewModel.reload()   // auto-dismisses spinner when await returns
}
```

### Search UI

```swift
// BEFORE — UISearchController bridged into SwiftUI
struct SearchableList: UIViewControllerRepresentable {
    @Binding var query: String
    // … UINavigationController + UISearchController setup …
}

// AFTER — .searchable (iOS 15+)
NavigationView {
    List(filteredItems) { item in Text(item.name) }
        .searchable(text: $searchText, prompt: "Search items")
        .navigationTitle("Items")
}
```

## Migration steps

1. Replace `URLSession` + `@State` image loading with `AsyncImage`
2. Replace `UISearchBar` / `UISearchController` bridging with `.searchable`
3. Replace `UIRefreshControl` bridging with `.refreshable { await … }`
4. Replace `onAppear { Task { } }` patterns with `.task { }`; cancellation is automatic
5. Replace `UISwipeActionsConfiguration` bridging with `.swipeActions`
6. Replace `NSAttributedString` bridging in `UILabel`/`UITextView` with Swift `AttributedString` + `Text`

## Compatibility notes

- All APIs require iOS 15+, macOS 12+
- `.task(id:)` re-runs the async body when the `id` value changes
- `FocusState` works with `TextField`, `TextEditor`, and custom views using `.focusable()`
- `Canvas` is not accessibility-native — add `accessibilityLabel` or use overlay `Text` for VoiceOver
