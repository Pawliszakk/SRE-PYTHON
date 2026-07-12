from utils import from_microseconds_to_seconds
import statistics
def show_duration(my_data):
    print("\n")
    
    sorted_all_durations_values = sorted(my_data, reverse=True)

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
