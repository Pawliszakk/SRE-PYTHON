from get_logs import get_logs
from utils import show_top_metrics, count_by_occurence
from log_parser import log_parser

def main():

    ingress_namespace = "kube-system"
    ingress_labels = "app.kubernetes.io/name=rke2-traefik"
    log_lines = 100000
    ip_hits = {}
    statuses_count = {}
    request_addr_count = {}
    request_path_count = {}
    
    logs = get_logs(ingress_namespace, ingress_labels, log_lines)

    for log in logs:
        parsed_log = log_parser(log)
        
        if parsed_log is None:
            continue

        count_by_occurence(parsed_log, "ClientHost", ip_hits)
        count_by_occurence(parsed_log, "DownstreamStatus", statuses_count)
        count_by_occurence(parsed_log, "RequestAddr", request_addr_count)
        count_by_occurence(parsed_log, "RequestPath", request_path_count)
    
    show_top_metrics("TOP 10 IP hit counts...",ip_hits)
    show_top_metrics("TOP 10 Status codes...",statuses_count)
    show_top_metrics("TOP 10 Request addresses...",request_addr_count)
    show_top_metrics("TOP 10 Request paths...",request_path_count)

if __name__ == "__main__":
    main()