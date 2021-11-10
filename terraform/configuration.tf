terraform {
  required_version = "~> 1.0"
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
  backend "s3" {
    // Variables may not be used here.
    // Also update in: variables.tf > variable.region.default
    region = "us-east-1"
    // Also update in: variables.tf > variable.repository.default
    key = "terraform_aws_template/terraform/terraform.tfstate"
  }
}

provider "aws" {
  region = var.region
  profile = var.provider-profile
  default_tags {
    tags = {
      repository-url = var.repository-url
      repository = var.repository
    }
  }
}
