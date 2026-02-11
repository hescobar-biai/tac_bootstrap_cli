# Plan de Tareas: Evolucion TAC Bootstrap para Celes Stack

## Assumptions

1. Current version is `1.0.0` as per CHANGELOG.md. This plan will bump to `1.1.0` (minor: new features, no breaking changes).
2. All new skills follow the Claude Code Skills specification (SKILL.md + supporting files + YAML frontmatter).
3. The `.claude/commands/` files remain functional (backward compatible). New skills are additive.
4. dbt dual-target means both `dbt-bigquery` and `dbt-postgres` adapters are supported.
5. ML multi-framework means templates support Prophet, LightGBM, XGBoost, PyTorch, scikit-learn, and statsmodels.
6. The plugin directory lives inside the existing repo at `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac-bootstrap-plugin/`.
7. Expert expertise.yaml files use `FileAction.SKIP_IF_EXISTS` to preserve learned knowledge.
8. Schema migration from v2 to v3 adds `data_engineering`, `ml`, and `infrastructure` optional sections to config.yml.
9. Templates for new skills are created as `.j2` files so `tac-bootstrap init` generates them for new projects.
10. The `.venv/` inside `templates/apps/orchestrator_3_stream/backend/` contains hundreds of site-packages and must be replaced with a `requirements.txt`.

---

## Tasks

### 1. [CHORE] Remove committed `.venv/` from template directory

**Title**: Delete `.venv/` from orchestrator backend template and replace with requirements.txt

**Description**:
- Delete the entire directory at `templates/apps/orchestrator_3_stream/backend/.venv/` which contains hundreds of Python site-packages committed to the repository
- Create a `requirements.txt` file inside `templates/apps/orchestrator_3_stream/backend/` listing all dependencies that were in the `.venv/`
- Add `.venv/` to `templates/apps/orchestrator_3_stream/backend/.gitignore` (create if not exists)
- Update `_add_orchestrator_apps()` in `scaffold_service.py` — the `_APPS_EXCLUDE_DIRS` set already excludes `.venv/` so no code change needed, but verify the requirements.txt is copied
- Acceptance: `du -sh tac_bootstrap_cli/tac_bootstrap/templates/apps/` shows >80% size reduction. `git status` shows `.venv/` files removed.

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/apps/orchestrator_3_stream/backend/.venv/` (DELETE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/apps/orchestrator_3_stream/backend/requirements.txt` (CREATE)

---

### 2. [CHORE] Remove dead ImportError fallback code from CLI

**Title**: Delete stale ImportError catch blocks in cli.py init, add-agentic, doctor, render commands

**Description**:
- In `cli.py`, locate the `except ImportError as e:` blocks in the `init`, `add_agentic`, `doctor`, and `render` command functions
- These blocks print "...not yet implemented... TAREA 4.2" / "FASE 6" / "FASE 7" messages — the services now exist and these branches are unreachable dead code
- Remove each `except ImportError` block entirely (4 total)
- Acceptance: `grep -n "not yet implemented" cli.py` returns 0 results. All 4 commands still function correctly.

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py` (MODIFY: lines ~352, ~507, ~605, ~727)

---

### 3. [CHORE] Remove duplicate domain model definitions

**Title**: Consolidate FieldType, EntitySpec, FieldSpec into single source in entity_config.py

**Description**:
- `domain/models.py` and `domain/entity_config.py` both define `FieldType`, `EntitySpec`, and `FieldSpec` with different validators
- Keep the more comprehensive versions in `domain/entity_config.py` (which has PascalCase, reserved name, and SQLAlchemy conflict validators)
- Remove `FieldType`, `FieldSpec`, and `EntitySpec` from `domain/models.py`
- Update all imports in `cli.py`, `generate_service.py`, `entity_generator_service.py`, and `entity_wizard.py` to import from `domain.entity_config`
- Acceptance: `grep -rn "class FieldType" tac_bootstrap/domain/` returns exactly 1 result (in `entity_config.py`). `uv run pytest` passes.

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/domain/models.py` (MODIFY: remove 3 classes)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/domain/entity_config.py` (no change, source of truth)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py` (MODIFY: update imports)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/application/generate_service.py` (MODIFY: update imports)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/application/entity_generator_service.py` (MODIFY: update imports)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/interfaces/entity_wizard.py` (MODIFY: update imports)

---

### 4. [CHORE] Remove stale files from repository

**Title**: Delete test_wizard.py.bak and orchestrator.db from repository root

**Description**:
- Delete `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tests/test_wizard.py.bak` — stale backup file
- Delete `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/orchestrator.db` — SQLite database that should not be committed (74KB)
- Add `orchestrator.db` to root `.gitignore` if not already present
- Acceptance: Both files no longer exist. `git status` shows them as deleted.

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tests/test_wizard.py.bak` (DELETE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/orchestrator.db` (DELETE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.gitignore` (MODIFY: add `orchestrator.db`)

---

### 5. [FEATURE] Create `bigquery-ops` skill

**Title**: Create BigQuery operations skill with reference documentation and supply chain query examples

**Description**:
- Create skill directory structure:
  - `.claude/skills/bigquery-ops/SKILL.md` — Main instructions with YAML frontmatter: `name: bigquery-ops`, `description: "Manage BigQuery datasets, tables, and queries..."`, `allowed-tools: Bash(bq *), Bash(gcloud *), Read, Write, Grep`
  - `.claude/skills/bigquery-ops/reference.md` — BigQuery best practices: partitioning by date, clustering by SKU/store, materialized views for demand aggregations, slot estimation formulas, cost optimization patterns
  - `.claude/skills/bigquery-ops/examples/supply_chain_queries.sql` — Example queries: demand aggregation by SKU, inventory turnover, stockout detection, fill rate calculation
- SKILL.md must include capabilities: DDL generation, query optimization, Python client scaffolding (`google-cloud-bigquery`), schema validation
- Acceptance: `/bigquery-ops` is listed when asking Claude "What skills are available?". Invoking `/bigquery-ops "Create a partitioned demand table"` produces a valid BigQuery DDL.

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/bigquery-ops/SKILL.md` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/bigquery-ops/reference.md` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/bigquery-ops/examples/supply_chain_queries.sql` (CREATE)

---

### 6. [FEATURE] Create `dbt-workflow` skill with dual-target support

**Title**: Create dbt workflow skill supporting BigQuery and PostgreSQL targets with supply chain model templates

**Description**:
- Create skill directory structure:
  - `.claude/skills/dbt-workflow/SKILL.md` — Main instructions with frontmatter: `name: dbt-workflow`, `description: "Create and manage dbt models, tests, and documentation. Supports dual-target BigQuery and PostgreSQL."`, `disable-model-invocation: true`, `allowed-tools: Bash(dbt *), Read, Write, Edit, Grep, Glob`
  - `.claude/skills/dbt-workflow/reference.md` — dbt conventions: staging/intermediate/marts layer pattern, naming conventions (`stg_`, `int_`, `fct_`, `dim_`), cross-database macros using `target.type`, `profiles.yml` dual-target configuration for `dbt-bigquery` and `dbt-postgres` adapters
  - `.claude/skills/dbt-workflow/templates/stg_template.sql` — Staging model template with source reference and column renaming
  - `.claude/skills/dbt-workflow/templates/fct_template.sql` — Fact model template with joins and metrics
  - `.claude/skills/dbt-workflow/templates/schema_template.yml` — schema.yml with tests (not_null, unique, accepted_values, relationships)
  - `.claude/skills/dbt-workflow/examples/` — Supply chain examples: `stg_orders.sql`, `fct_demand.sql`, `dim_products.sql`
- Acceptance: `/dbt-workflow "Create staging model for inventory snapshots"` produces valid dbt SQL with source macro and schema.yml.

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/dbt-workflow/SKILL.md` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/dbt-workflow/reference.md` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/dbt-workflow/templates/stg_template.sql` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/dbt-workflow/templates/fct_template.sql` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/dbt-workflow/templates/schema_template.yml` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/dbt-workflow/examples/` (CREATE directory + 3 files)

---

### 7. [FEATURE] Create `ml-forecast` skill with multi-framework support

**Title**: Create ML forecasting skill supporting Prophet, LightGBM, XGBoost, PyTorch, scikit-learn, and statsmodels

**Description**:
- Create skill directory structure:
  - `.claude/skills/ml-forecast/SKILL.md` — Main instructions with frontmatter: `name: ml-forecast`, `description: "Build and optimize demand forecasting models using multiple frameworks..."`, `context: fork`, `agent: ml-engineer`
  - `.claude/skills/ml-forecast/reference.md` — Multi-framework patterns: Prophet (seasonal decomposition, holiday effects), LightGBM/XGBoost (tabular features, hyperparameter tuning with Optuna), PyTorch (LSTM, Temporal Fusion Transformer), scikit-learn (pipelines, preprocessing), statsmodels (ARIMA, ETS). Feature engineering: lags, rolling stats, calendar features, promotional flags. Metrics: MAPE, WMAPE, bias, fill rate, OTIF.
  - `.claude/skills/ml-forecast/templates/train_pipeline.py` — Base training pipeline with sklearn Pipeline pattern, train/val/test split by time
  - `.claude/skills/ml-forecast/templates/evaluate.py` — Evaluation script with supply chain metrics (MAPE, WMAPE, bias, fill_rate)
  - `.claude/skills/ml-forecast/examples/demand_forecast_lightgbm.py` — Complete LightGBM demand forecasting example
  - `.claude/skills/ml-forecast/examples/demand_forecast_prophet.py` — Complete Prophet forecasting example
- Acceptance: `/ml-forecast "Create a demand forecasting pipeline using LightGBM"` produces a complete Python script with feature engineering, training, and evaluation using supply chain metrics.

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/ml-forecast/SKILL.md` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/ml-forecast/reference.md` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/ml-forecast/templates/train_pipeline.py` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/ml-forecast/templates/evaluate.py` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/ml-forecast/examples/` (CREATE directory + 2 files)

---

### 8. [FEATURE] Create `fastapi-ddd` skill

**Title**: Create FastAPI + DDD skill for generating vertical slice architecture components

**Description**:
- Create skill directory structure:
  - `.claude/skills/fastapi-ddd/SKILL.md` — Main instructions with frontmatter: `name: fastapi-ddd`, `description: "Generate and maintain FastAPI services with Domain-Driven Design patterns..."`. Include instructions for: vertical slice scaffolding (entity, repository, service, routes, schemas), Alembic migration generation, async SQLAlchemy patterns, dependency injection with FastAPI Depends.
  - `.claude/skills/fastapi-ddd/reference.md` — DDD patterns for FastAPI: Repository pattern (sync + async), Service layer with domain events, Value Objects, Aggregate Roots, CQRS read/write separation. Celes-specific: convention for domain directories, naming patterns, import structure.
  - `.claude/skills/fastapi-ddd/templates/` — Skeleton files for each DDD component: `entity.py`, `repository.py`, `service.py`, `routes.py`, `schemas.py`
- Acceptance: `/fastapi-ddd "Create a Product domain with CRUD"` produces 5 DDD files following the existing template patterns in `tac_bootstrap_cli/tac_bootstrap/templates/entity/`.

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/fastapi-ddd/SKILL.md` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/fastapi-ddd/reference.md` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/fastapi-ddd/templates/` (CREATE directory + 5 files)

---

### 9. [FEATURE] Create `react-frontend` skill

**Title**: Create React frontend skill for components, hooks, and supply chain dashboards

**Description**:
- Create skill directory structure:
  - `.claude/skills/react-frontend/SKILL.md` — Main instructions with frontmatter: `name: react-frontend`, `description: "Generate React components, hooks, and pages following project conventions..."`. Include instructions for: functional components with TypeScript, custom hooks, dashboard layouts (tables, filters, charts), FastAPI API integration with fetch/axios.
  - `.claude/skills/react-frontend/reference.md` — React patterns: component composition, custom hooks for data fetching, React Query/TanStack Query patterns, Zustand/Context for state, data table patterns for inventory/demand views
  - `.claude/skills/react-frontend/templates/` — `Component.tsx`, `useDataHook.ts`, `DashboardPage.tsx` skeleton files
- Acceptance: `/react-frontend "Create an inventory dashboard with filters and table"` produces valid TSX components.

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/react-frontend/SKILL.md` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/react-frontend/reference.md` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/react-frontend/templates/` (CREATE directory + 3 files)

---

### 10. [FEATURE] Create `gcp-infra` skill

**Title**: Create GCP infrastructure skill for Cloud Storage, BigQuery, Cloud Run, IAM, and Terraform

**Description**:
- Create skill directory structure:
  - `.claude/skills/gcp-infra/SKILL.md` — Main instructions with frontmatter: `name: gcp-infra`, `description: "Manage GCP infrastructure including Cloud Storage, Cloud Functions, Cloud Run, and IAM..."`, `allowed-tools: Bash(gcloud *), Bash(gsutil *), Bash(terraform *), Read, Write`
  - `.claude/skills/gcp-infra/reference.md` — GCP patterns: bucket lifecycle policies, IAM least-privilege for service accounts, Cloud Run deployment with environment variables, Terraform modules for GCP resources, BigQuery dataset permissions
  - `.claude/skills/gcp-infra/templates/` — `main.tf` (provider + backend), `bigquery.tf`, `storage.tf`, `cloudrun.tf` skeleton Terraform files
- Acceptance: `/gcp-infra "Create a Cloud Storage bucket with lifecycle policy"` produces a valid Terraform configuration or gcloud command.

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/gcp-infra/SKILL.md` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/gcp-infra/reference.md` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/gcp-infra/templates/` (CREATE directory + 4 files)

---

### 11. [FEATURE] Create `aws-ops` skill

**Title**: Create AWS operations skill for S3, Lambda, ECS, IAM, and Terraform

**Description**:
- Create skill directory structure:
  - `.claude/skills/aws-ops/SKILL.md` — Main instructions with frontmatter: `name: aws-ops`, `description: "Manage AWS resources including S3, Lambda, ECS, and IAM..."`, `allowed-tools: Bash(aws *), Bash(terraform *), Read, Write`
  - `.claude/skills/aws-ops/reference.md` — AWS patterns: S3 bucket policies, Lambda function packaging, ECS task definitions, IAM policies and roles, Terraform AWS provider modules
- Acceptance: `/aws-ops "Create an S3 bucket with versioning"` produces a valid Terraform configuration or AWS CLI command.

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/aws-ops/SKILL.md` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/aws-ops/reference.md` (CREATE)

---

### 12. [FEATURE] Create `data-pipeline` skill

**Title**: Create data pipeline skill for ETL/ELT workflows integrating BigQuery, Cloud Storage, and dbt

**Description**:
- Create skill directory structure:
  - `.claude/skills/data-pipeline/SKILL.md` — Main instructions with frontmatter: `name: data-pipeline`, `description: "Design and implement data pipelines for ETL/ELT workflows..."`, `allowed-tools: Bash(python *), Bash(dbt *), Bash(bq *), Read, Write, Edit`
  - `.claude/skills/data-pipeline/reference.md` — ETL/ELT patterns: Cloud Storage → BigQuery loading (bq load, external tables), dbt transformations, data quality checks (Great Expectations, dbt tests), Cloud Composer/Airflow DAG patterns, idempotent pipeline design, backfill strategies
  - `.claude/skills/data-pipeline/templates/dag_template.py` — Airflow DAG skeleton for Cloud Composer
  - `.claude/skills/data-pipeline/templates/loader.py` — BigQuery data loader skeleton with Cloud Storage integration
- Acceptance: `/data-pipeline "Create an ETL pipeline from Cloud Storage to BigQuery with dbt transformation"` produces a coherent pipeline design with loader and dbt model.

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/data-pipeline/SKILL.md` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/data-pipeline/reference.md` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/data-pipeline/templates/dag_template.py` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/data-pipeline/templates/loader.py` (CREATE)

---

### 13. [FEATURE] Create `data-engineer` agent definition

**Title**: Create data engineering agent specialized in dbt, BigQuery, and pipeline design

**Description**:
- Create agent file at `.claude/agents/data-engineer.md` with frontmatter: `model: opus`
- Agent persona: "Data Engineering Agent specialized in dbt model development, BigQuery query optimization, Cloud Storage management, and data pipeline design"
- Allowed tools: `Bash(dbt *), Bash(bq *), Bash(gsutil *), Bash(python *), Read, Write, Edit, Grep, Glob`
- Include domain context: dbt conventions (staging/marts), BigQuery partitioning/clustering, idempotent pipeline design, data quality testing
- Acceptance: Agent is available when using `context: fork` with `agent: data-engineer` in skills.

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/data-engineer.md` (CREATE)

---

### 14. [FEATURE] Create `ml-engineer` agent definition

**Title**: Create ML engineering agent specialized in demand forecasting and model evaluation

**Description**:
- Create agent file at `.claude/agents/ml-engineer.md` with frontmatter: `model: opus`
- Agent persona: "ML Engineering Agent specialized in demand forecasting, feature engineering, model training/evaluation, and deployment for supply chain optimization"
- Allowed tools: `Bash(python *), Read, Write, Edit, Grep, Glob, NotebookEdit`
- Include domain context: multi-framework support (Prophet, LightGBM, XGBoost, PyTorch, scikit-learn, statsmodels), supply chain metrics (MAPE, WMAPE, bias, fill rate, OTIF), ensemble methods
- Acceptance: Agent is available when using `context: fork` with `agent: ml-engineer` in skills.

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/ml-engineer.md` (CREATE)

---

### 15. [FEATURE] Create `infra-ops` agent definition

**Title**: Create infrastructure operations agent specialized in GCP/AWS and Terraform

**Description**:
- Create agent file at `.claude/agents/infra-ops.md` with frontmatter: `model: sonnet`
- Agent persona: "Infrastructure Operations Agent specialized in GCP and AWS infrastructure management, Terraform IaC, deployment pipelines, and cost optimization"
- Allowed tools: `Bash(gcloud *), Bash(aws *), Bash(terraform *), Bash(gsutil *), Read, Write, Edit, Grep, Glob`
- Include domain context: Terraform module patterns, IAM best practices, Cloud Run deployment, BigQuery dataset management
- Acceptance: Agent is available when using `context: fork` with `agent: infra-ops` in skills.

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/infra-ops.md` (CREATE)

---

### 16. [FEATURE] Create data-engineering expert with self-improving expertise

**Title**: Create data engineering expert system with expertise.yaml, question skill, and self-improve skill

**Description**:
- Create expert directory at `.claude/skills/experts/data-engineering/` with 3 files:
  - `SKILL.md` — Expert skill with frontmatter: `name: experts:data-engineering:question`, `description: "Answer questions about data engineering, dbt, BigQuery, and ETL patterns"`, `user-invocable: true`. Instructions: load expertise.yaml, validate against codebase, answer questions using domain knowledge.
  - `expertise.yaml` — Initial seed file (~400 lines) covering: dbt model layers (staging/intermediate/marts), BigQuery optimization (partitioning, clustering, materialized views), Cloud Storage patterns (lifecycle, notifications), ETL/ELT design patterns, data quality frameworks, scheduling (Cloud Composer), lineage tracking
  - `self-improve.md` — 7-phase self-improvement workflow: (1) load expertise.yaml, (2) scan codebase for data engineering files, (3) identify gaps, (4) validate patterns, (5) update expertise.yaml, (6) verify consistency, (7) report changes
- Also create `/experts:data-engineering:question` and `/experts:data-engineering:self-improve` as separate commands referencing the skill
- Acceptance: `/experts:data-engineering:question "How should I partition our demand table in BigQuery?"` returns a domain-specific answer using expertise.yaml context.

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/experts/data-engineering/SKILL.md` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/experts/data-engineering/expertise.yaml` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/data-engineering/question.md` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/data-engineering/self-improve.md` (CREATE)

---

### 17. [FEATURE] Create ML/forecasting expert with self-improving expertise

**Title**: Create ML forecasting expert system with expertise.yaml, question skill, and self-improve skill

**Description**:
- Create expert directory at `.claude/skills/experts/ml-forecasting/` with 3 files:
  - `SKILL.md` — Expert skill with frontmatter: `name: experts:ml-forecasting:question`, `description: "Answer questions about demand forecasting, ML pipelines, and model evaluation"`
  - `expertise.yaml` — Initial seed (~400 lines) covering: demand forecasting methods (Prophet, LightGBM, XGBoost, PyTorch LSTM/TFT, ARIMA), feature engineering (lags, rolling, calendar, promotions), evaluation metrics (MAPE, WMAPE, bias, fill rate, OTIF), model selection strategy, ensemble methods (stacking, blending), deployment patterns (batch, online, shadow)
  - `self-improve.md` — 7-phase self-improvement workflow
- Create corresponding command files for invocation
- Acceptance: `/experts:ml-forecasting:question "Which model should I use for intermittent demand?"` returns domain-specific guidance.

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/experts/ml-forecasting/SKILL.md` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/experts/ml-forecasting/expertise.yaml` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/ml-forecasting/question.md` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/ml-forecasting/self-improve.md` (CREATE)

---

### 18. [FEATURE] Create GCP infrastructure expert with self-improving expertise

**Title**: Create GCP infrastructure expert system with expertise.yaml, question skill, and self-improve skill

**Description**:
- Create expert directory at `.claude/skills/experts/gcp-infra/` with 3 files:
  - `SKILL.md` — Expert skill with frontmatter for question answering about GCP resources
  - `expertise.yaml` — Initial seed covering: BigQuery optimization (slot management, reservation, BI Engine), Cloud Storage (classes, lifecycle, notifications), Cloud Run (scaling, cold starts, concurrency), IAM (least privilege, workload identity), Terraform (module patterns, state management), cost optimization
  - `self-improve.md` — 7-phase self-improvement workflow
- Acceptance: `/experts:gcp-infra:question` returns domain-specific GCP answers.

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/experts/gcp-infra/SKILL.md` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/experts/gcp-infra/expertise.yaml` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/gcp-infra/question.md` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/gcp-infra/self-improve.md` (CREATE)

---

### 19. [FEATURE] Create React/frontend expert with self-improving expertise

**Title**: Create React frontend expert system with expertise.yaml, question skill, and self-improve skill

**Description**:
- Create expert directory at `.claude/skills/experts/react-frontend/` with 3 files:
  - `SKILL.md` — Expert skill for React/frontend questions
  - `expertise.yaml` — Initial seed covering: component architecture (atomic design), state management (Zustand, React Query), data visualization (Recharts, D3 patterns), forms (React Hook Form), testing (React Testing Library, Playwright), accessibility, performance (React.memo, useMemo, virtual lists)
  - `self-improve.md` — 7-phase self-improvement workflow
- Acceptance: `/experts:react-frontend:question` returns domain-specific React answers.

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/experts/react-frontend/SKILL.md` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/skills/experts/react-frontend/expertise.yaml` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/react-frontend/question.md` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/react-frontend/self-improve.md` (CREATE)

---

### 20. [FEATURE] Create Claude Code Plugin structure in same repo

**Title**: Create tac-bootstrap-plugin/ directory with plugin.json, skills symlinks, agents, and hooks

**Description**:
- Create directory `tac-bootstrap-plugin/` at repo root
- Create `tac-bootstrap-plugin/.claude-plugin/plugin.json` with metadata: name "tac-bootstrap", version "1.1.0", description, author "Celes", listing all skills and agents
- Create `tac-bootstrap-plugin/skills/` — symlink or copy each skill from `.claude/skills/` (bigquery-ops, dbt-workflow, ml-forecast, fastapi-ddd, react-frontend, gcp-infra, aws-ops, data-pipeline, meta-skill, start-orchestrator, and all experts)
- Create `tac-bootstrap-plugin/agents/` — copy each agent from `.claude/agents/` (all 11: 8 existing + 3 new)
- Create `tac-bootstrap-plugin/hooks/` — copy core hooks: dangerous_command_blocker.py, universal_hook_logger.py, context_bundle_builder.py
- Create `tac-bootstrap-plugin/README.md` — Installation instructions, skill listing, agent listing
- Acceptance: Adding `"tac-bootstrap-plugin"` to another project's `.claude/settings.json` plugins array makes all skills available with `tac-bootstrap:` namespace prefix.

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac-bootstrap-plugin/.claude-plugin/plugin.json` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac-bootstrap-plugin/skills/` (CREATE directory tree)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac-bootstrap-plugin/agents/` (CREATE directory + 11 files)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac-bootstrap-plugin/hooks/` (CREATE directory + 3 files)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac-bootstrap-plugin/README.md` (CREATE)

---

### 21. [FEATURE] Add Pydantic models for data_engineering, ml, and infrastructure config sections

**Title**: Extend TACConfig with optional DataEngineeringConfig, MLConfig, and InfrastructureConfig models

**Description**:
- In `domain/models.py`, add 3 new Pydantic BaseModel classes:
  - `DbtTargetConfig`: name (str), adapter (str: "dbt-bigquery" | "dbt-postgres"), project_id (Optional[str]), dataset (Optional[str]), host (Optional[str]), dbname (Optional[str])
  - `DbtConfig`: project_name (str), targets (List[DbtTargetConfig]), default_target (str), schema (str)
  - `BigQueryConfig`: project_id (str), dataset (str), location (str, default "US")
  - `CloudStorageConfig`: bucket (str), region (str, default "us-central1")
  - `DataEngineeringConfig`: enabled (bool, default False), dbt (Optional[DbtConfig]), bigquery (Optional[BigQueryConfig]), cloud_storage (Optional[CloudStorageConfig])
  - `MLFramework` enum: lightgbm, prophet, xgboost, pytorch, sklearn, statsmodels
  - `MLConfig`: enabled (bool, default False), frameworks (List[MLFramework]), pipeline_type (str, default "batch"), metrics (List[str]), experiment_tracking (Optional[str])
  - `InfrastructureConfig`: cloud_provider (str, default "gcp"), iac_tool (str, default "terraform"), regions (Dict[str, str])
- Add to `TACConfig` as optional fields: `data_engineering: Optional[DataEngineeringConfig] = None`, `ml: Optional[MLConfig] = None`, `infrastructure: Optional[InfrastructureConfig] = None`
- Set `model_config = {"extra": "ignore"}` on new models for forward compatibility
- Acceptance: `TACConfig(**yaml.safe_load(open("config.yml")))` succeeds with and without the new sections. `uv run pytest tests/test_models.py` passes.

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/domain/models.py` (MODIFY: add ~80 lines of new models)

---

### 22. [FEATURE] Create Jinja2 templates for new skills (for generated projects)

**Title**: Create .j2 template versions of all new skills so tac-bootstrap init generates them

**Description**:
- For each new skill created in tasks 5-12, create a corresponding `.j2` template in `tac_bootstrap_cli/tac_bootstrap/templates/claude/skills/`:
  - `bigquery-ops/SKILL.md.j2`, `bigquery-ops/reference.md.j2`, `bigquery-ops/examples/supply_chain_queries.sql.j2`
  - `dbt-workflow/SKILL.md.j2`, `dbt-workflow/reference.md.j2`, `dbt-workflow/templates/*.j2`
  - `ml-forecast/SKILL.md.j2`, `ml-forecast/reference.md.j2`, `ml-forecast/templates/*.j2`
  - `fastapi-ddd/SKILL.md.j2`, `fastapi-ddd/reference.md.j2`, `fastapi-ddd/templates/*.j2`
  - `react-frontend/SKILL.md.j2`, `react-frontend/reference.md.j2`, `react-frontend/templates/*.j2`
  - `gcp-infra/SKILL.md.j2`, `gcp-infra/reference.md.j2`, `gcp-infra/templates/*.j2`
  - `aws-ops/SKILL.md.j2`, `aws-ops/reference.md.j2`
  - `data-pipeline/SKILL.md.j2`, `data-pipeline/reference.md.j2`, `data-pipeline/templates/*.j2`
- Templates should use `{{ config.project.name }}` and conditional blocks `{% if config.data_engineering and config.data_engineering.enabled %}` to only include relevant skills
- Acceptance: Templates render without errors when `config.data_engineering` is None (backward compatible).

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/skills/bigquery-ops/` (CREATE directory tree)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/skills/dbt-workflow/` (CREATE directory tree)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/skills/ml-forecast/` (CREATE directory tree)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/skills/fastapi-ddd/` (CREATE directory tree)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/skills/react-frontend/` (CREATE directory tree)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/skills/gcp-infra/` (CREATE directory tree)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/skills/aws-ops/` (CREATE directory tree)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/skills/data-pipeline/` (CREATE directory tree)

---

### 23. [FEATURE] Register new skills and agents in scaffold_service.py

**Title**: Add new skills, agents, and expert directories to scaffold_service.py build_plan

**Description**:
- In `_add_directories()`: add directory entries for new skill directories (`.claude/skills/bigquery-ops`, `.claude/skills/dbt-workflow`, `.claude/skills/ml-forecast`, `.claude/skills/fastapi-ddd`, `.claude/skills/react-frontend`, `.claude/skills/gcp-infra`, `.claude/skills/aws-ops`, `.claude/skills/data-pipeline`, `.claude/skills/experts/data-engineering`, `.claude/skills/experts/ml-forecasting`, `.claude/skills/experts/gcp-infra`, `.claude/skills/experts/react-frontend`)
- In `_add_claude_files()`: add new skill SKILL.md + supporting files registration using conditional logic: `if config.data_engineering and config.data_engineering.enabled:` for data skills, `if config.ml and config.ml.enabled:` for ML skills, always include fastapi-ddd and react-frontend
- In `_add_claude_files()` agents section: add 3 new agents (data-engineer.md, ml-engineer.md, infra-ops.md)
- In `_add_claude_files()` expert_commands section: add 4 new expert domains (data-engineering, ml-forecasting, gcp-infra, react-frontend) with question.md and self-improve.md each
- In expertise_files section: add 4 new expertise.yaml seed files with `FileAction.CREATE` (skip if exists)
- Acceptance: `uv run pytest tests/test_scaffold_service.py` passes. Running `build_plan()` with a config that has `data_engineering.enabled=True` includes the new skills in the plan.

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` (MODIFY: add ~120 lines in 4 sections)

---

### 24. [FEATURE] Create Jinja2 templates for new agent definitions

**Title**: Create .j2 templates for data-engineer, ml-engineer, and infra-ops agents

**Description**:
- Create 3 new Jinja2 template files:
  - `templates/claude/agents/data-engineer.md.j2` — Renders the data engineering agent definition
  - `templates/claude/agents/ml-engineer.md.j2` — Renders the ML engineering agent definition
  - `templates/claude/agents/infra-ops.md.j2` — Renders the infrastructure operations agent definition
- Templates should be simple passthrough (agent definitions are static, no Jinja variables needed)
- Acceptance: `TemplateRepository().render("claude/agents/data-engineer.md.j2", config)` returns valid markdown.

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/data-engineer.md.j2` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/ml-engineer.md.j2` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/infra-ops.md.j2` (CREATE)

---

### 25. [FEATURE] Create Jinja2 templates for new expert commands and expertise seeds

**Title**: Create .j2 templates for 4 new expert domains (data-engineering, ml-forecasting, gcp-infra, react-frontend)

**Description**:
- For each of the 4 new expert domains, create template files:
  - `templates/claude/commands/experts/<domain>/question.md.j2` — Question command template
  - `templates/claude/commands/experts/<domain>/self-improve.md.j2` — Self-improve workflow template
  - `templates/claude/commands/experts/<domain>/expertise.yaml.j2` — Expertise seed file template
- Follow the pattern established by existing experts (cli, adw, commands, database, websocket)
- Question templates should reference `expertise.yaml` and include the Act-Learn-Reuse loop instructions
- Self-improve templates should implement the 7-phase validation workflow
- Acceptance: All 12 templates render without errors. Pattern matches existing expert templates.

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/data-engineering/question.md.j2` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/data-engineering/self-improve.md.j2` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/data-engineering/expertise.yaml.j2` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/ml-forecasting/question.md.j2` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/ml-forecasting/self-improve.md.j2` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/ml-forecasting/expertise.yaml.j2` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/gcp-infra/question.md.j2` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/gcp-infra/self-improve.md.j2` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/gcp-infra/expertise.yaml.j2` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/react-frontend/question.md.j2` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/react-frontend/self-improve.md.j2` (CREATE)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/react-frontend/expertise.yaml.j2` (CREATE)

---

### 26. [CHORE] Add config.yml.j2 template support for new optional sections

**Title**: Extend config.yml.j2 template with conditional data_engineering, ml, and infrastructure sections

**Description**:
- In `templates/config/config.yml.j2`, add conditional blocks at the end (before `metadata:`):
  ```jinja2
  {% if config.data_engineering %}
  data_engineering:
    enabled: {{ config.data_engineering.enabled | lower }}
    ...
  {% endif %}
  {% if config.ml %}
  ml:
    enabled: {{ config.ml.enabled | lower }}
    ...
  {% endif %}
  {% if config.infrastructure %}
  infrastructure:
    cloud_provider: "{{ config.infrastructure.cloud_provider }}"
    ...
  {% endif %}
  ```
- Sections only render when the user provides these config options (backward compatible: existing configs without these sections still render correctly)
- Acceptance: Rendering config.yml.j2 with a TACConfig that has `data_engineering=None` produces the same output as before. Rendering with `data_engineering=DataEngineeringConfig(enabled=True, ...)` includes the new section.

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/config/config.yml.j2` (MODIFY)

---

### 27. [CHORE] Add schema migration v2 to v3 for new config sections

**Title**: Create v2→v3 migration that adds data_engineering, ml, and infrastructure optional sections

**Description**:
- In `domain/migrations.py`:
  - Add `migrate_v2_to_v3()` function that: sets `schema_version: 3`, adds empty optional sections `data_engineering: null`, `ml: null`, `infrastructure: null`
  - Add `migrate_v3_to_v2()` rollback function that: removes these sections, sets `schema_version: 2`
  - Register migration `"2->3"` in `MIGRATION_REGISTRY`
  - Update `get_latest_version()` to return `3`
- Acceptance: Loading a v2 config.yml and running migration produces a v3 config. Rollback restores v2. `uv run pytest tests/test_migration_service.py` passes.

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/domain/migrations.py` (MODIFY: add ~40 lines)

---

### 28. [CHORE] Update CLI README.md with new skills, agents, and experts table

**Title**: Add "Celes Stack Skills", "New Agents", and "New Experts" tables to CLI README.md

**Description**:
- Add a new section `## Celes Stack Extensions (v1.1.0)` after the existing "Phase 3: Premium Features" section
- Add subsection `### Domain Skills` with table:

| Skill | Command | Description |
|-------|---------|-------------|
| BigQuery Ops | `/bigquery-ops` | Manage BigQuery datasets, tables, and queries for supply chain |
| dbt Workflow | `/dbt-workflow` | Create dbt models with dual-target BigQuery + PostgreSQL |
| ML Forecast | `/ml-forecast` | Build demand forecasting with LightGBM, Prophet, XGBoost, PyTorch |
| FastAPI DDD | `/fastapi-ddd` | Generate FastAPI vertical slice DDD components |
| React Frontend | `/react-frontend` | Generate React components and supply chain dashboards |
| GCP Infra | `/gcp-infra` | Manage GCP resources with Terraform |
| AWS Ops | `/aws-ops` | Manage AWS resources with Terraform |
| Data Pipeline | `/data-pipeline` | Design ETL/ELT pipelines with BigQuery + dbt |

- Add subsection `### New Agents` with table:

| Agent | Model | Specialization |
|-------|-------|---------------|
| data-engineer | opus | dbt, BigQuery, data pipelines |
| ml-engineer | opus | Demand forecasting, multi-framework ML |
| infra-ops | sonnet | GCP/AWS infrastructure, Terraform |

- Add subsection `### New Experts` with table:

| Expert | Domain | Commands |
|--------|--------|----------|
| data-engineering | dbt, BigQuery, ETL | question, self-improve |
| ml-forecasting | Forecasting, ML | question, self-improve |
| gcp-infra | GCP, Terraform | question, self-improve |
| react-frontend | React, dashboards | question, self-improve |

- Acceptance: Tables are properly formatted markdown and consistent with existing README style.

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/README.md` (MODIFY: add ~60 lines)

---

### 29. [CHORE] Update CHANGELOG.md with v1.1.0 release

**Title**: Add v1.1.0 changelog entry summarizing all Celes stack extensions and technical debt cleanup

**Description**:
- Add new section after `## [Unreleased]`:
  ```markdown
  ## [1.1.0] - 2026-02-11

  ### Added
  - 8 new Claude Code Skills for Celes stack: bigquery-ops, dbt-workflow, ml-forecast, fastapi-ddd, react-frontend, gcp-infra, aws-ops, data-pipeline
  - 3 new specialized agents: data-engineer (opus), ml-engineer (opus), infra-ops (sonnet)
  - 4 new self-improving expert systems: data-engineering, ml-forecasting, gcp-infra, react-frontend
  - Claude Code Plugin structure (tac-bootstrap-plugin/) for team distribution
  - Pydantic models for data_engineering, ml, and infrastructure config sections
  - Schema migration v2→v3 with new optional config sections
  - Jinja2 templates for all new skills, agents, and experts
  - dbt dual-target support (BigQuery + PostgreSQL)
  - ML multi-framework support (Prophet, LightGBM, XGBoost, PyTorch, scikit-learn, statsmodels)

  ### Fixed
  - Removed dead ImportError fallback code from CLI init, add-agentic, doctor, render commands
  - Consolidated duplicate FieldType/EntitySpec/FieldSpec definitions between models.py and entity_config.py
  - Removed committed orchestrator.db (74KB) from repository root
  - Removed stale test_wizard.py.bak from test directory

  ### Changed
  - Replaced committed .venv/ in orchestrator template with requirements.txt (>80% repo size reduction)
  ```
- Update version in `tac_bootstrap_cli/tac_bootstrap/__init__.py` from `"1.0.0"` to `"1.1.0"`
- Update version in `config.yml` root from `"0.10.4"` to `"1.1.0"` if applicable
- Acceptance: CHANGELOG.md follows Keep a Changelog format. Version bump is semantic (minor: new features, no breaking changes).

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/CHANGELOG.md` (MODIFY: add ~30 lines at top)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/__init__.py` (MODIFY: version bump)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/config.yml` (MODIFY: version field)

---

## Parallel Execution Groups

| Grupo | Tareas | Cantidad | Dependencia | Descripcion |
|-------|--------|----------|-------------|-------------|
| P1 | 1, 2, 3, 4 | 4 | Ninguna | Technical debt cleanup: .venv removal, dead code, duplicates, stale files |
| P2 | 5, 6, 7, 8, 9, 10, 11, 12 | 8 | Ninguna | Create all 8 Celes stack skills (.claude/skills/) |
| P3 | 13, 14, 15 | 3 | Ninguna | Create 3 new agent definitions (.claude/agents/) |
| P4 | 16, 17, 18, 19 | 4 | Ninguna | Create 4 new expert systems with self-improving expertise |
| P5 | 20 | 1 | P2, P3, P4 | Create Claude Code Plugin structure assembling all skills, agents, hooks |
| P6 | 21 | 1 | Ninguna | Extend Pydantic models with new config sections |
| P7 | 22, 24, 25 | 3 | P2, P3, P4 | Create Jinja2 templates for skills, agents, experts |
| P8 | 23 | 1 | P6, P7 | Register new templates in scaffold_service.py |
| P9 | 26, 27 | 2 | P6 | Config template and schema migration for new sections |
| P10 | 28 | 1 | P2, P3, P4 | Update CLI README.md with new tables |
| SEQ | 29 | 1 | TODOS | CHANGELOG update and version bump to 1.1.0 |
