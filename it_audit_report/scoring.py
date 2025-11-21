from typing import Dict, Iterable, List, Tuple

from .models import Checklist, ChecklistResult, Control, ControlResult, RiskRecord

STATUS_SCORES: Dict[str, int] = {"ok": 2, "warning": 1, "critical": 0, "unknown": 0}
STATUS_ORDER: Dict[str, int] = {"critical": 3, "warning": 2, "unknown": 1, "ok": 0}


def _match_answer(answer, expected_values: Iterable) -> bool:
    for candidate in expected_values:
        if isinstance(candidate, bool):
            if answer is candidate:
                return True
        else:
            if str(answer).lower() == str(candidate).lower():
                return True
    return False


def evaluate_status(control: Control, answer) -> str:
    scoring = control.scoring or {}
    if _match_answer(answer, scoring.get("ok", [])):
        return "ok"
    if _match_answer(answer, scoring.get("warning", [])):
        return "warning"
    if _match_answer(answer, scoring.get("critical", [])):
        return "critical"
    return "unknown"


def score_control(control: Control, answer) -> Tuple[ControlResult, float]:
    weight = float(control.scoring.get("weight", 1))
    status = evaluate_status(control, answer)
    score = weight * STATUS_SCORES.get(status, 0)
    result = ControlResult(
        id=control.id,
        title=control.title_ru,
        answer=answer,
        status=status,
        weight=weight,
        score=score,
        section=control.section,
    )
    max_score = weight * STATUS_SCORES["ok"]
    return result, max_score


def score_checklist(checklist: Checklist, answers: Dict[str, object]) -> ChecklistResult:
    control_results: List[ControlResult] = []
    total_score = 0.0
    max_score = 0.0

    for control in checklist.controls:
        answer = answers.get(control.id)
        result, control_max = score_control(control, answer)
        control_results.append(result)
        total_score += result.score
        max_score += control_max

    return ChecklistResult(
        name=checklist.name,
        description=checklist.description,
        controls=control_results,
        total_score=total_score,
        max_score=max_score,
        profile=None,
    )


def prioritize_findings(checklist_result: ChecklistResult) -> List[RiskRecord]:
    findings: List[RiskRecord] = []
    for control in checklist_result.controls:
        if control.status == "ok":
            continue
        findings.append(
            RiskRecord(
                id=control.id,
                title=control.title,
                level=control.status,
                recommendation=f"Усилить контроль для {control.title}",
                weight=control.weight,
            )
        )

    findings.sort(key=lambda r: (STATUS_ORDER.get(r.level, 0), r.weight), reverse=True)
    return findings
