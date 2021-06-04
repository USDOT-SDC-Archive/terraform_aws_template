// Use root.tf to pull info on existing resources and call modules
data "aws_caller_identity" "current" {}

data "aws_ssm_parameter" "environment" {
  name = "environment"
}

data "aws_vpcs" "public" {
  // Get a list of vpcs with tag: Network = Public tag
  tags = {
    Network = "Public"
  }
}

data "aws_vpc" "public" {
  // Assumes there is only one public vpc, so get the first one in the list
  id = element(tolist(data.aws_vpcs.public.ids), 0)
}

data "aws_subnet_ids" "public" {
  // Get a list of subnets in the public vpc
  vpc_id = data.aws_vpc.public.id
}

data "aws_security_group" "default" {
  // Get the default security group for the public vpc
  vpc_id = data.aws_vpc.public.id
  name = "default"
}

locals {
  // Setup some local vars for the info pulled above
  environment = data.aws_ssm_parameter.environment
  account_id = data.aws_caller_identity.current.account_id
  network = {
    vpc_id = data.aws_vpc.public.id
    cidr_block = data.aws_vpc.public.cidr_block
    subnet_ids = data.aws_subnet_ids.public.ids
    default_security_group_id = data.aws_security_group.default.id
  }
}

// Call the modules, passing in some of the local vars
module "module_one" {
  source = "./module_one"
  account_id = local.account_id
  vpc_id = local.network.vpc_id
  cidr_block = local.network.cidr_block
  subnet_ids = local.network.subnet_ids
  default_security_group_id = local.network.default_security_group_id
}

module "module_two" {
  source = "./module_two"
  account_id = local.account_id
  vpc_id = local.network.vpc_id
  cidr_block = local.network.cidr_block
  subnet_ids = local.network.subnet_ids
  default_security_group_id = local.network.default_security_group_id
}
