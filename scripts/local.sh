#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

cleanup() {
  echo "Stopping preview..."
  docker stop jekyll-preview 2>/dev/null || true
  docker rm jekyll-preview 2>/dev/null || true
}
trap cleanup EXIT

cleanup

echo "Starting Jekyll devcontainer..."
docker run -d --name jekyll-preview \
  -p 4444:4444 \
  -w /workspaces \
  -v "$ROOT_DIR:/workspaces" \
  mcr.microsoft.com/devcontainers/jekyll:latest \
  bundle exec jekyll serve --host 0.0.0.0 --port 4444

sleep 10

echo "Server running at http://localhost:4444"
docker logs -f jekyll-preview
