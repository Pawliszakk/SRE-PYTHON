#!/usr/bin/env python3
import os
import requests

AK_URL = os.environ["AK_URL"].rstrip("/")
AK_TOKEN = os.environ["AK_TOKEN"]

HEADERS = {
    "Authorization": f"Bearer {AK_TOKEN}",
    "Content-Type": "application/json",
}

GROUPS = [
    "group1"
]


def group_exists(name: str) -> dict | None:
    r = requests.get(
        f"{AK_URL}/api/v3/core/groups/",
        headers=HEADERS,
        params={"name": name},
    )
    r.raise_for_status()
    results = r.json()["results"]
    return results[0] if results else None


def create_group(name: str) -> dict:
    r = requests.post(
        f"{AK_URL}/api/v3/core/groups/",
        headers=HEADERS,
        json={"name": name, "is_superuser": False, "attributes": {}},
    )
    r.raise_for_status()
    return r.json()


def main():
    for name in GROUPS:
        existing = group_exists(name)
        if existing:
            print(f"SKIP  {name} (already exists, pk={existing['pk']})")
            continue
        created = create_group(name)
        print(f"OK    {name} -> pk={created['pk']}")


if __name__ == "__main__":
    main()