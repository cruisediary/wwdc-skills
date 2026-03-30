---
framework: Create ML
title: "Introducing Create ML"
session: WWDC18-703
year: 2018
applies_to: macOS 10.14+
status: deprecated
superseded_by: canonical/create-ml.md
shape: code-first
related:
  - canonical/create-ml.md
---

> **Deprecated:** This session introduces Create ML as a macOS 10.14 Swift Playground / CLI workflow. The drag-and-drop Create ML app and `CreateML` Swift framework covered here have since been superseded by the full Create ML app (macOS 11+) and the current `CreateML` framework. See `canonical/create-ml.md` for current status.

## Quick start

```swift
// Playgrounds / command-line Swift (macOS 10.14)
import CreateML

// Image classifier
let trainingData = URL(fileURLWithPath: "/path/to/training/")
let classifier = try MLImageClassifier(trainingData: .labeledDirectories(at: trainingData))
let metrics = classifier.evaluation(on: .labeledDirectories(at: testDataURL))
print("Accuracy: \(metrics.classificationError)")
try classifier.write(to: URL(fileURLWithPath: "/tmp/MyImageClassifier.mlmodel"))

// Text classifier
let textData = try MLDataTable(contentsOf: trainingCSV)
let textClassifier = try MLTextClassifier(
    trainingData: textData, textColumn: "text", labelColumn: "label")
try textClassifier.write(to: URL(fileURLWithPath: "/tmp/MySentimentClassifier.mlmodel"))
```

## Key APIs

| Type | Role |
|---|---|
| `MLImageClassifier` | Trains an image classification model via transfer learning |
| `MLTextClassifier` | Trains a text classification model (bag-of-words / max-entropy) |
| `MLRegressor` / `MLClassifier` | Tabular regression and classification |
| `MLDataTable` | In-memory tabular data loaded from CSV or JSON |
| `MLModelMetadata` | Author, description, version for the exported `.mlmodel` |

## Common patterns

**Drag-and-drop training (Create ML app)**
- Open `Create ML.app` (ships with Xcode 10 on macOS Mojave).
- Drag a folder of labeled images onto the Image Classifier template.
- Adjust max iterations, augmentation options.
- Click Train — the app exports a `.mlmodel` when complete.

**Exporting with metadata**

```swift
let metadata = MLModelMetadata(
    author: "Your Name",
    shortDescription: "Classifies flowers into 5 categories",
    version: "1.0")
try classifier.write(to: outputURL, metadata: metadata)
```

## Gotchas

- Training in a Swift Playground requires macOS 10.14+ — it will not run on iOS or in Xcode Playgrounds for iOS simulators.
- `MLImageClassifier` uses Vision's feature extractor for transfer learning; the base model is baked in and not swappable in this era.
- Exported `.mlmodel` files target whatever Core ML version ships with the macOS used for training — re-export with newer coremltools for updated deployment targets.
- The Create ML Swift API (`import CreateML`) was macOS-only; iOS training APIs arrived much later.
