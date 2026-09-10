# Remote state in S3, with a DynamoDB table for state locking.
#
# Terraform cannot create its own backend, so the bucket and table must exist
# first. Create them once (backend blocks can't use variables, hence the
# hard-coded values below — keep them in sync):
#
#   aws s3api create-bucket --bucket vns-tfstate-change-me --region eu-central-1 \
#       --create-bucket-configuration LocationConstraint=eu-central-1
#   aws s3api put-bucket-versioning --bucket vns-tfstate-change-me \
#       --versioning-configuration Status=Enabled
#   aws dynamodb create-table --table-name vns-tflock \
#       --attribute-definitions AttributeName=LockID,AttributeType=S \
#       --key-schema AttributeName=LockID,KeyType=HASH \
#       --billing-mode PAY_PER_REQUEST --region eu-central-1

terraform {
  backend "s3" {
    bucket         = "vns-tfstate-change-me" # must be globally unique
    key            = "infra/terraform.tfstate"
    region         = "eu-central-1"
    dynamodb_table = "vns-tflock"
    encrypt        = true
  }
}
