from rootline.engine import RootlineEngine


def test_incident_plan_is_read_only_and_cross_tool() -> None:
    plan = RootlineEngine().plan("Investigate the production API incident after the last deploy")

    assert plan.requires_approval is False
    assert [step.capability.name for step in plan.steps] == [
        "kubernetes.get_workload_status",
        "kubernetes.get_recent_events",
        "argocd.get_application_status",
        "git.get_recent_changes",
        "prometheus.query_range",
        "loki.query_logs",
    ]


def test_disk_plan_does_not_include_destructive_actions() -> None:
    plan = RootlineEngine().plan("disk usage on production")

    assert all(step.capability.kind.value == "read" for step in plan.steps)


def test_unknown_intent_is_explicit() -> None:
    plan = RootlineEngine().plan("make me coffee")

    assert not plan.steps
    assert plan.warnings
