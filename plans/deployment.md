# Deployment Plan

### Deployment Build Environment
- Windows or Linux
- AWS CLI [version 2](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- Terraform [1.0.10](https://releases.hashicorp.com/terraform/1.0.10/)
  - Update from 1.0.9
- AWS Provider [3.64.0](https://registry.terraform.io/providers/hashicorp/aws/3.64.0)
  - Update from 3.61.0

### Deployment of [v0.0.1](https://github.com/USDOT-SDC/terraform_aws_template/tree/0.0.1)
1. Install AWS CLI version 2 [download here](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
1. Install Terraform `~> 1.0` [download here](https://releases.hashicorp.com/terraform/)
1. Configuration
   1. Update `terraform/configuration.tf`
      1. terraform.backend.s3.region
      1. terraform.backend.s3.key
   1. Update `terraform/variables.tf`
   1. As needed create or update `terraform/conf/{env}.conf` with the following line    
      `bucket = "{env}.sdc.dot.gov.platform.terraform"`
1. Use the AWS Console to verify the AWS Systems Manager Parameter Store is set up
   1. Name = `environment`
   1. Description = `The environment of this AWS account (dev, test, stage or prod)`
   1. Tier = `Standard`
   1. Type = `String`
   1. Data type = `text`
   1. Value = As appropriate: `dev`, `test`, `stage` or `prod`
1. Use the AWS Console to verify the Terraform backend bucket is set up
   1. Name = `{env}.sdc.dot.gov.platform.terraform`
   1. Bucket Versioning = `Enabled`
   1. Default encryption = `Enabled`
1. Pull tag [0.0.1](https://github.com/USDOT-SDC/terraform_aws_template/tree/0.0.1) from the repo.
1. If any Lambda resources have been added or changed, run `build_lambda_deployment_packages.py`
1. Use Terraform to deploy the infrastructure-as-code
   1. Navigate to the root module directory `terraform`
   1. Run `terraform init -backend-config='conf/{env}.conf'`
   1. Run `terraform init -version` to verify the installed versions
      1. If the versions need to be updated, delete `.terraform` and `.terraform.lock.hcl` and return to step 8.ii
   1. Run `terraform plan -out=tfplan_v0.0.1`
      1. Check the plan, continue if it is correct
      1. Ensure there are no changes to out of scope teams
      1. If the plan file exists, it will overwrite it  
         (change the plan file name if you need to rerun `terraform plan`)
   1. Run `terraform apply tfplan_v0.0.1`
      1. This command uses the plan file specified  
         (it will not ask for conformation to proceed)
      1. If needed, run `terraform show tfplan_v0.0.1` to check the plan
   1. Attach `tfplan_v0.0.1` to the CRB
   1. Execute the [Test Plan](https://github.com/USDOT-SDC/terraform_aws_template/blob/0.0.1/plans/test.md) to ensure the deployment was successful
