#!/usr/bin/env python3
import subprocess
import ast
from pathlib import Path
from datetime import datetime
import sys

README = Path("README.md")
MARKER_START = "<!-- AUTO-GEN-START -->"
MARKER_END = "<!-- AUTO-GEN-END -->"

def repo_root():
    out = subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode().strip()
    return Path(out)

def git_changed_files():
    # files changed in last commit (robust)
    out = subprocess.check_output(["git", "--no-pager", "diff-tree", "--name-status", "--no-commit-id", "-r", "HEAD"]).decode().strip()
    files = []
    for line in out.splitlines():
        parts = line.split(maxsplit=1)
        if len(parts) == 2:
            status, fname = parts
            files.append((status, fname))
    return files

def summarize_python(path: Path):
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except Exception:
        return f"- {path}: (could not parse)"
    items = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            doc = ast.get_docstring(node) or ""
            items.append(f"  - class {node.name}: {doc.splitlines()[0] if doc else 'no doc'}")
        elif isinstance(node, ast.FunctionDef):
            doc = ast.get_docstring(node) or ""
            items.append(f"  - def {node.name}(): {doc.splitlines()[0] if doc else 'no doc'}")
    header = f"- {path}"
    if not items:
        return f"{header}"
    return "\n".join([header] + items)

def build_section(changes, root: Path):
    ts = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    lines = [f"## Auto-generated changelog (updated {ts})", ""]
    if not changes:
        lines.append("_No changes detected in last commit._")
    else:
        for status, fname in changes:
            p = root / fname
            if p.exists() and p.suffix == ".py":
                lines.append(f"- {status} {fname}")
                lines.append(summarize_python(p))
            else:
                lines.append(f"- {status} {fname}")
    return "\n".join(lines)

def replace_section(readme_text, new_section):
    if MARKER_START in readme_text and MARKER_END in readme_text:
        before, rest = readme_text.split(MARKER_START, 1)
        _, after = rest.split(MARKER_END, 1)
        return before + MARKER_START + "\n\n" + new_section + "\n\n" + MARKER_END + after
    else:
        return readme_text.rstrip() + "\n\n" + MARKER_START + "\n\n" + new_section + "\n\n" + MARKER_END + "\n"

def main(amend=False):
    root = repo_root()
    # run from repo root to resolve paths reliably
    README_path = root / README
    changes = git_changed_files()
    new_section = build_section(changes, root)
    if not README_path.exists():
        README_path.write_text("# Project\n\n", encoding="utf-8")
    original = README_path.read_text(encoding="utf-8")
    updated = replace_section(original, new_section)
    README_path.write_text(updated, encoding="utf-8")
    print("README.md updated (auto-generated section).")
    if amend:
        # add README and amend last commit so README is included
        try:
            subprocess.check_call(["git", "add", str(README_path)], cwd=str(root))
            subprocess.check_call(["git", "commit", "--amend", "--no-edit"], cwd=str(root))
            print("README.md added to last commit (amended).")
        except subprocess.CalledProcessError:
            print("Failed to amend commit with README.", file=sys.stderr)

if __name__ == "__main__":
    amend_flag = "--amend" in sys.argv
    main(amend=amend_flag)