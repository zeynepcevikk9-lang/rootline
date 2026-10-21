import pytest

from rootline.contracts import Capability, CapabilityKind
from rootline.tool_registry import DuplicateCapabilityError, ToolRegistry


def test_registry_returns_registered_capability() -> None:
    registry = ToolRegistry(
        [Capability("kubernetes.get_pods", "List pods in a namespace")]
    )

    assert registry.get("kubernetes.get_pods").kind is CapabilityKind.READ


def test_registry_rejects_duplicate_capabilities() -> None:
    registry = ToolRegistry()
    capability = Capability("dns.lookup", "Resolve a DNS name")
    registry.register(capability)

    with pytest.raises(DuplicateCapabilityError):
        registry.register(capability)

