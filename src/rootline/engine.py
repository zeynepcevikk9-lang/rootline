"""Small orchestration facade for the first Rootline vertical slice."""

from .mock_connector import build_mock_registry
from .planner import IntentPlanner, OperationPlan


class RootlineEngine:
    def __init__(self) -> None:
        self.registry = build_mock_registry()
        self.planner = IntentPlanner(self.registry)

    def plan(self, intent: str) -> OperationPlan:
        return self.planner.plan(intent)

    def execute_read_plan(self, plan: OperationPlan):
        if plan.requires_approval:
            raise PermissionError("This plan requires approval before execution.")
        return tuple(
            self.registry.execute(step.capability.name, step.parameters)
            for step in plan.steps
        )
