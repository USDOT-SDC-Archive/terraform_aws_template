# terraform_aws_template

## Terraform
A template of terraform code that retrieves key info about existing infrastructure.  
Any changes made to the infrastructure-as-code resources must be built and deployed using the following instructions:

1. Install AWS CLI version 2 [download here](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
1. Install Terraform `~> 0.15` [download here](https://releases.hashicorp.com/terraform/)
1. Configuration
   1. Update `terraform/configuration.tf`
      1. terraform.backend.s3.region and key
      1. terraform.backend.s3.key
   1. Update `terraform/variables.tf`
   1. As needed create or update `terraform/_{env}.conf` with the following line    
      `bucket = "{env}.{organization}.platform.terraform"`
1. Use the AWS Console to verify the AWS Systems Manager Parameter Store is set up
   1. Name = `environment`
   1. Description = `The environment of this AWS account (dev, test, stage or prod)`
   1. Tier = `Standard`
   1. Type = `String`
   1. Data type = `text`
   1. Value = As appropriate: `dev`, `test`, `stage` or `prod`
1. Use the AWS Console to verify the Terraform backend bucket is set up
   1. Name = `{env}.{organization}.platform.terraform`
   1. Bucket Versioning = `Enabled`
   1. Default encryption = `Enabled`
1. Use Terraform to deploy the infrastructure-as-code
   1. Navigate to the root module directory `terraform`
   1. Run `terraform init -backend-config=_{env}.conf`
   1. Run `terraform plan`
      1. Check the plan, continue if it is correct
   1. Run `terraform apply`
      1. Check the plan, enter `yes` if it is correct
