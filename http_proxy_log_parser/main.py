from get_logs import get_logs
from utils import show_top_metrics, count_by_occurence
from log_parser import log_parser
import statistics

MAX_REASONABLE_DURATION_SECONDS = 120
MAX_REASONABLE_DURATION = MAX_REASONABLE_DURATION_SECONDS * 1_000_000

def main():

    ingress_namespace = "kube-system"
    ingress_labels = "app.kubernetes.io/name=rke2-traefik"
    log_lines = 60
    log_count = 0
    bad_log_count = 0
    ip_hits = {}
    statuses_count = {}
    bad_statuses_count = {}
    request_addr_count = {}
    request_path_count = {}
    all_durations_values = []
    logs = get_logs(ingress_namespace, ingress_labels, log_lines)

    for log in logs:
        log_count += 1

        parsed_log = log_parser(log)
        
        if parsed_log is None:
            bad_log_count += 1
            continue
    
        for status_count in statuses_count.items():
            if status_count[0] >= 500 and status_count[0] <=599:
                bad_statuses_count.update({
                    status_count[0]: status_count[1]
                })

        if ("follow=true" not in parsed_log["RequestPath"] # Follow requests case
            and "rancher" not in parsed_log["RequestAddr"] # Rancher live logs fetching case
            and parsed_log["Duration"] < MAX_REASONABLE_DURATION): # Follow requests case + not normal requests that are bug probably

                all_durations_values.append(parsed_log["Duration"])

        count_by_occurence(parsed_log, "ClientHost", ip_hits)
        count_by_occurence(parsed_log, "DownstreamStatus", statuses_count)
        count_by_occurence(parsed_log, "RequestAddr", request_addr_count)
        count_by_occurence(parsed_log, "RequestPath", request_path_count)

                
    show_top_metrics("TOP 10 IP hit counts...",ip_hits)
    show_top_metrics("TOP 10 Status codes...",statuses_count)
    show_top_metrics("TOP 10 5xx Status codes...",bad_statuses_count)
    show_top_metrics("TOP 10 Request addresses...",request_addr_count)
    show_top_metrics("TOP 10 Request paths...",request_path_count)

    print("\n")
    def from_microseconds_to_seconds(value):
         return round(value/1000000,2)
    sorted_all_durations_values = sorted(all_durations_values, reverse=True)

    average_duration = sum(sorted_all_durations_values)/len(sorted_all_durations_values)
    
    average_duration_in_seconds = from_microseconds_to_seconds(average_duration)
    
    duration_median = from_microseconds_to_seconds(statistics.median(sorted_all_durations_values))
    
    percentyle = statistics.quantiles(sorted_all_durations_values, n=100)
    p50 = from_microseconds_to_seconds(percentyle[49])
    p95 = from_microseconds_to_seconds(percentyle[94])
    p99 = from_microseconds_to_seconds(percentyle[98])
    
    print(f"Average Request duration value: {round(average_duration_in_seconds,3)}s based on {len(sorted_all_durations_values)} requests")
    print(f'Request Median Value: {duration_median}s')
    print(f'Percentyles values: ')
    print(f'Requests P99 value: {p99}s')
    print(f'Requests P95 value: {p95}s')
    print(f'Requests P50 value: {p50}s')


    print("\n")
    print("-------------------")
    print(f"Total Log count: {log_count}")
    print(f"Failed to parse Log count: {bad_log_count}")

if __name__ == "__main__":
    main()