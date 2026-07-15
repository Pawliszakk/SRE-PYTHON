from connect_to_k8s import connect_to_k8s
from get_pods import get_pods
from get_args import get_args

def main():

    args = get_args()

    low_severity = 0
    medium_severity = 0
    high_severity = 0

    v1 = connect_to_k8s()

    pods = get_pods(v1,args.namespace)

    for pod in pods.items:
        print(pod.metadata.name)

if __name__ == "__main__":
    main()