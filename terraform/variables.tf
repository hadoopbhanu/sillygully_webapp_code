variable "vpc_name" {
  description = "Name of the VPC"
  type        = string
}

variable "project_name" {
  description = "GCP Project ID"
  type        = string
}

variable "subnet_names" {
  description = "List of subnet names"
  type        = list(string)
}

variable "subnet_cidrs" {
  description = "List of CIDR ranges for the subnets"
  type        = list(string)
}

variable "subnet2_range" {
  description = "The IP range of the second subnet"
  type        = string
}

variable "sql_instance_name" {
  description = "The name of the Cloud SQL instance"
  type        = string
}

variable "sql_admin_user" {
  description = "The admin username for the Cloud SQL instance"
  type        = string
  sensitive = true
}

variable "sql_admin_pass" {
  description = "The admin password for the Cloud SQL instance"
  type        = string
  sensitive   = true
}

variable "sql_proxy_service_account" {
  description = "The service account used by the Cloud SQL Proxy"
  type        = string
}