# =============================================================================
# IAM Member Module - Non-Authoritative Project IAM Bindings
# =============================================================================
# Uses the Celes cartesian product pattern: flatten() + for_each
# to create one google_project_iam_member per role-member combination.
#
# IMPORTANT: Always use google_project_iam_member (non-authoritative).
# NEVER use google_project_iam_binding or google_project_iam_policy.
# =============================================================================

# --- Variables ---------------------------------------------------------------

variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "iam_bindings" {
  description = "List of IAM bindings with roles and members"
  type = list(object({
    roles   = list(string)
    members = list(string)
    condition = optional(object({
      title       = string
      description = optional(string, "")
      expression  = string
    }))
  }))
}

# --- Locals (Cartesian Product) ---------------------------------------------

locals {
  all_combinations = flatten([
    for binding in var.iam_bindings : [
      for role in binding.roles : [
        for member in binding.members : {
          role      = role
          member    = member
          condition = binding.condition
        }
      ]
    ]
  ])
}

# --- Resource ----------------------------------------------------------------

resource "google_project_iam_member" "this" {
  for_each = {
    for combo in local.all_combinations :
    "${combo.role}-${combo.member}" => combo
  }

  project = var.project_id
  role    = each.value.role
  member  = each.value.member

  dynamic "condition" {
    for_each = each.value.condition != null ? [each.value.condition] : []
    content {
      title       = condition.value.title
      description = condition.value.description
      expression  = condition.value.expression
    }
  }
}

# --- Outputs -----------------------------------------------------------------

output "bindings" {
  description = "Map of created IAM bindings"
  value = {
    for k, v in google_project_iam_member.this :
    k => {
      role   = v.role
      member = v.member
    }
  }
}
