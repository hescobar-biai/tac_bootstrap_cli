# =============================================================================
# BigQuery Dataset & Table Resources
# =============================================================================
# Usage: Define BigQuery datasets with access controls and tables with
# partitioning, clustering, and schema definitions.
# Requires: main.tf for provider and variable configuration.
# =============================================================================

# -----------------------------------------------------------------------------
# Variables
# -----------------------------------------------------------------------------

variable "dataset_id" {
  description = "BigQuery dataset ID"
  type        = string
  default     = "analytics"
}

variable "dataset_friendly_name" {
  description = "Human-readable dataset name"
  type        = string
  default     = "Analytics Dataset"
}

variable "dataset_description" {
  description = "Description of the dataset's purpose"
  type        = string
  default     = "Central analytics dataset for application data"
}

variable "default_table_expiration_days" {
  description = "Default table expiration in days (null for no expiration)"
  type        = number
  default     = null
}

variable "default_partition_expiration_days" {
  description = "Default partition expiration in days (null for no expiration)"
  type        = number
  default     = null
}

variable "dataset_owner_email" {
  description = "Email of the dataset owner (user or group)"
  type        = string
}

variable "bq_reader_service_accounts" {
  description = "List of service account emails with read access"
  type        = list(string)
  default     = []
}

variable "bq_writer_service_accounts" {
  description = "List of service account emails with write access"
  type        = list(string)
  default     = []
}

# -----------------------------------------------------------------------------
# BigQuery Dataset
# -----------------------------------------------------------------------------

resource "google_bigquery_dataset" "main" {
  dataset_id    = var.dataset_id
  friendly_name = var.dataset_friendly_name
  description   = var.dataset_description
  location      = var.region
  project       = var.project_id

  default_table_expiration_ms = (
    var.default_table_expiration_days != null
    ? var.default_table_expiration_days * 86400000
    : null
  )

  default_partition_expiration_ms = (
    var.default_partition_expiration_days != null
    ? var.default_partition_expiration_days * 86400000
    : null
  )

  # Owner access
  access {
    role          = "OWNER"
    user_by_email = var.dataset_owner_email
  }

  # Writer access for service accounts
  dynamic "access" {
    for_each = var.bq_writer_service_accounts
    content {
      role          = "WRITER"
      user_by_email = access.value
    }
  }

  # Reader access for service accounts
  dynamic "access" {
    for_each = var.bq_reader_service_accounts
    content {
      role          = "READER"
      user_by_email = access.value
    }
  }

  labels = local.common_labels

  depends_on = [
    google_project_service.required_apis
  ]
}

# -----------------------------------------------------------------------------
# Events Table (Time-Partitioned + Clustered)
# -----------------------------------------------------------------------------

resource "google_bigquery_table" "events" {
  dataset_id          = google_bigquery_dataset.main.dataset_id
  table_id            = "events"
  project             = var.project_id
  deletion_protection = var.environment == "production" ? true : false

  description = "Application events partitioned by day and clustered by event type"

  time_partitioning {
    type                     = "DAY"
    field                    = "event_timestamp"
    require_partition_filter  = var.environment == "production" ? true : false
    expiration_ms            = var.default_partition_expiration_days != null ? var.default_partition_expiration_days * 86400000 : null
  }

  clustering = ["event_type", "user_id"]

  schema = jsonencode([
    {
      name        = "event_id"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Unique event identifier (UUID)"
    },
    {
      name        = "event_timestamp"
      type        = "TIMESTAMP"
      mode        = "REQUIRED"
      description = "When the event occurred (partition key)"
    },
    {
      name        = "event_type"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Type of event (cluster key)"
    },
    {
      name        = "user_id"
      type        = "STRING"
      mode        = "NULLABLE"
      description = "User who triggered the event (cluster key)"
    },
    {
      name        = "session_id"
      type        = "STRING"
      mode        = "NULLABLE"
      description = "Session identifier"
    },
    {
      name        = "properties"
      type        = "JSON"
      mode        = "NULLABLE"
      description = "Event-specific properties as JSON"
    },
    {
      name        = "created_at"
      type        = "TIMESTAMP"
      mode        = "REQUIRED"
      description = "Record insertion timestamp"
    }
  ])

  labels = local.common_labels
}

# -----------------------------------------------------------------------------
# Metrics Table (Ingestion-Time Partitioned)
# -----------------------------------------------------------------------------

resource "google_bigquery_table" "metrics" {
  dataset_id          = google_bigquery_dataset.main.dataset_id
  table_id            = "metrics"
  project             = var.project_id
  deletion_protection = var.environment == "production" ? true : false

  description = "Application metrics with ingestion-time partitioning"

  time_partitioning {
    type = "DAY"
    # No field specified = ingestion-time partitioning
  }

  clustering = ["metric_name", "service"]

  schema = jsonencode([
    {
      name        = "metric_name"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Name of the metric"
    },
    {
      name        = "metric_value"
      type        = "FLOAT64"
      mode        = "REQUIRED"
      description = "Numeric metric value"
    },
    {
      name        = "service"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Service that emitted the metric"
    },
    {
      name        = "labels"
      type        = "JSON"
      mode        = "NULLABLE"
      description = "Additional metric labels as JSON"
    },
    {
      name        = "recorded_at"
      type        = "TIMESTAMP"
      mode        = "REQUIRED"
      description = "When the metric was recorded"
    }
  ])

  labels = local.common_labels
}

# -----------------------------------------------------------------------------
# Outputs
# -----------------------------------------------------------------------------

output "dataset_id" {
  description = "The BigQuery dataset ID"
  value       = google_bigquery_dataset.main.dataset_id
}

output "dataset_self_link" {
  description = "The BigQuery dataset self link"
  value       = google_bigquery_dataset.main.self_link
}

output "events_table_id" {
  description = "The events table full ID"
  value       = "${google_bigquery_dataset.main.project}:${google_bigquery_dataset.main.dataset_id}.${google_bigquery_table.events.table_id}"
}

output "metrics_table_id" {
  description = "The metrics table full ID"
  value       = "${google_bigquery_dataset.main.project}:${google_bigquery_dataset.main.dataset_id}.${google_bigquery_table.metrics.table_id}"
}
