# ...existing code...
#!/usr/bin/env python3
import subprocess
import ast
from pathlib import Path
from datetime import datetime

README = Path("README.md")
MARKER_START = "<!-- AUTO-GEN-START -->"
MARKER_END = "<!-- AUTO-GEN-END -->"

def git_changed_files():
    # Get files changed in last commit
    out = subprocess.check_output(["git", "show", "--name-status", "--pretty=format:", "HEAD"]).decode().strip()
    files = []
    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            status, fname = parts[0], parts[1]
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

def build_section(changes):
    ts = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    lines = [f"## Auto-generated changelog (updated {ts})", ""]
    if not changes:
        lines.append("_No changes detected in last commit._")
    else:
        for status, fname in changes:
            p = Path(fname)
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
        # Append markers at end
        return readme_text.rstrip() + "\n\n" + MARKER_START + "\n\n" + new_section + "\n\n" + MARKER_END + "\n"

def main():
    changes = git_changed_files()
    new_section = build_section(changes)
    if not README.exists():
        README.write_text("# Project\n\n", encoding="utf-8")
    original = README.read_text(encoding="utf-8")
    updated = replace_section(original, new_section)
    README.write_text(updated, encoding="utf-8")
    print("README.md updated (auto-generated section).")

if __name__ == "__main__":
    main()
# ...existing code...