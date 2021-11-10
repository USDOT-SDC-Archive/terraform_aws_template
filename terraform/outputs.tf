// root
output "root_environment" {
  value = local.environment
  sensitive = true
}

output "root_repository" {
  value = var.repository
}

output "root_account_id" {
  value = local.account_id
}

output "module" {
  value = local.module
}

// module one
output "module_one_outputs" {
  value = module.module_one
}

// module two
output "module_two_outputs" {
  value = module.module_two
}
