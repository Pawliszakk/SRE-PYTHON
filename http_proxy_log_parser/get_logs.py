from log_parser import log_parser
from utils import show_top_metrics, count_by_occurence
from connect_to_k8s import connect_to_k8s
def get_logs():

    ingress_namespace = "kube-system"
    ingress_labels = "app.kubernetes.io/name=rke2-traefik"
    ip_hits = {}
    statuses_count = {}
    request_path_count = {}
    request_addr_count = {}

    
    v1 = connect_to_k8s(ingress_namespace, ingress_labels)

    pods = v1.list_namespaced_pod(
        namespace=ingress_namespace, 
        label_selector=ingress_labels)

    for pod in pods.items:
        pod_name = pod.metadata.name

        for container in pod.spec.containers:
            container_name = container.name
            try:
                logs = v1.read_namespaced_pod_log(
                    name=pod_name, 
                    namespace=ingress_namespace, 
                    container=container_name, 
                    tail_lines=100)

                container_logs = logs.strip("b'\"").encode().decode("unicode_escape").splitlines()


                for log in container_logs:
                    parsed_log = log_parser(log)
                    
                    if parsed_log == None:
                        continue

                    count_by_occurence(parsed_log, "ClientHost", ip_hits)
                    count_by_occurence(parsed_log, "DownstreamStatus", statuses_count)
                    count_by_occurence(parsed_log, "RequestPath", request_path_count)
                    count_by_occurence(parsed_log, "RequestAddr", request_addr_count)

            except Exception as e:
                print(f"Error getting logs for pod {pod_name}, container {container_name}: {e}")

    show_top_metrics("TOP 10 HIT COUNTS IP...",ip_hits)
    show_top_metrics("TOP 10 STATUS CODES...",statuses_count)
    show_top_metrics("TOP 10 Request Paths...",request_path_count)
    show_top_metrics("TOP 10 Request addresses...",request_addr_count)
