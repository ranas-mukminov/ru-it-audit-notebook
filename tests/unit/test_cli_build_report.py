from typer.testing import CliRunner

from it_audit_report.cli.main import app


def test_cli_build_report_generates_files(tmp_path):
    runner = CliRunner()
    out_html = tmp_path / "report.html"
    out_pdf = tmp_path / "report.pdf"

    result = runner.invoke(
        app,
        [
            "build-report",
            "--inventory",
            "examples/inventory/sample_inventory.csv",
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
