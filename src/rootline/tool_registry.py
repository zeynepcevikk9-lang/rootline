"""Registry for typed capabilities exposed by infrastructure connectors."""

from collections.abc import Iterable

from .contracts import Capability, ToolHandler, ToolResult


class DuplicateCapabilityError(ValueError):
    """Raised when two connectors expose the same capability name."""


class ToolRegistry:
    def __init__(self, capabilities: Iterable[Capability] = ()) -> None:
        self._capabilities: dict[str, Capability] = {}
        self._handlers: dict[str, ToolHandler] = {}
        for capability in capabilities:
            self.register(capability)

    def register(self, capability: Capability) -> None:
        if capability.name in self._capabilities:
            raise DuplicateCapabilityError(capability.name)
        self._capabilities[capability.name] = capability

    def register_handler(self, name: str, handler: ToolHandler) -> None:
        self.get(name)
        self._handlers[name] = handler

    def get(self, name: str) -> Capability:
        try:
            return self._capabilities[name]
        except KeyError as exc:
            raise KeyError(f"Unknown capability: {name}") from exc

    def list(self) -> tuple[Capability, ...]:
        return tuple(self._capabilities.values())

    def execute(self, name: str, params: dict[str, object] | None = None) -> ToolResult:
        handler = self._handlers.get(name)
        if handler is None:
            raise KeyError(f"No handler registered for capability: {name}")
        return handler(params or {})

