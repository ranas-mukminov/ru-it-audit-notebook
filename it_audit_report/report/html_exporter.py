from pathlib import Path


def export_html(markdown_text: str, output_path: Path) -> Path:
    """Simple HTML export without heavy dependencies."""
    html = "<html><body>\n"
    for line in markdown_text.splitlines():
        if line.startswith("# "):
            html += f"<h1>{line[2:]}</h1>\n"
        elif line.startswith("## "):
            html += f"<h2>{line[3:]}</h2>\n"
        else:
            html += f"<p>{line}</p>\n"
    html += "</body></html>\n"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    return output_path
