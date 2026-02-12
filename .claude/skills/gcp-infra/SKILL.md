---
name: gcp-infra
description: "Manages GCP infrastructure with reusable Terraform modules for IAM, Cloud Storage, Cloud Run, and BigQuery. Use when provisioning GCP resources, managing IAM bindings with non-authoritative patterns, creating service accounts, or configuring Terraform modules."
allowed-tools: Bash(gcloud *), Bash(gsutil *), Bash(terraform *), Read, Write
---

# GCP Infrastructure Management

Provision, configure, and manage Google Cloud Platform infrastructure using reusable Terraform modules. This skill follows the modular IAM patterns used in Celes production infrastructure with non-authoritative bindings, cartesian product patterns, and the Google provider 7.x.

## Prerequisites

1. **Google Cloud SDK** installed and authenticated:
   ```bash
   gcloud auth login
   gcloud config set project <PROJECT_ID>
   ```

2. **Terraform** >= 1.0 installed:
   ```bash
   terraform version
   ```

3. **Google Provider** 7.0.1 (pinned in all modules):
   ```hcl
   required_providers {
     google = {
       source  = "hashicorp/google"
       version = "7.0.1"
     }
   }
   ```

4. **GCS Backend** for remote state (always use empty config for flexibility):
   ```hcl
   backend "gcs" {}
   ```

## Instructions

### Terraform Module Architecture

Celes uses **reusable Terraform modules** with a consistent structure. Each module follows this pattern:

```
modules/
├── iam_member/                # Non-authoritative project IAM bindings
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── locals.tf
├── iam_role/                  # Custom IAM roles
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── iam_service_account/       # Service accounts with optional key generation
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── iam_storage_bucket_member/ # Non-authoritative bucket IAM bindings
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── locals.tf
└── project_service/           # GCP API enablement
    ├── main.tf
    ├── variables.tf
    └── outputs.tf
```

### Core Pattern: Flatten + for_each (Cartesian Product)

The key Terraform pattern for IAM is creating a **cartesian product** of roles and members using `flatten()` in locals, then iterating with `for_each`:

```hcl
# locals.tf
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

```hcl
# main.tf
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
```

### Non-Authoritative IAM (Critical)

**Always use `google_project_iam_member`** (non-authoritative), NEVER `google_project_iam_binding` or `google_project_iam_policy`. Non-authoritative resources:
- Add individual bindings without removing existing ones
- Are safe to use across multiple Terraform configurations
- Won't accidentally revoke access from other service accounts

### Resource Provisioning Workflow

1. **Identify the resource scope**: Which modules are needed (IAM, storage, service accounts, APIs)
2. **Review module templates** in [templates/](templates/):
   - [templates/main.tf](templates/main.tf) - Provider config and backend
   - [templates/iam_member.tf](templates/iam_member.tf) - Project IAM bindings module
   - [templates/iam_service_account.tf](templates/iam_service_account.tf) - Service account module
   - [templates/iam_role.tf](templates/iam_role.tf) - Custom role module
   - [templates/storage.tf](templates/storage.tf) - Cloud Storage buckets
   - [templates/cloudrun.tf](templates/cloudrun.tf) - Cloud Run services
3. **Apply changes**:
   ```bash
   terraform init -backend-config="bucket=<STATE_BUCKET>" -backend-config="prefix=<ENV>"
   terraform plan -out=tfplan
   terraform apply tfplan
   ```
4. **Verify**: `gcloud projects get-iam-policy <PROJECT_ID> --format=json`

### Complex Variables Pattern

Use `list(object({...}))` with `optional()` fields for flexible module inputs:

```hcl
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
```

### IAM Best Practices

1. **Least-privilege**: Use predefined roles over primitive (Editor, Owner)
2. **Purpose-specific service accounts**: One per service, never share
3. **Resource-level bindings** when possible (bucket-level, dataset-level)
4. **Workload Identity Federation** for external services (no service account keys)
5. **Audit regularly**: `gcloud projects get-iam-policy <PROJECT_ID> --format=json`

See [reference.md](reference.md) for detailed IAM patterns, module examples, and cost monitoring.

## Examples

### Example 1: Create IAM Bindings for Multiple Roles and Members

User request:
```
Set up IAM bindings so the data-pipeline SA has BigQuery data editor and Storage object viewer,
and the api-runner SA has only BigQuery data viewer.
```

You would:
1. Use the [templates/iam_member.tf](templates/iam_member.tf) module pattern:
   ```hcl
   module "iam_bindings" {
     source     = "./modules/iam_member"
     project_id = var.project_id

     iam_bindings = [
       {
         roles   = ["roles/bigquery.dataEditor", "roles/storage.objectViewer"]
         members = ["serviceAccount:data-pipeline@${var.project_id}.iam.gserviceaccount.com"]
       },
       {
         roles   = ["roles/bigquery.dataViewer"]
         members = ["serviceAccount:api-runner@${var.project_id}.iam.gserviceaccount.com"]
       },
     ]
   }
   ```
2. Run `terraform plan` to preview the 3 bindings that will be created
3. Apply and verify with `gcloud projects get-iam-policy`

### Example 2: Create Service Accounts with Optional Key Generation

User request:
```
Create service accounts for our forecast API and data pipeline, with a key file only for the pipeline SA.
```

You would:
1. Use [templates/iam_service_account.tf](templates/iam_service_account.tf):
   ```hcl
   variable "service_accounts" {
     default = [
       {
         account_id   = "forecast-api"
         display_name = "Forecast API Service Account"
         description  = "SA for forecast API Cloud Run service"
         generate_key = false
       },
       {
         account_id   = "data-pipeline"
         display_name = "Data Pipeline Service Account"
         description  = "SA for data pipeline with key for external access"
         generate_key = true
       },
     ]
   }

   module "service_accounts" {
     source   = "./modules/iam_service_account"
     for_each = { for sa in var.service_accounts : sa.account_id => sa }

     project_id   = var.project_id
     account_id   = each.value.account_id
     display_name = each.value.display_name
     description  = each.value.description
     generate_key = each.value.generate_key
   }
   ```
2. Apply -- the pipeline SA key will be exported as a local file
3. Store the key securely (never commit to git)

### Example 3: Storage Bucket IAM with Cartesian Product

User request:
```
Grant the data-pipeline SA object admin on both the raw-data and processed-data buckets,
and grant the api-runner SA object viewer on the processed-data bucket only.
```

You would:
1. Use the bucket IAM pattern with triple-nested flatten (buckets x roles x members):
   ```hcl
   module "bucket_iam" {
     source     = "./modules/iam_storage_bucket_member"
     project_id = var.project_id

     iam_bindings = [
       {
         buckets = ["${var.project_id}-raw-data", "${var.project_id}-processed-data"]
         roles   = ["roles/storage.objectAdmin"]
         members = ["serviceAccount:data-pipeline@${var.project_id}.iam.gserviceaccount.com"]
       },
       {
         buckets = ["${var.project_id}-processed-data"]
         roles   = ["roles/storage.objectViewer"]
         members = ["serviceAccount:api-runner@${var.project_id}.iam.gserviceaccount.com"]
       },
     ]
   }
   ```
2. This creates 3 bindings: pipeline-admin-raw, pipeline-admin-processed, api-viewer-processed
3. All non-authoritative -- won't affect existing bucket permissions
