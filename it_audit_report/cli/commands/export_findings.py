import json
from pathlib import Path
from typing import Literal

import typer
import yaml

from it_audit_report.cli.helpers import load_answers_from_dir, load_checklists
from it_audit_report.scoring import prioritize_findings, score_checklist


def export_findings_command(
    answers_dir: Path = typer.Option(Path("examples/inputs"), exists=True, file_okay=False, help="Directory with answers"),
    out: Path = typer.Option(Path(".artifacts/findings.json"), help="Destination file"),
    fmt: Literal["json", "yaml"] = typer.Option("json", help="Output format"),
) -> None:
    answers = load_answers_from_dir(answers_dir)
    findings = []
    for checklist in load_checklists():
        result = score_checklist(checklist, answers)
        findings.extend([f.__dict__ for f in prioritize_findings(result)])

    out.parent.mkdir(parents=True, exist_ok=True)
    if fmt == "json":
        out.write_text(json.dumps(findings, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        out.write_text(yaml.safe_dump(findings, allow_unicode=True), encoding="utf-8")
    typer.echo(f"Findings exported to {out}")
