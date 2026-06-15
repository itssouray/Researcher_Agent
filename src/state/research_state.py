from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    id: int
    description: str

    status: str = "pending"
    result: Optional[str] = None


@dataclass
class Finding:
    task_id: int

    source: str
    page: int

    content: str
    score: float


@dataclass
class Reflection:
    passed: bool

    feedback: str


@dataclass
class ResearchState:
    """
    Central source of truth for the entire research workflow.
    """

    # User Goal
    goal: str

    # Planner + Replanner
    tasks: list[Task] = field(default_factory=list)

    # Executor
    findings: list[Finding] = field(default_factory=list)

    # Reflector
    reflections: list[Reflection] = field(default_factory=list)

    # Workflow Control
    replan_count: int = 0
    max_replans: int = 3

    # Report Generator
    final_report: Optional[str] = None