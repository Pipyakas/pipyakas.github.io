#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cleanup() {
  echo "Stopping preview..."
  docker stop jekyll-preview 2>/dev/null || true
  docker rm jekyll-preview 2>/dev/null || true
}
trap cleanup EXIT

cleanup

echo "Starting Jekyll devcontainer..."
docker run -d --name jekyll-preview \
  -p 4000:4000 \
  -w /workspaces \
  -v "$SCRIPT_DIR:/workspaces" \
  mcr.microsoft.com/devcontainers/jekyll:latest \
  bundle exec jekyll serve --host 0.0.0.0 --port 4000

sleep 10

echo "Server running at http://localhost:4000"
docker logs -f jekyll-preview
