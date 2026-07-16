# SRE Log Parser CLI

A CLI tool for analyzing Traefik HTTP access logs — a learning project focused on Python for SRE use cases.

## Goal

Parse and analyze Traefik access logs from the command line, in a way that's genuinely useful when debugging production incidents.

## Input

- ✅ Traefik JSON access logs (`--accesslog.format=json`) pulled live from a production RKE2 cluster via the Kubernetes API.
- ✅ File input also supported (`--from-file`) for offline analysis of saved logs.

## Features

### 1. Parsing
Parses each log line into a structured record containing:
- ✅ client IP (`ClientHost`)
- ✅ timestamp (`time`, ISO8601 UTC)
- ✅ HTTP method (`RequestMethod`)
- ✅ path (`RequestPath`)
- ✅ status code (`DownstreamStatus`)
- ✅ response size (`DownstreamContentSize`)
- ✅ duration (`Duration`, in **microseconds** — converted before computing percentiles)
- ✅ service name (`ServiceName`) — useful for aggregating by application (e.g. Nextcloud, JumpServer)

### 2. Filtering
- ✅ by HTTP status (`--status`)
- ✅ by IP address (`--ip`)
- ✅ by path (`--path`) — exact match only, not substring/regex
- ✅ by host (`--host`)
- ✅ by time range (`--since` / `--until`)
- ✅ by minimum duration (`--slower-than`, in seconds)
- ✅ exclusion filters for noisy traffic (Rancher live-log streaming, `follow=true`, unreasonably long durations)

### 3. Statistics / aggregations
- ✅ top N IP addresses by request count
- ✅ request count per status code
- ✅ top N most requested endpoints
- ✅ top N 5xx error codes
- ✅ response time stats: average, median, p50/p95/p99
- ✅ slowest hosts, ranked by average response time

### 4. Error handling
- ✅ lines that don't match the expected pattern don't crash the program
- ✅ a summary report at the end shows how many lines failed to parse
- ✅ graceful "no data matched filters" message instead of crashing on empty result sets

### 5. Output
- ✅ readable terminal output via `show_top_metrics`, aligned columns
- ✅ CSV export for all metrics (`--output-dir`) — top IPs, status codes, error codes, request paths, request addresses, stats, slowest hosts, error logs, per-IP logs

### 6. CLI
- ✅ `argparse`-based CLI, with filter flags, `--show-all` convenience flag, `--results-number` for top-N size, and usage examples in `--help`

## Success criteria

Feeding the tool a real production access log produces a report that would genuinely help during incident debugging/analysis.

See `USAGE.md` for the full flag reference and examples.