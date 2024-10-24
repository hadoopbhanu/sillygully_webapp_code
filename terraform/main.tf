
variable "project_name" {}
variable "vpc_name" {}
variable "subnet1_name" {}
variable "subnet2_name" {}
variable "subnet1_range" {}
variable "subnet2_range" {}
variable "sql_instance_name" {}
variable "sql_admin_user" {}
variable "sql_admin_pass" {}
variable "sql_proxy_service_account" {}

# VPC creation
resource "google_compute_network" "vpc_network" {
  name       = var.vpc_name
  auto_create_subnetworks = false
  project    = var.project_name
}

# Subnets creation
resource "google_compute_subnetwork" "subnets" {
  count       = length(var.subnet_names)

  name        = var.subnet_names[count.index]
  ip_cidr_range = var.subnet_cidrs[count.index]
  region      = "us-central1"  # You can hardcode or pass it via another variable
  network     = google_compute_network.vpc_network.id
  project     = var.project_name
}

# Subnet 2
resource "google_compute_subnetwork" "subnet2" {
  name          = var.subnet2_name
  ip_cidr_range = var.subnet2_range
  region        = "asia-south1"
  network       = google_compute_network.vpc_network.name
}

# Cloud SQL instance
resource "google_sql_database_instance" "default" {
  name             = var.sql_instance_name
  region           = "us-central1"
  database_version = "MYSQL_8_0"
  settings {
    tier                        = "db-n1-standard-2"
    availability_type            = "REGIONAL"
    backup_configuration {
      enabled = true
    }
    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.vpc_network.id
    }
  }
}

# SQL User
resource "google_sql_user" "default" {
  instance   = google_sql_database_instance.default.name
  name       = var.sql_admin_user
  password   = var.sql_admin_pass
}

# IAM Service Account for SQL Proxy
resource "google_service_account" "sql_proxy" {
  account_id   = var.sql_proxy_service_account
  display_name = "SQL Proxy Service Account"
}

# IAM Binding to allow service account to access SQL
resource "google_project_iam_member" "sql_proxy_client_role" {
  project = var.project_name
  member  = "serviceAccount:${google_service_account.sql_proxy.email}"
  role    = "roles/cloudsql.client"
}

# Firewall rules for SSH
resource "google_compute_firewall" "allow_ssh" {
  name    = "allow-ssh"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]
}

# Cloud Router for NAT
resource "google_compute_router" "nat_router" {
  name    = "nat-router"
  network = google_compute_network.vpc_network.name
  region  = "us-central1"
}

# Cloud NAT Configuration
resource "google_compute_router_nat" "nat_config" {
  name                     = "nat-config"
  router                   = google_compute_router.nat_router.name
  region                   = google_compute_router.nat_router.region
  nat_ips                  = []
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
}