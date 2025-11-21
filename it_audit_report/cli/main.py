import typer

from it_audit_report.cli.commands.build_report import build_report_command
from it_audit_report.cli.commands.export_findings import export_findings_command
from it_audit_report.cli.commands.generate_summary import generate_summary_command
from it_audit_report.cli.commands.run_notebooks import run_notebooks_command

app = typer.Typer(help="ru-it-audit-notebook CLI")


app.command("run-notebooks")(run_notebooks_command)
app.command("build-report")(build_report_command)
app.command("export-findings")(export_findings_command)
app.command("generate-summary")(generate_summary_command)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
