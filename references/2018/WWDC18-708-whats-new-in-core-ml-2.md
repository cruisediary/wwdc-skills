---
framework: Core ML
title: "What's New in Core ML 2"
session: WWDC18-708
year: 2018
applies_to: iOS 12+
status: deprecated
superseded_by: null
shape: migration
related: []
---

> **Deprecated:** This session covers Core ML 2 (iOS 12 / Xcode 10 era). On-device model update, custom layers, and batch prediction APIs shown here remain valid, but the tooling (coremltools versions, model formats) has evolved substantially through Core ML 3–7. Consult current coremltools and Create ML documentation for new projects.

## What's new

- **Smaller model sizes** — quantization (16-bit and 8-bit weights) and flexible model archives (`mlpackage`) reduce model size; 4× reduction in some cases.
- **Batch prediction** — `MLModel.predictions(from:)` accepts a `MLBatchProvider` for efficient multi-sample inference in a single call.
- **Custom layers** — implement `MLCustomLayer` to run unsupported operations on the Neural Engine / GPU instead of falling back to CPU.
- **Custom models** — implement `MLCustomModel` to wrap non-neural-network models (e.g., a hand-coded algorithm) in the Core ML pipeline.
- **Flexible input shapes** — models can declare flexible or enumerated input sizes, removing the need for separate models per resolution.
- **On-device model update (preview)** — `MLUpdateTask` enables fine-tuning a model on-device with user data (drawing classifier, image personalization).

## Before / After

**Core ML 1 — single prediction**

```swift
let model = try MyModel(configuration: MLModelConfiguration())
let input = MyModelInput(image: pixelBuffer)
let output = try model.prediction(input: input)
```

**Core ML 2 — batch prediction**

```swift
let batchProvider = MLArrayBatchProvider(array: inputs)   // [MyModelInput]
let results = try model.predictions(from: batchProvider)
for i in 0..<results.count {
    let output = results.features(at: i)
    print(output.featureValue(for: "classLabel")?.stringValue ?? "")
}
```

**Custom layer skeleton**

```swift
class MyCustomLayer: NSObject, MLCustomLayer {
    required init(parameters: [String: Any]) throws { /* read params */ }
    func setWeightData(_ weights: [Data]) throws { /* load weights */ }
    func outputShapes(forInputShapes inputShapes: [[NSNumber]]) throws -> [[NSNumber]] { return inputShapes }
    func evaluate(inputs: [MLMultiArray], outputs: [MLMultiArray]) throws { /* compute */ }
}
```

## Migration steps

1. Update coremltools and re-export models to gain quantization and flexible-shape support.
2. Replace repeated single-sample `prediction(input:)` calls in loops with a single `predictions(from:)` batch call for measurable throughput gains.
3. Register custom layers with `MLModelConfiguration.setCustomLayer(_:forClassName:)` before loading the model.
4. For on-device personalization, evaluate `MLUpdateTask` with `MLUpdateProgressHandlers` — still experimental; Core ML 3 stabilized this API.

## Compatibility notes

- `MLBatchProvider` and `MLUpdateTask` require iOS 12+.
- Custom layers (`MLCustomLayer`) require iOS 12+; they run on CPU unless the Neural Engine supports the operation.
- `mlpackage` model archives require Xcode 12+ / Core ML 4+ tooling — older `.mlmodel` format still loads on iOS 12.
