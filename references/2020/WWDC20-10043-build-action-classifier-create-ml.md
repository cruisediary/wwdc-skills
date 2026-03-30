---
framework: Create ML
title: "Build an Action Classifier with Create ML"
session: WWDC20-10043
year: 2020
applies_to: macOS 11+
status: reference-only
superseded_by: null
shape: code-first
related:
  - canonical/create-ml.md
---

# Build an Action Classifier with Create ML — WWDC20

Action classifiers recognize human body actions (e.g., jumping, waving) from video using pose estimation. Training uses `MLActionClassifier` in Create ML.

## Quick start

```swift
import CreateML
import Foundation

// 1. Prepare training data — one folder per action label, each containing video files
let trainingDataURL = URL(fileURLWithPath: "/path/to/TrainingVideos")
// Structure:
//   TrainingVideos/
//     jumping/  (video files)
//     waving/   (video files)
//     running/  (video files)

// 2. Configure and train the classifier
let parameters = MLActionClassifier.ModelParameters(
    validation: .split(strategy: .automatic),
    augmentation: [],          // MLActionClassifier.VideoAugmentationOptions
    algorithm: .automatic
)

let classifier = try MLActionClassifier(
    trainingData: .labeledDirectories(at: trainingDataURL),
    parameters: parameters
)

// 3. Evaluate
let evaluation = classifier.evaluation(on: .labeledDirectories(at: trainingDataURL))
print("Accuracy: \(evaluation.classificationError)")

// 4. Save the Core ML model
let modelURL = URL(fileURLWithPath: "/path/to/ActionClassifier.mlmodel")
try classifier.write(to: modelURL)
```

## Key APIs

| API | Description |
|---|---|
| `MLActionClassifier` | Trains a body action recognition model from labeled videos |
| `MLActionClassifier.ModelParameters` | Configuration: validation, augmentation, algorithm, prediction window |
| `MLActionClassifier.VideoAugmentationOptions` | Data augmentation options: `.horizontallyFlipped` |
| `MLActionClassifier.DataSource` | `.labeledDirectories(at:)` — one subfolder per action label |
| `MLActionClassifier.ModelParameters.ValidationData` | `.split(strategy:)` or `.dataSource(_:)` |
| `classifier.evaluation(on:)` | Returns `MLClassifierMetrics` with accuracy/confusion matrix |
| `classifier.write(to:)` | Saves the trained `.mlmodel` file |
| `predictionWindowSize` | Number of video frames per prediction window (default: 90 at 30fps = 3s) |

## Common patterns

**Configuring augmentation and window size:**
```swift
var params = MLActionClassifier.ModelParameters()
params.augmentation = [.horizontallyFlipped]
params.predictionWindowSize = 60  // ~2 seconds at 30fps

let classifier = try MLActionClassifier(
    trainingData: .labeledDirectories(at: trainingDataURL),
    parameters: params
)
```

**Async training with progress:**
```swift
let job = try MLActionClassifier.train(
    trainingData: .labeledDirectories(at: trainingDataURL),
    parameters: params
)

// Monitor progress
for try await event in job.result {
    // handle progress updates if API supports AsyncSequence
}
let classifier = try await job.result
```

**Using the model in an app with Vision:**
```swift
import Vision
import CoreML

// Load the compiled model
let model = try MLModel(contentsOf: compiledModelURL)
let vnModel = try VNCoreMLModel(for: model)

// Create request for body pose + action classification
let request = VNCoreMLRequest(model: vnModel) { request, error in
    guard let observations = request.results as? [VNClassificationObservation] else { return }
    let topAction = observations.max(by: { $0.confidence < $1.confidence })
    print("Action: \(topAction?.identifier ?? "unknown")")
}
```

## Gotchas

- Action classifiers require videos with a clearly visible full human body — occlusion or partial bodies reduce accuracy
- The `predictionWindowSize` must match at inference time; the model expects the same frame count it was trained on
- Training is macOS-only (Create ML framework); the resulting `.mlmodel` runs on iOS, macOS, and other Apple platforms
- Video files must be in a format readable by AVFoundation (`.mp4`, `.mov`, `.m4v`)
- Minimum recommended videos per class: ~30–50 clips; more data significantly improves accuracy
- `MLActionClassifier.VideoAugmentationOptions.horizontallyFlipped` doubles effective training data for symmetric actions but can hurt asymmetric actions (e.g., throwing with a specific hand)
- The canonical `create-ml.md` marks this framework as deprecated in favor of the Create ML app and Core ML workflow — use `MLActionClassifier` for programmatic pipelines only
