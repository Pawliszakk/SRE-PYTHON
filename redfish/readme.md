podman run --rm -d --name redfish-mock-0 -p 8000:8000 docker.io/dmtf/redfish-mockup-server:latest

podman run --rm -d --name redfish-mock-1 -p 8001:8000 docker.io/dmtf/redfish-mockup-server:latest

podman run --rm -d --name redfish-mock-2 -p 8002:8000 docker.io/dmtf/redfish-mockup-server:latest

podman run --rm -d --name redfish-mock-3 -p 8003:8000 docker.io/dmtf/redfish-mockup-server:latest