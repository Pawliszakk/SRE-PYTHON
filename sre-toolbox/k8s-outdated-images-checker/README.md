# k8s-image-drift-checker

CLI that scans workloads in RKE2 cluster, checks image tags against registry via skopeo, reports outdated ones.

## Steps

1. **Scaffold**
   - `pyproject.toml`, `src/` layout, venv
   - `cli.py` with argparse: `--namespace`, `--label-selector`, `--output text|json`

2. **K8s client** (`k8s_client.py`)
   - Reuse auth pattern from `kube-compliance-checker`
   - List Deployment/StatefulSet/DaemonSet
   - Extract `namespace`, `workload name`, `kind`, `image` per container
   - Split image → `registry`, `repo`, `tag`

3. **Models** (`models.py`)
   - `ImageRef(registry, repo, tag)`
   - `ImageCheckResult(image_ref, latest_tag, status, namespace, workload, kind)`
   - status: `up_to_date | outdated | skipped | error`

4. **Skopeo wrapper** (`skopeo_client.py`)
   - `subprocess.run(["skopeo", "list-tags", f"docker://{registry}/{repo}"], timeout=X, capture_output=True)`
   - parse JSON output
   - add retry + backoff
   - handle errors: timeout, auth fail, repo not found

5. **Version compare** (`version_compare.py`)
   - try parse tags with `packaging.version.Version`
   - not semver (`latest`, sha, date) → `skipped`
   - semver → compare, set `outdated`/`up_to_date`

6. **Report** (`report.py`)
   - text: table (namespace, workload, image, current→latest, status)
   - json: full dump, non-zero exit code if any `outdated`

7. **Tests**
   - `test_version_compare.py` — priority, most edge cases (v-prefix, pre-release, build metadata)
   - mock K8s API + mock subprocess for skopeo, no live calls in unit tests

8. **Wire together, run end-to-end**

## Build order

1. CLI skeleton + hardcoded fake data, no K8s/skopeo yet — get flow working
2. K8s client — real cluster data, just print image list
3. Skopeo wrapper — test manually against 1-2 images
4. Version compare — with tests
5. Wire full pipeline + report
6. pytest coverage