# Common Architecture Decisions

> Source: `projects/plan/documentation-framework/templates/adr/COMMON-DECISIONS.md`

Every new project should evaluate these decision points and create ADRs for the relevant ones. Not all projects need all of these — pick the ones that apply.

---

## Stack Decisions (Shared ADRs — already provided)

These are answered by the shared ADRs in `shared/adr/`. You should NOT re-create these unless you're deviating from the standard stack:

| ADR | Decision | When to Override |
|-----|----------|-----------------|
| 001 | FastAPI backend | If using a different Python framework or a different language |
| 002 | Next.js frontend | If using a different React framework or SPA approach |
| 003 | Custom Tailwind UI | If adopting a component library (shadcn, Material UI, etc.) |
| 005 | FastAPI depends services | Using different DI pattern |
| 006 | React hooks state | If adopting Redux, Zustand, or Context for state management |
| 007 | Recharts visualization | If using a different charting library (D3, Chart.js, Nivo, etc.) |

---

## Project-Specific Decisions (Create new ADRs for these)

### Authentication Strategy

**Question**: How do users authenticate?

| Option | When to Use |
|--------|------------|
| No auth (network-level) | Internal tools behind VPN, read-only dashboards |
| JWT tokens | APIs consumed by multiple clients, mobile apps |
| OAuth2 / SSO | Enterprise apps, integration with identity providers |
| API keys | Service-to-service, developer APIs |
| Session-based | Traditional web apps with server-rendered pages |

### Database Choice & Usage

**Question**: What persistent storage does the project need?

| Option | When to Use |
|--------|------------|
| No database | Data comes entirely from external APIs/services |
| PostgreSQL (active) | CRUD operations, relational data, user management |
| PostgreSQL (provisioned) | No immediate need, but future features will require it |
| SQLite | Single-user tools, prototypes, embedded applications |
| Redis | Caching layer, session storage, pub/sub |

### Primary Data Source

**Question**: Where does the domain data come from?

| Option | When to Use |
|--------|------------|
| External API (REST/GraphQL) | Aggregating data from third-party services |
| Data warehouse (BigQuery, Snowflake, etc.) | Analytics dashboards over large datasets |
| Own database | CRUD applications managing their own data |
| File system | Log analysis, document processing |
| Message queue | Event-driven architectures |

### Caching Strategy

**Question**: How do we handle data freshness vs. performance?

| Option | When to Use |
|--------|------------|
| No caching | Data source is fast enough, data must always be fresh |
| Data source native cache | BigQuery query cache, database query cache |
| Application-level cache | Redis/in-memory for frequently accessed data |
| CDN/browser cache | Static assets, rarely-changing API responses |
| Stale-while-revalidate | Dashboard data that can be slightly stale |

### Deployment Model

**Question**: How is the application deployed?

| Option | When to Use |
|--------|------------|
| Docker Compose (local/VM) | Internal tools, development environments, small teams |
| Kubernetes | Production workloads, auto-scaling, multi-environment |
| Serverless (Lambda/Cloud Run) | Event-driven, variable traffic, cost optimization |
| Platform (Vercel/Railway) | Quick deployment, managed infrastructure |

### Error Handling Approach

**Question**: How do we handle and report errors?

| Option | When to Use |
|--------|------------|
| HTTPException + logging | Simple APIs, internal tools |
| Structured error codes | Public APIs, client SDKs |
| Error tracking (Sentry) | Production apps needing visibility |
| Custom error middleware | Complex error transformation, audit trails |

### Multi-Tenancy / Multi-Environment

**Question**: Does the app need to handle multiple tenants, environments, or data sources?

| Option | When to Use |
|--------|------------|
| Single tenant | One deployment per customer/environment |
| Multi-tenant (shared DB) | SaaS with row-level isolation |
| Multi-environment (UNION) | Analytics across DEV/QAS/PRD environments |
| Config-driven | Different behavior per deployment via env vars |

---

## How to Use This Catalog

1. Go through each section above
2. For decisions where the shared ADRs apply, note "Using shared ADR-00X"
3. For decisions that need a project-specific choice, create a new ADR using the template below
4. Number project-specific ADRs starting from 004 (001-003, 005-007 are shared stack ADRs)
5. Record your decision even if the answer is "not needed" — future team members will thank you

---

## ADR Template (Nygard Format)

> Source: `projects/plan/documentation-framework/templates/adr/ADR-TEMPLATE.md`

```markdown
# ADR-[NNN]: [FILL IN: Decision Title]

**Status**: [Proposed | Accepted | Deprecated | Superseded]

**Date**: [YYYY-MM-DD]

## Context

[FILL IN: What is the technical or organizational context? What problem or decision point are we facing? Include constraints, requirements, and relevant background. Be specific about what forces are at play.]

## Decision

[FILL IN: What is the decision? State it clearly and concisely. Include the specific technology, pattern, or approach chosen. If relevant, mention the version.]

## Consequences

### Positive

- [FILL IN: Benefit of this decision]
- [FILL IN: Benefit of this decision]
- [FILL IN: Benefit of this decision]

### Negative

- [FILL IN: Trade-off or downside (with mitigation if applicable)]
- [FILL IN: Trade-off or downside (with mitigation if applicable)]
```

**Tips for good ADRs:**
- One decision per ADR — don't bundle multiple choices
- Number sequentially: 001, 002, 003...
- Link to PRD features (F-XX) or TDD sections when relevant
- "Accepted" means it's the current active decision
- Use "Superseded by ADR-NNN" when replacing a decision
- Keep Context section focused on WHY, not HOW (that's for TDD)
- Negative consequences should be honest — every decision has trade-offs

---

## Example: Celes Cost Project-Specific ADRs

### ADR-004: Multi-Environment via UNION ALL Query Strategy

**Status**: Accepted | **Date**: 2026-02-09

**Context**: Cost data lives in separate BigQuery datasets per environment (DEV, QAS, PRD) with different GCP projects. Users need cross-environment combined results.

**Decision**: Dynamically build SQL using UNION ALL when multiple environments are selected. Template system with `{full_table}` placeholder and regex-based WHERE clause extraction.

**Positive**: Single API call for cross-env data, template reuse across 13 queries, per-subquery filters.
**Negative**: Complex regex-based query builder, no parameterized table names (BQ limitation), cost scales linearly.

### ADR-008: No Authentication Layer (v1)

**Status**: Accepted | **Date**: 2026-02-09

**Context**: Internal deployment behind VPN/firewall. Dashboard is read-only. Adding auth increases v1 complexity.

**Decision**: No user authentication in v1. Network-level access control. GCP service account for BigQuery access.

**Positive**: Faster development, simpler deployment, no user management overhead.
**Negative**: No usage attribution, must be behind VPN, no audit trail, future auth refactoring.

### ADR-009: PostgreSQL Provisioned but Not Actively Used

**Status**: Accepted | **Date**: 2026-02-09

**Context**: PostgreSQL could store metadata (saved filters, preferences, audit logs) but v1 queries BigQuery directly.

**Decision**: Provision PostgreSQL 16 in Docker Compose with named volume. Include asyncpg in deps. No schemas or usage in v1.

**Positive**: Ready for future features without infrastructure changes, connection settings pre-configured.
**Negative**: ~50MB RAM overhead for unused service, adds Docker Compose complexity.
