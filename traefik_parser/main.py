from get_logs_from_k8s import get_logs_from_k8s
from get_logs_from_file import get_logs_from_file
from utils import show_top_metrics, count_by_occurence
from log_parser import log_parser
from show_duration import show_duration
from get_args import get_args
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
    all_durations_values = []
    # custom_ip = "10.1.10.253" add custom ip chosing function
    logs = []

    if args.from_file: 
        logs = get_logs_from_file(args.from_file)
    else:
        logs = get_logs_from_k8s(args.namespace, args.labels, args.lines)



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

        if args.show_all:
            if parsed_log["DownstreamStatus"] >= 500 and parsed_log["DownstreamStatus"] <=599:
                print(parsed_log)
        
            count_by_occurence(parsed_log, "ClientHost", ip_hits)
            count_by_occurence(parsed_log, "DownstreamStatus", statuses_count)
            count_by_occurence(parsed_log, "RequestAddr", request_addr_count)            
            count_by_occurence(parsed_log, "RequestPath", request_path_count)

        else:
            if args.show_error_logs:
                if parsed_log["DownstreamStatus"] >= 500 and parsed_log["DownstreamStatus"] <=599:
                    print(parsed_log)
            # if parsed_log["ClientHost"] == custom_ip:
            #      print(f"IP: {parsed_log["ClientHost"]} {parsed_log["RequestAddr"]}{parsed_log["RequestPath"]} {parsed_log["DownstreamStatus"]}")
            if args.show_top_ips:
                count_by_occurence(parsed_log, "ClientHost", ip_hits)
            if  args.show_top_status_codes:
                count_by_occurence(parsed_log, "DownstreamStatus", statuses_count)
            if  args.show_top_request_addr:
                count_by_occurence(parsed_log, "RequestAddr", request_addr_count)
            if  args.show_top_request_paths:
                count_by_occurence(parsed_log, "RequestPath", request_path_count)

    if args.show_top_error_codes or args.show_all:
        for status in statuses_count.items():
            if status[0] >= 500 and status[0] <=599:
                bad_statuses_count.update({
                    status[0]: status[1]
                })
        show_top_metrics("TOP 10 5xx Status codes...",bad_statuses_count)    

    if args.show_all:
            show_top_metrics("TOP 10 IP hit counts...",ip_hits)
            show_top_metrics("TOP 10 Status codes...",statuses_count)
            show_top_metrics("TOP 10 Request addresses...",request_addr_count)
            show_top_metrics("TOP 10 Request paths...",request_path_count)
            show_duration(all_durations_values)
    else:
        if args.show_top_ips:
            show_top_metrics("TOP 10 IP hit counts...",ip_hits)
        if  args.show_top_status_codes:
            show_top_metrics("TOP 10 Status codes...",statuses_count)
        if  args.show_top_request_addr:
            show_top_metrics("TOP 10 Request addresses...",request_addr_count)
        if  args.show_top_request_paths:
            show_top_metrics("TOP 10 Request paths...",request_path_count)
        if args.show_stats:
            show_duration(all_durations_values)

    print("-------------------")
    print(f"Total Log count: {log_count}")
    print(f"Failed to parse Log count: {bad_log_count}")

if __name__ == "__main__":
    main()