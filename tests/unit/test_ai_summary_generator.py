from it_audit_report.ai.ai_provider import NoopAIProvider
from it_audit_report.ai.summary_generator import generate_summary
from it_audit_report.ai.workplan_generator import generate_workplan
from it_audit_report.models import ChecklistResult, ControlResult, InventorySummary


def test_generate_summary_and_workplan_from_context():
    controls = [
        ControlResult(
            id="R-1",
            title="Critical gap",
            answer="no",
            status="critical",
            weight=3,
            score=0,
            section="backup",
        ),
        ControlResult(
            id="R-2",
            title="Minor gap",
            answer="partial",
            status="warning",
            weight=1,
            score=1,
            section="pdn",
        ),
    ]
    checklist_result = ChecklistResult(
        name="Example",
        description="",
        controls=controls,
        total_score=1,
        max_score=10,
        profile="smb_default",
    )
    inventory = InventorySummary(
        total_nodes=2,
        os_distribution={"Ubuntu": 2},
        environment_distribution={"prod": 2},
        gaps=[],
    )

    summary = generate_summary(
        checklist_results=[checklist_result],
        inventory_summary=inventory,
        profile="smb_default",
        provider=NoopAIProvider(),
    )
    assert summary.overview
    assert summary.profile == "smb_default"
    assert summary.top_risks

    workplan = generate_workplan([checklist_result])
    assert any(item.priority in {"high", "medium"} for item in workplan)
