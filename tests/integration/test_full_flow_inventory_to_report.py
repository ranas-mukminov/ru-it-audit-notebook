from pathlib import Path

from typer.testing import CliRunner

from it_audit_report.cli.main import app


def test_full_flow_inventory_to_report(tmp_path: Path):
    runner = CliRunner()
    artifacts = tmp_path / ".artifacts" / "notebooks"
    out_html = tmp_path / "report.html"
    out_pdf = tmp_path / "report.pdf"

    run_result = runner.invoke(
        app,
        [
            "run-notebooks",
            "--inventory",
            "examples/inventory/sample_inventory.csv",
            "--answers-dir",
            "examples/inputs",
            "--out-dir",
            str(artifacts),
        ],
    )
    assert run_result.exit_code == 0
    assert (artifacts / "00_inventory_servers.ipynb").exists()

    build_result = runner.invoke(
        app,
        [
            "build-report",
            "--inventory",
            "examples/inventory/sample_inventory.csv",
            "--answers-dir",
            "examples/inputs",
            "--artifacts-dir",
            str(artifacts),
            "--out-html",
            str(out_html),
            "--out-pdf",
            str(out_pdf),
        ],
    )

    assert build_result.exit_code == 0
    assert out_html.exists()
    assert out_pdf.exists()
