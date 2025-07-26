provider "aws" {
  region = "ap-south-1"
}

resource "aws_instance" "web" {
  ami           = "ami-12345678"
  instance_type = "t2.micro"
  count         = 2
  tags = {
    Name = "DemoWebServer"
  }
}
