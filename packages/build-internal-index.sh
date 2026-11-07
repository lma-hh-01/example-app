#!/usr/bin/env bash
# Baut das interne Paket firma-utils neu und legt es im internen Paketindex ab.
# Nur noetig, wenn sich packages/src/firma-utils aendert. Das Ergebnis wird committet,
# damit der Build in der Pipeline ohne eigene Paket-Registry auskommt.
set -euo pipefail

PACKAGES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INDEX_DIR="$PACKAGES_DIR/internal/firma-utils"
PYTHON_IMAGE="docker.io/library/python:3.14-slim@sha256:af8a5aa14780025dbfbcfbc81bd8a91ebd87711dd5b0f48ed71090949dd7cb1d"

rm -rf "$INDEX_DIR"
mkdir -p "$INDEX_DIR"

docker run --rm -v "$PACKAGES_DIR:/packages" -w /packages "$PYTHON_IMAGE" \
  pip wheel --quiet --disable-pip-version-check --no-deps ./src/firma-utils -w ./internal/firma-utils

# pip erwartet je Paket eine index.html mit Links auf die Dateien (Simple Repository API).
{
  echo "<!DOCTYPE html>"
  echo "<html><body>"
  for wheel in "$INDEX_DIR"/*.whl; do
    name="$(basename "$wheel")"
    echo "<a href=\"$name\">$name</a>"
  done
  echo "</body></html>"
} > "$INDEX_DIR/index.html"

echo "Interner Index aktualisiert: $INDEX_DIR"
