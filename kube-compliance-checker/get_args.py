import argparse

def get_args():
    parser = argparse.ArgumentParser(description='Kube Compliance Checker - CLI Tool to check compliance of k8s cluster pods')

    parser.add_argument('--namespace', type=str, help='Namespace of pods to check', default=None)
    parser.add_argument('-n', type=str, help='Namespace of pods to check', default=None)
    parser.add_argument('--severity', type=str, help='Severity to check, | low | medium | high |', default=0)

    args = parser.parse_args()

    if args.n:
        args.namespace = args.n
    return args