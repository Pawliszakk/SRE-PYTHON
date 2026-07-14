# Usage

Run `python main.py --help` for the full, up-to-date list of flags.

## Examples

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

# Show requests slower than 10 seconds
python main.py --slower-than 10

# Show slowest hosts, ranked by average response time
python main.py --show-slowest

# Filter by a time window (from a saved log file)
python main.py --from-file access.log --since "2026-07-14 07:00" --until "2026-07-14 12:00" --show-top-request-addr

# Export all results to CSV instead of printing to terminal
python main.py --show-all --output-dir ./results
```