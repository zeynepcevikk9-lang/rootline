"""Deterministic connector used for local development and planner tests."""

from .contracts import Capability, Evidence, ToolResult
from .tool_registry import ToolRegistry


def build_mock_registry() -> ToolRegistry:
    definitions = (
        ("kubernetes.get_workload_status", "Read workload status from Kubernetes."),
        ("kubernetes.get_recent_events", "Read recent Kubernetes events."),
        ("argocd.get_application_status", "Read Argo CD application status."),
        ("git.get_recent_changes", "Read recent Git changes."),
        ("prometheus.query_range", "Read a metric range from Prometheus."),
        ("loki.query_logs", "Read relevant logs from Loki."),
        ("tls.inspect_certificate", "Inspect a TLS certificate."),
        ("dns.resolve", "Resolve a DNS name."),
        ("backup.get_last_run", "Read the latest backup result."),
        ("backup.verify_restore_readiness", "Read restore readiness evidence."),
        ("system.get_disk_usage", "Read filesystem usage."),
        ("system.find_large_paths", "Find large paths without deleting anything."),
    )
    registry = ToolRegistry(
        Capability(name, description) for name, description in definitions
    )
    for capability in registry.list():
        registry.register_handler(capability.name, _mock_handler(capability.name))
    return registry


def _mock_handler(name: str):
    def handler(_params: dict[str, object]) -> ToolResult:
        evidence = Evidence(
            source=f"mock://{name}",
            summary=f"Deterministic sample result for {name}.",
            data={"status": "sample", "capability": name},
        )
        return ToolResult(
            capability=name,
            success=True,
            output={"status": "sample", "message": "Replace with a real connector."},
            evidence=(evidence,),
        )

    return handler
