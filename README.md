# Rootline

Rootline is a privacy-first infrastructure operations agent for system, DevOps, SRE, network and security engineers.

It connects to existing tools, understands operational documentation and history, and turns natural-language intent into safe, auditable workflows.

## Product direction

Rootline is not a monitoring replacement and does not require an agent installed on every server. It is an orchestration and reasoning layer that can connect to existing APIs, webhooks and tools such as Kubernetes, Argo CD, Git, Prometheus, Loki, DNS providers, backup systems and messaging platforms.

The first product principles are:

- Read-only by default.
- Evidence before conclusions.
- Human approval before write or destructive actions.
- Local-first and provider-neutral AI.
- Every action is typed, auditable and reproducible.
- Documentation and operational history are first-class context.

## Planned capabilities

- Natural-language operations chat and CLI.
- Connector and tool registry.
- Documentation and runbook intelligence.
- Operational memory for systems, owners, incidents and decisions.
- Multi-step workflow planning and execution.
- Incident investigation across existing tools.
- Security, expiry and backup skills.
- Approval policies, audit trails and evidence reports.

## Status

Early development. The first vertical slice includes a deterministic intent planner, typed capabilities and a mock connector.

## Local demo

```bash
python -m pip install -e .
rootline plan "investigate the production api incident after the last deploy"
```

The demo is intentionally read-only. It prints the typed capabilities Rootline would use; real connectors will be added incrementally.

## License

TBD
