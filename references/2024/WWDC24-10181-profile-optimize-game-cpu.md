---
framework: Instruments
title: "Profile and optimize your game's CPU performance"
session: WWDC24-10181
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: guide-first
related: []
---

## What changed and why

Xcode 16 adds the Game Performance template to Instruments, consolidating CPU counters, GPU frame capture, and thread-scheduling data into one view. Previously, optimizing game CPU work required jumping between the Time Profiler, GPU Frame Debugger, and manual `os_signpost` logging. The new template surfaces hardware CPU performance counters (cache misses, branch mispredictions) alongside your signpost intervals, making it straightforward to correlate code-level work with silicon-level cost.

## Mental model

Think of game performance as a pipeline with three measurable stages per frame:

1. **CPU simulation** — update physics, AI, game state (measure with `os_signpost` intervals per system)
2. **CPU render encoding** — build Metal command buffers (visible in CPU counters: cache pressure, IPC)
3. **GPU execution** — the encoded work on the GPU (visualized in the GPU Frame Capture timeline)

Each stage has a budget proportional to your target frame rate (e.g., 8.3 ms per stage at 60 fps). Instruments lets you see exactly where the budget is spent or exceeded.

## Usage

```swift
import os.signpost

// Create a log handle once (reuse across frames)
let perfLog = OSLog(subsystem: "com.example.mygame", category: "GameLoop")

func update(deltaTime: Float) {
    // Mark the entire game-loop tick
    os_signpost(.begin, log: perfLog, name: "GameLoopTick")
    defer { os_signpost(.end, log: perfLog, name: "GameLoopTick") }

    // Mark individual systems for fine-grained breakdown
    os_signpost(.begin, log: perfLog, name: "PhysicsUpdate")
    physicsWorld.step(deltaTime: deltaTime)
    os_signpost(.end, log: perfLog, name: "PhysicsUpdate")

    os_signpost(.begin, log: perfLog, name: "AIUpdate")
    agentSystem.update(deltaTime: deltaTime)
    os_signpost(.end, log: perfLog, name: "AIUpdate")
}
```

```
Instruments — Game Performance template workflow:
1. Product > Profile (⌘I) → Game Performance template
2. Press Record; play through the bottleneck scenario
3. In the CPU Counters track: look for spikes in L1/L2 cache misses or branch misprediction rate
4. Correlate with your os_signpost intervals in the "Points of Interest" track
5. In the GPU timeline: identify frames where GPU work overruns the frame deadline
6. Double-click a hot frame → GPU Frame Debugger for draw-call-level analysis
```

## Adopting this pattern

- Add `os_signpost` begin/end pairs around every distinct game system (physics, AI, animation, render encoding) — these become your instrumentation points in the Game Performance template
- Profile on device, not simulator — CPU counters reflect actual A-series/M-series silicon characteristics
- Treat cache-miss spikes as a data-layout problem: consider AoS → SoA (Array of Structs → Struct of Arrays) transformations for hot paths
- Keep GPU frame capture sessions short (10–30 seconds) to avoid large `.gputrace` files
