variable "project_name" {
  description = "The name of the GCP project"
  type        = string
}

variable "vpc_name" {
  description = "The name of the VPC network"
  type        = string
}

variable "subnet1_name" {
  description = "The name of the first subnet"
  type        = string
}

variable "subnet2_name" {
  description = "The name of the second subnet"
  type        = string
}

variable "subnet1_range" {
  description = "The IP range of the first subnet"
  type        = string
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