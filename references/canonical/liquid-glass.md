---
framework: Liquid Glass
status: current
applies_to: iOS 26+
shape: guide-first
superseded_by: null
history:
  - year: 2025
    file: 2025/liquid-glass.md
    summary: "Initial introduction — Glass material, specular highlights, dynamic blur"
---

## What changed and why

iOS 26 introduces Liquid Glass, a new design language where UI surfaces behave like physical glass — refractive, specular, and depth-aware. It replaces the translucent material system (`.ultraThinMaterial`, `.regularMaterial`, etc.) as the preferred treatment for floating UI elements like toolbars, sheets, and cards.

## Mental model

UI elements feel like real glass — they refract the content behind them, catch specular highlights from virtual light sources, and blur dynamically based on depth. The tint you apply colors the glass rather than masking it, so the underlying content remains visible through the element.

```
Old model:  frosted overlay — flat blur + opacity
New model:  glass object — refraction + specular + depth blur
```

**Key APIs:**

| API | Purpose |
|---|---|
| `.glassEffect()` | Apply Liquid Glass material to any view |
| `GlassEffectContainer` | Group multiple glass views sharing one glass slab |
| `.tint(Color)` | Color the glass without fully opaquing it |

## Usage

**Applying glass to a card view:**

```swift
struct GlassCard: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("Session Title")
                .font(.headline)
            Text("10:00 AM · Hall A")
                .font(.subheadline)
                .foregroundStyle(.secondary)
        }
        .padding()
        .glassEffect()
    }
}
```

**Tinting the glass:**

```swift
Text("Featured")
    .padding(.horizontal, 12)
    .padding(.vertical, 6)
    .glassEffect()
    .tint(.blue)
```

**Grouping multiple glass elements:**

```swift
GlassEffectContainer {
    HStack {
        Button("Cancel") { }
            .glassEffect()
        Button("Confirm") { }
            .glassEffect()
    }
}
```

## Adopting this pattern

Replace existing material modifiers with `.glassEffect()` on floating elements (cards, overlays, toolbars). System components (sheets, navigation bars) adopt Liquid Glass automatically on iOS 26 — no code change needed there. Test on a real device; the Simulator does not fully render glass refraction and specular effects.
