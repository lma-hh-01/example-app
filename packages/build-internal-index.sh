#!/usr/bin/env bash
# Rebuilds the internal package company-utils and stores it in the internal package index.
# Only needed when packages/src/company-utils changes. The result is committed,
# so that the build in the pipeline works without a package registry of its own.
set -euo pipefail

PACKAGES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INDEX_DIR="$PACKAGES_DIR/internal/company-utils"
PYTHON_IMAGE="docker.io/library/python:3.14-slim@sha256:af8a5aa14780025dbfbcfbc81bd8a91ebd87711dd5b0f48ed71090949dd7cb1d"

rm -rf "$INDEX_DIR"
mkdir -p "$INDEX_DIR"

docker run --rm -v "$PACKAGES_DIR:/packages" -w /packages "$PYTHON_IMAGE" \
  pip wheel --quiet --disable-pip-version-check --no-deps ./src/company-utils -w ./internal/company-utils

# pip expects one index.html per package with links to the files (Simple Repository API).
{
  echo "<!DOCTYPE html>"
  echo "<html><body>"
  for wheel in "$INDEX_DIR"/*.whl; do
    name="$(basename "$wheel")"
    echo "<a href=\"$name\">$name</a>"
  done
  echo "</body></html>"
} > "$INDEX_DIR/index.html"

echo "Internal index updated: $INDEX_DIR"
