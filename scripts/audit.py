#!/usr/bin/env python3
"""
wwdc-skills structural integrity audit.

Checks:
  1a. INDEX.md completeness — all referenced files exist; no duplicate session IDs
  1b. Frontmatter schema — required fields present and valid values
  1c. Content shape compliance — required section headers per declared shape
  1d. Session ID format — flags IDs that won't match the router regex

Usage:
    python3 scripts/audit.py [--fail-on-issues]

Exit codes:
    0  All checks passed
    1  Issues found (only when --fail-on-issues is set)
"""

import os
import re
import sys
import argparse

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(REPO_ROOT, "references", "INDEX.md")

REQUIRED_FIELDS = {"framework", "title", "session", "year", "applies_to",
                   "status", "superseded_by", "shape", "related"}
VALID_STATUS = {"current", "reference-only", "deprecated"}
VALID_SHAPE = {"code-first", "guide-first", "migration"}

SHAPE_SECTIONS = {
    "code-first": ["## Quick start", "## Key APIs", "## Common patterns", "## Gotchas"],
    "guide-first": ["## What changed", "## Mental model"],  # partial match OK
    "migration": ["## What's new", "## Migration steps", "## Compatibility notes"],
}

# Router regex: WWDC\d{2}-\d{3,6}
ROUTER_REGEX = re.compile(r"WWDC\d{2}-\d{3,6}")
SESSION_ID_REGEX = re.compile(r"WWDC(\d{2})-(\d+)")


def read_frontmatter(path):
    """Return dict of frontmatter fields from a .md file."""
    fields = {}
    try:
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return None, None

    if not lines or lines[0].strip() != "---":
        return fields, "".join(lines)

    in_front = False
    body_start = 0
    for i, line in enumerate(lines):
        if i == 0:
            in_front = True
            continue
        if in_front and line.strip() == "---":
            body_start = i + 1
            break
        if in_front:
            match = re.match(r"^(\w[\w_-]*):\s*(.*)", line)
            if match:
                fields[match.group(1)] = match.group(2).strip()

    body = "".join(lines[body_start:])
    return fields, body


def check_index(issues):
    """1a: INDEX.md completeness."""
    if not os.path.exists(INDEX_PATH):
        issues.append("CRITICAL: references/INDEX.md not found")
        return []

    session_ids_seen = {}
    referenced_files = []

    with open(INDEX_PATH, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            if not line.startswith("|"):
                continue
            cols = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cols) < 2:
                continue
            file_col = cols[0]
            if file_col in ("File", "---", ""):
                continue
            if file_col == "—":
                continue

            abs_path = os.path.join(REPO_ROOT, "references", file_col)
            referenced_files.append((file_col, abs_path))

            # Extract session ID from file path
            m = SESSION_ID_REGEX.search(file_col)
            if m:
                sid = f"WWDC{m.group(1)}-{m.group(2)}"
                if sid in session_ids_seen:
                    issues.append(f"1a DUPLICATE session ID {sid}: "
                                  f"{session_ids_seen[sid]} and {file_col}")
                else:
                    session_ids_seen[sid] = file_col

    for file_col, abs_path in referenced_files:
        if not os.path.exists(abs_path):
            issues.append(f"1a MISSING FILE: references/{file_col} (referenced in INDEX.md)")

    return referenced_files


def check_session_files(issues):
    """1b + 1c + 1d: schema, shape compliance, ID format."""
    year_dirs = [str(y) for y in range(2017, 2026)]
    session_files = []

    for year in year_dirs:
        year_path = os.path.join(REPO_ROOT, "references", year)
        if not os.path.isdir(year_path):
            continue
        for fname in sorted(os.listdir(year_path)):
            if fname.startswith("WWDC") and fname.endswith(".md"):
                session_files.append(os.path.join(year_path, fname))

    for path in session_files:
        rel = os.path.relpath(path, REPO_ROOT)
        fields, body = read_frontmatter(path)

        if fields is None:
            issues.append(f"1b READ ERROR: {rel}")
            continue

        # 1b: required fields
        for field in REQUIRED_FIELDS:
            if field not in fields:
                issues.append(f"1b MISSING FIELD `{field}`: {rel}")

        status = fields.get("status", "")
        if status and status not in VALID_STATUS:
            issues.append(f"1b INVALID status `{status}`: {rel}")

        shape = fields.get("shape", "")
        if shape and shape not in VALID_SHAPE:
            issues.append(f"1b INVALID shape `{shape}`: {rel}")

        # session field vs filename match
        session_field = fields.get("session", "")
        fname_base = os.path.basename(path)
        if session_field and not fname_base.startswith(session_field + "-"):
            # filename might just start with the session ID
            if session_field not in fname_base:
                issues.append(f"1b SESSION MISMATCH: frontmatter `{session_field}` "
                               f"vs filename `{fname_base}`: {rel}")

        # 1c: shape compliance
        if shape in SHAPE_SECTIONS and body:
            for required_section in SHAPE_SECTIONS[shape]:
                # Partial match: "## What changed" matches "## What changed and why"
                if not any(required_section.lower() in line.lower()
                           for line in body.splitlines()):
                    issues.append(f"1c MISSING SECTION `{required_section}` "
                                  f"(shape={shape}): {rel}")

        # 1d: session ID router compatibility
        if session_field:
            if not ROUTER_REGEX.fullmatch(session_field):
                issues.append(f"1d ROUTER DEAD ZONE — `{session_field}` won't match "
                               f"router regex WWDC\\d{{2}}-\\d{{3,5}}: {rel}")

    return session_files


def main():
    parser = argparse.ArgumentParser(description="wwdc-skills audit")
    parser.add_argument("--fail-on-issues", action="store_true",
                        help="Exit with code 1 if any issues found")
    args = parser.parse_args()

    issues = []

    print("=== wwdc-skills Structural Integrity Audit ===\n")

    print("Check 1a: INDEX.md completeness...")
    referenced = check_index(issues)
    print(f"  Checked {len(referenced)} referenced files\n")

    print("Check 1b/1c/1d: Session files (schema, shape, router)...")
    session_files = check_session_files(issues)
    print(f"  Checked {len(session_files)} session files\n")

    if not issues:
        print("✅ All checks passed — no issues found.")
        return 0

    # Group by check prefix
    by_check = {}
    for issue in issues:
        prefix = issue.split()[0] + " " + issue.split()[1] if len(issue.split()) > 1 else issue[:5]
        key = issue[:2]
        by_check.setdefault(key, []).append(issue)

    print(f"❌ {len(issues)} issue(s) found:\n")
    for key in sorted(by_check):
        for issue in by_check[key]:
            print(f"  {issue}")

    if args.fail_on_issues:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
