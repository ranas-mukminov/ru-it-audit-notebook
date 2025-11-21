from pathlib import Path

import typer

from it_audit_report import config, scoring
from it_audit_report.ai.summary_generator import generate_summary
from it_audit_report.ai.workplan_generator import generate_workplan
from it_audit_report.cli.helpers import load_answers_from_dir, load_checklists
from it_audit_report.inventory.collectors import load_inventory
from it_audit_report.report import context_builder
from it_audit_report.report.html_exporter import export_html
from it_audit_report.report.markdown_renderer import render_markdown
from it_audit_report.report.pdf_exporter import export_pdf


def build_report_command(
    artifacts_dir: Path = typer.Option(Path(".artifacts/notebooks"), help="Executed notebooks directory"),
    inventory: Path = typer.Option(None, exists=True, file_okay=True, dir_okay=False, help="Inventory source"),
    answers_dir: Path = typer.Option(Path("examples/inputs"), exists=True, file_okay=False, help="Checklist answers dir"),
    out_html: Path = typer.Option(..., help="Output HTML path"),
    out_pdf: Path = typer.Option(..., help="Output PDF path"),
    profile: str = typer.Option(config.DEFAULT_PROFILE, help="Scoring profile key"),
) -> None:
    _ = artifacts_dir  # reserved for future use
    answers = load_answers_from_dir(answers_dir)
    checklists = load_checklists()

    checklist_results = [scoring.score_checklist(cl, answers) for cl in checklists]

    if inventory is not None:
        inventory_summary = load_inventory(inventory)
    else:
        from it_audit_report.models import InventorySummary

        inventory_summary = InventorySummary(total_nodes=0, os_distribution={}, environment_distribution={}, gaps=[])

    summary = generate_summary(checklist_results, inventory_summary, profile=profile)
    workplan = generate_workplan(checklist_results)
    ctx = context_builder.build_context(
        inventory_summary=inventory_summary,
        checklist_results=checklist_results,
        summary=summary,
        workplan=workplan,
    )

    exec_template = config.TEMPLATE_DIR / "executive_summary_template.md.j2"
    tech_template = config.TEMPLATE_DIR / "technical_appendix_template.md.j2"

    exec_md = render_markdown(exec_template, ctx)
    tech_md = render_markdown(tech_template, ctx)
    combined = exec_md + "\n\n" + tech_md

    export_html(combined, out_html)
    export_pdf(combined, out_pdf)
    typer.echo(f"Report created: {out_html} and {out_pdf}")
