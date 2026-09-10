variable "region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "eu-central-1" # Frankfurt
}

variable "project_name" {
  description = "Name prefix for all resources"
  type        = string
  default     = "vns"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "cluster_version" {
  description = "Kubernetes version for EKS (check which versions EKS currently supports)"
  type        = string
  default     = "1.31"
}

variable "node_instance_type" {
  description = "EC2 instance type for the EKS worker nodes"
  type        = string
  default     = "t3.medium"
}

variable "node_min_size" {
  description = "Minimum number of worker nodes"
  type        = number
  default     = 1
}

variable "node_max_size" {
  description = "Maximum number of worker nodes"
  type        = number
  default     = 3
}

variable "node_desired_size" {
  description = "Desired number of worker nodes"
  type        = number
  default     = 2
}

variable "postgres_version" {
  description = "Major PostgreSQL engine version"
  type        = string
  default     = "16"
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "db_name" {
  description = "Initial database name"
  type        = string
  default     = "vns"
}

variable "db_username" {
  description = "RDS master username"
  type        = string
  default     = "vns"
}

variable "db_password" {
  description = "RDS master password — supply via TF_VAR_db_password or a tfvars file kept out of git"
  type        = string
  sensitive   = true
}
