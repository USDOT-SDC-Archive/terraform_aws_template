// root
output "root_env" {
  value = var.env
}

output "root_repo_name" {
  value = var.repo_name
}

output "root_region" {
  value = var.region
}

output "root_account_id" {
  value = local.account_id
}

output "root_vpc_id" {
  value = local.network.vpc_id
}

output "root_subnet_ids" {
  value = local.network.subnet_ids
}

output "root_default_security_group_id" {
  value = local.network.default_security_group_id
}

// module one
output "module_one_outputs" {
  value = module.module_one
}

// module two
output "module_two_outputs" {
  value = module.module_two
}
