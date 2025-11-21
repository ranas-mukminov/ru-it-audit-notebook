import csv
import json
from pathlib import Path
from typing import Dict, List, Tuple

import yaml

from it_audit_report.models import InventorySummary


def _load_records(path: Path) -> List[Dict[str, str]]:
    if path.suffix.lower() == ".csv":
        with path.open(encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            return [row for row in reader]
    if path.suffix.lower() in {".yml", ".yaml"}:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return data.get("servers", []) if isinstance(data, dict) else data
    if path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    raise ValueError(f"Unsupported inventory format: {path.suffix}")


def _tally(records: List[Dict[str, str]], key: str) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for rec in records:
        value = rec.get(key, "unknown") or "unknown"
        counts[value] = counts.get(value, 0) + 1
    return counts


def _find_gaps(records: List[Dict[str, str]]) -> List[str]:
    gaps: List[str] = []
    for rec in records:
        hostname = rec.get("hostname", "unknown")
        if not rec.get("owner"):
            gaps.append(f"Нет владельца для {hostname}")
        os_value = (rec.get("os") or "").lower()
        if any(marker in os_value for marker in ["centos 7", "unknown", "eol"]):
            gaps.append(f"Неподдерживаемая или неизвестная ОС на {hostname}")
        backup = (rec.get("backup") or "").lower()
        if backup in {"no", "absent", ""}:
            gaps.append(f"Нет резервирования для {hostname}")
    return gaps


def load_inventory(path: Path) -> InventorySummary:
    records = _load_records(path)
    total = len(records)
    os_distribution = _tally(records, "os")
    env_distribution = _tally(records, "environment")
    gaps = _find_gaps(records)

    return InventorySummary(
        total_nodes=total,
        os_distribution=os_distribution,
        environment_distribution=env_distribution,
        gaps=gaps,
    )
