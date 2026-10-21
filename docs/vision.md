# Rootline Vision

## Problem

Infrastructure engineers work across many disconnected tools and documents. A single request often requires manually switching between Kubernetes, GitOps, monitoring, DNS, security systems, backup consoles, tickets and private runbooks.

The main cost is not the lack of another dashboard. It is the mental work required to find context, choose the right procedure, assess risk and verify the result.

## Product hypothesis

Rootline should act as an operational reasoning and workflow layer over existing infrastructure tools.

Given an intent such as:

> Investigate the production API issue, compare it with the last deployment, and prepare a safe rollback plan.

Rootline should:

1. Identify the relevant systems and tools.
2. Gather evidence through typed read operations.
3. Retrieve relevant documentation and historical context.
4. Produce explicit hypotheses with evidence and uncertainty.
5. Propose a workflow with risk and approval requirements.
6. Execute only approved, typed actions.
7. Verify the result and produce an auditable report.

## Non-goals

- Replacing Prometheus, Grafana, Loki or existing observability systems.
- Installing a permanent agent on every server.
- Giving an LLM unrestricted shell access.
- Building a generic chatbot with no operational memory.
- Automatically changing production systems by default.

## Differentiation

Rootline combines four capabilities that are usually separate:

1. Operational memory.
2. Documentation-to-runbook intelligence.
3. Cross-tool workflow orchestration.
4. Evidence-based, approval-gated execution.

