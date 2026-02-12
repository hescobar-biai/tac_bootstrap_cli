# =============================================================================
# Cloud Storage Bucket with Lifecycle Policies
# =============================================================================
# Usage: Define GCS buckets with tiered lifecycle rules, versioning,
# access controls, and CORS configuration.
# Requires: main.tf for provider and variable configuration.
# =============================================================================

# -----------------------------------------------------------------------------
# Variables
# -----------------------------------------------------------------------------

variable "bucket_name_suffix" {
  description = "Suffix appended to project_id for the bucket name"
  type        = string
  default     = "data"
}

variable "storage_class" {
  description = "Default storage class (STANDARD, NEARLINE, COLDLINE, ARCHIVE)"
  type        = string
  default     = "STANDARD"

  validation {
    condition     = contains(["STANDARD", "NEARLINE", "COLDLINE", "ARCHIVE"], var.storage_class)
    error_message = "Storage class must be one of: STANDARD, NEARLINE, COLDLINE, ARCHIVE."
  }
}

variable "enable_versioning" {
  description = "Enable object versioning on the bucket"
  type        = bool
  default     = true
}

variable "retention_days" {
  description = "Number of days before objects are deleted (0 to disable)"
  type        = number
  default     = 365
}

variable "nearline_transition_days" {
  description = "Days before transitioning to Nearline (0 to disable)"
  type        = number
  default     = 30
}

variable "coldline_transition_days" {
  description = "Days before transitioning to Coldline (0 to disable)"
  type        = number
  default     = 90
}

variable "cors_origins" {
  description = "List of allowed CORS origins (empty list to disable CORS)"
  type        = list(string)
  default     = []
}

# -----------------------------------------------------------------------------
# Primary Data Bucket
# -----------------------------------------------------------------------------

resource "google_storage_bucket" "data" {
  name          = "${var.project_id}-${var.bucket_name_suffix}"
  location      = var.region
  project       = var.project_id
  storage_class = var.storage_class

  # Security: enforce uniform bucket-level access (no per-object ACLs)
  uniform_bucket_level_access = true

  # Security: prevent public access
  public_access_prevention = "enforced"

  # Versioning for data protection
  versioning {
    enabled = var.enable_versioning
  }

  # Transition to Nearline storage
  dynamic "lifecycle_rule" {
    for_each = var.nearline_transition_days > 0 ? [1] : []
    content {
      action {
        type          = "SetStorageClass"
        storage_class = "NEARLINE"
      }
      condition {
        age = var.nearline_transition_days
      }
    }
  }

  # Transition to Coldline storage
  dynamic "lifecycle_rule" {
    for_each = var.coldline_transition_days > 0 ? [1] : []
    content {
      action {
        type          = "SetStorageClass"
        storage_class = "COLDLINE"
      }
      condition {
        age = var.coldline_transition_days
      }
    }
  }

  # Delete objects after retention period
  dynamic "lifecycle_rule" {
    for_each = var.retention_days > 0 ? [1] : []
    content {
      action {
        type = "Delete"
      }
      condition {
        age = var.retention_days
      }
    }
  }

  # Clean up non-current versions (keep last 3)
  dynamic "lifecycle_rule" {
    for_each = var.enable_versioning ? [1] : []
    content {
      action {
        type = "Delete"
      }
      condition {
        num_newer_versions = 3
        with_state         = "ARCHIVED"
      }
    }
  }

  # Abort incomplete multipart uploads after 7 days
  lifecycle_rule {
    action {
      type = "AbortIncompleteMultipartUpload"
    }
    condition {
      age = 7
    }
  }

  # CORS configuration (optional)
  dynamic "cors" {
    for_each = length(var.cors_origins) > 0 ? [1] : []
    content {
      origin          = var.cors_origins
      method          = ["GET", "HEAD", "PUT", "POST", "DELETE"]
      response_header = ["Content-Type", "Content-Disposition"]
      max_age_seconds = 3600
    }
  }

  labels = local.common_labels

  depends_on = [
    google_project_service.required_apis
  ]
}

# -----------------------------------------------------------------------------
# Logging Bucket (Short Retention)
# -----------------------------------------------------------------------------

resource "google_storage_bucket" "logs" {
  name          = "${var.project_id}-logs"
  location      = var.region
  project       = var.project_id
  storage_class = "STANDARD"

  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"

  # No versioning for logs
  versioning {
    enabled = false
  }

  # Delete logs after 90 days
  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 90
    }
  }

  # Abort incomplete uploads
  lifecycle_rule {
    action {
      type = "AbortIncompleteMultipartUpload"
    }
    condition {
      age = 1
    }
  }

  labels = merge(local.common_labels, {
    purpose = "logging"
  })

  depends_on = [
    google_project_service.required_apis
  ]
}

# -----------------------------------------------------------------------------
# IAM Bindings for Buckets
# -----------------------------------------------------------------------------

# Example: Grant a service account read access to the data bucket
# Uncomment and modify as needed:
#
# resource "google_storage_bucket_iam_member" "data_reader" {
#   bucket = google_storage_bucket.data.name
#   role   = "roles/storage.objectViewer"
#   member = "serviceAccount:${google_service_account.reader.email}"
# }
#
# resource "google_storage_bucket_iam_member" "data_writer" {
#   bucket = google_storage_bucket.data.name
#   role   = "roles/storage.objectCreator"
#   member = "serviceAccount:${google_service_account.writer.email}"
# }

# -----------------------------------------------------------------------------
# Outputs
# -----------------------------------------------------------------------------

output "data_bucket_name" {
  description = "Name of the primary data bucket"
  value       = google_storage_bucket.data.name
}

output "data_bucket_url" {
  description = "URL of the primary data bucket"
  value       = google_storage_bucket.data.url
}

output "data_bucket_self_link" {
  description = "Self link of the primary data bucket"
  value       = google_storage_bucket.data.self_link
}

output "logs_bucket_name" {
  description = "Name of the logs bucket"
  value       = google_storage_bucket.logs.name
}

output "logs_bucket_url" {
  description = "URL of the logs bucket"
  value       = google_storage_bucket.logs.url
}
