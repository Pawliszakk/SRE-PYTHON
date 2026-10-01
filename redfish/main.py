import redfish

redfish_hosts = ["8000"]


def print_system_info(data):
    print(f"Server: {data['Manufacturer']} {data['Name']} {data['Model']}")
    print(f"  Power:     {data['PowerState']}")
    print(f"  State:     {data['Status']['State']}")
    print(f"  Health:    {data['Status']['Health']}")
    print(f"  Rollup:    {data['Status']['HealthRollup']}")
    print(f"  CPU:       {data['ProcessorSummary']['Status']['Health']}")
    print(f"  RAM:       {data['MemorySummary']['Status']['Health']}")


def print_sensor_info(c, sensors):
    print("Sensors:")

    for m in sensors["Members"]:

        s = c.get(m["@odata.id"]).dict
        if s.get("Reading") is None:
            continue
        health = s.get("Status", {}).get("Health")
        print(f"  {s['Name']:<25} {s.get('Reading')} {s.get('ReadingUnits')}  [{health}]")


for host in redfish_hosts:

    host_url = f'http://localhost:{host}'

    try:
        c = redfish.redfish_client(base_url=host_url, default_prefix="/redfish/v1")

        systems = c.get("/redfish/v1/Systems").dict
        system_path = systems["Members"][0]['@odata.id']
        system = c.get(system_path)

        chassis = c.get("/redfish/v1/Chassis/1U").dict
        sensors = c.get(chassis["Sensors"]["@odata.id"]).dict

        print_system_info(system.dict)
        print_sensor_info(c, sensors) 


        print_system_info(system.dict)
    except Exception as e:
        print(e)
        continue



