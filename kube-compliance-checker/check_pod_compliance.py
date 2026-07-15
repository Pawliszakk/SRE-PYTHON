from models import Finding

def check_pod_compliance(pod, findings):
    for container in pod.spec.containers:
        requests = container.resources.requests
        limits = container.resources.limits

        if requests:
            requests_cpu = requests.get("cpu")
            requests_memory = requests.get("memory")
            if not requests_cpu:
                print("Są requesty bez cpu")
            if not requests_memory:
                print("Są requesty memory!")

        else:

            print(requests)
            print("NIE MA REQUESTOW!!!")
            
            print(requests_cpu)
            finding = Finding(
                pod.metadata.namespace,
                pod.metadata.name,
                container.name,
                "Resources",
                "RES-001",
                "HIGH",
                requests,
                "{'cpu': 'CPU_VALUE', 'memory': 'MEMORY_VALUE'}"

            )
            findings.append(finding)

        if limits:
            limits_cpu = limits.get("cpu")
            limits_memory = limits.get("memory")

            if not limits_cpu:
                print("Są limity bez CPU!!")

            if not limits_memory:
                print("Są limity bez MEMORY!!!")


        else:
            print("NIE MA LIMITOW!!!")
        #HIGH



        #LOW

        #INFO

        #OK