from connect_to_k8s import connect_to_k8s
from get_pods import get_pods


def main():
    #Args to add
    namespace = "jumpserver"

    v1 = connect_to_k8s()

    pods = get_pods(v1,namespace)

    for pod in pods.items:
        print(pod.metadata.name)

if __name__ == "__main__":
    main()