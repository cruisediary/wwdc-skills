# Contributing to wwdc-skills

Thank you for helping keep wwdc-skills accurate and up-to-date.

## What to contribute

- **New session files** — WWDC sessions not yet covered in `references/`
- **API accuracy fixes** — incorrect method names, fabricated types, wrong signatures
- **Canonical updates** — when a framework evolves and the canonical file needs updating
- **Routing improvements** — edge cases in SKILL.md or INDEX.md

## File structure

```
references/
  canonical/          # Always reflects current best practice
  YYYY/               # Per-session files (e.g. 2024/WWDC24-10137-...)
  INDEX.md            # Router index — must stay in sync with files
SKILL.md              # Router logic
scripts/audit.py      # Structural integrity checks
```

## Adding a session file

1. Check `references/INDEX.md` — confirm the session isn't already covered.
2. Create `references/YYYY/WWDC{YY}-{ID}-{slug}.md` using the frontmatter schema:

```yaml
---
framework: FrameworkName
title: "Exact session title from developer.apple.com"
session: WWDC24-10137
year: 2024
applies_to: iOS 18+
status: reference-only        # current | reference-only | deprecated
superseded_by: null           # path to newer file, or null
shape: code-first             # code-first | guide-first | migration
related: []
---
```

3. Choose the right **shape**:
   - `code-first` — Quick start → Key APIs → Common patterns → Gotchas
   - `guide-first` — What changed and why → Mental model → Usage example → Adopting this pattern
   - `migration` — What's new → Before / After → Migration steps → Compatibility notes

4. Add a row to `references/INDEX.md`.

5. Run the audit and confirm it passes:
   ```bash
   python3 scripts/audit.py
   ```

## API accuracy rules

- Only include API names you can verify against Apple documentation or Xcode autocomplete.
- When uncertain, use prose ("see Apple docs for exact API") rather than guessing.
- Never fabricate type names, initializer labels, or method signatures.

## Pull request checklist

- [ ] `python3 scripts/audit.py` passes with no issues
- [ ] Session ID verified against `developer.apple.com/videos`
- [ ] All code examples compile (or are clearly marked as illustrative)
- [ ] INDEX.md row added/updated

## Commit style

```
feat: add WWDC24-10137 SwiftData session file
fix: correct #Index macro placement in WWDC24-10137
docs: update canonical/swiftdata.md for iOS 18
```
