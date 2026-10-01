import redfish

# For this we need to give real data but for this tests we are only going with ports of mock containers on pc
redfish_hosts = ["8000","8001","8002","8003"]


for host in redfish_hosts:

    host_url = f'http://localhost:{host}'

    try:
        c = redfish.redfish_client(base_url=host_url, default_prefix="/redfish/v1")

        r = c.get("/redfish/v1/Chassis/1U")
    except Exception as e:
        print(f'{host_url} is unreachable.')
        continue

    print(r)