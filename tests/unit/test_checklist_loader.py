import textwrap
from pathlib import Path

import pytest

from it_audit_report.checklist_loader import load_checklist


def test_load_valid_checklist():
    path = Path("checklists/pdn_152fz.yaml")
    checklist = load_checklist(path)

    assert checklist.name == "Персональные данные / 152-ФЗ"
    assert checklist.version == "0.1"
    assert len(checklist.controls) >= 5
    first = checklist.controls[0]
    assert first.id == "PDN-001"
    assert first.answer_type in {"boolean", "choice", "scale"}


def test_missing_required_fields(tmp_path: Path):
    bad_yaml = textwrap.dedent(
        """
        metadata:
          name: "Bad checklist"
          version: "0.1"
          description: "invalid"
        controls:
          - id: BAD-1
            title_ru: "Нет обязательных полей"
        """
    )
    path = tmp_path / "bad.yaml"
    path.write_text(bad_yaml, encoding="utf-8")

    with pytest.raises(ValueError) as excinfo:
        load_checklist(path)

    assert "missing" in str(excinfo.value)
