from pathlib import Path
from typing import Dict, List

import yaml

from it_audit_report import config
from it_audit_report.checklist_loader import load_all_checklists
from it_audit_report.models import Checklist


def load_answers_from_dir(answers_dir: Path) -> Dict[str, object]:
    answers: Dict[str, object] = {}
    for path in answers_dir.glob("*.y*ml"):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        answers.update(data.get("answers", {}))
    return answers


def load_checklists(directory: Path = config.CHECKLIST_DIR) -> List[Checklist]:
    return load_all_checklists(directory)
