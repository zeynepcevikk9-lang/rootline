"""Registry for typed capabilities exposed by infrastructure connectors."""

from collections.abc import Iterable

from .contracts import Capability


class DuplicateCapabilityError(ValueError):
    """Raised when two connectors expose the same capability name."""


class ToolRegistry:
    def __init__(self, capabilities: Iterable[Capability] = ()) -> None:
        self._capabilities: dict[str, Capability] = {}
        for capability in capabilities:
            self.register(capability)

    def register(self, capability: Capability) -> None:
        if capability.name in self._capabilities:
            raise DuplicateCapabilityError(capability.name)
        self._capabilities[capability.name] = capability

    def get(self, name: str) -> Capability:
        try:
            return self._capabilities[name]
        except KeyError as exc:
            raise KeyError(f"Unknown capability: {name}") from exc

    def list(self) -> tuple[Capability, ...]:
        return tuple(self._capabilities.values())

