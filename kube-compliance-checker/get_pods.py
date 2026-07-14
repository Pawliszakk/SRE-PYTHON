def get_pods(v1, namespace=None):
    
    pods = None
    if namespace:
        print("namespaced pods load...")
        pods = v1.list_namespaced_pod(namespace)
    
    else:
        print("All pods...")
        pods = v1.list_pod_for_all_namespaces(watch=False)

    return pods