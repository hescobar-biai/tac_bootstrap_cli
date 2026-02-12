# =============================================================================
# Cloud Run Service Definition
# =============================================================================
# Usage: Deploy a containerized service to Cloud Run with a dedicated service
# account, Secret Manager integration, health checks, and autoscaling.
# Requires: main.tf for provider and variable configuration.
# =============================================================================

# -----------------------------------------------------------------------------
# Variables
# -----------------------------------------------------------------------------

variable "service_name" {
  description = "Name of the Cloud Run service"
  type        = string
}

variable "container_image" {
  description = "Full container image URI (e.g., us-central1-docker.pkg.dev/project/repo/image:tag)"
  type        = string
}

variable "container_port" {
  description = "Port the container listens on"
  type        = number
  default     = 8080
}

variable "cpu_limit" {
  description = "CPU limit (e.g., '1000m' for 1 vCPU, '2000m' for 2 vCPUs)"
  type        = string
  default     = "1000m"
}

variable "memory_limit" {
  description = "Memory limit (e.g., '512Mi', '1Gi', '2Gi')"
  type        = string
  default     = "512Mi"
}

variable "min_instances" {
  description = "Minimum number of instances (0 allows scale to zero)"
  type        = number
  default     = 0
}

variable "max_instances" {
  description = "Maximum number of instances"
  type        = number
  default     = 10
}

variable "env_vars" {
  description = "Plain-text environment variables as a map"
  type        = map(string)
  default     = {}
}

variable "secret_env_vars" {
  description = "Secret environment variables as a map of name to Secret Manager secret ID"
  type        = map(string)
  default     = {}
}

variable "vpc_connector" {
  description = "VPC connector name for private network access (null to disable)"
  type        = string
  default     = null
}

variable "allow_unauthenticated" {
  description = "Allow unauthenticated access to the service"
  type        = bool
  default     = false
}

variable "max_request_timeout" {
  description = "Maximum request timeout in seconds"
  type        = string
  default     = "300s"
}

variable "concurrency" {
  description = "Maximum concurrent requests per instance"
  type        = number
  default     = 80
}

# -----------------------------------------------------------------------------
# Service Account
# -----------------------------------------------------------------------------

resource "google_service_account" "cloud_run" {
  account_id   = "${var.service_name}-runner"
  display_name = "${var.service_name} Cloud Run Service Account"
  description  = "Dedicated service account for the ${var.service_name} Cloud Run service"
  project      = var.project_id

  depends_on = [
    google_project_service.required_apis
  ]
}

# Grant the service account access to pull images from Artifact Registry
resource "google_project_iam_member" "artifact_reader" {
  project = var.project_id
  role    = "roles/artifactregistry.reader"
  member  = "serviceAccount:${google_service_account.cloud_run.email}"
}

# Grant access to Secret Manager secrets (if any)
resource "google_project_iam_member" "secret_accessor" {
  count   = length(var.secret_env_vars) > 0 ? 1 : 0
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.cloud_run.email}"
}

# -----------------------------------------------------------------------------
# Cloud Run Service
# -----------------------------------------------------------------------------

resource "google_cloud_run_v2_service" "service" {
  name     = var.service_name
  location = var.region
  project  = var.project_id
  ingress  = "INGRESS_TRAFFIC_ALL"

  labels = local.common_labels

  template {
    service_account                  = google_service_account.cloud_run.email
    timeout                          = var.max_request_timeout
    max_instance_request_concurrency = var.concurrency

    containers {
      image = var.container_image

      ports {
        container_port = var.container_port
      }

      # Inject common environment variables
      env {
        name  = "PROJECT_ID"
        value = var.project_id
      }
      env {
        name  = "ENVIRONMENT"
        value = var.environment
      }
      env {
        name  = "SERVICE_NAME"
        value = var.service_name
      }

      # User-defined plain-text environment variables
      dynamic "env" {
        for_each = var.env_vars
        content {
          name  = env.key
          value = env.value
        }
      }

      # Secret environment variables from Secret Manager
      dynamic "env" {
        for_each = var.secret_env_vars
        content {
          name = env.key
          value_source {
            secret_key_ref {
              secret  = env.value
              version = "latest"
            }
          }
        }
      }

      # Resource limits
      resources {
        limits = {
          cpu    = var.cpu_limit
          memory = var.memory_limit
        }
        cpu_idle          = var.environment != "production"
        startup_cpu_boost = true
      }

      # Startup probe - allow time for initialization
      startup_probe {
        http_get {
          path = "/health"
          port = var.container_port
        }
        initial_delay_seconds = 5
        period_seconds        = 10
        timeout_seconds       = 5
        failure_threshold     = 3
      }

      # Liveness probe - detect stuck processes
      liveness_probe {
        http_get {
          path = "/health"
          port = var.container_port
        }
        period_seconds    = 30
        timeout_seconds   = 5
        failure_threshold = 3
      }
    }

    # Autoscaling
    scaling {
      min_instance_count = var.environment == "production" ? max(var.min_instances, 1) : var.min_instances
      max_instance_count = var.max_instances
    }

    # VPC connector for private network access (optional)
    dynamic "vpc_access" {
      for_each = var.vpc_connector != null ? [1] : []
      content {
        connector = var.vpc_connector
        egress    = "PRIVATE_RANGES_ONLY"
      }
    }
  }

  # Route all traffic to the latest revision
  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  depends_on = [
    google_project_service.required_apis,
    google_service_account.cloud_run
  ]
}

# -----------------------------------------------------------------------------
# IAM: Allow Unauthenticated Access (optional)
# -----------------------------------------------------------------------------

resource "google_cloud_run_v2_service_iam_member" "allow_unauthenticated" {
  count    = var.allow_unauthenticated ? 1 : 0
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.service.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# -----------------------------------------------------------------------------
# Outputs
# -----------------------------------------------------------------------------

output "service_url" {
  description = "The URL of the deployed Cloud Run service"
  value       = google_cloud_run_v2_service.service.uri
}

output "service_name" {
  description = "The name of the Cloud Run service"
  value       = google_cloud_run_v2_service.service.name
}

output "service_account_email" {
  description = "The email of the Cloud Run service account"
  value       = google_service_account.cloud_run.email
}

output "latest_revision" {
  description = "The latest ready revision of the Cloud Run service"
  value       = google_cloud_run_v2_service.service.latest_ready_revision
}
