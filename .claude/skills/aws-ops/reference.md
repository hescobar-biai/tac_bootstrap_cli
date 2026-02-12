# AWS Operations Reference

Detailed patterns, templates, and best practices for AWS resource management. This file is referenced from [SKILL.md](SKILL.md) and provides in-depth guidance for each supported AWS service.

## Table of Contents

1. [S3 Bucket Policies and Versioning](#s3-bucket-policies-and-versioning)
2. [Lambda Function Packaging and Deployment](#lambda-function-packaging-and-deployment)
3. [ECS Task Definitions and Services](#ecs-task-definitions-and-services)
4. [IAM Policies and Roles](#iam-policies-and-roles)
5. [Terraform AWS Provider Modules](#terraform-aws-provider-modules)
6. [Cost Optimization Patterns](#cost-optimization-patterns)

---

## S3 Bucket Policies and Versioning

### Bucket Creation Best Practices

- Always enable versioning for data protection
- Enable server-side encryption (SSE-S3 or SSE-KMS)
- Block all public access by default
- Enable access logging for audit trails
- Configure lifecycle rules to manage storage costs

### Standard Bucket Policy Template (Terraform)

```hcl
resource "aws_s3_bucket" "main" {
  bucket = "${var.project}-${var.purpose}-${var.environment}"

  tags = {
    Environment = var.environment
    Project     = var.project
    ManagedBy   = "terraform"
    Purpose     = var.purpose
  }
}

resource "aws_s3_bucket_versioning" "main" {
  bucket = aws_s3_bucket.main.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "main" {
  bucket = aws_s3_bucket.main.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = var.kms_key_id  # Optional: use default AWS-managed key if omitted
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "main" {
  bucket                  = aws_s3_bucket.main.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_logging" "main" {
  bucket        = aws_s3_bucket.main.id
  target_bucket = var.log_bucket_id
  target_prefix = "s3-access-logs/${aws_s3_bucket.main.id}/"
}
```

### Lifecycle Rules for Cost Management

```hcl
resource "aws_s3_bucket_lifecycle_configuration" "main" {
  bucket = aws_s3_bucket.main.id

  rule {
    id     = "archive-old-objects"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }

    noncurrent_version_transition {
      noncurrent_days = 30
      storage_class   = "GLACIER"
    }

    noncurrent_version_expiration {
      noncurrent_days = 90
    }
  }
}
```

### Bucket Policy for Cross-Account Access

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowCrossAccountRead",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::TRUSTED_ACCOUNT_ID:root"
      },
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::BUCKET_NAME",
        "arn:aws:s3:::BUCKET_NAME/*"
      ],
      "Condition": {
        "StringEquals": {
          "aws:PrincipalOrgID": "o-ORGANIZATION_ID"
        }
      }
    }
  ]
}
```

### AWS CLI Quick Reference for S3

```bash
# Create bucket
aws s3 mb s3://my-bucket-name --region us-east-1

# Enable versioning
aws s3api put-bucket-versioning --bucket my-bucket-name \
  --versioning-configuration Status=Enabled

# Enable default encryption
aws s3api put-bucket-encryption --bucket my-bucket-name \
  --server-side-encryption-configuration '{
    "Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "aws:kms"}}]
  }'

# Block public access
aws s3api put-public-access-block --bucket my-bucket-name \
  --public-access-block-configuration \
  BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

# Sync local directory to S3
aws s3 sync ./build/ s3://my-bucket-name/artifacts/ --delete

# List object versions
aws s3api list-object-versions --bucket my-bucket-name --prefix "path/to/key"
```

---

## Lambda Function Packaging and Deployment

### Lambda Project Structure

```
src/lambda/
  function-name/
    handler.py          # Entry point
    requirements.txt    # Dependencies (if any)
    utils/              # Shared utilities
      __init__.py
      helpers.py
```

### Packaging a Python Lambda

```bash
# Simple function (no dependencies)
cd src/lambda/my-function
zip -r ../../../build/my-function.zip handler.py utils/

# Function with dependencies
cd src/lambda/my-function
pip install -r requirements.txt -t ./package/
cd package && zip -r ../../../../build/my-function.zip . && cd ..
zip -g ../../../build/my-function.zip handler.py utils/*.py
```

### Lambda Terraform Module

```hcl
resource "aws_lambda_function" "main" {
  function_name = "${var.project}-${var.function_name}-${var.environment}"
  runtime       = "python3.12"
  handler       = "handler.lambda_handler"
  timeout       = var.timeout
  memory_size   = var.memory_size

  filename         = var.deployment_package_path
  source_code_hash = filebase64sha256(var.deployment_package_path)

  role = aws_iam_role.lambda_execution.arn

  environment {
    variables = merge(var.environment_variables, {
      ENVIRONMENT = var.environment
      LOG_LEVEL   = var.log_level
    })
  }

  tracing_config {
    mode = "Active"  # Enable X-Ray tracing
  }

  dead_letter_config {
    target_arn = var.dlq_arn
  }

  tags = {
    Environment = var.environment
    Project     = var.project
    ManagedBy   = "terraform"
  }
}

# CloudWatch Log Group with retention
resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${aws_lambda_function.main.function_name}"
  retention_in_days = var.log_retention_days
}
```

### Lambda Layers for Shared Dependencies

```hcl
resource "aws_lambda_layer_version" "common_deps" {
  layer_name          = "${var.project}-common-deps"
  filename            = var.layer_package_path
  source_code_hash    = filebase64sha256(var.layer_package_path)
  compatible_runtimes = ["python3.11", "python3.12"]
  description         = "Common dependencies shared across Lambda functions"
}
```

### Event Source Mappings

```hcl
# SQS trigger
resource "aws_lambda_event_source_mapping" "sqs" {
  event_source_arn                   = var.sqs_queue_arn
  function_name                      = aws_lambda_function.main.arn
  batch_size                         = 10
  maximum_batching_window_in_seconds = 5
  function_response_types            = ["ReportBatchItemFailures"]
}

# DynamoDB Streams trigger
resource "aws_lambda_event_source_mapping" "dynamodb" {
  event_source_arn  = var.dynamodb_stream_arn
  function_name     = aws_lambda_function.main.arn
  starting_position = "LATEST"
  batch_size        = 100

  filter_criteria {
    filter {
      pattern = jsonencode({ eventName = ["INSERT", "MODIFY"] })
    }
  }
}
```

### AWS CLI Quick Reference for Lambda

```bash
# Create function
aws lambda create-function \
  --function-name my-function \
  --runtime python3.12 \
  --handler handler.lambda_handler \
  --role arn:aws:iam::ACCOUNT_ID:role/lambda-role \
  --zip-file fileb://build/my-function.zip

# Update function code
aws lambda update-function-code \
  --function-name my-function \
  --zip-file fileb://build/my-function.zip

# Invoke function
aws lambda invoke \
  --function-name my-function \
  --payload '{"key": "value"}' \
  --cli-binary-format raw-in-base64-out \
  output.json

# View recent logs
aws logs tail /aws/lambda/my-function --since 1h --follow

# Update environment variables
aws lambda update-function-configuration \
  --function-name my-function \
  --environment 'Variables={KEY1=value1,KEY2=value2}'
```

---

## ECS Task Definitions and Services

### Fargate Task Definition Template

```hcl
resource "aws_ecs_task_definition" "app" {
  family                   = "${var.project}-${var.service_name}"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.cpu
  memory                   = var.memory
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn

  container_definitions = jsonencode([
    {
      name      = var.service_name
      image     = "${var.ecr_repo_url}:${var.image_tag}"
      essential = true

      portMappings = [
        {
          containerPort = var.container_port
          protocol      = "tcp"
        }
      ]

      environment = [
        for k, v in var.environment_variables : {
          name  = k
          value = v
        }
      ]

      secrets = [
        for k, v in var.secrets : {
          name      = k
          valueFrom = v  # ARN of SSM Parameter or Secrets Manager secret
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.ecs.name
          "awslogs-region"        = var.region
          "awslogs-stream-prefix" = "ecs"
        }
      }

      healthCheck = {
        command     = ["CMD-SHELL", "curl -f http://localhost:${var.container_port}/health || exit 1"]
        interval    = 30
        timeout     = 5
        retries     = 3
        startPeriod = 60
      }
    }
  ])

  tags = {
    Environment = var.environment
    Project     = var.project
    ManagedBy   = "terraform"
  }
}
```

### ECS Service with Load Balancer

```hcl
resource "aws_ecs_service" "app" {
  name            = "${var.project}-${var.service_name}"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.ecs_service.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = var.service_name
    container_port   = var.container_port
  }

  deployment_configuration {
    maximum_percent         = 200
    minimum_healthy_percent = 100
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  depends_on = [aws_lb_listener_rule.app]

  tags = {
    Environment = var.environment
    Project     = var.project
    ManagedBy   = "terraform"
  }
}
```

### Auto-Scaling Configuration

```hcl
resource "aws_appautoscaling_target" "ecs" {
  max_capacity       = var.max_capacity
  min_capacity       = var.min_capacity
  resource_id        = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.app.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

# Scale based on CPU utilization
resource "aws_appautoscaling_policy" "cpu" {
  name               = "${var.service_name}-cpu-scaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    target_value       = 70.0
    scale_in_cooldown  = 300
    scale_out_cooldown = 60
  }
}

# Scale based on memory utilization
resource "aws_appautoscaling_policy" "memory" {
  name               = "${var.service_name}-memory-scaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageMemoryUtilization"
    }
    target_value       = 80.0
    scale_in_cooldown  = 300
    scale_out_cooldown = 60
  }
}

# Scale based on ALB request count
resource "aws_appautoscaling_policy" "requests" {
  name               = "${var.service_name}-request-scaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ALBRequestCountPerTarget"
      resource_label         = "${aws_lb.main.arn_suffix}/${aws_lb_target_group.app.arn_suffix}"
    }
    target_value       = 1000.0
    scale_in_cooldown  = 300
    scale_out_cooldown = 60
  }
}
```

### Common Fargate CPU/Memory Combinations

| CPU (units) | Memory (MiB) options           | Use case                      |
|-------------|--------------------------------|-------------------------------|
| 256         | 512, 1024, 2048                | Lightweight APIs, cron jobs   |
| 512         | 1024, 2048, 3072, 4096         | Standard web services         |
| 1024        | 2048, 3072, 4096, 5120-8192    | Compute-intensive APIs        |
| 2048        | 4096-16384 (1 GiB increments)  | Data processing, ML inference |
| 4096        | 8192-30720 (1 GiB increments)  | Heavy workloads               |

### AWS CLI Quick Reference for ECS

```bash
# List clusters
aws ecs list-clusters

# Describe service
aws ecs describe-services --cluster my-cluster --services my-service

# Update service (force new deployment)
aws ecs update-service --cluster my-cluster --service my-service \
  --force-new-deployment

# View running tasks
aws ecs list-tasks --cluster my-cluster --service-name my-service

# Execute command in running container
aws ecs execute-command --cluster my-cluster --task TASK_ID \
  --container my-container --interactive --command "/bin/sh"

# View task logs
aws logs get-log-events --log-group-name /ecs/my-service \
  --log-stream-name "ecs/my-container/TASK_ID"
```

---

## IAM Policies and Roles

### Principle of Least Privilege Checklist

Before creating any IAM policy, verify:

1. **Actions**: List only the specific API actions required (avoid `*`)
2. **Resources**: Scope to specific ARNs (avoid `Resource: *`)
3. **Conditions**: Add conditions to restrict access context where possible
4. **Duration**: Use temporary credentials (STS) over long-lived access keys
5. **Review**: Validate with IAM Access Analyzer before deployment

### Service Role Template (Lambda Example)

```hcl
# Execution role (what AWS needs to run the service)
resource "aws_iam_role" "lambda_execution" {
  name = "${var.project}-lambda-${var.function_name}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Condition = {
          StringEquals = {
            "aws:SourceAccount" = data.aws_caller_identity.current.account_id
          }
        }
      }
    ]
  })

  tags = {
    Environment = var.environment
    Project     = var.project
    ManagedBy   = "terraform"
  }
}

# Basic Lambda execution policy (CloudWatch Logs)
resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Custom policy for specific permissions
resource "aws_iam_role_policy" "lambda_custom" {
  name = "${var.function_name}-custom-policy"
  role = aws_iam_role.lambda_execution.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "ReadFromS3"
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          var.source_bucket_arn,
          "${var.source_bucket_arn}/*"
        ]
      },
      {
        Sid    = "WriteToS3"
        Effect = "Allow"
        Action = [
          "s3:PutObject"
        ]
        Resource = [
          "${var.destination_bucket_arn}/*"
        ]
      },
      {
        Sid    = "ReadSecrets"
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = [
          "arn:aws:secretsmanager:${var.region}:${data.aws_caller_identity.current.account_id}:secret:${var.project}/${var.environment}/*"
        ]
      }
    ]
  })
}
```

### ECS Task and Execution Roles

```hcl
# Execution role (for ECS agent to pull images, write logs)
resource "aws_iam_role" "ecs_execution" {
  name = "${var.project}-ecs-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_execution" {
  role       = aws_iam_role.ecs_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Allow reading secrets from SSM/Secrets Manager
resource "aws_iam_role_policy" "ecs_execution_secrets" {
  name = "ecs-execution-secrets"
  role = aws_iam_role.ecs_execution.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ssm:GetParameters",
          "secretsmanager:GetSecretValue"
        ]
        Resource = [
          "arn:aws:ssm:${var.region}:${data.aws_caller_identity.current.account_id}:parameter/${var.project}/${var.environment}/*",
          "arn:aws:secretsmanager:${var.region}:${data.aws_caller_identity.current.account_id}:secret:${var.project}/${var.environment}/*"
        ]
      }
    ]
  })
}

# Task role (for application code running inside the container)
resource "aws_iam_role" "ecs_task" {
  name = "${var.project}-ecs-task-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
    }]
  })
}

# Application-specific permissions
resource "aws_iam_role_policy" "ecs_task_app" {
  name = "ecs-task-app-permissions"
  role = aws_iam_role.ecs_task.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AccessAppBucket"
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          var.app_bucket_arn,
          "${var.app_bucket_arn}/*"
        ]
      },
      {
        Sid    = "PublishToSNS"
        Effect = "Allow"
        Action = [
          "sns:Publish"
        ]
        Resource = var.notification_topic_arn
      }
    ]
  })
}
```

### Common IAM Policy Patterns

**Deny-by-default with explicit allows:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyUnencryptedUploads",
      "Effect": "Deny",
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::my-bucket/*",
      "Condition": {
        "StringNotEquals": {
          "s3:x-amz-server-side-encryption": "aws:kms"
        }
      }
    }
  ]
}
```

**Restrict access by IP or VPC:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "VPCRestricted",
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": "arn:aws:s3:::my-bucket/*",
      "Condition": {
        "StringEquals": {
          "aws:SourceVpce": "vpce-1234567890abcdef0"
        }
      }
    }
  ]
}
```

**Tag-based access control:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ManageOwnResources",
      "Effect": "Allow",
      "Action": ["ec2:StartInstances", "ec2:StopInstances"],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:ResourceTag/Owner": "${aws:PrincipalTag/Owner}"
        }
      }
    }
  ]
}
```

---

## Terraform AWS Provider Modules

### Provider Configuration

```hcl
terraform {
  required_version = ">= 1.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "my-project-terraform-state"
    key            = "infrastructure/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-lock"
  }
}

provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Environment = var.environment
      Project     = var.project
      ManagedBy   = "terraform"
      Repository  = var.repository_url
    }
  }
}
```

### Recommended Module Structure

```
infra/
  environments/
    dev/
      main.tf           # Module calls with dev-specific variables
      variables.tf
      terraform.tfvars
      backend.tf
    staging/
      main.tf
      variables.tf
      terraform.tfvars
      backend.tf
    prod/
      main.tf
      variables.tf
      terraform.tfvars
      backend.tf
  modules/
    networking/
      main.tf           # VPC, subnets, NAT gateway, security groups
      variables.tf
      outputs.tf
    compute/
      main.tf           # ECS cluster, task definitions, services
      variables.tf
      outputs.tf
    storage/
      main.tf           # S3 buckets, DynamoDB tables
      variables.tf
      outputs.tf
    iam/
      main.tf           # Roles, policies, instance profiles
      variables.tf
      outputs.tf
    monitoring/
      main.tf           # CloudWatch alarms, dashboards, SNS topics
      variables.tf
      outputs.tf
```

### State Management Best Practices

- **Remote state**: Always use S3 backend with DynamoDB locking
- **State isolation**: Separate state files per environment
- **Encryption**: Enable server-side encryption on the state bucket
- **Versioning**: Enable versioning on the state bucket for state recovery
- **Access control**: Restrict state bucket access with IAM policies

### Terraform Workflow Commands

```bash
# Initialize working directory
terraform init

# Format code
terraform fmt -recursive

# Validate configuration
terraform validate

# Plan changes (always review before applying)
terraform plan -out=tfplan

# Apply changes from saved plan
terraform apply tfplan

# Destroy resources (use with extreme caution)
terraform plan -destroy -out=destroy-plan
terraform apply destroy-plan

# Import existing resources
terraform import aws_s3_bucket.main my-existing-bucket

# Show current state
terraform state list
terraform state show aws_s3_bucket.main

# Move resources within state (refactoring)
terraform state mv aws_s3_bucket.old aws_s3_bucket.new
```

### Common Variables Pattern

```hcl
variable "environment" {
  description = "Deployment environment (dev, staging, prod)"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}

variable "region" {
  description = "AWS region for resource deployment"
  type        = string
  default     = "us-east-1"
}

variable "project" {
  description = "Project name used for resource naming and tagging"
  type        = string
}
```

---

## Cost Optimization Patterns

### Compute Cost Optimization

| Strategy                    | Service       | Potential Savings | Implementation Effort |
|-----------------------------|---------------|-------------------|-----------------------|
| Reserved Instances          | EC2, RDS      | 30-72%            | Low                   |
| Savings Plans               | EC2, Fargate  | 20-72%            | Low                   |
| Spot Instances              | EC2, ECS      | 60-90%            | Medium                |
| Right-sizing                | All compute   | 10-50%            | Medium                |
| Graviton (ARM) instances    | EC2, ECS, RDS | 20-40%            | Low-Medium            |
| Auto-scaling                | EC2, ECS      | 20-60%            | Medium                |
| Scheduled scaling           | EC2, ECS      | 30-70%            | Low                   |

### Storage Cost Optimization

| Strategy                     | Service       | Potential Savings | Implementation Effort |
|------------------------------|---------------|-------------------|-----------------------|
| S3 Lifecycle policies        | S3            | 30-80%            | Low                   |
| S3 Intelligent-Tiering       | S3            | 10-40%            | Low                   |
| EBS volume right-sizing      | EC2           | 10-40%            | Medium                |
| GP3 over GP2 volumes         | EC2           | 20%               | Low                   |
| Delete unused snapshots      | EBS           | Variable          | Low                   |

### Lambda Cost Optimization

- **Right-size memory**: Use AWS Lambda Power Tuning to find optimal memory
- **Reduce cold starts**: Use provisioned concurrency for latency-sensitive functions
- **Optimize code**: Reduce execution time by optimizing imports and logic
- **Use ARM64 architecture**: Graviton2 provides better price-performance
- **Batch processing**: Use larger batch sizes for event source mappings

```hcl
# Example: Graviton2 Lambda
resource "aws_lambda_function" "optimized" {
  function_name = "my-optimized-function"
  architectures = ["arm64"]  # 20% cheaper than x86_64
  memory_size   = 256        # Right-sized with Power Tuning
  runtime       = "python3.12"
  # ... other config
}
```

### ECS/Fargate Cost Optimization

- **Use Fargate Spot**: Up to 70% savings for fault-tolerant workloads
- **Right-size tasks**: Monitor CPU/memory utilization and adjust
- **Use ARM64 (Graviton)**: 20% lower price, 40% better price-performance
- **Schedule scale-down**: Reduce capacity during off-peak hours

```hcl
# Fargate Spot capacity provider
resource "aws_ecs_cluster_capacity_providers" "main" {
  cluster_name = aws_ecs_cluster.main.name

  capacity_providers = ["FARGATE", "FARGATE_SPOT"]

  default_capacity_provider_strategy {
    base              = 1
    weight            = 1
    capacity_provider = "FARGATE"
  }

  default_capacity_provider_strategy {
    weight            = 3
    capacity_provider = "FARGATE_SPOT"
  }
}
```

### Cost Monitoring with AWS CLI

```bash
# Get current month cost estimate
aws ce get-cost-and-usage \
  --time-period Start=$(date -u +"%Y-%m-01"),End=$(date -u +"%Y-%m-%d") \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by Type=DIMENSION,Key=SERVICE

# Find unused EBS volumes
aws ec2 describe-volumes \
  --filters "Name=status,Values=available" \
  --query 'Volumes[*].{ID:VolumeId,Size:Size,Type:VolumeType}' \
  --output table

# Find unattached Elastic IPs (charged when unused)
aws ec2 describe-addresses \
  --query 'Addresses[?AssociationId==`null`].{IP:PublicIp,AllocationId:AllocationId}' \
  --output table

# Find old snapshots (older than 90 days)
aws ec2 describe-snapshots --owner-ids self \
  --query 'Snapshots[?StartTime<=`'"$(date -u -d '90 days ago' +%Y-%m-%dT%H:%M:%S)"'`].{ID:SnapshotId,Size:VolumeSize,Start:StartTime}' \
  --output table
```

### Cost Optimization Terraform Module

```hcl
# Budget alarm
resource "aws_budgets_budget" "monthly" {
  name         = "${var.project}-monthly-budget"
  budget_type  = "COST"
  limit_amount = var.monthly_budget_limit
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = var.budget_alert_emails
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = var.budget_alert_emails
  }
}
```
