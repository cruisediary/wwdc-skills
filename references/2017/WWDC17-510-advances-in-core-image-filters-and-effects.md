---
framework: Core Image
title: "Advances in Core Image: Filters and Effects"
session: WWDC17-510
year: 2017
applies_to: iOS 11+
status: reference-only
superseded_by: null
shape: code-first
related: []
---

> **Reference-only (iOS 11+):** Core Image APIs introduced in iOS 11 remain stable. Metal-backed CIKernel is the modern path; the CIFilter API shown here is unchanged in iOS 18.

## Quick start

```swift
import CoreImage

let context = CIContext()
guard let image = CIImage(image: uiImage) else { return }
let blur = CIFilter(name: "CIGaussianBlur")!
blur.setValue(image, forKey: kCIInputImageKey)
blur.setValue(10.0, forKey: kCIInputRadiusKey)
if let output = blur.outputImage,
   let cgImage = context.createCGImage(output, from: image.extent) {
    let result = UIImage(cgImage: cgImage)
    _ = result
}
```

## Key APIs

| Type | Role |
|---|---|
| `CIFilter` | Named filter with key-value inputs; 200+ built-in filters |
| `CIImage` | Immutable image recipe; not rendered until a `CIContext` renders it |
| `CIContext` | Rendering engine; GPU-backed via Metal by default in iOS 11+ |
| `CIKernel` | Custom kernel in Core Image Kernel Language or Metal Shading Language |
| `CIColorKernel` | Per-pixel color transformation kernel |
| `CIWarpKernel` | Coordinate remapping kernel |

## Common patterns

**Chain filters**

```swift
let sepia = CIFilter(name: "CISepiaTone", parameters: [
    kCIInputImageKey: image,
    kCIInputIntensityKey: 0.8
])!
let vignette = CIFilter(name: "CIVignette", parameters: [
    kCIInputImageKey: sepia.outputImage!,
    kCIInputIntensityKey: 1.0,
    kCIInputRadiusKey: 2.0
])!
```

**Metal-backed custom kernel (iOS 11+)**

```swift
let url = Bundle.main.url(forResource: "MyKernels", withExtension: "ci.metallib")!
let data = try! Data(contentsOf: url)
let kernel = try! CIColorKernel(functionName: "colorInvert", fromMetalLibraryData: data)
let output = kernel.apply(extent: image.extent, arguments: [image])
```

## Gotchas

- `CIImage` is lazy — chain filters without intermediate renders.
- Reuse `CIContext` instances; creating one per frame is expensive.
- Use `CIFilter.filterNames(inCategory: kCICategoryBuiltIn)` to enumerate available filters at runtime.
- Metal-backed kernels require `.ci.metal` source compiled into `.ci.metallib`.
