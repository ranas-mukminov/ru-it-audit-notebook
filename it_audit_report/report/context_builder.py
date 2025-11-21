from dataclasses import asdict
from typing import Dict, List, Optional

from it_audit_report.ai.models import AuditSummary, WorkPlanItem
from it_audit_report.models import ChecklistResult, InventorySummary
from it_audit_report.scoring import prioritize_findings


def build_context(
    inventory_summary: InventorySummary,
    checklist_results: List[ChecklistResult],
    summary: Optional[AuditSummary] = None,
    workplan: Optional[List[WorkPlanItem]] = None,
) -> Dict:
    risks = []
    for result in checklist_results:
        risks.extend(prioritize_findings(result))

    checklists_payload = []
    for result in checklist_results:
        checklists_payload.append(
            {
                "name": result.name,
                "description": result.description,
                "total_score": result.total_score,
                "max_score": result.max_score,
                "controls": [asdict(ctrl) for ctrl in result.controls],
            }
        )

    context = {
        "inventory": asdict(inventory_summary),
        "checklists": checklists_payload,
        "risks": [asdict(r) for r in risks],
        "summary": asdict(summary) if summary else {},
        "workplan": [asdict(item) for item in workplan] if workplan else [],
    }
    return context
