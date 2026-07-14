# Kube Compliance Checker

A CLI tool for auditing Kubernetes Pods against security and resource standards — a learning project focused on Python for SRE use cases.

## Goal

Scan running Pods from the command line and report every compliance deviation, in a way that's genuinely useful when reviewing a cluster's security and resource posture.

The goal is **not** to invent arbitrary rules. Checks are anchored in existing sources of truth (Kubernetes Pod Security Standards, QoS semantics, runtime facts), so results are defensible rather than opinionated. Conceptually it's *"OpenSCAP for Kubernetes Pods"*.

## Input

- Primary source: live Pods pulled from a cluster via the Kubernetes Python client (`~/.kube/config`).
- Fallback: static YAML/JSON manifests, for auditing before anything is applied (shift-left).
- The scanner should support both, not just one — this mirrors real-world use where you want to catch issues both in the cluster and in CI before deploy.

## What we check in a Pod

Severity legend: 🟢 OK · 🔵 LOW · 🟡 MEDIUM · 🔴 HIGH · ℹ️ INFO

### Security (source: Pod Security Standards)

| Check | Bad state | Severity |
|-------|-----------|----------|
| Privileged container | `privileged: true` | 🔴 HIGH |
| Host namespaces | `hostNetwork` / `hostPID` / `hostIPC: true` | 🔴 HIGH |
| Extra capabilities | `capabilities.add` outside Baseline set | 🔴 HIGH |
| hostPath volume | `hostPath` mounted | 🔴 HIGH |
| Runs as root | `runAsNonRoot` not `true` | 🟡 MEDIUM |
| Privilege escalation | `allowPrivilegeEscalation` not `false` | 🟡 MEDIUM |
| Capabilities not dropped | `capabilities.drop` missing `ALL` | 🟡 MEDIUM |
| Seccomp | not `RuntimeDefault` | 🟡 MEDIUM |

### Resources (source: QoS semantics)

| Check | Bad state | Severity |
|-------|-----------|----------|
| QoS = BestEffort | no requests/limits at all | 🔴 HIGH |
| Missing requests | no `requests.cpu` / `requests.memory` | 🔴 HIGH |
| Missing memory limit | no `limits.memory` | 🟡 MEDIUM |
| QoS = Burstable (partial) | some limit missing | 🟡 MEDIUM |
| Missing CPU limit | no `limits.cpu` | 🔵 LOW |
| QoS = Guaranteed | requests == limits | 🟢 OK |

### Runtime (source: containerStatuses / metrics-server)

| Check | Bad state | Severity |
|-------|-----------|----------|
| OOMKilled before | `lastState.terminated.reason == OOMKilled` | 🔴 HIGH |
| Current utilization | usage vs limit (snapshot) | ℹ️ INFO |

## Features (MVP)

### 1. Scanning
Pull all (or selected) Pods and resolve each into a set of checks. Key gotchas handled:
- `securityContext` exists at **Pod and container** level — compute the *effective* value (container overrides Pod), don't check one level blindly.
- Iterate over `initContainers` and `ephemeralContainers`, not just `containers`.
- Compute the resulting **QoS class** rather than eyeballing requests/limits.

### 2. Filtering
- by namespace (single / all)
- by minimum severity (e.g. HIGH only)
- by standard (`PSS-Baseline`, `PSS-Restricted`, `QoS`, `Runtime`)

### 3. Findings
Each deviation becomes a structured record:
- namespace, pod, container (`null` for pod-level checks)
- standard + `rule_id`
- severity
- observed vs. expected value

### 4. Error handling
- Pods with unexpected/partial specs don't crash the scan
- a summary at the end shows how many objects were skipped and why

### 5. Output
- readable table in the terminal
- optional export to CSV / JSON
- (phase 2) Prometheus exporter `/metrics` → Grafana + alerting

### 6. CLI
- namespace / all-namespaces flags
- filter flags (severity, standard)
- flag to choose output format
- optional path to a manifest file instead of a live cluster

## Success criteria

Running the tool against a real cluster produces a report that would genuinely help during a security/resource review — clear enough to hand to a team and act on.

## Status

🚧 In progress — personal project, being built independently.

---

## Progress Checklist

### Input

- [ ] ❌ Live cluster scan (Kubernetes Python client)
- [ ] ❌ Static manifest fallback (YAML/JSON file)
- [ ] ❌ RBAC-minimal ServiceAccount for in-cluster use

### 1. Scanning

- [ ] ❌ List Pods across namespaces
- [ ] ❌ Effective `securityContext` resolution (pod + container merge)
- [ ] ❌ Cover `initContainers` / `ephemeralContainers`
- [ ] ❌ QoS class computation

### 2. Checks — Security (PSS)

- [ ] ❌ Privileged / host namespaces / hostPath (Baseline)
- [ ] ❌ Extra capabilities (Baseline)
- [ ] ❌ runAsNonRoot / allowPrivilegeEscalation (Restricted)
- [ ] ❌ capabilities.drop ALL / seccomp RuntimeDefault (Restricted)

### 2. Checks — Resources

- [ ] ❌ QoS class findings (BestEffort / Burstable / Guaranteed)
- [ ] ❌ Missing requests / limits

### 2. Checks — Runtime

- [ ] ❌ OOMKilled history from containerStatuses
- [ ] ❌ Current utilization (INFO, from metrics-server)

### 3. Filtering

- [ ] ❌ By namespace
- [ ] ❌ By minimum severity
- [ ] ❌ By standard

### 4. Error Handling

- [ ] ❌ Malformed / partial specs don't crash the scan
- [ ] ❌ Summary of skipped objects

### 5. Output

- [ ] ❌ Readable terminal table
- [ ] ❌ Export to CSV / JSON
- [ ] ❌ Prometheus exporter `/metrics`

### 6. CLI

- [ ] ❌ `argparse` skeleton
- [ ] ❌ Namespace / severity / standard flags
- [ ] ❌ Output format flag
- [ ] ❌ Manifest-file input mode

### Summary

| Area | Status |
|---|---|
| Cluster scan | 🔴 Not started |
| Security checks (PSS) | 🔴 Not started |
| Resource checks (QoS) | 🔴 Not started |
| Runtime checks | 🔴 Not started |
| Filtering | 🔴 Not started |
| CLI interface | 🔴 Not started |
| Export | 🔴 Not started |

**Overall: greenfield — scope defined, implementation not yet started.**

### Next steps (priority order)

1. Kubernetes client wiring — list Pods across namespaces
2. Effective `securityContext` + QoS resolution helpers
3. First PSS Baseline rule end-to-end, with a `pytest` fixture
4. Remaining PSS + resource rules as pure functions
5. `argparse` CLI skeleton + JSON report
6. Filter flags (severity, standard, namespace)
7. Runtime checks (OOMKilled, utilization INFO)
8. CSV/JSON export
9. Prometheus exporter → Grafana dashboard
10. Polish: manifest-file input, in-cluster CronJob deployment