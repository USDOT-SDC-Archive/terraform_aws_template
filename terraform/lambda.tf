resource "aws_lambda_function" "hello-world" {
  function_name = "${var.repository}_hello-world"
  handler       = "lambda_function.lambda_handler"
  s3_bucket     = local.terraform_bucket
  s3_key        = "${var.repository}/lambdas/hello-world.zip"
  role          = aws_iam_role.hello-world_lambda.arn
  runtime       = "python3.9"
  layers        = [aws_lambda_layer_version.pandas-layer.arn]
}

resource "aws_lambda_layer_version" "pandas-layer" {
  layer_name          = "${var.repository}_pandas-layer"
  s3_bucket           = local.terraform_bucket
  s3_key              = "${var.repository}/lambdas/pandas-layer.zip"
  compatible_runtimes = ["python3.8", "python3.9"]
}
