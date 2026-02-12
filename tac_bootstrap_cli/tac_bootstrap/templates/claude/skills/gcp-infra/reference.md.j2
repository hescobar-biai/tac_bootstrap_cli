# GCP Infrastructure Reference Patterns (Celes)

Patterns from the real `terraform-gcp-management-modules` codebase.

## Table of Contents

- [Provider and Backend Configuration](#provider-and-backend-configuration)
- [Module Architecture](#module-architecture)
- [IAM Cartesian Product Pattern](#iam-cartesian-product-pattern)
- [Non-Authoritative IAM Rules](#non-authoritative-iam-rules)
- [Service Account Management](#service-account-management)
- [Custom IAM Roles](#custom-iam-roles)
- [Storage Bucket IAM](#storage-bucket-iam)
- [Project Service API Enablement](#project-service-api-enablement)
- [Common Patterns](#common-patterns)
- [Bucket Lifecycle Policies](#bucket-lifecycle-policies)
- [Cloud Run Deployment](#cloud-run-deployment)
- [Cost Monitoring](#cost-monitoring)

---

## Provider and Backend Configuration

### backend.tf

GCS backend with **empty config block**. Values injected via `-backend-config` at runtime.

```hcl
terraform {
    required_providers {
        google = {
            source  = "hashicorp/google"
            version = "7.0.1"
        }
    }

    backend "gcs" {}
}
```

Key rules:
- Pin google provider to **exact version** (`"7.0.1"`), never `~> 5.0`.
- **No `google-beta` provider**. All resources use the standard google provider.
- **No `required_version`** in backend file. README states `Terraform >= 1.0`.
- Backend values passed at init: `terraform init -backend-config="bucket=..." -backend-config="prefix=..."`

### provider.tf

```hcl
provider "google" {
    project = var.project_id
}
```

No region/zone in provider; passed per-resource or per-module.

---

## Module Architecture

```
terraform-gcp-management-modules/
├── modules/
│   ├── iam_member/                  # Project-level IAM bindings (cartesian product)
│   │   ├── locals.tf, main.tf, outputs.tf, variables.tf
│   ├── iam_role/                    # Custom IAM roles
│   │   ├── main.tf, outputs.tf, variables.tf
│   ├── iam_service_account/         # Service accounts + optional key
│   │   ├── main.tf, outputs.tf, variables.tf
│   ├── iam_storage_bucket_member/   # Bucket-level IAM (cartesian product)
│   │   ├── locals.tf, main.tf, outputs.tf, variables.tf
│   └── project_service/             # Enable GCP APIs
│       ├── main.tf, outputs.tf, variables.tf
├── examples/                        # One per module: backend.tf + provider.tf + main.tf + variables.tf + output.tf
└── environments/                    # dev/, qas/
```

Conventions:
- Modules: `main.tf` + `variables.tf` + `outputs.tf` (+ `locals.tf` for cartesian product modules).
- **No `terraform.tfvars` inside modules**. Values live in `environments/` or caller.

---

## IAM Cartesian Product Pattern

**Core innovation** of the codebase. Generates every `(role, member)` combination and
creates one `google_project_iam_member` per pair.

### locals.tf

```hcl
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
```

### main.tf

```hcl
resource "google_project_iam_member" "members" {
    for_each = { for idx, binding in local.all_combinations : "${binding.role}-${binding.member}" => binding }

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
```

### variables.tf

```hcl
variable "project_id" {
  description = "The project ID where the IAM members will be assigned"
  type        = string
}

variable "iam_bindings" {
  description = "List of IAM bindings to create with multiple roles and members"
  type = list(object({
    roles   = list(string)
    members = list(string)
    condition = optional(object({
      title       = string
      description = optional(string)
      expression  = string
    }))
  }))
}
```

### outputs.tf

```hcl
output "iam_members" {
    description = "Map of all IAM member bindings created"
    value = {
        for k, v in google_project_iam_member.members :
            "${split("/", v.role)[length(split("/", v.role)) - 1]}-${v.member}" => {
                key = k, id = v.id, member = v.member, role = v.role, project = v.project
            }
    }
}
```

### Cartesian product example

Input: `roles = ["roles/viewer", "roles/storage.objectViewer"]`, `members = ["user:alice@ex.com", "serviceAccount:sa@proj.iam"]`
produces 4 resources (2 roles x 2 members).

### Caller invocation (Pattern A: module handles iteration internally)

```hcl
module "iam_member" {
  source     = "../../modules/iam_member"
  project_id = var.project_id
  iam_bindings = var.iam_member_config
}
```

---

## Non-Authoritative IAM Rules

| Resource | Type | Used? |
|----------|------|-------|
| `google_project_iam_member` | Non-authoritative (additive) | **YES** |
| `google_project_iam_binding` | Authoritative for a role | **NEVER** |
| `google_project_iam_policy` | Authoritative for entire project | **NEVER** |
| `google_storage_bucket_iam_member` | Non-authoritative (additive) | **YES** |

- `iam_member` **adds** a binding without touching existing ones.
- `iam_binding` **replaces all members** for a role -- removes members from other configs.
- `iam_policy` **replaces the entire policy** -- extremely dangerous.

**Rule: Always use `*_iam_member`. Never use `*_iam_binding` or `*_iam_policy`.**

---

## Service Account Management

### main.tf

```hcl
resource "google_service_account" "service_account" {
    account_id                   = var.account_id
    display_name                 = var.display_name
    description                  = var.description
    disabled                     = var.disabled
    project                      = var.project
    create_ignore_already_exists = var.create_ignore_already_exists
}

resource "google_service_account_key" "service_account_key" {
    count              = var.generate_key_json ? 1 : 0
    service_account_id = google_service_account.service_account.name
}

resource "local_file" "private_key_file" {
    count    = var.generate_key_json ? 1 : 0
    content  = base64decode(google_service_account_key.service_account_key[0].private_key)
    filename = "${var.project}/${var.account_id}.json"
}
```

Key patterns:
- Key generation **conditional** via `count` on `var.generate_key_json` (default `false`).
- `local_file` writes decoded key to `{project}/{account_id}.json`.
- `create_ignore_already_exists` avoids errors on re-runs.
- **Single-account module**. Multi-account via `for_each` at caller.
- Outputs: `id`, `email`, `name`, `unique_id`, `member` (returns `serviceAccount:email` format).

### Caller invocation (Pattern B: caller does for_each)

```hcl
module "iam_service_account" {
    source   = "../../modules/iam_service_account"
    for_each = { for sa in var.iam_service_account_config : sa.account_id => sa }

    account_id                   = each.value.account_id
    display_name                 = each.value.display_name
    generate_key_json            = each.value.generate_key_json
    description                  = each.value.description
    disabled                     = each.value.disabled
    project                      = var.project_id
    create_ignore_already_exists = each.value.create_ignore_already_exists
}
```

Example variable uses `list(object)` with `optional()` fields:

```hcl
variable "iam_service_account_config" {
    type = list(object({
        account_id                   = string
        display_name                 = optional(string)
        generate_key_json            = optional(bool, false)
        disabled                     = optional(bool)
        description                  = optional(string)
        create_ignore_already_exists = optional(bool)
    }))
}
```

---

## Custom IAM Roles

### main.tf (single-role module)

```hcl
resource "google_project_iam_custom_role" "custom_role" {
    role_id     = var.role_id
    title       = var.title
    permissions = var.permissions
    project     = var.project
    description = var.description
    stage       = var.stage
}
```

Variables: `role_id` (string), `title` (string), `permissions` (list(string)), `project` (string), `description` (string), `stage` (string, default `"GA"` -- accepts `"GA"`, `"BETA"`, `"ALPHA"`).

Outputs: `id`, `name`, `deleted`.

### Caller invocation (Pattern B: caller does for_each)

```hcl
module "iam_role" {
    source      = "../../modules/iam_role"
    for_each    = { for role in var.iam_role_config : role.role_id => role }
    role_id     = each.value.role_id
    title       = each.value.title
    description = each.value.description
    permissions = each.value.permissions
    project     = var.project_id
    stage       = each.value.stage
}
```

---

## Storage Bucket IAM

Same cartesian product as `iam_member`, but with a **third dimension** (`buckets`).
Produces `bucket x role x member` combinations.

### locals.tf

```hcl
locals {
    all_combinations = flatten([
        for binding in var.iam_storage_bucket_member_config : [
            for bucket in binding.buckets : [
                for role in binding.roles : [
                    for member in binding.members : {
                        bucket    = bucket
                        role      = role
                        member    = member
                        condition = binding.condition
                    }
                ]
            ]
        ]
    ])
}
```

### main.tf

```hcl
resource "google_storage_bucket_iam_member" "storage_bucket_members" {
    for_each = {
      for idx, binding in local.all_combinations :
        "${binding.bucket}-${binding.role}-${binding.member}" => binding
    }

    bucket = each.value.bucket
    role   = each.value.role
    member = each.value.member

    dynamic "condition" {
        for_each = each.value.condition != null ? [each.value.condition] : []
        content {
            title       = condition.value.title
            description = condition.value.description
            expression  = condition.value.expression
        }
    }
}
```

### variables.tf

```hcl
variable "iam_storage_bucket_member_config" {
  type = list(object({
    buckets   = list(string)
    roles     = list(string)
    members   = list(string)
    condition = optional(object({
      title       = string
      description = optional(string)
      expression  = string
    }))
  }))
}
```

**No `project_id` variable** -- bucket names are globally unique in GCS.

### Caller invocation (Pattern A: module handles iteration)

```hcl
module "iam_storage_bucket_member" {
    source = "../../modules/iam_storage_bucket_member"
    iam_storage_bucket_member_config = var.iam_storage_bucket_member_config
}
```

---

## Project Service API Enablement

### main.tf (single-API module)

```hcl
resource "google_project_service" "project_service" {
  project            = var.project
  service            = var.service
  disable_on_destroy = var.disable_on_destroy
}
```

Variables: `project` (string), `service` (string), `disable_on_destroy` (bool, default `false` -- safe default, APIs stay enabled on destroy).

### Caller invocation (Pattern B)

```hcl
module "project_service" {
  source   = "../../modules/project_service"
  for_each = { for api in var.apis_to_enable : api.service => api }

  project            = var.project_id
  service            = each.value.service
  disable_on_destroy = each.value.disable_on_destroy
}
```

---

## Common Patterns

### list(object) with optional()

All multi-instance config uses `list(object)` with `optional()` fields:
- Required fields: no wrapper. Optional fields: `optional(string)`, `optional(bool, false)`.
- Nested optional objects: `optional(object({...}))` for things like `condition`.

### for_each from list

Converts list to map: `{ for item in var.items : item.unique_key => item }`

### Two module invocation patterns

| Pattern | Who iterates? | Used by |
|---------|--------------|---------|
| A: internal cartesian product | Module (flatten + for_each) | `iam_member`, `iam_storage_bucket_member` |
| B: caller for_each | Caller | `iam_role`, `iam_service_account`, `project_service` |

### Dynamic blocks (optional condition)

```hcl
dynamic "condition" {
    for_each = each.value.condition != null ? [each.value.condition] : []
    content { title = condition.value.title; description = condition.value.description; expression = condition.value.expression }
}
```

### Output key shortening

Extract short role name: `split("/", v.role)[length(split("/", v.role)) - 1]`
Example: `roles/storage.objectViewer` -> `storage.objectViewer`

---

## Bucket Lifecycle Policies

```hcl
resource "google_storage_bucket" "tiered_bucket" {
  name          = "${var.project_id}-data-lake"
  location      = var.region
  storage_class = "STANDARD"

  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  versioning { enabled = true }

  lifecycle_rule {
    action { type = "SetStorageClass"; storage_class = "NEARLINE" }
    condition { age = 30 }
  }
  lifecycle_rule {
    action { type = "SetStorageClass"; storage_class = "COLDLINE" }
    condition { age = 90 }
  }
  lifecycle_rule {
    action { type = "SetStorageClass"; storage_class = "ARCHIVE" }
    condition { age = 365 }
  }
  lifecycle_rule {
    action { type = "Delete" }
    condition { age = 2555 }
  }
  lifecycle_rule {
    action { type = "Delete" }
    condition { num_newer_versions = 3; with_state = "ARCHIVED" }
  }
}
```

---

## Cloud Run Deployment

```hcl
resource "google_cloud_run_v2_service" "service" {
  name     = var.service_name
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    service_account = google_service_account.runner.email
    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/${var.artifact_repo}/${var.service_name}:${var.image_tag}"
      env { name = "PROJECT_ID"; value = var.project_id }
      env {
        name = "DATABASE_URL"
        value_source {
          secret_key_ref { secret = google_secret_manager_secret.db_url.secret_id; version = "latest" }
        }
      }
      resources {
        limits            = { cpu = var.cpu_limit; memory = var.memory_limit }
        cpu_idle          = true
        startup_cpu_boost = true
      }
    }
    scaling {
      min_instance_count = var.environment == "production" ? 1 : 0
      max_instance_count = var.max_instances
    }
  }

  traffic { type = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"; percent = 100 }
}
```

---

## Cost Monitoring

### Budget alerts

```hcl
resource "google_billing_budget" "project_budget" {
  billing_account = var.billing_account_id
  display_name    = "${var.project_id}-monthly-budget"

  budget_filter {
    projects               = ["projects/${var.project_number}"]
    credit_types_treatment = "EXCLUDE_ALL_CREDITS"
  }
  amount {
    specified_amount { currency_code = "USD"; units = var.monthly_budget_usd }
  }

  threshold_rules { threshold_percent = 0.5; spend_basis = "CURRENT_SPEND" }
  threshold_rules { threshold_percent = 0.8; spend_basis = "CURRENT_SPEND" }
  threshold_rules { threshold_percent = 1.0; spend_basis = "CURRENT_SPEND" }
  threshold_rules { threshold_percent = 1.0; spend_basis = "FORECASTED_SPEND" }

  all_updates_rule {
    monitoring_notification_channels = var.notification_channels
    disable_default_iam_recipients   = false
  }
}
```

### Resource labeling

```hcl
locals {
  common_labels = {
    environment = var.environment
    team        = var.team
    service     = var.service_name
    managed_by  = "terraform"
  }
}
```

Apply `labels = local.common_labels` to all resources that support labels.
