from it_audit_report import scoring
from it_audit_report.models import Checklist, Control


def build_sample_checklist() -> Checklist:
    controls = [
        Control(
            id="C-1",
            section="general",
            title_ru="Тестовый контроль 1",
            description_ru="boolean ok",
            tags=["test"],
            answer_type="boolean",
            artifacts=[],
            scoring={"weight": 2, "ok": [True], "warning": [False], "critical": []},
        ),
        Control(
            id="C-2",
            section="process",
            title_ru="Тестовый контроль 2",
            description_ru="warning case",
            tags=["test"],
            answer_type="choice",
            artifacts=[],
            scoring={"weight": 3, "ok": ["ok"], "warning": ["partial"], "critical": ["bad"]},
        ),
        Control(
            id="C-3",
            section="docs",
            title_ru="Без ответа",
            description_ru="unknown status",
            tags=["test"],
            answer_type="text",
            artifacts=[],
            scoring={"weight": 1, "ok": ["provided"], "warning": ["draft"], "critical": []},
        ),
    ]
    return Checklist(name="Test checklist", version="0.1", description="demo", controls=controls)


def test_score_checklist_basic():
    checklist = build_sample_checklist()
    answers = {"C-1": True, "C-2": "partial"}

    result = scoring.score_checklist(checklist, answers)

    assert result.total_score == 7  # 2*2 for ok + 3*1 for warning
    assert result.max_score == 12
    status_map = {c.id: c.status for c in result.controls}
    assert status_map["C-1"] == "ok"
    assert status_map["C-2"] == "warning"
    assert status_map["C-3"] == "unknown"


def test_prioritize_findings_orders_by_risk():
    checklist = build_sample_checklist()
    answers = {"C-1": True, "C-2": "bad", "C-3": "draft"}

    result = scoring.score_checklist(checklist, answers)
    findings = scoring.prioritize_findings(result)

    assert findings[0].level in {"critical", "warning"}
    assert findings[0].weight >= findings[-1].weight
