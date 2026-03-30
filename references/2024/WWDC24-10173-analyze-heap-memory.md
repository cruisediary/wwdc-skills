---
framework: Instruments
title: "Analyze heap memory"
session: WWDC24-10173
year: 2024
applies_to: iOS 18+
status: reference-only
superseded_by: null
shape: guide-first
related: []
---

## What changed and why

Xcode 16's memory tools get tighter integration between Instruments' Allocations template and the in-IDE Memory Graph Debugger. The session teaches a systematic workflow: capture an allocation backtrace to find the call site that created a leaking object, then pivot to the memory graph to see the reference chain keeping it alive. MetricKit's `MXMemoryMetric` rounds out the picture with field data from real devices.

## Mental model

Think of heap analysis as a three-layer funnel:

1. **Instruments / Allocations** — "what was allocated and when?" Shows allocation count, persistent bytes, and backtraces per call site.
2. **Memory Graph Debugger** — "why is it still alive?" Renders the live object graph; follow reference edges back to a root (e.g., a strong capture in a closure or a retain cycle).
3. **MetricKit** — "how bad is it in the field?" `MXMemoryMetric` delivers peak/average memory from real user sessions via `MXMetricPayload`.

## Usage

```swift
// --- MetricKit: receive memory metrics from the field ---
import MetricKit

class MetricsSubscriber: NSObject, MXMetricManagerSubscriber {
    func didReceive(_ payloads: [MXMetricPayload]) {
        for payload in payloads {
            guard let mem = payload.memoryMetrics else { continue }
            let peak = mem.peakMemoryUsage          // Measurement<UnitInformationStorage>
            let avg  = mem.averageSuspendedMemory   // Measurement<UnitInformationStorage>
            print("Peak: \(peak), Avg suspended: \(avg)")
        }
    }
}

// Register once at app launch:
MXMetricManager.shared.add(MetricsSubscriber())
```

```
Instruments workflow:
1. Product > Profile (⌘I) → choose Allocations template
2. Run the scenario that triggers growth
3. Click "Mark Generation" before and after the suspect action
4. Inspect the generation delta: look for unexpected persistent objects
5. Click a row → Backtrace pane → double-click frame to jump to source
```

```
Memory Graph Debugger workflow (Xcode):
1. Run app → Debug > Memory Graph Debugger (debug bar memory icon)
2. Xcode pauses execution and captures the live heap
3. Left panel lists object types; select a leaking instance
4. Center canvas shows reference graph — follow the arrows to the retaining root
5. Fix: break the cycle (weak/unowned capture, manual nil-out) then re-profile
```

## Adopting this pattern

- Instrument early and often — don't wait for an OOM report; set a generation mark before and after each major user flow
- Pair Instruments data (backtrace = where allocated) with the Memory Graph (reference chain = why alive) — one without the other leaves half the story
- Add `MXMetricManager` subscriber in production builds to catch field regressions before they surface in reviews
