from get_logs import get_logs
from utils import show_top_metrics, count_by_occurence
from log_parser import log_parser
from show_duration import show_duration
MAX_REASONABLE_DURATION_SECONDS = 60
MAX_REASONABLE_DURATION = MAX_REASONABLE_DURATION_SECONDS * 1_000_000

def main():

    ingress_namespace = "kube-system"
    ingress_labels = "app.kubernetes.io/name=rke2-traefik"
    log_lines = 100000
    log_count = 0
    bad_log_count = 0
    ip_hits = {}
    statuses_count = {}
    bad_statuses_count = {}
    request_addr_count = {}
    request_path_count = {}
    all_durations_values = []
    logs = get_logs(ingress_namespace, ingress_labels, log_lines)

    custom_ip = "10.1.10.253"

    for log in logs:
        log_count += 1

        parsed_log = log_parser(log)
        
        if parsed_log is None:
            bad_log_count += 1
            continue

        if ("follow=true" not in parsed_log["RequestPath"] # Follow requests case
            and "rancher" not in parsed_log["RequestAddr"] # Rancher live logs fetching case
            and parsed_log["Duration"] < MAX_REASONABLE_DURATION): # Follow requests case + not normal requests that are bug probably
                all_durations_values.append(parsed_log["Duration"])

        # 5xx logs
        # if parsed_log["DownstreamStatus"] >= 500 and parsed_log["DownstreamStatus"] <=599:
        #      print(parsed_log)
        
        # Logs By IP 
        # if parsed_log["ClientHost"] == custom_ip:
        #      print(f"IP: {parsed_log["ClientHost"]} {parsed_log["RequestAddr"]}{parsed_log["RequestPath"]} {parsed_log["DownstreamStatus"]}")

        count_by_occurence(parsed_log, "ClientHost", ip_hits)
        count_by_occurence(parsed_log, "DownstreamStatus", statuses_count)
        count_by_occurence(parsed_log, "RequestAddr", request_addr_count)
        count_by_occurence(parsed_log, "RequestPath", request_path_count)

    for status in statuses_count.items():
        if status[0] >= 500 and status[0] <=599:
            bad_statuses_count.update({
                status[0]: status[1]
            })
    

                
    show_top_metrics("TOP 10 IP hit counts...",ip_hits)
    show_top_metrics("TOP 10 Status codes...",statuses_count)
    show_top_metrics("TOP 10 5xx Status codes...",bad_statuses_count)
    show_top_metrics("TOP 10 Request addresses...",request_addr_count)
    show_top_metrics("TOP 10 Request paths...",request_path_count)
    show_duration(all_durations_values)

    print("\n")
    print("-------------------")
    print(f"Total Log count: {log_count}")
    print(f"Failed to parse Log count: {bad_log_count}")

if __name__ == "__main__":
    main()