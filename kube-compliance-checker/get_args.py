import argparse

def get_args():
    parser = argparse.ArgumentParser(description='Kube Compliance Checker - CLI Tool to check compliance of k8s cluster pods')

    parser.add_argument('--namespace', type=str, help='Namespace of pods to check', default=None)
    parser.add_argument('-n', type=str, help='Namespace of pods to check', default=None)
    parser.add_argument('--ok', action='store_true', help='Show only ok severity findings')
    parser.add_argument('--info', action='store_true', help='Show only info severity findings')
    parser.add_argument('--low', action='store_true', help='Show only low severity findings')
    parser.add_argument('--medium', action='store_true', help='Show only medium severity findings')
    parser.add_argument('--high', action='store_true', help='Show only high severity findings')
    parser.add_argument('--show-all', action='store_true', default=True, help='Show all findings')
    parser.add_argument(
        '-o', '--output',
        choices=['human', 'json', 'yaml'],
        default='human',
        help='Output format: human, json, or yaml'
    )

    args = parser.parse_args()


    if args.n:
        args.namespace = args.n
    return args