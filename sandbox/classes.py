from models import Finding

servers = []

srv1 = Finding("oskar-srv-01","192.168.0.1")
srv2 = Finding("oskar-srv-02","192.168.0.2")

servers.append(srv1)
servers.append(srv2)

for server in servers:
    print(server.hostname)
