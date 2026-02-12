# =============================================================================
# GCP Terraform Provider & Backend Configuration
# =============================================================================
# Celes production pattern: Google provider 7.0.1, GCS backend with empty
# config for flexibility (pass bucket/prefix at terraform init time).
# =============================================================================

terraform {
  required_version = ">= 1.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.0.1"
    }
  }

  # Empty backend config -- pass bucket and prefix at init time:
  #   terraform init -backend-config="bucket=STATE_BUCKET" -backend-config="prefix=ENV"
  backend "gcs" {}
}

# -----------------------------------------------------------------------------
# Provider Configuration
# -----------------------------------------------------------------------------

provider "google" {
  project = var.project_id
  region  = var.region
}

# -----------------------------------------------------------------------------
# Variables
# -----------------------------------------------------------------------------

variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The default GCP region for resources"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "Environment name (dev, staging, production)"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "Environment must be one of: dev, staging, production."
  }
}

# -----------------------------------------------------------------------------
# Common Labels
# -----------------------------------------------------------------------------

locals {
  common_labels = {
    environment = var.environment
    managed_by  = "terraform"
    project     = var.project_id
  }
}

# -----------------------------------------------------------------------------
# Data Sources
# -----------------------------------------------------------------------------

data "google_project" "current" {
  project_id = var.project_id
}

# -----------------------------------------------------------------------------
# Outputs
# -----------------------------------------------------------------------------

output "project_id" {
  description = "The GCP project ID"
  value       = var.project_id
}

output "project_number" {
  description = "The GCP project number"
  value       = data.google_project.current.number
}

output "region" {
  description = "The configured region"
  value       = var.region
}
