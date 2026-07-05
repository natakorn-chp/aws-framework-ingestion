terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Backend intentionally left empty (partial configuration).
  # Supply real values at init time with:
  #   terraform init -backend-config=backend.hcl
  # See backend.hcl.example for the expected keys.
  backend "s3" {}
}
