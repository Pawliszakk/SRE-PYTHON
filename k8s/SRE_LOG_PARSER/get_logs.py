from kubernetes import client, config
from log_parser import parser
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_logs():

    ingress_namespace = "kube-system"
    ingress_labels = "app.kubernetes.io/name=rke2-traefik"
    
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
                    tail_lines = 2
                    )
                
                container_logs = container_logs.strip("b'\"").encode().decode("unicode_escape")

                for log in container_logs.splitlines():
                    if "new release of Traefik has been found" not in log:
                        parser(log)

    except Exception as e:
        print("Something went wrong with getting logs from k8s api server")
        print(e)

