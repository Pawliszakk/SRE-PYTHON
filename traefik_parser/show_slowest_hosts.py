from utils import from_microseconds_to_seconds


def show_slowest_hosts(my_dict):
    def average_request_time(item):
        return item[1]["sum"] / item[1]["count"]

    sorted_request_times = sorted(my_dict.items(), key=average_request_time, reverse=True)

    for item in sorted_request_times:
        avg = average_request_time(item)
        avg_in_seconds = from_microseconds_to_seconds(int(avg))
        print(f'{item[0]} {avg_in_seconds}s')