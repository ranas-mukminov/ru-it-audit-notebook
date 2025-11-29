from typing import List, Optional

from it_audit_report.ai.ai_provider import AIProvider, NoopAIProvider
from it_audit_report.ai.models import AuditSummary
from it_audit_report.models import ChecklistResult, InventorySummary


def _collect_top_risks(checklist_results: List[ChecklistResult], limit: int = 7) -> List[dict]:
    risks: List[dict] = []
    for result in checklist_results:
        for control in result.controls:
            if control.status == "ok":
                continue
            risks.append(
                {
                    "title": control.title,
                    "description": f"Статус: {control.status}, ответ: {control.answer}",
                    "priority": control.status,
                }
            )
            if len(risks) >= limit:
                return risks
    return risks


def generate_summary(
    checklist_results: List[ChecklistResult],
    inventory_summary: InventorySummary,
    profile: str = "smb_default",
    provider: Optional[AIProvider] = None,
) -> AuditSummary:
    provider = provider or NoopAIProvider()

    total_score = sum(result.total_score for result in checklist_results)
    max_score = sum(result.max_score for result in checklist_results) or 1.0

    top_risks = _collect_top_risks(checklist_results)
    director_focus = [
        f"Профиль оценки: {profile}",
        f"Общий балл: {int(total_score)}/{int(max_score)}",
        f"Количество рисков: {len(top_risks)}",
    ]
    overview_prompt = (
        f"Оцени результаты аудита: профиль {profile}, балл {total_score}/{max_score}, "
        f"узлов {inventory_summary.total_nodes}."
    )
    overview = provider.complete(overview_prompt)

    return AuditSummary(
        overview=overview,
        top_risks=top_risks,
        profile=profile,
        score=total_score,
        max_score=max_score,
        director_focus=director_focus,
    )
