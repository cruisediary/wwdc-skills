---
framework: Create ML
session: WWDC18-703
year: 2018
applies_to: macOS 10.14+
status: deprecated
superseded_by: canonical/create-ml.md
shape: migration
related:
  - canonical/create-ml.md
---

## What's new

- **First introduction of Create ML** — train machine learning models entirely in Swift, on-device, without Python or a server.
- **Swift Playground workflow** — drag training data into a Playground, write a few lines of Swift, and export a `.mlmodel` ready for Core ML.
- **MLImageClassifier** — train image classifiers from labeled photo directories; transfer learning from built-in feature extractors.
- **MLTextClassifier** — train NLP classification models (e.g., sentiment, topic) from labeled strings.
- **MLDataTable** — load tabular CSV/JSON data and train regression or classification models.
- Small model sizes — transfer learning produces compact `.mlmodel` files (often < 1 MB) instead of full neural networks.

## Before / After

**Before Create ML — import a Python-trained model**

```swift
// Workflow: train in Python (Keras/scikit-learn) → convert with coremltools → import .mlmodel
// No on-device or Swift training; model iteration required a Python environment.
import CoreML

let model = try! MyModel(configuration: MLModelConfiguration())
let prediction = try! model.prediction(input: MyModelInput(image: pixelBuffer))
```

**After Create ML — train in a Swift Playground (WWDC18)**

```swift
import CreateML
import Foundation

// In an Xcode Playground on macOS 10.14
let trainingData = try MLDataTable(
    contentsOf: URL(fileURLWithPath: "/Users/me/data/reviews.csv"))

let classifier = try MLTextClassifier(
    trainingData: trainingData,
    textColumn: "review",
    labelColumn: "sentiment")

print("Training accuracy: \(1 - classifier.trainingMetrics.classificationError)")

try classifier.write(
    to: URL(fileURLWithPath: "/Users/me/SentimentClassifier.mlmodel"))
```

## Migration steps

1. Install Xcode 10+ on macOS 10.14 Mojave.
2. Create a new macOS Playground in Xcode.
3. Prepare training data: image classifiers expect one folder per label; text/tabular classifiers accept CSV or JSON.
4. Import `CreateML` and instantiate the appropriate classifier (`MLImageClassifier`, `MLTextClassifier`, or `MLClassifier`).
5. Call `.write(to:)` to export the `.mlmodel` file.
6. Drag the `.mlmodel` into your Xcode project — Core ML generates a Swift class automatically.

> For new projects, skip this workflow and use the **Create ML app** (Xcode > Open Developer Tool > Create ML) or `CreateMLComponents`. See `canonical/create-ml.md`.

## Compatibility notes

- Requires macOS 10.14 Mojave and Xcode 10; the `CreateML` module is macOS-only.
- Training runs on the Mac CPU/GPU — A-series chip acceleration is not available on Intel Macs.
- Exported `.mlmodel` files work on iOS 12+, watchOS 5+, and tvOS 12+ via Core ML.
- The Playground-based API is still present in macOS 14, but Apple deprecated this workflow in favour of the Create ML app launched at WWDC19.
