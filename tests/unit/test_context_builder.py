from it_audit_report.ai.models import AuditSummary, WorkPlanItem
from it_audit_report.models import ChecklistResult, ControlResult, InventorySummary
from it_audit_report.report.context_builder import build_context


def test_build_context_combines_inventory_and_findings():
    inventory = InventorySummary(
        total_nodes=4,
        os_distribution={"Ubuntu": 2, "Debian": 1, "CentOS": 1},
        environment_distribution={"prod": 3, "dev": 1},
        gaps=["Нет владельца сервера srv-legacy-01"],
    )
    controls = [
        ControlResult(
            id="T-1",
            title="Критичный контроль",
            answer="no",
            status="critical",
            weight=2,
            score=0,
            section="general",
        ),
        ControlResult(
            id="T-2",
            title="Предупреждение",
            answer="partial",
            status="warning",
            weight=1,
            score=1,
            section="process",
        ),
    ]
    checklist_result = ChecklistResult(
        name="Demo checklist",
        description="demo",
        controls=controls,
        total_score=1,
        max_score=6,
        profile="smb_default",
    )
    summary = AuditSummary(
        overview="test overview",
        top_risks=[{"title": "risk1", "description": "desc", "priority": "high"}],
        profile="smb_default",
        score=6,
        max_score=10,
        director_focus=["focus"],
    )
    workplan = [WorkPlanItem(action="Fix backup", area="backup", priority="high", effort="M")]

    context = build_context(
        inventory_summary=inventory,
        checklist_results=[checklist_result],
        summary=summary,
        workplan=workplan,
    )

    assert context["inventory"]["total_nodes"] == 4
    assert context["checklists"][0]["name"] == "Demo checklist"
    assert context["risks"][0]["level"] in {"critical", "warning"}
    assert context["summary"]["profile"] == "smb_default"
