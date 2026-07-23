from connect_to_k8s import connect_to_k8s
from models import Entry
import subprocess
import json

def main():

    container_images = []

    v1 = connect_to_k8s()

    pods = v1.list_pod_for_all_namespaces()

    for pod in pods.items:
        pod_name = pod.metadata.name
        pod_namespace = pod.metadata.namespace

        for container in pod.spec.containers:
            if "rancher" in container.image:
                continue

            is_duplicate = False

            for entry in container_images:
                if entry.image == container.image:
                    is_duplicate = True
                    break

            if is_duplicate:
                continue

            container_images.append(Entry(
                pod=pod_name,
                namespace=pod_namespace,
                container=container.name,
                image=container.image
            ))

    for i,entry in enumerate(container_images, start=1):


        if i > 1:
            continue
# ZROBIC TUTAJ SKOPEO TESTING,
# Wyrzucić tag z obrazu
# Skopeo list-tags
# z listy json skopeo wyciagnac latest tag (ostatni)
# dopisac do entry 

        image_without_tag = entry.image.split(":",1)[0]


        command = ["skopeo","list-tags",f"docker://{image_without_tag}"]
        result = subprocess.run(command, capture_output=True, text=True)
        data = json.loads(result.stdout)

        image_tags = data["Tags"]
## SORT TAGS
        print(image_tags[0])
if __name__ == "__main__":
    main()