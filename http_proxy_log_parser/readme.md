# SRE Log Parser CLI

A CLI tool for analyzing HTTP access logs (nginx / Traefik) — a learning project focused on Python for SRE use cases.

## Goal

Parse and analyze HTTP access logs from the command line, in a way that's genuinely useful when debugging production incidents.

## Input

- Primary source: Traefik JSON access logs (`--accesslog.format=json`) pulled from a production RKE2 cluster.
- Fallback: nginx/Traefik combined (plain text) log format, for cases where JSON logging isn't available.
- The parser should support both formats, not just one — this mirrors real-world environments where log format isn't always under your control.

## Features (MVP)

### 1. Parsing
Parse each log line into a structured record containing:
- client IP (`ClientAddr` / `ClientHost` in JSON)
- timestamp (`time`, ISO8601 UTC)
- HTTP method (`RequestMethod`)
- path (`RequestPath`)
- status code (`DownstreamStatus`)
- response size (`DownstreamContentSize`)
- duration (`Duration`, in **microseconds** — convert before computing percentiles)
- router / service name (`RouterName`, `ServiceName`) — useful for aggregating by application (e.g. Nextcloud, JumpServer)
- user-agent, if present (not guaranteed in Traefik's default JSON fields — treat as optional)

### 2. Filtering
- by HTTP status (e.g. `5xx` only)
- by time range
- by IP address
- by path (substring / regex)

### 3. Statistics / aggregations
- top N IP addresses by request count
- request count per status code
- top N most requested endpoints
- (optional, if response time is present in the log) slowest endpoints

### 4. Error handling
- lines that don't match the expected pattern don't crash the program
- a summary report at the end shows how many lines failed to parse

### 5. Output
- readable table in the terminal
- optional export to CSV / JSON

### 6. CLI
- input file as a positional argument
- filter flags (status, IP, path, time range)
- flag to choose output format

## Success criteria

Feeding the tool a real production access log produces a report that would genuinely help during incident debugging/analysis.

## Status

🚧 In progress — personal project, being built independently.

---

## Progress Checklist

### Input

- [x] ✅ Primary source: Traefik JSON access logs (pulled from K8s API)
- [ ] ❌ Fallback: nginx/Traefik plain text (combined) format
- [ ] ❌ Input file as positional argument (currently hardcoded to K8s API only)

### 1. Parsing

- [x] ✅ Client IP (`ClientHost`)
- [x] ✅ Timestamp (`time`)
- [x] ✅ HTTP method (`RequestMethod`)
- [x] ✅ Path (`RequestPath`)
- [x] ✅ Status code (`DownstreamStatus`)
- [x] ✅ Response size (`DownstreamContentSize`)
- [x] ✅ Duration (`Duration`)
- [x] ✅ Service name (`ServiceName`)
- [ ] ❌ Router name (`RouterName`) — not currently parsed
- [ ] ❌ User-agent (optional field)

### 2. Filtering

- [ ] ❌ By HTTP status (e.g. 5xx only) — as CLI option (currently hardcoded logic only)
- [ ] ❌ By time range
- [ ] ❌ By IP address
- [ ] ❌ By path (substring / regex)
- [x] ✅ *(bonus, not in original MVP)* Exclusion filters for noisy traffic (Rancher live-log streaming, `follow=true`, unreasonably long durations)

### 3. Statistics / Aggregations

- [x] ✅ Top N IP addresses by request count
- [x] ✅ Request count per status code
- [x] ✅ Top N most requested endpoints
- [x] ✅ Response time stats: average, median, p50/p95/p99 (global)
- [ ] ❌ Slowest endpoints (per-path latency ranking, not just global stats)

### 4. Error Handling

- [x] ✅ Malformed lines don't crash the program
- [x] ✅ Summary report of failed-to-parse line count

### 5. Output

- [ ] ⚠️ Readable terminal output — present, but not a real aligned table with headers
- [ ] ❌ Export to CSV / JSON

### 6. CLI

- [ ] ❌ Input file as positional argument
- [ ] ❌ Filter flags (status, IP, path, time range)
- [ ] ❌ Output format flag
- [ ] ❌ `argparse` (or equivalent) — currently all params hardcoded in `main()`

### Summary

| Area | Status |
|---|---|
| Core parsing (JSON) | 🟢 Done |
| Aggregations | 🟢 Mostly done |
| Error handling | 🟢 Done |
| Filtering (as CLI options) | 🔴 Not started (only hardcoded) |
| CLI interface | 🔴 Not started |
| Export | 🔴 Not started |
| Plain text fallback | 🔴 Not started |

**Overall: solid working core (~45-50% of MVP), missing the CLI/filtering/export layer that turns it into the tool described above.**

### Next steps (priority order)

1. File input support (`get_logs_from_file`) — decouple from K8s-only source
2. `argparse` CLI skeleton
3. Filter flags (status, IP, path, time range)
4. Plain text log fallback parser
5. Per-endpoint slowest-requests ranking
6. CSV/JSON export
7. Polish: `RouterName`, aligned table output