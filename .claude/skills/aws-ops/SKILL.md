---
name: aws-ops
description: "Manages AWS resources including S3, Lambda, ECS, and IAM. Use when working with AWS infrastructure, deploying services, configuring Terraform for AWS, or managing IAM roles and policies."
allowed-tools: Bash(aws *), Bash(terraform *), Read, Write
---

# AWS Operations

Manage AWS infrastructure resources, deploy services, configure Terraform modules, and maintain IAM policies following AWS best practices and the principle of least privilege.

## Prerequisites

- **AWS CLI v2** installed and configured (`aws --version`)
- **Terraform** >= 1.5 installed (`terraform --version`)
- **Valid AWS credentials** configured via environment variables, AWS profiles, or IAM roles:
  ```bash
  aws sts get-caller-identity
  ```
- **Required environment variables** (or AWS profile configured):
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_DEFAULT_REGION` (defaults to `us-east-1` if unset)

## Instructions

Before performing any AWS operation, read the [reference.md](reference.md) file for detailed patterns, policy templates, and Terraform module structures.

### Workflow

1. **Identify the target AWS service and operation**:
   - Determine whether this is an S3, Lambda, ECS, IAM, or multi-service task
   - Check if Terraform state already exists for the target resources
   - Verify the AWS account and region are correct:
     ```bash
     aws sts get-caller-identity
     aws configure get region
     ```

2. **Check existing infrastructure state**:
   - Look for existing Terraform files in `infra/`, `terraform/`, or `iac/` directories
   - If Terraform is in use, always run `terraform plan` before `terraform apply`
   - If using AWS CLI directly, list existing resources before creating new ones:
     ```bash
     aws s3 ls
     aws lambda list-functions --region us-east-1
     aws ecs list-clusters --region us-east-1
     ```

3. **Apply the principle of least privilege for all IAM operations**:
   - Never use wildcard (`*`) actions in production IAM policies
   - Scope resources to specific ARNs whenever possible
   - Add condition keys to restrict access context (e.g., `aws:SourceIp`, `aws:PrincipalOrgID`)
   - Refer to [reference.md](reference.md) for IAM policy templates

4. **Implement the change**:
   - For Terraform: write or modify `.tf` files, then run `terraform fmt`, `terraform validate`, `terraform plan`
   - For AWS CLI: execute commands and capture output for verification
   - For both: tag all resources with `Environment`, `Project`, and `ManagedBy` tags

5. **Verify and validate**:
   - Confirm resources were created or modified as expected
   - Verify IAM policies are not overly permissive
   - Check that encryption is enabled where applicable (S3, EBS, RDS)
   - Validate security groups do not expose unnecessary ports

6. **Document the change**:
   - Update any infrastructure documentation
   - Record resource ARNs and endpoints
   - Note any manual steps required for completion

### Key Principles

- **Encryption by default**: Enable server-side encryption on S3 buckets, EBS volumes, and RDS instances
- **Tagging discipline**: Every resource must have `Environment`, `Project`, and `ManagedBy` tags at minimum
- **Least privilege**: IAM policies should grant the minimum permissions required
- **Infrastructure as Code preferred**: Use Terraform over manual AWS CLI when possible for reproducibility
- **Cost awareness**: Check pricing implications before provisioning; prefer reserved/spot instances when suitable
- **Region awareness**: Always confirm the target region before creating resources

### Supporting Reference

For detailed patterns, templates, and best practices for each AWS service, see [reference.md](reference.md). It covers:

- S3 bucket policies, versioning, and lifecycle rules
- Lambda packaging, deployment, and layer management
- ECS task definitions, services, and auto-scaling
- IAM policy structures and role trust relationships
- Terraform AWS provider modules and state management
- Cost optimization strategies

## Examples

### Example 1: Create an S3 Bucket with Versioning and Encryption

User request:
```
Create an S3 bucket for storing application logs with versioning and encryption enabled
```

You would:
1. Verify AWS credentials and target region:
   ```bash
   aws sts get-caller-identity
   ```
2. Check for existing Terraform infrastructure files in the project
3. If using Terraform, create or update `s3.tf`:
   ```hcl
   resource "aws_s3_bucket" "app_logs" {
     bucket = "myproject-app-logs-${var.environment}"
     tags = {
       Environment = var.environment
       Project     = "myproject"
       ManagedBy   = "terraform"
     }
   }

   resource "aws_s3_bucket_versioning" "app_logs" {
     bucket = aws_s3_bucket.app_logs.id
     versioning_configuration {
       status = "Enabled"
     }
   }

   resource "aws_s3_bucket_server_side_encryption_configuration" "app_logs" {
     bucket = aws_s3_bucket.app_logs.id
     rule {
       apply_server_side_encryption_by_default {
         sse_algorithm = "aws:kms"
       }
     }
   }

   resource "aws_s3_bucket_public_access_block" "app_logs" {
     bucket                  = aws_s3_bucket.app_logs.id
     block_public_acls       = true
     block_public_policy     = true
     ignore_public_acls      = true
     restrict_public_buckets = true
   }
   ```
4. Run `terraform fmt && terraform validate && terraform plan`
5. After user confirmation, run `terraform apply`
6. Verify the bucket was created:
   ```bash
   aws s3api get-bucket-versioning --bucket myproject-app-logs-dev
   aws s3api get-bucket-encryption --bucket myproject-app-logs-dev
   ```

### Example 2: Deploy a Lambda Function with an IAM Role

User request:
```
Deploy a Python Lambda function that processes SQS messages with proper IAM permissions
```

You would:
1. Read [reference.md](reference.md) for Lambda packaging and IAM policy patterns
2. Create the Lambda handler code in `src/lambda/processor/handler.py`
3. Create the IAM role with least-privilege permissions in Terraform:
   ```hcl
   resource "aws_iam_role" "lambda_processor" {
     name = "lambda-sqs-processor-role"
     assume_role_policy = jsonencode({
       Version = "2012-10-17"
       Statement = [{
         Action = "sts:AssumeRole"
         Effect = "Allow"
         Principal = { Service = "lambda.amazonaws.com" }
       }]
     })
   }

   resource "aws_iam_role_policy" "sqs_read" {
     name = "sqs-read-policy"
     role = aws_iam_role.lambda_processor.id
     policy = jsonencode({
       Version = "2012-10-17"
       Statement = [{
         Effect   = "Allow"
         Action   = [
           "sqs:ReceiveMessage",
           "sqs:DeleteMessage",
           "sqs:GetQueueAttributes"
         ]
         Resource = aws_sqs_queue.processor_queue.arn
       }]
     })
   }
   ```
4. Package and deploy the Lambda:
   ```bash
   cd src/lambda/processor
   zip -r ../../../build/processor.zip handler.py
   ```
5. Apply Terraform and verify:
   ```bash
   terraform apply
   aws lambda invoke --function-name sqs-processor --payload '{}' output.json
   ```
6. Confirm the event source mapping connects SQS to Lambda

### Example 3: Set Up an ECS Fargate Service with Auto-Scaling

User request:
```
Create an ECS Fargate service for our API with auto-scaling based on CPU usage
```

You would:
1. Read [reference.md](reference.md) for ECS task definition and service patterns
2. Check for existing VPC, subnets, and security group resources in Terraform state
3. Create the ECS task definition with appropriate resource limits:
   ```hcl
   resource "aws_ecs_task_definition" "api" {
     family                   = "api-task"
     network_mode             = "awsvpc"
     requires_compatibilities = ["FARGATE"]
     cpu                      = "256"
     memory                   = "512"
     execution_role_arn       = aws_iam_role.ecs_execution.arn
     task_role_arn            = aws_iam_role.ecs_task.arn

     container_definitions = jsonencode([{
       name      = "api"
       image     = "${var.ecr_repo_url}:latest"
       essential = true
       portMappings = [{ containerPort = 8000, protocol = "tcp" }]
       logConfiguration = {
         logDriver = "awslogs"
         options = {
           "awslogs-group"         = "/ecs/api"
           "awslogs-region"        = var.region
           "awslogs-stream-prefix" = "ecs"
         }
       }
     }])
   }
   ```
4. Create the ECS service and attach it to a load balancer
5. Configure auto-scaling:
   ```hcl
   resource "aws_appautoscaling_target" "api" {
     max_capacity       = 10
     min_capacity       = 2
     resource_id        = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.api.name}"
     scalable_dimension = "ecs:service:DesiredCount"
     service_namespace  = "ecs"
   }

   resource "aws_appautoscaling_policy" "cpu" {
     name               = "api-cpu-scaling"
     policy_type        = "TargetTrackingScaling"
     resource_id        = aws_appautoscaling_target.api.resource_id
     scalable_dimension = aws_appautoscaling_target.api.scalable_dimension
     service_namespace  = aws_appautoscaling_target.api.service_namespace

     target_tracking_scaling_policy_configuration {
       predefined_metric_specification {
         predefined_metric_type = "ECSServiceAverageCPUUtilization"
       }
       target_value = 70.0
     }
   }
   ```
6. Run `terraform plan` and `terraform apply`
7. Verify the service is running:
   ```bash
   aws ecs describe-services --cluster main --services api-service --region us-east-1
   ```
8. Monitor the auto-scaling configuration:
   ```bash
   aws application-autoscaling describe-scaling-policies --service-namespace ecs
   ```
