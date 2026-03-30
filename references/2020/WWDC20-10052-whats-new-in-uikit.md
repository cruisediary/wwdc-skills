---
framework: UIKit
title: "What's new in UIKit"
session: WWDC20-10052
year: 2020
applies_to: iOS 14+
status: reference-only
superseded_by: null
shape: migration
related: []
---

# What's new in UIKit — WWDC20 (iOS 14)

iOS 14 modernized UICollectionView with modern cell registration, list layouts, and compositional layouts improvements, plus new controls and an updated color picker.

## What's new

- `UICollectionView.CellRegistration` — type-safe cell registration without `dequeueReusableCell(withReuseIdentifier:)`
- `UICollectionViewDiffableDataSource` cell provider updated to use `CellRegistration`
- `UIListContentConfiguration` — value-type list cell content configuration replacing direct property mutation on `UITableViewCell`
- `UICollectionLayoutListConfiguration` — list-style `UICollectionView` layout (replaces `UITableView` for new code)
- `UIContentConfiguration` protocol — composable cell content and background configurations
- `UIColorPickerViewController` — system color picker sheet
- `UIDatePicker` inline and compact styles (`.inline`, `.compact`)
- `UIMenu` / `UIAction` for context menus and pull-down buttons (expanded from iOS 13)
- `UIBarButtonItem` with `menu` property for pull-down menus
- `UIButton.Configuration` — declarative button styling (note: formally introduced in iOS 15, but button menu work began in iOS 14)
- Sidebar `UISplitViewController` with `.doubleColumn` / `.tripleColumn` styles (iPadOS 14)

## Before / After

**Cell registration (before — string-based):**
```swift
collectionView.register(MyCell.self, forCellWithReuseIdentifier: "MyCell")

// In data source:
let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "MyCell", for: indexPath) as! MyCell
cell.configure(with: item)
return cell
```

**Cell registration (after — type-safe):**
```swift
let registration = UICollectionView.CellRegistration<MyCell, Item> { cell, indexPath, item in
    cell.configure(with: item)
}

let dataSource = UICollectionViewDiffableDataSource<Section, Item>(collectionView: collectionView) {
    collectionView, indexPath, item in
    collectionView.dequeueConfiguredReusableCell(using: registration, for: indexPath, item: item)
}
```

**List content configuration (before — direct mutation):**
```swift
// UITableViewCell direct property access
cell.textLabel?.text = item.title
cell.detailTextLabel?.text = item.subtitle
cell.imageView?.image = UIImage(systemName: item.iconName)
```

**List content configuration (after — UIListContentConfiguration):**
```swift
var content = UIListContentConfiguration.cell()
content.text = item.title
content.secondaryText = item.subtitle
content.image = UIImage(systemName: item.iconName)
cell.contentConfiguration = content
```

**Collection view as a list (replacing UITableView):**
```swift
var config = UICollectionLayoutListConfiguration(appearance: .insetGrouped)
config.trailingSwipeActionsConfigurationProvider = { indexPath in
    let delete = UIContextualAction(style: .destructive, title: "Delete") { _, _, completion in
        // handle delete
        completion(true)
    }
    return UISwipeActionsConfiguration(actions: [delete])
}
let layout = UICollectionViewCompositionalLayout.list(using: config)
let collectionView = UICollectionView(frame: .zero, collectionViewLayout: layout)
```

**Color picker:**
```swift
let picker = UIColorPickerViewController()
picker.selectedColor = currentColor
picker.delegate = self
present(picker, animated: true)

// Delegate
func colorPickerViewControllerDidSelectColor(_ viewController: UIColorPickerViewController) {
    let color = viewController.selectedColor
    // apply color
}
```

**Inline date picker:**
```swift
let datePicker = UIDatePicker()
datePicker.preferredDatePickerStyle = .inline  // or .compact
datePicker.datePickerMode = .date
```

## Migration steps

1. Replace `register(_:forCellWithReuseIdentifier:)` + `dequeueReusableCell` with `CellRegistration` + `dequeueConfiguredReusableCell`
2. Replace `UITableView` list UIs with `UICollectionView` + `UICollectionLayoutListConfiguration` for new code
3. Replace direct `textLabel`/`detailTextLabel`/`imageView` mutation with `UIListContentConfiguration`
4. Replace custom color pickers with `UIColorPickerViewController`
5. Replace wheel-only `UIDatePicker` with `.compact` or `.inline` style where appropriate

## Compatibility notes

- `UICollectionView.CellRegistration` requires iOS 14+
- `UIListContentConfiguration` requires iOS 14+
- `UIColorPickerViewController` requires iOS 14+
- `UIDatePicker` compact and inline styles require iOS 14+
- `UICollectionLayoutListConfiguration` requires iOS 14+
- `UITableView` is not deprecated but `UICollectionView` list layout is the preferred path for new list UIs
