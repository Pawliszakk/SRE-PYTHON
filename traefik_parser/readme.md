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

## Usage

```bash
# Show everything, pulling live from the cluster
python main.py --show-all

# Show top 20 IPs instead of default 10
python main.py --show-top-ips --results-number 20

# Analyze a saved log file instead of live cluster
python main.py --from-file access.log --show-stats

# Filter to a specific status code and print matching logs
python main.py --status 500 --show-error-logs

# Pull more lines and check top requested paths
python main.py --lines 5000 --show-top-request-paths

# Check stats for a specific IP address
python main.py --ip 10.150.13.100 --show-top-ips

# Custom namespace/labels when pulling from a different cluster setup
python main.py --namespace default --labels app=my-ingress --show-all
```

Run `python main.py --help` for the full list of flags.

## Success criteria

Feeding the tool a real production access log produces a report that would genuinely help during incident debugging/analysis.

## Status

🚧 In progress — personal project, being built independently.

---

## Progress Checklist

### Input

- [x] ✅ Primary source: Traefik JSON access logs (pulled from K8s API)
- [x] ✅ Input file support (`--from-file`), decoupled from K8s-only source
- [ ] ❌ Fallback: nginx/Traefik plain text (combined) format — JSON-only parser for now

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

- [x] ✅ By HTTP status (`--status`)
- [x] ✅ By IP address (`--ip`)
- [x] ✅ By path (`--path`) — exact match only, not substring/regex yet
- [x] ✅ By host (`--host`) — bonus, not in original MVP
- [ ] ❌ By time range
- [x] ✅ Exclusion filters for noisy traffic (Rancher live-log streaming, `follow=true`, unreasonably long durations)

### 3. Statistics / Aggregations

- [x] ✅ Top N IP addresses by request count (N configurable via `--results-number`)
- [x] ✅ Request count per status code
- [x] ✅ Top N most requested endpoints
- [x] ✅ Top N 5xx error codes
- [x] ✅ Response time stats: average, median, p50/p95/p99 (global)
- [ ] ❌ Slowest endpoints (per-path latency ranking, not just global stats)

### 4. Error Handling

- [x] ✅ Malformed lines don't crash the program
- [x] ✅ Summary report of failed-to-parse line count

### 5. Output

- [ ] ⚠️ Readable terminal output — present, aligned columns via `show_top_metrics`, but no real table headers
- [ ] ❌ Export to CSV / JSON

### 6. CLI

- [x] ✅ `argparse`-based CLI (`get_args.py`) — namespace, labels, lines, file input, all display/filter flags
- [x] ✅ Filter flags (status, IP, path, host)
- [x] ✅ `--show-all` convenience flag (sets all display flags at once)
- [x] ✅ `--results-number` to control top-N size
- [x] ✅ Help text with usage examples (`epilog`)
- [ ] ❌ Time range filter flags
- [ ] ❌ Output format flag (CSV/JSON)
- [ ] ❌ Path filter as substring/regex (currently exact match)

### Summary

| Area | Status |
|---|---|
| Core parsing (JSON) | 🟢 Done |
| Aggregations | 🟢 Done |
| Error handling | 🟢 Done |
| CLI interface | 🟢 Done |
| Filtering (as CLI options) | 🟢 Mostly done (status/IP/path/host done, time range missing) |
| Export | 🔴 Not started |
| Plain text fallback | 🔴 Not started |
| Per-endpoint slowest ranking | 🔴 Not started |

**Overall: ~75-80% of MVP. Core engine, aggregations, and full CLI are done. Remaining gaps: export, plain text fallback, time-range filtering, and per-endpoint latency ranking.**

### Next steps (priority order)

1. Per-endpoint slowest-requests ranking (`{path: [durations]}` → avg/median per path)
2. CSV/JSON export
3. Time range filter flags (`--since` / `--until`)
4. Path filter as substring/regex instead of exact match
5. Plain text log fallback parser (nginx/Traefik combined format)
6. Polish: `RouterName` field, real table headers in terminal output