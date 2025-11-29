from pathlib import Path


def export_pdf(markdown_text: str, output_path: Path) -> Path:
    """Lightweight PDF fallback: write plain text with hint."""
    try:
        from nbconvert import PDFExporter
        from nbformat import v4 as nbf

        nb = nbf.new_notebook()
        nb.cells.append(nbf.new_markdown_cell(markdown_text))
        pdf_exporter = PDFExporter()
        body, _ = pdf_exporter.from_notebook_node(nb)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(body)
        return output_path
    except Exception:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("PDF placeholder\n" + markdown_text, encoding="utf-8")
        return output_path
