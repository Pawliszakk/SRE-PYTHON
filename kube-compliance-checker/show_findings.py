import json
from pprint import pprint


def show_findings(findings, args):

    if args.ok or args.info or args.low or args.medium or args.high:
        allowed_severities = set()
        if args.ok:
            allowed_severities.add("OK")
        if args.info:
            allowed_severities.add("INFO")
        if args.low:
            allowed_severities.add("LOW")
        if args.medium:
            allowed_severities.add("MEDIUM")
        if args.high:
            allowed_severities.add("HIGH")

        filtered = [f for f in findings if f.severity in allowed_severities]
    else:
        filtered = findings

    if args.output == "json":
        print(json.dumps([vars(f) for f in filtered], indent=2))
    elif args.output == "yaml":
        import yaml
        print(yaml.dump([vars(f) for f in filtered], default_flow_style=False))
    else:  # human
        for finding in filtered:
            print(f"Pod: {finding.namespace}/{finding.pod}| Container: {finding.container} | {finding.severity} | {finding.message} ")