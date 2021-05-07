# terraform_template

## Terraform
A template of terraform code that retrieves key info about existing infrastructure.  
Any changes made to the infrastructure-as-code resources must be built and deployed using the following instructions:

1. Install AWS CLI version 2 [download here](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
1. Install Terraform `~> 0.15` [download here](https://releases.hashicorp.com/terraform/)
1. Configuration
   1. Update `configuration.tf` terraform.backend.s3.key
   1. Update `variables.tf` repo_name.default
   1. Create a config file `terraform/_{env}.conf` with the following line    
      `bucket = "{env}.{organization}.platform.terraform"`
1. Use the AWS Console to verify the Terraform backend bucket is setup
   1. Name = `s3://{env}.{organization}.platform.terraform`
   1. Bucket Versioning = `Enabled`
   1. Default encryption = `Enabled`
1. Use Terraform to deploy the infrastructure-as-code
   1. Navigate to the root module directory `terraform`
   1. Run `terraform init -backend-config=_{env}.conf`
   1. Run `terraform plan`
      1. Enter the environment `dev, test, stage or prod`
      1. Check the plan, continue if it is correct
   1. Run `terraform apply`
      1. Enter the environment `dev, test, stage or prod`
      1. Check the plan, enter `yes` if it is correct

### Notes
1. Terraform 0.13 upgrade  
   If you get this error:  
   ```
   Error: Invalid legacy provider address
   This configuration or its associated state refers to the unqualified provider "aws".
   You must complete the Terraform 0.13 upgrade process before upgrading to later versions.
   ```
   Then run:  
   `terraform state replace-provider registry.terraform.io/-/aws hashicorp/aws`