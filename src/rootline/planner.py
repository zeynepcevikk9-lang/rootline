"""Deterministic intent planner used before an LLM planner is introduced."""

from dataclasses import dataclass

from .contracts import Capability
from .tool_registry import ToolRegistry


@dataclass(frozen=True)
class PlanStep:
    capability: Capability
    reason: str
    parameters: dict[str, object]


@dataclass(frozen=True)
class OperationPlan:
    intent: str
    summary: str
    steps: tuple[PlanStep, ...]
    requires_approval: bool
    warnings: tuple[str, ...] = ()


class IntentPlanner:
    """Map a small set of operational intents to typed read-only capabilities."""

    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry

    def plan(self, intent: str) -> OperationPlan:
        normalized = intent.casefold()
        if any(word in normalized for word in ("incident", "alarm", "hata", "error", "sorun")):
            return self._incident_plan(intent)
        if any(word in normalized for word in ("certificate", "sertifika", "tls", "domain")):
            return self._expiry_plan(intent)
        if any(word in normalized for word in ("backup", "yedek", "restore")):
            return self._backup_plan(intent)
        if any(word in normalized for word in ("disk", "storage", "volume", "depo")):
            return self._disk_plan(intent)
        return OperationPlan(
            intent=intent,
            summary="No deterministic skill matched this request yet.",
            steps=(),
            requires_approval=False,
            warnings=("Add or enable a skill pack for this intent.",),
        )

    def _steps(self, names: tuple[str, ...], reason: str) -> tuple[PlanStep, ...]:
        return tuple(
            PlanStep(self.registry.get(name), reason, {})
            for name in names
        )

    def _incident_plan(self, intent: str) -> OperationPlan:
        names = (
            "kubernetes.get_workload_status",
            "kubernetes.get_recent_events",
            "argocd.get_application_status",
            "git.get_recent_changes",
            "prometheus.query_range",
            "loki.query_logs",
        )
        return OperationPlan(
            intent=intent,
            summary="Collect workload, change and telemetry evidence before forming a hypothesis.",
            steps=self._steps(names, "Correlate the incident with recent state and changes."),
            requires_approval=False,
        )

    def _expiry_plan(self, intent: str) -> OperationPlan:
        names = ("tls.inspect_certificate", "dns.resolve")
        return OperationPlan(
            intent=intent,
            summary="Inspect certificate validity and DNS resolution without changing the system.",
            steps=self._steps(names, "Validate expiry and the endpoint currently serving the certificate."),
            requires_approval=False,
        )

    def _backup_plan(self, intent: str) -> OperationPlan:
        names = ("backup.get_last_run", "backup.verify_restore_readiness")
        return OperationPlan(
            intent=intent,
            summary="Check backup freshness and whether recovery evidence is available.",
            steps=self._steps(names, "Separate backup existence from recovery readiness."),
            requires_approval=False,
        )

    def _disk_plan(self, intent: str) -> OperationPlan:
        names = ("system.get_disk_usage", "system.find_large_paths")
        return OperationPlan(
            intent=intent,
            summary="Inspect disk pressure and identify candidate paths without deleting anything.",
            steps=self._steps(names, "Produce safe cleanup candidates; no destructive action is included."),
            requires_approval=False,
        )
