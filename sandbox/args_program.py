import argparse
parser = argparse.ArgumentParser(description="Test argparse")
parser.add_argument("--log-lines", type=int, default=100, help="Number of log lines")

args = parser.parse_args()
print(args.log_lines)