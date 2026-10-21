from typing import Any

import pytest

from rootline.kubernetes import KubernetesConnector
from rootline.tool_registry import ToolRegistry


class FakeKubernetesClient:
    def __init__(self, responses: dict[str, dict[str, Any]]) -> None:
        self.responses = responses
        self.paths: list[str] = []

    def get(self, path: str):
        self.paths.append(path)
        return self.responses[path]


def test_connector_registers_read_only_capabilities() -> None:
    client = FakeKubernetesClient(
        {
            "/api/v1/namespaces/prod/pods": {"items": [{"metadata": {"name": "api-1"}}]},
            "/apis/apps/v1/namespaces/prod/deployments": {"items": []},
        }
    )
    registry = ToolRegistry()
    KubernetesConnector(client).register(registry)

    result = registry.execute("kubernetes.get_workload_status", {"namespace": "prod"})

    assert result.success is True
    assert result.output["pods"][0]["metadata"]["name"] == "api-1"
    assert all(step.kind.value == "read" for step in registry.list())


def test_connector_rejects_path_injection_in_namespace() -> None:
    client = FakeKubernetesClient({})
    connector = KubernetesConnector(client)

    with pytest.raises(ValueError):
        connector.get_recent_events({"namespace": "prod/../../secrets"})
