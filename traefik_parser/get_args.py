import argparse

def get_args():
    default_namespace = "kube-system"
    default_labels = "app.kubernetes.io/name=rke2-traefik"

    parser = argparse.ArgumentParser(description='Http Proxy log parser CLI tool')
    parser.add_argument('--from-file', type=str, help='A path to file with logs')
    parser.add_argument('--namespace', type=str, help='Namespace where pods with http proxy are deployed in',default=default_namespace)
    parser.add_argument('--labels', type=str, help='Labels to pods where you want to get logs from',default=default_labels)
    parser.add_argument('--lines', type=int, help='How much lines from source do you want to parse',default=100)
    parser.add_argument('--show-top-ips', action='store_true', help='Show top source IP addresses')
    parser.add_argument('--show-top-status-codes', action='store_true', help='Show top HTTP status codes')
    parser.add_argument('--show-top-error-codes', action='store_true', help='Show top HTTP error codes (4xx/5xx)')
    parser.add_argument('--show-top-request-addr', action='store_true', help='Show top requested sites')
    parser.add_argument('--show-top-request-paths', action='store_true', help='Show top requested paths')
    parser.add_argument('--show-stats', action='store_true', help='Show aggregated stats (p50/p95/p99)')
    parser.add_argument('--show-error-logs', action='store_true', help='Show logs that caused 5xx error code')
    parser.add_argument('--show-all', action='store_true', help='Show all statistics that this tool is capable of...')
    
    args = parser.parse_args()

    if (args.from_file and args.namespace != default_namespace) or (args.from_file and args.labels != default_labels):
        parser.error("--namespace and --labels cannot be used with --from-file argument.")
    
    return args