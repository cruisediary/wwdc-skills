---
framework: Create ML
title: "Compose advanced models with Create ML"
session: WWDC22-10019
year: 2022
applies_to: macOS 13+
status: reference-only
superseded_by: null
shape: guide-first
related:
  - canonical/create-ml.md
---

# Compose advanced models with Create ML — WWDC22

WWDC22 introduced multi-task training in Create ML, allowing a single model to perform several related tasks simultaneously, improving accuracy and reducing model size.

## What changed and why

- **Multi-task training** — train one model that shares learned representations across multiple tasks
- `MLTaskConfiguration` — configure individual tasks within a composite training job
- `MLTrainingSession` — represents an active or completed training run; observe progress asynchronously
- Custom training loops — finer control over epochs, learning rate, and checkpointing
- Improved `MLJob` — async/await friendly training observation

## Mental model

Think of a multi-task Create ML model as a shared feature extractor with multiple specialist heads: the backbone learns general representations from all tasks simultaneously, while each head specializes on its own label set. This joint training tends to produce a more accurate and compact model than training separate single-task models, because the tasks reinforce each other's signal. The `MLTrainingSession` acts as a resumable checkpoint — training is a long-running async process, not a single blocking call.

## Usage example

```swift
import CreateML

// Configure a multi-task training job (conceptual — exact API may vary by task type)
let imageClassifierConfig = MLImageClassifier.ModelParameters(
    validationData: .split(strategy: .automatic),
    maxIterations: 25
)

// Training session with async progress
let job = try MLImageClassifier.train(
    trainingData: trainingData,
    parameters: imageClassifierConfig
)

// Observe training progress (async sequence)
for await snapshot in job.phase {
    print("Phase: \(snapshot), progress: \(job.progress)")
}

let model = try await job.result.get()
try model.write(to: outputURL)
```

## Multi-task pattern

```swift
// A multi-task model shares a common feature extractor.
// Each task head specialises on its own label set.
// This is configured in the Create ML app UI (macOS 13)
// or via MLTaskConfiguration in code:
// - Task A: image classification (object type)
// - Task B: regression (object count)
// Both tasks train together, improving the shared backbone.
```

## MLTrainingSession

```swift
// MLTrainingSession captures checkpoints and metadata
// so training can be resumed after interruption.
let session = MLTrainingSession(
    sessionDirectory: sessionURL
)
// Pass to training call to enable resumable training
```

## Compatibility notes

- Multi-task training requires macOS 13+ and Xcode 14
- Create ML framework is macOS-only; resulting Core ML models deploy to iOS 16+
- The Create ML app on macOS 13 exposes multi-task configuration in its UI
- `MLTrainingSession` replaces manual checkpoint management from earlier releases
