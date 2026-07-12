from parser import parser
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
                    tail_lines=10000)

                container_logs = logs.strip("b'\"").encode().decode("unicode_escape").splitlines()


                for log in container_logs:
                    parsed_log = parser(log)
                    
                    if parsed_log == None:
                        continue

                    # Top n IP Addresses by request count
                    ClientHost = parsed_log["ClientHost"]
                    
                    client_ip_hits = ip_hits.get(ClientHost)
                    is_client_in_ip_hits = bool(client_ip_hits)

                    if is_client_in_ip_hits:
                        updated_client_ip_hits = client_ip_hits + 1
                        ip_hits.update(
                            {ClientHost: updated_client_ip_hits}
                        )
                    else:
                        ip_hits.update({
                            ClientHost: 1
                        })

                    # Request count per status code
                    DownstreamStatus = parsed_log["DownstreamStatus"]

                    status_count = statuses_count.get(DownstreamStatus)
                    is_status_in_status_count = bool(status_count)

                    if is_status_in_status_count:
                        updated_status_count = status_count + 1
                        statuses_count.update(
                            {DownstreamStatus: updated_status_count}
                        )
                    else:
                        statuses_count.update({
                            DownstreamStatus: 1
                        })

                    # Requested Endpoints
                    RequestPath = parsed_log["RequestPath"]

                    request_path = request_path_count.get(RequestPath)
                    is_request_path_in_request_path_count = bool(request_path)

                    if is_request_path_in_request_path_count:
                        updated_request_path = request_path + 1
                        request_path_count.update(
                            {RequestPath: updated_request_path}
                        )
                    else:
                        request_path_count.update({
                            RequestPath: 1
                        })
                    # Request address     
                    RequestAddr= parsed_log["RequestAddr"]

                    request_addr = request_addr_count.get(RequestAddr)
                    is_request_addr_in_request_addr_count = bool(request_addr)

                    if is_request_addr_in_request_addr_count:
                        updated_request_addr = request_addr + 1
                        request_addr_count.update(
                            {RequestAddr: updated_request_addr}
                        )
                    else:
                        request_addr_count.update({
                            RequestAddr: 1
                        })




            except Exception as e:
                print(f"Error getting logs for pod {pod_name}, container {container_name}: {e}")
 

    def get_second_value(item):
        return item[1]
    
    #IP HITS
    sorted_ip_hits = sorted(ip_hits.items(), key=get_second_value, reverse=True)

    print("TOP 10 HIT COUNTS IP...")
    print("-----------------------")
    
    for i,entry in enumerate(sorted_ip_hits, start=1):
        if i <= 10:
            print(f'{i}. {entry[0]:<16} | {entry[1]} {"hit" if entry[1] == 1 else "hits"}')

    # STATUS CODES
    sorted_statuses_count = sorted(statuses_count.items(), key=get_second_value, reverse=True)
    print("\n")
    print("TOP STATUS CODES...")
    print("-----------------------")
    
    for i,entry in enumerate(sorted_statuses_count, start=1):
        print(f'{i}. {entry[0]:<6} | {entry[1]}')
    
    # REQUEST PATHS
    sorted_request_path_count = sorted(request_path_count.items(), key=get_second_value, reverse=True)
    print("\n")
    print("TOP 10 Request Paths...")
    print("-----------------------")
    
    for i,entry in enumerate(sorted_request_path_count, start=1):
        if i <= 10:
            print(f'{i}. {entry[0]:<6} | {entry[1]}')

    # REQUEST ADDR
    sorted_request_addr_count = sorted(request_addr_count.items(), key=get_second_value, reverse=True)
    print("\n")
    print("TOP 10 Request addresses...")
    print("-----------------------")
    
    for i,entry in enumerate(sorted_request_addr_count, start=1):
        if i <= 10:
            print(f'{i}. {entry[0]:<6} | {entry[1]}')
