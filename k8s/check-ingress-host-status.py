import subprocess
import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_hosts():
    ingress_hosts = []
    command = ["kubectl","get","ingress","-A","-o","json"]
    
    try:
        print("Getting available hosts data from kubernetes api...")
        response = subprocess.run(command, capture_output=True, text=True)
        if response.returncode != 0:
            print("Something went wrong with kubernetes command, terminating...")
            return 1
        data = json.loads(response.stdout)

        for ingress in data["items"]:
            for rules in ingress["spec"]["rules"]:
                ingress_hosts.append(rules["host"])

    except Exception as e:
        print("Something went wrong.")
        print(e)
        return
    print(f'Fetched {len(ingress_hosts)} hosts from kubernetes...')
    check_hosts(ingress_hosts)

def check_hosts(ingress_hosts):
    healthy_hosts = []
    unhealthy_hosts = []

    print("Starting testing...")
    for host in ingress_hosts:
        try:
            url = f'https://{host}'
            res = requests.get(url, verify=False, timeout=5)
            
            print(f"CHECKING {host} --> {res.status_code}")

            checked_host = {"host": host, "status": res.status_code}
            if res.status_code != 200:
                unhealthy_hosts.append(checked_host)
            else:
                healthy_hosts.append(checked_host)

        except Exception as e:
            checked_host = {"host": host, "status": None, "error": e}
            unhealthy_hosts.append(checked_host)
            print(e)
            
    print("\n")
    print('---RESULTS---')
    print(f"Healthy hosts: {len(healthy_hosts)} | Unhealthy hosts: {len(unhealthy_hosts)}")

    if len(unhealthy_hosts) > 0:
        print("Printing unhealthy hosts:")
        for host in unhealthy_hosts:
            print(f'{host["host"]} {host["error"]}')
get_hosts()