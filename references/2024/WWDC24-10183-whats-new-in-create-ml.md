---
framework: Create ML
title: "What's new in Create ML"
session: WWDC24-10183
year: 2024
applies_to: macOS 15+
status: reference-only
superseded_by: null
shape: migration
related:
  - canonical/create-ml.md
---

## What's new

- **Tabular forecasting** — new task type for predicting future numeric values from time-series tabular data
- **Body action recognition** — new action classification task that works on full-body poses rather than just upper body
- **Hand pose classification** — new task for recognizing hand gestures from camera or Vision-detected hand landmarks
- `MLModelCollection` — manages groups of related Core ML models for on-device deployment scenarios

> **Note:** Specific API signatures for the new tasks (`MLBodyActionClassifier`, `MLHandPoseClassifier`, tabular forecasting) are not included here to avoid inaccuracy — see the Create ML framework documentation for exact types and parameters.

## Before / After

```swift
// BEFORE (macOS 14): body action classification was part of the action classifier
// with limited skeleton joint coverage
let actionClassifier = try MLActionClassifier(
    trainingData: videoDataSource,
    parameters: MLActionClassifier.ModelParameters()
)

// AFTER (macOS 15): dedicated body action classifier with full-body pose support
// see Apple docs for MLBodyActionClassifier exact initializer signature
```

```swift
// BEFORE: hand pose was handled through Vision framework only at runtime
// No training workflow in Create ML

// AFTER (macOS 15): train hand pose classifiers in Create ML
// see Apple docs for MLHandPoseClassifier exact API
```

## Migration steps

1. For existing action classification models trained on upper-body poses: evaluate whether the new body action classifier improves accuracy for your use case — retrain if needed.
2. For hand gesture recognition previously implemented with Vision + custom logic: consider training a dedicated `MLHandPoseClassifier` model for more reliable classification.
3. If you manage multiple variants of a Core ML model (e.g., one per locale or user tier), explore `MLModelCollection` to unify deployment and update logic.
4. Tabular forecasting is a net-new task — no migration needed; add it where time-series prediction was previously out of scope.

## Compatibility notes

- All new Create ML task types require macOS 15+ for training in Create ML framework.
- Resulting `.mlmodel` files can be deployed to earlier OS versions if Core ML supports the model type — check Core ML compatibility per task.
- `MLModelCollection` on-device model management has separate deployment requirements; see CloudKit and Core ML documentation for the full pipeline.
