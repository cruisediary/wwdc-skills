---
framework: Metal
title: "Metal 2 Optimization and Debugging"
session: WWDC17-607
year: 2017
applies_to: iOS 11+
status: reference-only
superseded_by: null
shape: guide-first
related: []
---

> **Reference-only (iOS 11+):** Covers Metal Frame Debugger and GPU profiling tools introduced with Metal 2 in Xcode 9. The tooling has evolved substantially in Xcode 12+ (Shader Debugger, Memory Viewer, Acceleration Structure Viewer), but the workflow concepts — capture, inspect, profile — remain the same.

## What changed and why

Metal 2 and Xcode 9 brought a fully integrated Metal Frame Debugger, replacing the separate GPU Frame Capture workflow. New in this release:

- **Metal Pipeline Statistics** — direct access to GPU compiler metrics (instruction counts, register usage, occupancy) without external tools.
- **GPU Counter Profiling** — per-stage hardware performance counter data exposed through Xcode's GPU report.
- **Metal System Trace** — dedicated VR and multi-GPU rendering timeline support added to Instruments.
- **Dependency Viewer** — visual graph of render pass resource dependencies to identify hazards and redundant barriers.

## Mental model

Metal 2 optimization works in three layers:

1. **Correctness** — use the Frame Debugger to capture a frame, verify resource state, and step through draw calls to isolate rendering bugs.
2. **Pipeline efficiency** — use Pipeline Statistics to ensure shaders compile efficiently (low register pressure, high occupancy).
3. **System throughput** — use GPU Counter Profiling and Metal System Trace to identify CPU/GPU synchronization stalls and memory bandwidth bottlenecks.

## Usage

**Triggering a frame capture programmatically**

```swift
import Metal

let device = MTLCreateSystemDefaultDevice()!
let captureManager = MTLCaptureManager.shared()
let captureDescriptor = MTLCaptureDescriptor()
captureDescriptor.captureObject = device

do {
    try captureManager.startCapture(with: captureDescriptor)
    // encode and commit command buffers
    captureManager.stopCapture()
} catch {
    print("Capture failed:", error)
}
```

**Checking pipeline statistics at compile time**

Pipeline statistics are surfaced in Xcode's Metal frame capture UI — select a pipeline state object in the Resource inspector to see per-stage instruction counts and register usage reported by the GPU compiler.

**Instruments — Metal System Trace**

Launch the Metal System Trace template in Instruments to record:
- GPU command buffer scheduling timeline
- CPU/GPU synchronization points
- Per-queue workload distribution (useful for VR multi-pass rendering)

## Adopting this pattern

1. Add a debug capture trigger (button or programmatic call) during development builds.
2. Review Pipeline Statistics for any shader with > 128 registers — high register pressure reduces occupancy.
3. Use the Dependency Viewer to check for unintentional texture barriers between render passes; merge passes where possible.
4. Profile with GPU Counters to distinguish ALU-bound vs. memory-bandwidth-bound workloads before optimizing shaders.
5. For VR / multi-view rendering, verify in Metal System Trace that both eyes render within the vsync budget.
