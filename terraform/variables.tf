variable "provider-profile" {
  description = "The terraform provider profile"
  default = "sdc"
}
variable "region" {
  type = string
  description = "AWS region"
  // Also update in: configuration.tf > terraform.backend.region
  default = "us-east-1"
}

variable "repository-url" {
  type = string
  description = "The host, where all this lives"
  default = "https://github.com/USDOT-SDC/"
}

variable "repository" {
  type = string
  description = "The repository, where all this lives"
  // Also update in: configuration.tf > terraform.backend.key
  default = "terraform_aws_template"
}

locals {
  module = basename(abspath(path.module))
}
