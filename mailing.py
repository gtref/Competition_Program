#!/usr/bin/env python3
import re
import sys
import fnmatch
import subprocess
from pathlib import Path

EMAIL_RE = re.compile(r"<([^>]+)>")

# ------------------------------------------------------------
# Utility helpers
# ------------------------------------------------------------

def run(cmd):
    """Run a shell command and return output."""
    return subprocess.check_output(cmd, text=True).strip()

def ask(prompt):
    """Ask user for input."""
    return input(prompt).strip()

def sanitize_filename(name):
    """Make commit title safe as a filename."""
    name = name.strip().replace(" ", "_")
    return re.sub(r"[^A-Za-z0-9._-]", "", name)

def extract_email(field):
    m = EMAIL_RE.search(field)
    return m.group(1).strip() if m else field.strip()

# ------------------------------------------------------------
# Maintainer parsing
# ------------------------------------------------------------

def parse_maintainers(path):
    sections = []
    current = {"name": None, "emails": [], "lists": [], "files": []}

    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue

            if line.startswith("#"):
                if any(current.values()):
                    sections.append(current)
                current = {"name": line.lstrip("#").strip(),
                           "emails": [], "lists": [], "files": []}
                continue

            tag, _, value = line.partition(":")
            value = value.strip()

            if tag == "M":
                current["emails"].append(extract_email(value))
            elif tag == "L":
                current["lists"].append(extract_email(value))
            elif tag == "F":
                current["files"].append(value)

    if any(current.values()):
        sections.append(current)

    return sections

def match_maintainers(changed_files, sections):
    main = set()
    cc = set()

    for section in sections:
        for pattern in section["files"]:
            is_dir = pattern.endswith("/")

            for f in changed_files:
                if (is_dir and f.startswith(pattern)) or fnmatch.fnmatch(f, pattern):
                    main.update(section["emails"])
                    cc.update(section["lists"])
                    break

    return main, cc

# ------------------------------------------------------------
# Patch file extraction
# ------------------------------------------------------------

def extract_changed_files(patch_path):
    changed = []
    with open(patch_path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("+++ b/"):
                changed.append(line[6:].strip())
    return changed

# ------------------------------------------------------------
# Commit message builder
# ------------------------------------------------------------

def build_commit_message(title, body, extra, coauthors):
    lines = [title]

    if body:
        lines.append("")
        lines.append(body)

    if extra:
        lines.append("")
        lines.append(extra)

    if coauthors:
        lines.append("")
        for name, email in coauthors:
            lines.append(f"Co-authored-by: {name} <{email}>")

    return "\n".join(lines)

# ------------------------------------------------------------
# Main workflow
# ------------------------------------------------------------

def main():
    repo_root = Path(run(["git", "rev-parse", "--show-toplevel"]))
    maintainers_path = repo_root / "MAINTAINERS.md"

    print("📌 Adding all files to staging...")
    run(["git", "add", "."])

    print("\n📝 Commit message builder:")
    title = ask("Commit title: ")
    body = ask("Commit body (optional): ")
    extra = ask("Extra message (optional): ")

    coauthors = []
    if ask("Any co-authors? (y/n): ").lower().startswith("y"):
        while True:
            name = ask("Co-author name: ")
            email = ask("Co-author email: ")
            coauthors.append((name, email))

            if not ask("Add another? (y/n): ").lower().startswith("y"):
                break

    commit_msg = build_commit_message(title, body, extra, coauthors)

    print("\n🔧 Writing commit message...")
    msg_path = repo_root / ".git" / "AUTO_COMMIT_MSG"
    msg_path.write_text(commit_msg, encoding="utf-8")

    print("🔧 Committing with -s (Signed-off-by)...")
    run(["git", "commit", "-s", "-F", str(msg_path)])

    # ------------------------------------------------------------
    # Patch generation with commit-title filename
    # ------------------------------------------------------------
    safe_title = sanitize_filename(title)
    patch_name = f"{safe_title}.patch"
    patch_path = repo_root / patch_name

    print(f"\n📦 Generating patch named after commit title: {patch_name}")

    # format-patch normally writes its own filename; we redirect to stdout
    patch_data = run(["git", "format-patch", "-1", "--stdout"])
    patch_path.write_text(patch_data, encoding="utf-8")

    print(f"Patch created: {patch_path}")

    # ------------------------------------------------------------
    # Maintainer matching
    # ------------------------------------------------------------
    print("\n🔍 Extracting changed files...")
    changed_files = extract_changed_files(patch_path)
    for f in changed_files:
        print("  -", f)

    print("\n📚 Parsing MAINTAINERS.md...")
    sections = parse_maintainers(maintainers_path)

    main_devs, cc_list = match_maintainers(changed_files, sections)

    print("\n👤 Main developer(s):")
    print("  - None" if not main_devs else "\n".join(f"  - {m}" for m in sorted(main_devs)))

    print("\n📨 CC list:")
    print("  - None" if not cc_list else "\n".join(f"  - {c}" for c in sorted(cc_list)))

    print("\n💡 Suggested git send-email command:")
    cmd = ["git", "send-email", str(patch_path)]
    for m in sorted(main_devs):
        cmd += ["--to", m]
    for c in sorted(cc_list):
        cmd += ["--cc", c]
    print(" ".join(cmd))

    print("\n✅ Workflow complete.")

if __name__ == "__main__":
    main()
