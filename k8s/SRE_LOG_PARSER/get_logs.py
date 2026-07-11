from kubernetes import client, config
from log_parser import parser
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_logs():

    ingress_namespace = "kube-system"
    ingress_labels = "app.kubernetes.io/name=rke2-traefik"
    
    ip_hits = {}
    
    try:
        config.load_kube_config()
        configuration = client.Configuration.get_default_copy()
        configuration.verify_ssl = False
        client.Configuration.set_default(configuration)
        v1 = client.CoreV1Api()

        ingress_pods = v1.list_namespaced_pod(
            namespace=ingress_namespace,
            label_selector=ingress_labels
            )

        for ingress_pod in ingress_pods.items:


            for container in ingress_pod.spec.containers:

                container_logs = v1.read_namespaced_pod_log(
                    name = ingress_pod.metadata.name,
                    namespace = ingress_namespace,
                    container = container.name,
                    tail_lines = 5
                    )
                
                container_logs = container_logs.strip("b'\"").encode().decode("unicode_escape")

                for log in container_logs.splitlines():
                    if "new release of Traefik has been found" not in log:

                        parsed_log = parser(log)
                        if parsed_log is None:
                            continue
                        # HTTP REQUESTS  LOGIC
                        log_code = parsed_log["DownstreamStatus"]
                            #get only those logs that contain 5xx status code indicating server error

                        print(log_code)
                        # HTTP REQUESTS  LOGIC

                        # IP HITS LOGIC
                        ip_from_log = parsed_log["ClientHost"]
                        ip_in_hits = ip_hits.get(ip_from_log)
                        is_in_ip_hits = bool(ip_in_hits)

                        if is_in_ip_hits:
                            new_hit_value = ip_in_hits + 1
                            ip_hits.update(
                                { str(ip_from_log): new_hit_value }
                                )
                        else:
                            ip_hits.update(
                                { str(ip_from_log): 1 }
                                )
                        # IP HITS LOGIC
                            


    except Exception as e:
        print("Something went wrong with getting logs from k8s api server")
        print(e)

# PRINTING IP HITS 
    def get_value(item):
        return item[1]
    sorted_hits = sorted(ip_hits.items(), key=get_value, reverse=True)
    # for i,hit in enumerate(sorted_hits, start=1):
    #     print(f'{i}. {hit[0]:<16} | {hit[1]} {"hit" if hit[1] == 1 else "hits" }')

