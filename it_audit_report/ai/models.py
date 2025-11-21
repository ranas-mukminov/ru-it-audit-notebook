from dataclasses import dataclass, field
from typing import List


@dataclass
class AuditSummary:
    overview: str
    top_risks: List[dict] = field(default_factory=list)
    profile: str = "smb_default"
    score: float = 0.0
    max_score: float = 0.0
    director_focus: List[str] = field(default_factory=list)


@dataclass
class WorkPlanItem:
    action: str
    area: str
    priority: str
    effort: str
