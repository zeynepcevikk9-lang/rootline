"""Command-line entry point for the first Rootline vertical slice."""

import json
import sys

from . import __version__
from .engine import RootlineEngine


def main() -> None:
    if len(sys.argv) < 2:
        print(f"rootline {__version__} — infrastructure operations agent")
        print("Usage: rootline plan \"investigate the production api incident\"")
        return
    if sys.argv[1] != "plan":
        raise SystemExit(f"Unknown command: {sys.argv[1]}")
    intent = " ".join(sys.argv[2:]).strip()
    if not intent:
        raise SystemExit("A natural-language intent is required.")
    plan = RootlineEngine().plan(intent)
    print(json.dumps(_serialize_plan(plan), indent=2))


def _serialize_plan(plan):
    return {
        "intent": plan.intent,
        "summary": plan.summary,
        "requires_approval": plan.requires_approval,
        "warnings": list(plan.warnings),
        "steps": [
            {
                "capability": step.capability.name,
                "description": step.capability.description,
                "kind": step.capability.kind.value,
                "risk": step.capability.risk,
                "reason": step.reason,
            }
            for step in plan.steps
        ],
    }

