---
framework: Create ML
status: deprecated
applies_to: macOS 10.14+
shape: code-first
superseded_by: null
history:
  - year: 2018
    file: 2018/create-ml.md
    summary: "Initial introduction — MLDataTable, image classifiers, NLP"
---

## Quick start

```swift
import CreateML
import Foundation

// Original Playground-based training API (macOS 10.14+)
let trainingData = try MLDataTable(
    contentsOf: URL(fileURLWithPath: "/path/to/training.csv"))

let classifier = try MLClassifier(trainingData: trainingData,
                                   targetColumn: "label")

let metrics = classifier.trainingMetrics
print("Accuracy: \(metrics.classificationError)")

// Save the trained model
try classifier.write(to: URL(fileURLWithPath: "/path/to/MyModel.mlmodel"))
```

> **Deprecated:** The Swift Playground / command-line Create ML API still compiles on macOS 14, but Apple's preferred workflow since WWDC19 is the **Create ML app** (included in Xcode). Use the GUI app or the `CreateMLComponents` framework (macOS 13+) for new projects.

## Key APIs

| API | Purpose |
|---|---|
| `MLDataTable` | Loads tabular training data from CSV or JSON |
| `MLImageClassifier` | Trains an image classification Core ML model |
| `MLTextClassifier` | Trains a text classification model from labeled strings |
| `MLClassifier` | General tabular classifier (decision tree, boosted tree, etc.) |
| `MLRegressor` | Tabular regression model |
| `MLModelMetadata` | Metadata attached to the exported `.mlmodel` |

## Common patterns

```swift
// Image classifier
let imageClassifier = try MLImageClassifier(
    trainingData: .labeledDirectories(
        at: URL(fileURLWithPath: "/path/to/images")))

try imageClassifier.write(to: URL(fileURLWithPath: "/output/Classifier.mlmodel"),
                           metadata: MLModelMetadata(author: "Me",
                                                      shortDescription: "Cat vs Dog",
                                                      version: "1.0"))
```

## Gotchas

- The original `CreateML` module requires a Mac; it cannot run on iOS or in a simulator build step.
- The Swift Playground training workflow is effectively superseded — the **Create ML app** provides drag-and-drop training with live previews and no code required.
- For production pipelines, use `CreateMLComponents` (macOS 13+) which offers composable transformers and async training.
- Exported `.mlmodel` files are consumed by Core ML on all Apple platforms, regardless of which tool created them.
