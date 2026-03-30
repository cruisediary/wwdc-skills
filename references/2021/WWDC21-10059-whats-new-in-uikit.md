---
framework: UIKit
title: "What's new in UIKit"
session: WWDC21-10059
year: 2021
applies_to: iOS 15+
status: reference-only
superseded_by: null
shape: migration
related: []
---

# What's New in UIKit (WWDC21)

iOS 15 UIKit additions: `UIButton.Configuration`, `UISheetPresentationController`, `UIListContentConfiguration`, updated cell content configuration, and SF Symbols 3.

## What's new

- **`UIButton.Configuration`** — unified button styling replacing `UIButton` property soup
- **`UISheetPresentationController`** — bottom sheets with detents (`medium`, `large`)
- **`UIListContentConfiguration`** — replaces `textLabel`/`detailTextLabel`/`imageView` on `UITableViewCell`
- **Cell content configurations** — `UIBackgroundConfiguration` for cell backgrounds
- **`UIBarButtonItem` with `primaryAction`** — simpler action wiring for bar buttons
- **`UIBarAppearance` improvements** — scroll-edge appearance now configurable on all bar types
- **SF Symbols 3** — multicolor and hierarchical rendering modes
- **`UIFocusEffect`** — custom focus feedback for iPad pointer and keyboard navigation
- **`UIWindowScene.activationConditions`** — multi-window routing on iPad

## Key APIs

### UIButton.Configuration

```swift
// Plain configuration
var config = UIButton.Configuration.plain()
config.title = "Tap me"
config.image = UIImage(systemName: "star")
config.imagePlacement = .trailing
config.imagePadding = 8
let button = UIButton(configuration: config)

// Filled configuration with custom corner style
var filledConfig = UIButton.Configuration.filled()
filledConfig.title = "Submit"
filledConfig.baseBackgroundColor = .systemBlue
filledConfig.cornerStyle = .capsule
let filledButton = UIButton(configuration: filledConfig)

// Tinted configuration
var tintedConfig = UIButton.Configuration.tinted()
tintedConfig.title = "Cancel"

// Dynamic title and loading state
button.configurationUpdateHandler = { button in
    var config = button.configuration ?? UIButton.Configuration.plain()
    config.showsActivityIndicator = button.isSelected
    config.title = button.isSelected ? "Loading…" : "Load"
    button.configuration = config
}
```

### UISheetPresentationController

```swift
let vc = DetailViewController()
if let sheet = vc.sheetPresentationController {
    sheet.detents = [.medium(), .large()]
    sheet.prefersGrabberVisible = true
    sheet.prefersScrollingExpandsWhenScrolledToEdge = false
    sheet.largestUndimmedDetentIdentifier = .medium
}
present(vc, animated: true)

// Animating detent changes
sheet.animateChanges {
    sheet.selectedDetentIdentifier = .large
}
```

### UIListContentConfiguration

```swift
// Modern cell configuration — replaces cell.textLabel!.text
var content = UIListContentConfiguration.cell()
content.text = item.title
content.secondaryText = item.subtitle
content.image = UIImage(systemName: item.iconName)
content.imageProperties.tintColor = .systemBlue
cell.contentConfiguration = content

// Background configuration
var background = UIBackgroundConfiguration.listGroupedCell()
background.backgroundColor = .systemBackground
background.strokeColor = .separator
background.strokeWidth = 0.5
cell.backgroundConfiguration = background
```

### SF Symbols 3 rendering modes

```swift
// Hierarchical rendering
let config = UIImage.SymbolConfiguration(hierarchicalColor: .systemBlue)
imageView.image = UIImage(systemName: "person.3.fill", withConfiguration: config)

// Palette rendering (explicit colors per layer)
let paletteConfig = UIImage.SymbolConfiguration(
    paletteColors: [.systemBlue, .systemGreen, .systemRed]
)
imageView.image = UIImage(systemName: "person.3.fill", withConfiguration: paletteConfig)

// Multicolor (system-defined colors)
let multiConfig = UIImage.SymbolConfiguration.preferringMulticolor()
imageView.preferredSymbolConfiguration = multiConfig
```

## Migration steps

1. Replace `button.setTitle`, `button.setImage`, `button.backgroundColor` with `UIButton.Configuration`
2. Replace custom bottom-sheet view controllers with `UISheetPresentationController` detents
3. Replace `cell.textLabel!.text`, `cell.detailTextLabel!.text`, `cell.imageView!.image` with `UIListContentConfiguration`
4. Update `UIBarAppearance` setup to configure `scrollEdgeAppearance` separately from `standardAppearance`

## Compatibility notes

- `UIButton.Configuration` requires iOS 15+; older `setTitle`/`setImage` APIs still work
- `UISheetPresentationController` requires iOS 15+; custom sheet implementations needed for iOS 13/14
- `UIListContentConfiguration` requires iOS 14+; `textLabel`/`detailTextLabel` are deprecated from iOS 14
- SF Symbols 3 hierarchical/palette rendering requires iOS 15+
