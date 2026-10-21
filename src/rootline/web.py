"""Web API for the first Rootline planning experience."""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from .engine import RootlineEngine


class PlanRequest(BaseModel):
    intent: str = Field(min_length=3, max_length=2000)


engine = RootlineEngine()
app = FastAPI(
    title="Rootline",
    description="Privacy-first infrastructure operations agent",
    version="0.1.0",
)


@app.get("/", response_class=FileResponse)
def index() -> Path:
    return Path(__file__).parent / "static" / "index.html"


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "rootline"}


@app.get("/api/capabilities")
def capabilities() -> list[dict[str, object]]:
    return [
        {
            "name": capability.name,
            "description": capability.description,
            "kind": capability.kind.value,
            "risk": capability.risk,
            "requires_approval": capability.requires_approval,
        }
        for capability in engine.registry.list()
    ]


@app.post("/api/plan")
def plan(request: PlanRequest) -> dict[str, object]:
    try:
        operation_plan = engine.plan(request.intent)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "intent": operation_plan.intent,
        "summary": operation_plan.summary,
        "requires_approval": operation_plan.requires_approval,
        "warnings": list(operation_plan.warnings),
        "steps": [
            {
                "capability": step.capability.name,
                "description": step.capability.description,
                "kind": step.capability.kind.value,
                "risk": step.capability.risk,
                "reason": step.reason,
            }
            for step in operation_plan.steps
        ],
    }
