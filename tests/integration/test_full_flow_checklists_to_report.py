from pathlib import Path

from typer.testing import CliRunner

from it_audit_report.cli.main import app


def test_full_flow_checklists_only(tmp_path: Path):
    runner = CliRunner()
    out_html = tmp_path / "report.html"
    out_pdf = tmp_path / "report.pdf"

    result = runner.invoke(
        app,
        [
            "build-report",
            "--answers-dir",
            "examples/inputs",
            "--out-html",
            str(out_html),
            "--out-pdf",
            str(out_pdf),
        ],
    )

    assert result.exit_code == 0
    assert out_html.exists()
    assert out_pdf.exists()
    assert out_html.read_text(encoding="utf-8")
