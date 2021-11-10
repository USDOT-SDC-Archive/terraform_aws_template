variable "account_id" {}
variable "vpc_id" {}
variable "cidr_block" {}
variable "subnet_ids" {}
variable "default_security_group_id" {}
variable "terraform_bucket" {}
variable "repository" {}

locals {
  module = basename(abspath(path.module))
}
