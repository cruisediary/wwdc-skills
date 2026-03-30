---
framework: SwiftUI
title: "The SwiftUI cookbook for focus"
session: WWDC23-10157
year: 2023
applies_to: iOS 17+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/swiftui.md
---

# The SwiftUI cookbook for focus (WWDC23)

SwiftUI's focus system lets you programmatically control which view holds keyboard/input focus, react to focus changes, and share focus state across view hierarchies via the environment.

## What changed and why

Focus management has existed since iOS 15, but iOS 17 refines `@FocusState` ergonomics and adds new `@FocusedValue` / `@FocusedBinding` capabilities for propagating focused data up the view tree. The "cookbook" framing means the session is structured as a set of patterns rather than a single feature introduction.

## Mental model

- `@FocusState` is a property wrapper that binds a piece of state to which field is focused. Set it programmatically to move focus; read it to react to user-driven focus changes.
- `.focused(_:equals:)` connects a focusable view to a specific value of a `@FocusState` enum/optional.
- `.focused(_:)` is the Bool-based variant for a single focusable view.
- `@FocusedValue` / `@FocusedObject` let a focused view publish a value into the environment so ancestor views (e.g., toolbars) can read it without explicit data passing.
- `.focusable()` makes a non-interactive view participate in focus (useful for tvOS-style navigation and accessibility).
- `.focusSection()` groups views into a navigable section on tvOS / game controllers.

## Usage

**Moving focus to a specific field on appear:**
```swift
enum Field { case username, password }

struct LoginForm: View {
    @FocusState private var focusedField: Field?
    @State private var username = ""
    @State private var password = ""

    var body: some View {
        VStack {
            TextField("Username", text: $username)
                .focused($focusedField, equals: .username)
            SecureField("Password", text: $password)
                .focused($focusedField, equals: .password)
            Button("Log in") { /* submit */ }
        }
        .onAppear { focusedField = .username }
        .onSubmit {
            if focusedField == .username { focusedField = .password }
            else { /* submit */ }
        }
    }
}
```

**Publishing focused data up the tree with @FocusedValue:**
```swift
// Define the focused value key
struct FocusedNoteKey: FocusedValueKey {
    typealias Value = Note
}

extension FocusedValues {
    var note: Note? {
        get { self[FocusedNoteKey.self] }
        set { self[FocusedNoteKey.self] = newValue }
    }
}

// Set the focused value in a child view
struct NoteEditorView: View {
    let note: Note
    var body: some View {
        TextEditor(text: .constant(note.body))
            .focusedValue(\.note, note)
    }
}

// Read it in a toolbar or menu
struct NoteToolbar: View {
    @FocusedValue(\.note) var focusedNote

    var body: some View {
        Button("Share") {
            guard let note = focusedNote else { return }
            // share note
        }
        .disabled(focusedNote == nil)
    }
}
```

**Bool-based focus for a single field:**
```swift
struct SearchBar: View {
    @FocusState private var isSearchFocused: Bool
    @State private var query = ""

    var body: some View {
        TextField("Search", text: $query)
            .focused($isSearchFocused)
        Button("Focus") { isSearchFocused = true }
    }
}
```

## Adopting this pattern

1. Use `@FocusState` with an enum for multi-field forms; use the Bool variant for single-field scenarios.
2. Drive focus programmatically by assigning to the `@FocusState` variable rather than calling UIKit focus APIs.
3. Use `@FocusedValue` to surface the currently-focused model object to toolbars, menus, or commands without coupling the toolbar to the editor view.
4. Call `.focusable()` on custom controls that should participate in keyboard/game-controller navigation.
5. On tvOS / visionOS, use `.focusSection()` to control how spatial focus navigates between groups of views.
