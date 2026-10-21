"""Read-only Kubernetes API connector.

The connector deliberately accepts a small client interface so it can be tested
without a cluster and later reused with different authentication transports.
"""

import json
import ssl
from collections.abc import Mapping
from typing import Any, Protocol
from urllib.parse import quote
from urllib.request import Request, urlopen

from .contracts import Capability, Evidence, ToolResult
from .tool_registry import ToolRegistry


class KubernetesClient(Protocol):
    def get(self, path: str) -> Mapping[str, Any]: ...


class KubernetesApiError(RuntimeError):
    """Raised when the Kubernetes API returns an unusable response."""


class UrllibKubernetesClient:
    """Minimal stdlib Kubernetes API client for read-only requests."""

    def __init__(
        self,
        base_url: str,
        token: str,
        ca_file: str | None = None,
        timeout: float = 10.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout = timeout
        self.context = ssl.create_default_context(cafile=ca_file)

    def get(self, path: str) -> Mapping[str, Any]:
        request = Request(
            f"{self.base_url}/{path.lstrip('/')}",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {self.token}",
            },
            method="GET",
        )
        try:
            with urlopen(request, timeout=self.timeout, context=self.context) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except Exception as exc:  # pragma: no cover - network-specific errors
            raise KubernetesApiError(f"Kubernetes API request failed: {path}") from exc
        if not isinstance(payload, Mapping):
            raise KubernetesApiError(f"Kubernetes API returned a non-object response: {path}")
        return payload


class KubernetesConnector:
    """Expose safe Kubernetes read capabilities to a Rootline registry."""

    capabilities = (
        Capability(
            "kubernetes.get_workload_status",
            "Read pod and deployment status for a namespace.",
        ),
        Capability(
            "kubernetes.get_recent_events",
            "Read recent Kubernetes events for a namespace.",
        ),
    )

    def __init__(self, client: KubernetesClient) -> None:
        self.client = client

    def register(self, registry: ToolRegistry) -> None:
        for capability in self.capabilities:
            registry.register(capability)
        registry.register_handler(
            "kubernetes.get_workload_status", self.get_workload_status
        )
        registry.register_handler(
            "kubernetes.get_recent_events", self.get_recent_events
        )

    def get_workload_status(self, params: Mapping[str, object]) -> ToolResult:
        namespace = _namespace(params)
        namespace_path = quote(namespace, safe="")
        pods = self.client.get(f"/api/v1/namespaces/{namespace_path}/pods")
        deployments = self.client.get(
            f"/apis/apps/v1/namespaces/{namespace_path}/deployments"
        )
        output = {
            "namespace": namespace,
            "pods": _items(pods),
            "deployments": _items(deployments),
        }
        return _result(
            "kubernetes.get_workload_status",
            "Kubernetes workload status collected.",
            output,
        )

    def get_recent_events(self, params: Mapping[str, object]) -> ToolResult:
        namespace = _namespace(params)
        namespace_path = quote(namespace, safe="")
        payload = self.client.get(f"/api/v1/namespaces/{namespace_path}/events")
        return _result(
            "kubernetes.get_recent_events",
            "Kubernetes events collected.",
            {"namespace": namespace, "events": _items(payload)},
        )


def _namespace(params: Mapping[str, object]) -> str:
    namespace = str(params.get("namespace", "default")).strip()
    if not namespace or "/" in namespace:
        raise ValueError("namespace must be a non-empty Kubernetes namespace name")
    return namespace


def _items(payload: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    items = payload.get("items", [])
    return list(items) if isinstance(items, list) else []


def _result(capability: str, summary: str, output: Mapping[str, Any]) -> ToolResult:
    return ToolResult(
        capability=capability,
        success=True,
        output=output,
        evidence=(
            Evidence(
                source=f"kubernetes://{capability}",
                summary=summary,
                data=output,
            ),
        ),
    )
