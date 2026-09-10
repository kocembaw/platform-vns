#!/usr/bin/env bash
# Build and tag the container images. Run from the repository root.
#
#   IMAGE_TAG  image tag (default: short git SHA, or "local")
#   REGISTRY   container registry host, e.g. <acct>.dkr.ecr.eu-central-1.amazonaws.com
#              (leave empty for local / kind builds)
set -euo pipefail

IMAGE_TAG="${IMAGE_TAG:-$(git rev-parse --short HEAD 2>/dev/null || echo local)}"
REGISTRY="${REGISTRY:-}"

prefix=""
[ -n "$REGISTRY" ] && prefix="${REGISTRY}/"

echo "Building images (tag: ${IMAGE_TAG}, registry: ${REGISTRY:-none})"

docker build -t "${prefix}vns-api:${IMAGE_TAG}" ./api
docker build -t "${prefix}vns-generator:${IMAGE_TAG}" ./data-generator

# Also tag :local so kind and docker-compose can use them without a registry.
docker tag "${prefix}vns-api:${IMAGE_TAG}" vns-api:local
docker tag "${prefix}vns-generator:${IMAGE_TAG}" vns-generator:local

echo "Build complete."
