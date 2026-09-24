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

def extract_email(field):
    """Extract only the raw email address."""
    m = re.search(r"<([^>]+)>", field)
    if m:
        return m.group(1).strip()
    return field.strip()

def parse_maintainers(maintainers_path):
    """Parse MAINTAINERS.md into structured sections."""
    sections = []
    current = {"name": None, "emails": [], "lists": [], "files": []}

    with open(maintainers_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # SECTION HEADER: "# Something"
            if line.startswith("#"):
                name = line.lstrip("#").strip()

                # Save previous section if it had content
                if current["name"] or current["emails"] or current["lists"] or current["files"]:
                    sections.append(current)

                current = {"name": name, "emails": [], "lists": [], "files": []}
                continue

            # M:, L:, F: lines
            if line.startswith("M:"):
                current["emails"].append(extract_email(line[2:].strip()))
            elif line.startswith("L:"):
                current["lists"].append(extract_email(line[2:].strip()))
            elif line.startswith("F:"):
                current["files"].append(line[2:].strip())

    # Append last section
    if current["name"] or current["emails"] or current["lists"] or current["files"]:
        sections.append(current)

    return sections

def match_maintainers(changed_files, sections):
    """Find maintainers whose file patterns match changed files."""
    main = set()
    cc = set()

    for section in sections:
        for pattern in section["files"]:
            is_dir = pattern.endswith("/")

            for f in changed_files:
                matched = False

                if is_dir:
                    if f.startswith(pattern):
                        matched = True
                else:
                    if fnmatch.fnmatch(f, pattern):
                        matched = True

                if matched:
                    main.update(section["emails"])
                    cc.update(section["lists"])

    return main, cc

def main():
    if len(sys.argv) != 2:
        print("Usage: python mailing.py <patchfile>")
        sys.exit(1)

    patch_path = Path(sys.argv[1])
    repo_root = find_repo_root()
    maintainers_path = repo_root / "MAINTAINERS.md"

    if not maintainers_path.exists():
        print(f"⚠️ MAINTAINERS.md not found in {repo_root}")
        sys.exit(1)

    changed_files = extract_changed_files(patch_path)
    sections = parse_maintainers(maintainers_path)
    main_devs, cc_list = match_maintainers(changed_files, sections)

    print("📄 Changed files:")
    for f in changed_files:
        print("  -", f)

    print("\n👤 Main developer(s):")
    if main_devs:
        for m in sorted(main_devs):
            print("  -", m)
    else:
        print("  - None")

    print("\n📨 CC list:")
    if cc_list:
        for c in sorted(cc_list):
            print("  -", c)
    else:
        print("  - None")

    # Build git send-email command
    cmd = ["git", "send-email", str(patch_path)]

    for m in sorted(main_devs):
        cmd += ["--to", m]

    for c in sorted(cc_list):
        cmd += ["--cc", c]

    print("\n💡 Suggested git send-email command:")
    print(" ".join(cmd))

if __name__ == "__main__":
    main()
