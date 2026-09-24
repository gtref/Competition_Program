#!/usr/bin/env python3
import re
import sys
import fnmatch
import subprocess
from pathlib import Path

def extract_changed_files(patch_path):
    """Extract changed file paths from a git patch."""
    changed = []
    with open(patch_path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("+++ b/"):
                changed.append(line.strip()[6:])
    return changed

def find_repo_root():
    """Find the git repository root using git rev-parse."""
    try:
        root = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True
        ).strip()
        return Path(root)
    except subprocess.CalledProcessError:
        print("⚠️ Not inside a git repository.")
        sys.exit(1)

def parse_maintainers(maintainers_path):
    """Parse MAINTAINERS.md file into structured sections."""
    sections = []
    current = {"name": None, "emails": [], "lists": [], "files": []}
    with open(maintainers_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if re.match(r"^[A-Z0-9 _-]+$", line):
                if current["name"]:
                    sections.append(current)
                current = {"name": line.strip(), "emails": [], "lists": [], "files": []}
            elif line.startswith("M:"):
                current["emails"].append(line[2:].strip())
            elif line.startswith("L:"):
                current["lists"].append(line[2:].strip())
            elif line.startswith("F:"):
                current["files"].append(line[2:].strip())
        sections.append(current)
    return sections

def match_maintainers(changed_files, sections):
    """Find maintainers whose file patterns match changed files."""
    matched = set()
    for section in sections:
        for pattern in section["files"]:
            for f in changed_files:
                if fnmatch.fnmatch(f, pattern) or f.startswith(pattern.rstrip("/")):
                    matched.update(section["emails"])
                    matched.update(section["lists"])
    return matched

def main():
    if len(sys.argv) != 2:
        print("Usage: python who_to_email.py <patchfile>")
        sys.exit(1)

    patch_path = Path(sys.argv[1])
    repo_root = find_repo_root()
    maintainers_path = repo_root / "MAINTAINERS.md"

    if not maintainers_path.exists():
        print(f"⚠️ MAINTAINERS.md not found in {repo_root}")
        sys.exit(1)

    changed_files = extract_changed_files(patch_path)
    sections = parse_maintainers(maintainers_path)
    maintainers = match_maintainers(changed_files, sections)

    print("📄 Changed files:")
    for f in changed_files:
        print("  -", f)

    if maintainers:
        print("\n📧 Email your patch to:")
        for m in sorted(maintainers):
            print("  -", m)
    else:
        print("\n⚠️ No maintainers found for these files.")

if __name__ == "__main__":
    main()
