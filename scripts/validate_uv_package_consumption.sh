#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cache_dir="${UV_CACHE_DIR:-/tmp/uv-cache}"
tmp_root="$(mktemp -d "${TMPDIR:-/tmp}/clockodo-api-lib-uv-XXXXXX")"

cleanup() {
    rm -rf "$tmp_root"
}

trap cleanup EXIT

wheel_project="$tmp_root/wheel-consumer"
path_project="$tmp_root/path-consumer"
editable_project="$tmp_root/editable-consumer"

echo "[1/7] Building distribution artifacts"
UV_CACHE_DIR="$cache_dir" uv build --project "$repo_root"

wheel_path="$(find "$repo_root/dist" -maxdepth 1 -type f -name 'clockodo_api_lib-*.whl' | sort | tail -n 1)"

if [[ -z "$wheel_path" ]]; then
    echo "No wheel found under $repo_root/dist" >&2
    exit 1
fi

echo "[2/7] Creating wheel-based consumer project"
UV_CACHE_DIR="$cache_dir" uv init --bare --no-workspace --no-description --vcs none "$wheel_project"

echo "[3/7] Installing built wheel"
UV_CACHE_DIR="$cache_dir" uv add --project "$wheel_project" "$wheel_path"
UV_CACHE_DIR="$cache_dir" uv run --project "$wheel_project" python -c "from clockodo_api_lib import ClockodoClient; assert ClockodoClient.__name__ == 'ClockodoClient'"

echo "[4/7] Creating local-path consumer project"
UV_CACHE_DIR="$cache_dir" uv init --bare --no-workspace --no-description --vcs none "$path_project"

echo "[5/7] Installing local path dependency"
UV_CACHE_DIR="$cache_dir" uv add --project "$path_project" "$repo_root"
UV_CACHE_DIR="$cache_dir" uv run --project "$path_project" python -c "from clockodo_api_lib import ClockodoClient; assert ClockodoClient.__name__ == 'ClockodoClient'"

echo "[6/7] Creating editable consumer project"
UV_CACHE_DIR="$cache_dir" uv init --bare --no-workspace --no-description --vcs none "$editable_project"

echo "[7/7] Installing editable local dependency"
UV_CACHE_DIR="$cache_dir" uv add --project "$editable_project" --editable "$repo_root"
UV_CACHE_DIR="$cache_dir" uv run --project "$editable_project" python -c "from clockodo_api_lib import ClockodoClient; assert ClockodoClient.__name__ == 'ClockodoClient'"

echo "Validated wheel, local path, and editable local installs."
