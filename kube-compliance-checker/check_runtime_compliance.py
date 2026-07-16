from models import Finding

def check_runtime_compliance(pod, findings):

    for status in pod.status.container_statuses:

        last_state = status.last_state
        

        if last_state and last_state.terminated:
            if last_state.terminated.reason == "OOMKilled":
                finding = Finding(
                    pod.metadata.namespace,
                    pod.metadata.name,
                    status.name,
                    "Runtime",
                    "RT-001",
                    "HIGH",
                    {"reason": "OOMKilled", "exit_code": last_state.terminated.exit_code},
                    {"reason": "not OOMKilled"},
                    "Container was OOMKilled"
                )
                findings.append(finding)