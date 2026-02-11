# Claude Model Resolution for TAC Bootstrap Commands

All commands in `.claude/commands/` support **3-tier model resolution** when specifying model references.

## Model Specification Syntax

Commands use short model references in the YAML frontmatter:

```yaml
---
model: opus        # Reference to "opus" model
---
```

Supported short references:
- `opus` - Powerful model for complex tasks
- `sonnet` - Balanced model for most tasks
- `haiku` - Fast, cost-effective model

## 3-Tier Resolution Hierarchy

When Claude Code processes a command with a model reference (e.g., `model: opus`), it resolves the actual model ID using this hierarchy:

### Tier 1: Environment Variables (Highest Priority)
```bash
export ANTHROPIC_DEFAULT_OPUS_MODEL="claude-opus-4-5-20251101"
export ANTHROPIC_DEFAULT_SONNET_MODEL="claude-sonnet-4-5-20250929"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="claude-haiku-4-5-20251001"
```

If set, these override everything else.

### Tier 2: config.yml (Project Configuration)
```yaml
# config.yml
agentic:
  model_policy:
    opus_model: "claude-opus-4-5-20251101"
    sonnet_model: "claude-sonnet-4-5-20250929"
    haiku_model: "claude-haiku-4-5-20251001"
```

If environment variables are not set, uses values from project's config.yml.

### Tier 3: Hardcoded Defaults (Fallback)
```
opus → "claude-opus-4-5-20251101"
sonnet → "claude-sonnet-4-5-20250929"
haiku → "claude-haiku-4-5-20251001"
```

Used only if neither environment variables nor config.yml specify a value.

## Resolution Flow Diagram

```
Command: model: opus
    ↓
[Check ANTHROPIC_DEFAULT_OPUS_MODEL env var]
    ↓ Not found
[Check config.yml agentic.model_policy.opus_model]
    ↓ Not found
[Use hardcoded default: "claude-opus-4-5-20251101"]
    ↓
Claude Code uses resolved model for execution
```

## Examples

### Example 1: Using Environment Variables
```bash
# Set environment variable
export ANTHROPIC_DEFAULT_OPUS_MODEL="claude-opus-4-5-20251101"

# Any command with "model: opus" will use this value
/quick-plan "Add authentication to API"
```

### Example 2: Using config.yml
```yaml
# config.yml
agentic:
  model_policy:
    opus_model: "claude-opus-4-5-20251101"
    sonnet_model: "claude-sonnet-4-5-20250929"

# Commands automatically use these models
/plan "Design database schema"
```

### Example 3: Using Hardcoded Defaults
```bash
# No env var, no config.yml specified
# Command uses hardcoded default
/quick-plan "Optimize performance"
# Uses: claude-opus-4-5-20251101
```

## Switching Models Without Changing Code

To use different models across environments:

```bash
# Development: Use Haiku for cost optimization
export ANTHROPIC_DEFAULT_OPUS_MODEL="claude-haiku-4-5-20251001"
/plan "Quick test"

# Production: Use Opus for quality
export ANTHROPIC_DEFAULT_OPUS_MODEL="claude-opus-4-5-20251101"
/plan "Critical feature"
```

## Benefits

- **Flexibility**: Change models without modifying code
- **Multi-Environment**: Different models for dev/staging/prod
- **Cost Optimization**: Switch to cheaper models for testing
- **Configuration**: Override defaults via environment or config.yml
- **Consistency**: Same 3-tier hierarchy across entire TAC Bootstrap

## All Commands Using 3-Tier Resolution

Every command in `.claude/commands/` automatically supports 3-tier resolution for model references.

Commands that specify explicit models:
- `model: opus` - Uses 3-tier resolution for opus
- `model: sonnet` - Uses 3-tier resolution for sonnet
- `model: haiku` - Uses 3-tier resolution for haiku

No changes needed to commands - the resolution happens automatically.
