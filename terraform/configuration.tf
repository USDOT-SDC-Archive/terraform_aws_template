terraform {
  required_version = "~> 0.15"
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 3.39"
    }
  }
  backend "s3" {
    region = "us-east-1"
    // Don't forget to change this to {repo_name}/terraform/terraform.tfstate
    key = "terraform_aws_template/terraform/terraform.tfstate"
  }
}

provider "aws" {
  region = var.region
  profile = "sdc"
}

variable "env" {
  type = string
  description = "Weyland-Yutani Corporation. Building Better Worlds. What would you like to terraform: dev, test, stage or prod?"
}

variable "region" {
  type = string
  description = "AWS region"
  default = "us-east-1"
}
