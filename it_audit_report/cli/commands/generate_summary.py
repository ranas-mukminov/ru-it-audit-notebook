from pathlib import Path

import typer


from it_audit_report import config, scoring
from it_audit_report.ai.summary_generator import generate_summary
from it_audit_report.ai.workplan_generator import generate_workplan
from it_audit_report.cli.helpers import load_answers_from_dir, load_checklists
from it_audit_report.inventory.collectors import load_inventory
from it_audit_report.models import InventorySummary


def generate_summary_command(
    answers_dir: Path = typer.Option(Path("examples/inputs"), exists=True, file_okay=False, help="Directory with answers"),
    inventory: Path = typer.Option(None, exists=True, dir_okay=False, file_okay=True, help="Inventory optional"),
    out: Path = typer.Option(None, help="Optional path to save markdown"),
    profile: str = typer.Option(config.DEFAULT_PROFILE, help="Scoring profile"),
) -> None:
    answers = load_answers_from_dir(answers_dir)
    checklists = load_checklists()
    checklist_results = [scoring.score_checklist(cl, answers) for cl in checklists]

    inv_summary = (
        load_inventory(inventory)
        if inventory
        else InventorySummary(total_nodes=0, os_distribution={}, environment_distribution={}, gaps=[])
    )

    summary = generate_summary(checklist_results, inv_summary, profile=profile)
    workplan = generate_workplan(checklist_results)

    lines = [
        f"# Executive summary ({profile})",
        summary.overview,
        "",
        "## Топ-риски",
    ]
    for risk in summary.top_risks:
        lines.append(f"- {risk['title']}: {risk['description']} ({risk['priority']})")
    lines.append("\n## План работ")
    for item in workplan:
        lines.append(f"- [{item.priority}] {item.area}: {item.action} (effort: {item.effort})")
    content = "\n".join(lines)

    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
        typer.echo(f"Summary saved to {out}")
    else:
        typer.echo(content)
