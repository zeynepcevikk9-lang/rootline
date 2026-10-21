# Rootline Architecture

## Initial architecture

```text
User: CLI / Telegram / Slack / Web
                 |
                 v
        Intent and conversation layer
                 |
                 v
       Planner + policy engine
          |              |
          v              v
  Operational memory   Tool registry
  Docs/runbooks        Typed connectors
          |              |
          +------+-------+
                 v
          Evidence and workflow
                 |
        approval -> execute -> verify
                 |
                 v
          audit and reporting
```

## Connector model

Connectors expose typed capabilities instead of arbitrary shell commands. Each capability declares:

- name and description
- input schema
- output schema
- read or write classification
- required permissions
- risk level
- approval requirement
- verification procedure

The first real connector is a read-only Kubernetes API connector. It uses the
Kubernetes API directly, does not require a daemon on every node, and accepts a
small client interface so authentication and transport can be tested separately
from the workflow planner.

Example capabilities:

- `kubernetes.get_pods`
- `argocd.get_application_status`
- `gitea.get_commit`
- `prometheus.query_range`
- `dns.lookup`
- `telegram.send_message`

## Execution safety

The model may choose a capability, but it does not invent the underlying command. Connectors own request construction and validation. Write operations require policy evaluation and, where configured, human approval.

## Privacy

- Local model support is a first-class option.
- Secrets and credentials are never placed into model context by default.
- Sensitive values are redacted before external model calls.
- Evidence retention is configurable.
- Each organization can choose which data may leave its environment.

