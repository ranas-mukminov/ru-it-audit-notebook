from typing import List

from it_audit_report.ai.models import WorkPlanItem
from it_audit_report.models import ChecklistResult

PRIORITY_MAP = {"critical": "high", "warning": "medium", "unknown": "medium", "ok": "low"}


def _effort_from_weight(weight: float) -> str:
    if weight >= 3:
        return "L"
    if weight >= 2:
        return "M"
    return "S"


def generate_workplan(checklist_results: List[ChecklistResult]) -> List[WorkPlanItem]:
    items: List[WorkPlanItem] = []
    for result in checklist_results:
        for control in result.controls:
            if control.status == "ok":
                continue
            items.append(
                WorkPlanItem(
                    action=f"Устранить: {control.title}",
                    area=control.section,
                    priority=PRIORITY_MAP.get(control.status, "medium"),
                    effort=_effort_from_weight(control.weight),
                )
            )

    items.sort(key=lambda i: {"high": 3, "medium": 2, "low": 1}.get(i.priority, 1), reverse=True)
    return items
