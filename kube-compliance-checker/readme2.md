# Kube Compliance Checker

A CLI tool for auditing Kubernetes Pods against security and resource standards.
Conceptually: *"OpenSCAP for Kubernetes Pods"*.

Checks are anchored in existing sources of truth — Kubernetes [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/), QoS semantics and runtime facts — so findings are defensible rather than opinionated.

> 🚧 Status: in progress — personal project, scope defined, implementation starting.

## Input modes

| Mode | Source | Use case |
|------|--------|----------|
| Live cluster | Kubernetes Python client (`~/.kube/config`) | audit what is actually running |
| Manifest file | static YAML / JSON | shift-left, catch issues in CI before deploy |

## Checks

Severity legend: 🔴 HIGH · 🟡 MEDIUM · 🔵 LOW · ℹ️ INFO · 🟢 OK

### 🔴 HIGH

| Rule | Bad state | Standard |
|------|-----------|----------|
| Privileged container | `securityContext.privileged: true` | PSS-Baseline |
| Host namespaces | `hostNetwork` / `hostPID` / `hostIPC: true` | PSS-Baseline |
| Extra capabilities | `capabilities.add` outside the Baseline set | PSS-Baseline |
| hostPath volume | volume of type `hostPath` mounted | PSS-Baseline |
| QoS = BestEffort | no requests and no limits at all | QoS |
| Missing requests | no `requests.cpu` / `requests.memory` | QoS |
| OOMKilled before | `lastState.terminated.reason == OOMKilled` | Runtime |

### 🟡 MEDIUM

| Rule | Bad state | Standard |
|------|-----------|----------|
| Runs as root | `runAsNonRoot` not `true` | PSS-Restricted |
| Privilege escalation | `allowPrivilegeEscalation` not `false` | PSS-Restricted |
| Capabilities not dropped | `capabilities.drop` missing `ALL` | PSS-Restricted |
| Seccomp | profile not `RuntimeDefault` | PSS-Restricted |
| Missing memory limit | no `limits.memory` | QoS |
| QoS = Burstable (partial) | some limit missing | QoS |

### 🔵 LOW

| Rule | Bad state | Standard |
|------|-----------|----------|
| Missing CPU limit | no `limits.cpu` | QoS |

### ℹ️ INFO

| Rule | Observation | Standard |
|------|-------------|----------|
| Current utilization | usage vs limit (snapshot from metrics-server) | Runtime |

### 🟢 OK

| Rule | Good state | Standard |
|------|------------|----------|
| QoS = Guaranteed | requests == limits for every container | QoS |

## Evaluation rules (gotchas)

- **Effective `securityContext`** — the value exists at both Pod and container level; the container overrides the Pod. Never check one level blindly.
- **All container types** — iterate over `initContainers` and `ephemeralContainers`, not just `containers`.
- **QoS class is computed**, not eyeballed from requests/limits.

## Findings

Every deviation becomes a structured record:

```json
{
  "namespace": "prod",
  "pod": "api-7d9f8c-x2k4l",
  "container": "api",
  "standard": "PSS-Restricted",
  "rule_id": "PSS-R-002",
  "severity": "MEDIUM",
  "observed": "allowPrivilegeEscalation: null",
  "expected": "allowPrivilegeEscalation: false"
}
```

`container` is `null` for pod-level checks.

## Filtering

- by namespace (single / all)
- by minimum severity (e.g. HIGH only)
- by standard (`PSS-Baseline`, `PSS-Restricted`, `QoS`, `Runtime`)

## Output

- readable table in the terminal
- optional export to CSV / JSON
- *(phase 2)* Prometheus exporter `/metrics` → Grafana + alerting

## Error handling

- Pods with unexpected or partial specs never crash the scan
- a summary at the end reports how many objects were skipped and why

## Roadmap

- [ ] Kubernetes client wiring — list Pods across namespaces
- [ ] Effective `securityContext` + QoS resolution helpers
- [ ] First PSS Baseline rule end-to-end, with a `pytest` fixture
- [ ] Remaining PSS + resource rules as pure functions
- [ ] `argparse` CLI skeleton + JSON report
- [ ] Filter flags (severity, standard, namespace)
- [ ] Runtime checks (OOMKilled, utilization INFO)
- [ ] CSV / JSON export
- [ ] Prometheus exporter → Grafana dashboard
- [ ] Manifest-file input mode
- [ ] RBAC-minimal ServiceAccount + in-cluster CronJob deployment