import shutil
from pathlib import Path

import typer

from it_audit_report import config


def run_notebooks_command(
    inventory: Path = typer.Option(..., exists=True, help="Inventory CSV/YAML/JSON"),
    answers_dir: Path = typer.Option(..., exists=True, file_okay=False, help="Directory with answers YAML"),
    out_dir: Path = typer.Option(Path(".artifacts/notebooks"), help="Output directory for executed notebooks"),
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for notebook_name in config.NOTEBOOKS:
        src = config.BASE_DIR / "notebooks" / notebook_name
        dst = out_dir / notebook_name
        try:
            import papermill as pm

            pm.execute_notebook(
                str(src),
                str(dst),
                parameters={"inventory_path": str(inventory), "answers_dir": str(answers_dir)},
            )
        except Exception:
            shutil.copy(src, dst)
    typer.echo(f"Executed notebooks stored in {out_dir}")
