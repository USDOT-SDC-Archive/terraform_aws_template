// s3://dev.sdc.dot.gov.platform.terraform/terraform_aws_template/lambdas/module_one/hello-world_one.zip
resource "aws_lambda_function" "hello-world" {
  function_name = "${var.repository}_${local.module}_hello-world"
  handler       = "lambda_function.lambda_handler"
  s3_bucket     = var.terraform_bucket
  s3_key        = "${var.repository}/lambdas/${local.module}/hello-world_one.zip"
  role          = aws_iam_role.hello-world_lambda.arn
  runtime       = "python3.9"
}
