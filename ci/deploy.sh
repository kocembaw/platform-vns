#!/usr/bin/env bash
# Push images (on AWS) and apply the Kubernetes manifests. Run from repo root.
#
#   IMAGE_TAG   image tag (default: short git SHA, or "local")
#   REGISTRY    ECR host, e.g. <acct>.dkr.ecr.eu-central-1.amazonaws.com
#               (leave empty for local / kind — images are already loaded)
#   AWS_REGION  region for ECR login (default: eu-central-1)
#
# Prerequisite: the vns-secret Secret must exist. Locally the template in
# deploy/base/secret.example.yaml is enough; on AWS create it from the RDS
# endpoint (Terraform output rds_address) before running this.
set -euo pipefail

IMAGE_TAG="${IMAGE_TAG:-$(git rev-parse --short HEAD 2>/dev/null || echo local)}"
REGISTRY="${REGISTRY:-}"
AWS_REGION="${AWS_REGION:-eu-central-1}"

if [ -n "$REGISTRY" ]; then
  API_IMAGE="${REGISTRY}/vns-api:${IMAGE_TAG}"
  GENERATOR_IMAGE="${REGISTRY}/vns-generator:${IMAGE_TAG}"

  echo "Logging in to ECR and pushing images..."
  aws ecr get-login-password --region "$AWS_REGION" \
    | docker login --username AWS --password-stdin "$REGISTRY"
  docker push "$API_IMAGE"
  docker push "$GENERATOR_IMAGE"
else
  # Local / kind: images are already present on the cluster nodes.
  API_IMAGE="vns-api:local"
  GENERATOR_IMAGE="vns-generator:local"
fi

echo "Applying manifests..."
kubectl apply -f deploy/base/

# Point the Deployment at the image we just built/pushed, and wait for rollout.
kubectl set image deployment/api "api=${API_IMAGE}"
kubectl rollout status deployment/api --timeout=180s

# Re-run the one-shot seed Job with the right image (Jobs are immutable).
kubectl delete job seed --ignore-not-found
sed "s#image: vns-generator:local#image: ${GENERATOR_IMAGE}#" deploy/job-seed.yaml \
  | kubectl apply -f -

echo "Deploy complete."
