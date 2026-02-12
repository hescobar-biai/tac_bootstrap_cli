# =============================================================================
# IAM Custom Role Module
# =============================================================================
# Creates a project-level custom IAM role with specified permissions.
# Use when predefined roles are too broad or too narrow.
# =============================================================================

# --- Variables ---------------------------------------------------------------

variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "role_id" {
  description = "The role ID (e.g., 'customDataPipelineRunner')"
  type        = string

  validation {
    condition     = can(regex("^[a-zA-Z][a-zA-Z0-9_.]{2,63}$", var.role_id))
    error_message = "role_id must start with a letter and contain only letters, digits, dots, underscores."
  }
}

variable "title" {
  description = "Human-readable title for the role"
  type        = string
}

variable "description" {
  description = "Description of the custom role"
  type        = string
  default     = ""
}

variable "permissions" {
  description = "List of IAM permissions to grant"
  type        = list(string)
}

variable "stage" {
  description = "Launch stage of the role (GA, BETA, ALPHA)"
  type        = string
  default     = "GA"

  validation {
    condition     = contains(["GA", "BETA", "ALPHA"], var.stage)
    error_message = "stage must be GA, BETA, or ALPHA."
  }
}

# --- Resource ----------------------------------------------------------------

resource "google_project_iam_custom_role" "this" {
  role_id     = var.role_id
  project     = var.project_id
  title       = var.title
  description = var.description
  permissions = var.permissions
  stage       = var.stage
}

# --- Outputs -----------------------------------------------------------------

output "role_name" {
  description = "The full resource name of the custom role"
  value       = google_project_iam_custom_role.this.name
}

output "role_id" {
  description = "The role_id of the custom role"
  value       = google_project_iam_custom_role.this.role_id
}
