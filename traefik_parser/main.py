from get_logs_from_k8s import get_logs_from_k8s
from get_logs_from_file import get_logs_from_file
from utils import show_top_metrics, count_by_occurence, parse_user_datetime
from log_parser import log_parser
from show_duration import show_duration
from get_args import get_args
from calculate_slowest_hosts import calculate_slowest_hosts
from show_slowest_hosts import show_slowest_hosts
from show_slower_than import show_slower_than
from datetime import datetime

MAX_REASONABLE_DURATION_SECONDS = 60
MAX_REASONABLE_DURATION = MAX_REASONABLE_DURATION_SECONDS * 1_000_000

def main():
    args = get_args()
    log_count = 0
    bad_log_count = 0
    ip_hits = {}
    statuses_count = {}
    bad_statuses_count = {}
    request_addr_count = {}
    request_path_count = {}
    request_times = {}
    all_durations_values = []
    logs = []

    if args.show_all:
        args.show_top_ips = True
        args.show_top_status_codes = True
        args.show_top_error_codes = True
        args.show_top_request_addr = True
        args.show_top_request_paths = True
        args.show_stats = True
        args.show_error_logs = True


    if args.from_file: 
        logs = get_logs_from_file(args.from_file)
    else:
        logs = get_logs_from_k8s(args.namespace, args.labels, args.lines)

    for log in logs:
        log_count += 1

        parsed_log = log_parser(log)
        # Filters
        if parsed_log is None:
            bad_log_count += 1
            continue
        
        if args.since or args.until:
            log_dt = datetime.fromisoformat(parsed_log["time"].replace("Z", "+00:00")).replace(tzinfo=None)

            if args.since and log_dt < parse_user_datetime(args.since):
                continue
            if args.until and log_dt > parse_user_datetime(args.until):
                continue

        if args.ip:
            if parsed_log["ClientHost"] != args.ip:
                continue
        if args.status:
            if parsed_log["DownstreamStatus"] != args.status:
                continue
        if args.path:
            if parsed_log["RequestPath"] != args.path:
                continue
        if args.host:
            if parsed_log["RequestAddr"] != args.host:
                continue

        if args.show_stats:
            if ("follow=true" not in parsed_log["RequestPath"] # Follow requests case
                and "rancher" not in parsed_log["RequestAddr"] # Rancher live logs fetching case
                and parsed_log["Duration"] < MAX_REASONABLE_DURATION): # Follow requests case + not normal requests that are bug probably
                    all_durations_values.append(parsed_log["Duration"])
        
        if args.show_error_logs:
            if parsed_log["DownstreamStatus"] >= 500 and parsed_log["DownstreamStatus"] <=599:
                print(parsed_log)
        
        if args.ip:
            if parsed_log["ClientHost"] == args.ip:
                print(f"IP: {parsed_log["ClientHost"]} {parsed_log["RequestAddr"]}{parsed_log["RequestPath"]} {parsed_log["DownstreamStatus"]}")

        if args.show_top_ips:
            count_by_occurence(parsed_log, "ClientHost", ip_hits)
        if  args.show_top_status_codes:
            count_by_occurence(parsed_log, "DownstreamStatus", statuses_count)
        if  args.show_top_request_addr:
            count_by_occurence(parsed_log, "RequestAddr", request_addr_count)
        if  args.show_top_request_paths:
            count_by_occurence(parsed_log, "RequestPath", request_path_count)
        if args.show_slowest:
            calculate_slowest_hosts(parsed_log, request_times)
        if args.slower_than:
            show_slower_than(parsed_log,args.slower_than,args.slower_than_show_path)


    if args.show_top_error_codes:
        for status in statuses_count.items():
            if status[0] >= 500 and status[0] <=599:
                bad_statuses_count.update({
                    status[0]: status[1]
                })
        show_top_metrics("5xx Status codes...",bad_statuses_count,args.results_number)    

    if args.show_top_ips:
        show_top_metrics("IP hit counts...",ip_hits, args.results_number)
    if  args.show_top_status_codes:
        show_top_metrics("Status codes...",statuses_count, args.results_number)
    if  args.show_top_request_addr:
        show_top_metrics("Request addresses...",request_addr_count, args.results_number)
    if  args.show_top_request_paths:
        show_top_metrics("Request paths...",request_path_count, args.results_number)
    if args.show_stats:
        show_duration(all_durations_values)
    if args.show_slowest:
        show_slowest_hosts(request_times)

    print("SUMMARY")
    print("-------------------")
    print(f"Total Log count: {log_count}")
    print(f"Failed to parse Log count: {bad_log_count}")

if __name__ == "__main__":
    main()