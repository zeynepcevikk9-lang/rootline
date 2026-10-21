"""Small, provider-neutral contracts used by Rootline tools and workflows."""

from dataclasses import dataclass, field
from enum import Enum
from collections.abc import Callable
from typing import Any, Mapping


class CapabilityKind(str, Enum):
    READ = "read"
    WRITE = "write"
    DESTRUCTIVE = "destructive"


@dataclass(frozen=True)
class Capability:
    name: str
    description: str
    kind: CapabilityKind = CapabilityKind.READ
    risk: str = "low"
    requires_approval: bool = False
    input_schema: Mapping[str, Any] = field(default_factory=dict)


ToolHandler = Callable[[Mapping[str, Any]], "ToolResult"]


@dataclass(frozen=True)
class Evidence:
    source: str
    summary: str
    data: Mapping[str, Any] = field(default_factory=dict)
    collected_at: str | None = None


@dataclass(frozen=True)
class ToolResult:
    capability: str
    success: bool
    output: Mapping[str, Any] = field(default_factory=dict)
    evidence: tuple[Evidence, ...] = ()
    error: str | None = None

