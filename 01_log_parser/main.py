# TASK: Server Log Analysis
# ====================================

# Context
# -------
# You are given a file server.log containing logs from a fleet of servers
# (node-01 through node-08). Each line follows the format:

# <date> <time> <LEVEL> <node> <message>

# Example:
# 2026-09-21 08:12:03 WARNING node-01 Disk usage at 85%

# Log levels (increasing severity): INFO, WARNING, ERROR, CRITICAL


# Tasks
# -----

# 1. Parsing
#    Write a function parse_log(filepath) that reads the file and returns
#    a list of dictionaries, one per line, with keys:
#    'timestamp' (a datetime object), 'level', 'node', 'message'

# 2. Level statistics
#    Write a function count_by_level(logs) that returns a dictionary with
#    the count of each level, e.g.:
#    {'INFO': 120, 'WARNING': 80, 'ERROR': 55, 'CRITICAL': 16}

# 3. Most problematic node
#    Write a function worst_node(logs) that returns the name of the node
#    with the highest combined count of ERROR + CRITICAL entries, along
#    with that count.

# 4. Recurring errors
#    Write a function recurring_errors(logs, min_count=2) that returns a
#    list of unique ERROR messages that occurred at least min_count times
#    across the whole log (regardless of node), sorted descending by
#    occurrence count. Return a list of tuples (message, count).

# 5. Burst detection (harder)
#    Write a function detect_bursts(logs, window_minutes=5, min_errors=2)
#    that detects situations where the SAME node produced at least
#    min_errors errors (ERROR or CRITICAL) within a window_minutes time
#    window. Return a list of such events in the format:
#    [{'node': 'node-03', 'start': <timestamp>, 'end': <timestamp>,
#      'count': 4, 'messages': [...]}, ...]

#    Hint: this is not about fixed time buckets (e.g. 08:00-08:05,
#    08:05-08:10), but about detecting that consecutive errors on the
#    same node are close enough together in time to be considered a
#    "burst".

# 6. Final report
#    Write a function print_report(logs) that prints a readable summary
#    combining the results from tasks 2-5, suitable for a stand-up update.


# Evaluation criteria
# --------------------
# - Correctness of results
# - Code readability (naming, no unnecessary duplication)
# - Handling of edge cases (empty file, no errors present, etc.)
# - Performance is not critical at this data scale, but avoid clearly
#   suboptimal approaches (e.g. O(n^3) where O(n) would do)

# Time: ~45-60 minutes


def main():

    log_file = 'server.log'

    # parse_log(log_file)
    # count_by_level(log_file)
    # worst_node(log_file)
    # recurring_errors(log_file)
    detect_bursts(log_file)
#1
def parse_log(log_path):

    dict_data = []

    with open(log_path, 'r') as f:

        for line in f:

            log = line.split()

            dict_data.append({
                "timestamp": f'{log[0]} {log[1]}',
                "level": log[2],
                "node": log[3],
                "message": log[4]
            })

    print(dict_data)

#2 
def count_by_level(log_path):
    level_count = {}

    with open(log_path, 'r') as f:

        for line in f:

            level = line.split()[2]

            if level_count.get(level) == None:
                level_count.update({
                    level: 1
                })
            else:
                level_count.update({
                    level: level_count.get(level) + 1
                })
    print(level_count)

#3
def worst_node(log_path):

    statistics = {}

    with open(log_path, 'r') as f:

        for line in f:
            log = line.split()
            node = log[3]
            level = log[2]

            if level == "ERROR" or level == "CRITICAL":

                if statistics.get(node) == None:
                    statistics.update({
                        node: 1
                    })
                else:
                    statistics.update({
                        node: statistics.get(node) + 1
                        })
    most_problematic_node = max(statistics, key=statistics.get)
    print(f"{most_problematic_node}: {statistics.get(most_problematic_node)}")

#4
def recurring_errors(log_path, min_count=2):

    error_messages = {}
    error_messages_list = []
    with open(log_path, 'r') as f:
        for line in f:

            log = line.split()

            message = " ".join(log[4:])
            level = log[2]

            if level == "ERROR":

                if error_messages.get(message) == None:
                    error_messages.update({
                        message: 1
                    })

                else:
                    error_messages.update({
                        message: error_messages.get(message) + 1
                    })    
            else:
                continue

    for item in error_messages:
        if error_messages.get(item) >= min_count:
            error_messages_list.append((item,error_messages.get(item)))

    error_messages_list.sort(key=lambda x: x[1],reverse=True)

    print(error_messages_list)

#5
def detect_bursts(log_file, windows_minutes=5, min_errors=2):

    with open(log_file, 'r') as f:
        for line in f:
            print(line)

if __name__ == "__main__":
    main()