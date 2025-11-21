from pathlib import Path
from typing import List

import yaml

from .models import Checklist, Control

REQUIRED_CONTROL_FIELDS = [
    "id",
    "section",
    "title_ru",
    "description_ru",
    "tags",
    "answer_type",
    "artifacts",
    "scoring",
]


def _validate_control(raw: dict, idx: int) -> None:
    missing = [field for field in REQUIRED_CONTROL_FIELDS if field not in raw]
    if missing:
        raise ValueError(f"Control #{idx} is missing fields: {', '.join(missing)}")
    if "weight" not in raw.get("scoring", {}):
        raise ValueError(f"Control {raw.get('id', idx)} missing scoring.weight")


def load_checklist(path: Path) -> Checklist:
    if not path.exists():
        raise FileNotFoundError(f"Checklist not found: {path}")

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not data or "metadata" not in data or "controls" not in data:
        raise ValueError(f"Checklist {path} missing metadata or controls")

    metadata = data["metadata"]
    for field in ("name", "version", "description"):
        if field not in metadata:
            raise ValueError(f"Checklist {path} missing metadata.{field}")

    controls: List[Control] = []
    for idx, raw_control in enumerate(data["controls"]):
        _validate_control(raw_control, idx)
        controls.append(
            Control(
                id=str(raw_control["id"]),
                section=str(raw_control["section"]),
                title_ru=str(raw_control["title_ru"]),
                description_ru=str(raw_control["description_ru"]),
                tags=list(raw_control["tags"]),
                answer_type=str(raw_control["answer_type"]),
                artifacts=list(raw_control["artifacts"]),
                scoring=dict(raw_control["scoring"]),
            )
        )

    return Checklist(
        name=str(metadata["name"]),
        version=str(metadata["version"]),
        description=str(metadata["description"]),
        controls=controls,
    )


def load_all_checklists(directory: Path) -> List[Checklist]:
    files = sorted(directory.glob("*.yaml"))
    return [load_checklist(path) for path in files if path.name != "scoring_profiles.yaml"]
