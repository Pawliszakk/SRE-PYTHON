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
- duration (`Duration`, in nanoseconds — convert before computing percentiles)
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

