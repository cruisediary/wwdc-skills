---
framework: Core ML
title: "Core ML in Depth"
session: WWDC17-710
year: 2017
applies_to: iOS 11+
status: deprecated
superseded_by: null
shape: code-first
related:
  - 2017/WWDC17-703-introducing-core-ml.md
---

> **Deprecated:** Covers Core ML 1.0 internals and model conversion. The coremltools Python package has evolved significantly since (v3+). Use for background on the original protobuf model spec.

## Quick start

```python
# Model conversion with coremltools 0.x (Python)
import coremltools
from sklearn.linear_model import LogisticRegression
sklearn_model = LogisticRegression()
coreml_model = coremltools.converters.sklearn.convert(
    sklearn_model,
    input_features=['feature1', 'feature2'],
    output_feature_names='label')
coreml_model.save('MyClassifier.mlmodel')
```

## Key APIs

| Type | Role |
|---|---|
| `MLModel` | Runtime inference endpoint; wraps a compiled `.mlmodelc` package |
| `MLModelDescription` | Describes input/output feature names and types |
| Custom layers | Protocol `MLCustomLayer` allows Swift/Obj-C fallback for unsupported ops |
| Model spec | Protobuf schema `CoreML.proto`; defines NeuralNetwork, Pipeline, GLMClassifier etc. |

## Common patterns

**Inspecting model metadata at runtime**

```swift
let model = try MLModel(contentsOf: modelURL)
let desc = model.modelDescription
for (name, feature) in desc.inputDescriptionsByName {
    print("\(name): \(feature.type)")
}
```

**Custom layer fallback**

```swift
class MyCustomLayer: NSObject, MLCustomLayer {
    required init(parameters: [String: Any]) throws { }
    func setWeightData(_ weights: [Data]) throws { }
    func outputShapes(forInputShapes inputShapes: [[NSNumber]]) throws -> [[NSNumber]] {
        return inputShapes
    }
    func evaluate(inputs: [MLMultiArray], outputs: [MLMultiArray]) throws { }
}
```

## Gotchas

- Register custom layers before loading the model: `MLModel.registerCustomLayer(MyCustomLayer.self, forClassName: "MyOp")`.
- The `.mlmodelc` compiled bundle is what ships in the app, not the `.mlmodel` source file.
- For uncertain op support, consult current coremltools docs — supported ops have expanded significantly.
