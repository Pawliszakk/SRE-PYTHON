from connect_to_k8s import connect_to_k8s
from get_pods import get_pods
from get_args import get_args
from check_pod_compliance import check_pod_compliance

def main():



    args = get_args()

    findings = []
    ok = []
    info = []
    low_severity = []
    medium_severity = []
    high_severity = []


    v1 = connect_to_k8s()

    pods = get_pods(v1,args.namespace)

    for pod in pods.items:
        check_pod_compliance(pod, findings)        

    print("\n")
    print(f"PODS CHECKED: { len(pods.items) }")
    print(f'OK: {len(ok)}, INFO: {len(info)}, LOW: {len(low_severity)}, MEDIUM: {len(medium_severity)}, HIGH: {len(high_severity)}')



if __name__ == "__main__":
    main()