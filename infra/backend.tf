terraform {
  backend "s3" {
    bucket = "proto-dw-infra"
    key    = "proto-dw/terraform.tfstate"
    region = "us-east-2"

    encrypt = true
  }
}
