---
framework: Core ML
title: "Introducing Core ML"
session: WWDC17-703
year: 2017
applies_to: iOS 11+
status: deprecated
superseded_by: null
shape: code-first
related: []
---

> **Deprecated:** Core ML 1.0 as introduced in iOS 11. The `.mlmodel` format and `MLModel` class remain available, but the workflow has evolved significantly through Core ML 3+. Use this for historical context on the original API surface.

## Quick start

```swift
import CoreML
import Vision

let model = try! MobileNet(configuration: MLModelConfiguration())
let input = MobileNetInput(image: pixelBuffer)
let output = try! model.prediction(input: input)
print(output.classLabel)
```

## Key APIs

| Type | Role |
|---|---|
| `MLModel` | Base class for all compiled Core ML models |
| `MLModelConfiguration` | Controls compute units (`cpu`, `cpuAndGPU`, `all`) |
| `MLMultiArray` | Multi-dimensional numeric array; maps to model input/output tensors |
| `MLFeatureValue` | Typed wrapper (double, string, image, multiArray, sequence) |
| `MLFeatureProvider` | Protocol for typed model input/output |
| `VNCoreMLModel` | Wraps `MLModel` for use with the Vision framework |
| `VNCoreMLRequest` | Vision request that runs a Core ML image classifier |

## Common patterns

**Vision + Core ML image classification**

```swift
import Vision

guard let model = try? VNCoreMLModel(for: MobileNet().model) else { return }
let request = VNCoreMLRequest(model: model) { request, error in
    guard let results = request.results as? [VNClassificationObservation] else { return }
    let top = results.first!
    print("\(top.identifier): \(top.confidence)")
}
request.imageCropAndScaleOption = .centerCrop
let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
try? handler.perform([request])
```

## Gotchas

- `.mlmodel` files must be added to the Xcode target to trigger automatic code generation.
- `MLMultiArray` indices are row-major; consult the model spec for shape interpretation.
- Core ML 1.0 runs inference only; on-device training was added in Core ML 3 (iOS 13).
- Compute unit selection defaults to `all` (ANE + GPU + CPU). Benchmark before overriding.
