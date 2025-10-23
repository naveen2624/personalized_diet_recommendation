# Create VPC
resource "aws_vpc" "diet_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "diet-vpc"
  }
}

# Create Public Subnet 1
resource "aws_subnet" "public_subnet_1" {
  vpc_id                  = aws_vpc.diet_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "ap-south-1a"
  tags = {
    Name = "diet-public-subnet-1"
  }
}

# Create Public Subnet 2
resource "aws_subnet" "public_subnet_2" {
  vpc_id                  = aws_vpc.diet_vpc.id
  cidr_block              = "10.0.2.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "ap-south-1b"
  tags = {
    Name = "diet-public-subnet-2"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "diet_igw" {
  vpc_id = aws_vpc.diet_vpc.id
  tags = {
    Name = "diet-igw"
  }
}

# Route Table
resource "aws_route_table" "diet_public_rt" {
  vpc_id = aws_vpc.diet_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.diet_igw.id
  }

  tags = {
    Name = "diet-public-rt"
  }
}

# Associate Subnets with Route Table
resource "aws_route_table_association" "pub_subnet_1" {
  subnet_id      = aws_subnet.public_subnet_1.id
  route_table_id = aws_route_table.diet_public_rt.id
}

resource "aws_route_table_association" "pub_subnet_2" {
  subnet_id      = aws_subnet.public_subnet_2.id
  route_table_id = aws_route_table.diet_public_rt.id
}
