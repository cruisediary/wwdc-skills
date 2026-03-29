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

**Migration mode** — check this first. Triggers if the query contains "migrate", "convert", "from X to Y", or explicitly names two APIs/frameworks as source and target:
- Same framework, different years (e.g., "migrate SwiftData 2023 → 2024"): load `references/{source-year}/{framework}.md` AND `references/canonical/{framework}.md`
- Different frameworks (e.g., "migrate from Combine to async/await"): load `references/canonical/{source-framework}.md` AND `references/canonical/{target-framework}.md`
- If the source file doesn't exist in the repo: load only the canonical target file and explain the current approach
- In migration mode: always produce a before/after diff response, ignoring the loaded file's `shape` field

**Year/session mode** — triggers if the query names a specific WWDC year or session ID (e.g., "WWDC23", "WWDC21-10132"):
Load `references/{year}/{framework}.md`

**Current API mode** — default for all other queries:
Load `references/canonical/{framework}.md`. If multiple INDEX.md rows match the same framework, always prefer the canonical file over year-stamped files.

**Step 3: Handle not-found**
If no matching framework is found in INDEX.md, respond exactly:
> "This session or framework isn't covered yet in wwdc-skills."
Do not attempt to answer from general knowledge.

**Step 4: Apply status behavior**
Check the `status` field in the loaded file's YAML frontmatter:
- `current` → answer directly
- `reference-only` → answer fully, then append a **Modern alternative** section pointing to the file listed in `related`
- `deprecated` → briefly acknowledge what was asked, then say: "This API has been superseded — see [superseded_by path] for the current approach."

**Step 5: Structure the response**
Use the `shape` field to structure your response (migration mode always overrides to before/after diff):
- `code-first` → Quick start example → Key APIs table → Common patterns → Gotchas
- `guide-first` → What changed and why → Mental model → Usage example → Adopting this pattern (if present in the file)
- `migration` → What's new → Before / After → Migration steps → Compatibility notes
- Migration mode override → Before / After → Migration steps → Compatibility notes

Produce a **conversational answer** using the reference file as source material. Do not dump the file verbatim.
