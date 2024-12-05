
#AWS Provider with profile Stage account
provider "aws" {
  region = var.REGION
  alias = "deployment-eu"   # Specify a default AWS region here
  profile = "belinapayroll-${var.STAGE}"
}


resource "null_resource" "python" {
  provisioner "local-exec" {
    command = "pip install -r requirements.txt -t python_lib/python"
  }
}

resource "aws_lambda_layer_version" "lambda_python_layer" {
  layer_name          = "python_dependency-${var.STAGE}"
  filename            = data.archive_file.python_layer_code_zip.output_path
  provider=aws.deployment-eu
}


data "archive_file" "python_layer_code_zip" {
  type        = "zip"
  source_dir  = "./python_lib"
  output_path = "./python.zip"
  depends_on = [resource.null_resource.python]
}

#storing in SSM
resource "aws_ssm_parameter" "s3_bucket" {
  name  = "/COMMON_LIB_ARN_PYTHON"
  overwrite = true
  type  = "String"
  value = aws_lambda_layer_version.lambda_python_layer.arn
  provider = aws.deployment-eu
}
