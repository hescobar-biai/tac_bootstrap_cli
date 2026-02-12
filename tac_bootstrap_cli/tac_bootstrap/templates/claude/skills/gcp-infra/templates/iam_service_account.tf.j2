# =============================================================================
# IAM Service Account Module - Service Accounts with Optional Key Generation
# =============================================================================
# Creates a GCP service account with optional JSON key file generation.
# Use generate_key = true only when Workload Identity Federation is not possible.
# =============================================================================

# --- Variables ---------------------------------------------------------------

variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "account_id" {
  description = "The service account ID (e.g., 'forecast-api')"
  type        = string

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{4,28}[a-z0-9]$", var.account_id))
    error_message = "account_id must be 6-30 chars, lowercase letters, digits, hyphens."
  }
}

variable "display_name" {
  description = "Display name for the service account"
  type        = string
}

variable "description" {
  description = "Description of the service account's purpose"
  type        = string
  default     = ""
}

variable "generate_key" {
  description = "Whether to generate a JSON key file (prefer Workload Identity instead)"
  type        = bool
  default     = false
}

# --- Resources ---------------------------------------------------------------

resource "google_service_account" "this" {
  account_id   = var.account_id
  display_name = var.display_name
  description  = var.description
  project      = var.project_id
}

resource "google_service_account_key" "this" {
  count              = var.generate_key ? 1 : 0
  service_account_id = google_service_account.this.name
}

# --- Outputs -----------------------------------------------------------------

output "email" {
  description = "The email address of the service account"
  value       = google_service_account.this.email
}

output "member" {
  description = "The IAM member string for this service account"
  value       = "serviceAccount:${google_service_account.this.email}"
}

output "name" {
  description = "The fully-qualified name of the service account"
  value       = google_service_account.this.name
}

output "private_key" {
  description = "The base64-encoded private key (only when generate_key = true)"
  value       = var.generate_key ? google_service_account_key.this[0].private_key : null
  sensitive   = true
}
