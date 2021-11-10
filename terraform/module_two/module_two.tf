module "module_two_one" {
  source                    = "./module_two_one"
  account_id                = var.account_id
  vpc_id                    = var.vpc_id
  cidr_block                = var.cidr_block
  subnet_ids                = var.subnet_ids
  default_security_group_id = var.default_security_group_id
  terraform_bucket          = var.terraform_bucket
  repository                = var.repository
}
