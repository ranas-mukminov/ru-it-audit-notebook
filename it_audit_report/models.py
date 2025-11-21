from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Control:
    id: str
    section: str
    title_ru: str
    description_ru: str
    tags: List[str]
    answer_type: str
    artifacts: List[str]
    scoring: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Checklist:
    name: str
    version: str
    description: str
    controls: List[Control]


@dataclass
class ControlResult:
    id: str
    title: str
    answer: Any
    status: str
    weight: float
    score: float
    section: str


@dataclass
class ChecklistResult:
    name: str
    description: str
    controls: List[ControlResult]
    total_score: float
    max_score: float
    profile: Optional[str] = None


@dataclass
class InventorySummary:
    total_nodes: int
    os_distribution: Dict[str, int]
    environment_distribution: Dict[str, int]
    gaps: List[str] = field(default_factory=list)


@dataclass
class RiskRecord:
    id: str
    title: str
    level: str
    recommendation: str
    weight: float = 1.0
