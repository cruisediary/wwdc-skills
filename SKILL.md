---
name: wwdc-skills
description: Reference skill for Apple WWDC developer sessions (WWDC18–WWDC25). Covers Swift, SwiftUI, SwiftData, Swift Concurrency, UIKit, ARKit, RealityKit, visionOS, Xcode, and all Apple frameworks. Use when asked about Apple APIs, iOS/macOS/visionOS development, WWDC session content, API migration, or any Apple developer topic. Also supports direct session lookup by session ID (e.g. WWDC24-10137) or session title.
---

# WWDC Skills

Reference skill for Apple WWDC sessions (WWDC18–WWDC25). Helps iOS/Swift developers write code using Apple APIs.

## Invocation

Invoke this skill with a query about any Apple framework, API, or WWDC session:
- "How do I use SwiftData?"
- "What was new in WWDC23 for SwiftUI?"
- "Migrate from @Published to @Observable"
- "Show me the Swift Concurrency mental model"
- "WWDC24-10137"

## Routing instructions

Follow these steps exactly when this skill is invoked:

**Step 1: Read the index**
Read `references/INDEX.md`. All file paths in that file are relative to the `references/` directory — prepend `references/` when loading them.

**Step 2: Classify the query** (use this priority order)

**Migration mode** — check this first. Triggers if the query contains "migrate" or "convert", OR if two distinct named Apple APIs/frameworks are explicitly identified as source and target. Do NOT trigger on year-to-year iOS/macOS version comparisons (e.g., "What changed from iOS 16 to iOS 17?") — those are year/session mode queries.
- Same framework, different years (e.g., "migrate SwiftData 2023 → 2024"): load `references/{source-year}/{framework}.md` AND `references/canonical/{framework}.md`
- Different frameworks (e.g., "migrate from Combine to async/await"): load `references/canonical/{source-framework}.md` AND `references/canonical/{target-framework}.md`
- If the source file doesn't exist in the repo: load only the canonical target file and explain the current approach
- In migration mode: always produce a before/after diff response, ignoring the loaded file's `shape` field

**Session ID mode** — check this before Year/session mode. Triggers when the query contains a string matching the pattern `WWDC\d{2}-\d{5}` (e.g., `WWDC24-10179`). Session IDs are handled exclusively here and never fall through to Year/session mode.
- Scan INDEX.md for any row whose `File` path contains that session ID string
- If found: load that file directly
- If not found: respond "This session isn't covered yet in wwdc-skills." Do not fall through to other modes.

**Year/session mode** — triggers if the query names a specific WWDC year (e.g., "WWDC23", "WWDC24") or a named Apple framework alongside a year. Does not apply to bare session IDs — those are handled exclusively by Session ID mode above.
- If a year is identified but no specific framework is named, list the key topics from INDEX.md rows for that year and ask the user which framework to focus on before loading any file.
- If a framework is identified, load `references/{year}/{framework}.md`.

**Session title mode** — triggers when the query contains words that closely match a `Title` column entry in INDEX.md (case-insensitive, partial match):
- Rows where `Title` is `—` (canonical files and framework-level year files) have no title to match against and are excluded from title matching entirely
- Title matching applies only to session files — rows where `Title` is not `—`
- If one titled session row matches: load that session file
- If multiple titled session rows match: prefer the most recent year; if same year and still tied, load both files and answer from both
- If no title matches: fall through to Current API mode

**Current API mode** — default for all other queries:
Load `references/canonical/{framework}.md`. If multiple INDEX.md rows match the same framework, always prefer the canonical file over year-stamped files.

**Step 3: Handle not-found**
If no matching framework is found in INDEX.md, respond exactly:
> "This session or framework isn't covered yet in wwdc-skills."
If INDEX.md has a matching row but the resolved file path does not exist on disk, respond with the same not-found message rather than erroring.
Do not attempt to answer from general knowledge.

**Step 4: Apply status behavior**
Check the `status` field in the loaded file's YAML frontmatter:
- `current` → answer directly
- `reference-only` → answer fully, then append a **Modern alternative** section pointing to the file listed in `related`
- `deprecated` → briefly acknowledge what was asked, then say: "This API has been superseded — see [superseded_by path] for the current approach."

**Step 5: Structure the response**
Use the `shape` field to structure your response:
- `code-first` → Quick start example → Key APIs table → Common patterns → Gotchas
- `guide-first` → What changed and why → Mental model → Usage example → Adopting this pattern (if present in the file)
- `migration` → What's new → Before / After → Migration steps → Compatibility notes

Note on `shape: migration` vs migration mode:
- `shape: migration` is a field that may appear on year-stamped files loaded via year/session mode or current API mode. It indicates the file's content is structured as a migration guide and should be rendered accordingly.
- Migration mode (Step 2) is a router state triggered by the query itself. When the router is in migration mode, always produce a before/after diff response regardless of the loaded file's `shape` field.
- Canonical files (loaded in current API mode) will never have `shape: migration`; the migration mode override only applies when the Step 2 router classified the query as migration mode.

Produce a **conversational answer** using the reference file as source material. Do not dump the file verbatim.
