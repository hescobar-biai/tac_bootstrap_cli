# Claude Model Configuration System

## Overview

TAC Bootstrap implements a **3-tier runtime model configuration system** that allows you to change Claude model versions without modifying code. This is essential for:

- 🔄 **Version Management**: Update model versions across the entire system
- 💰 **Cost Optimization**: Use cheaper models (Haiku) for testing, more powerful models (Opus) for production
- 🌍 **Environment Flexibility**: Different models for dev, staging, and production
- 🔒 **Vendor Stability**: Pin to specific model versions for reproducibility

## Resolution Hierarchy

The system resolves model IDs in this priority order:

```
┌─────────────────────────────────────────────────┐
│ 1. Environment Variables (Highest Priority)     │ ← ANTHROPIC_DEFAULT_*_MODEL
│    └─ Most flexible, changes at runtime         │
├─────────────────────────────────────────────────┤
│ 2. Configuration File (Medium Priority)         │ ← config.yml
│    └─ Project-specific settings                 │
├─────────────────────────────────────────────────┤
│ 3. Hardcoded Defaults (Lowest Priority)         │ ← Fallback values
│    └─ Built-in sensible defaults                │
└─────────────────────────────────────────────────┘
```

## Usage Examples

### 1. Environment Variables (Recommended for CI/CD)

Set environment variables before running workflows:

```bash
# Use specific model versions
export ANTHROPIC_DEFAULT_OPUS_MODEL="claude-opus-4-6"
export ANTHROPIC_DEFAULT_SONNET_MODEL="claude-sonnet-4-6"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="claude-haiku-4-6"

# Run workflow with configured models
uv run adws/adw_sdlc_iso.py --issue 123
```

In Docker or CI/CD:

```dockerfile
FROM python:3.11
ENV ANTHROPIC_DEFAULT_OPUS_MODEL="claude-opus-4-6"
ENV ANTHROPIC_DEFAULT_SONNET_MODEL="claude-sonnet-4-6"
ENV ANTHROPIC_DEFAULT_HAIKU_MODEL="claude-haiku-4-6"
```

### 2. Configuration File (Recommended for Projects)

Edit `config.yml`:

```yaml
agentic:
  model_policy:
    default: "sonnet"           # Which model to use for standard tasks
    heavy: "opus"               # Which model for complex/heavy tasks
    fallback: "haiku"           # Model when quota is exhausted

    # Optional: Override fully qualified model IDs
    opus_model: "claude-opus-4-6"
    sonnet_model: "claude-sonnet-4-6"
    haiku_model: "claude-haiku-4-6"
```

### 3. Defaults (No Configuration Needed)

If nothing is configured, the system uses built-in defaults:

```python
get_model_id("opus")    # "claude-opus-4-5-20251101"
get_model_id("sonnet")  # "claude-sonnet-4-5-20250929"
get_model_id("haiku")   # "claude-haiku-4-5-20251001"
```

## Core Functions

### `get_model_id(model_type: str) -> str`

Get the resolved model ID with 3-tier resolution:

```python
from adw_modules.workflow_ops import get_model_id

# Returns the fully qualified model ID
opus = get_model_id("opus")      # "claude-opus-4-5-20251101" (or env/config override)
sonnet = get_model_id("sonnet")  # "claude-sonnet-4-5-20250929" (or override)
haiku = get_model_id("haiku")    # "claude-haiku-4-5-20251001" (or override)
```

### `get_resolved_model_opus/sonnet/haiku()`

Helper functions in `adw_agent_sdk.py`:

```python
from adw_modules.adw_agent_sdk import (
    get_resolved_model_opus,
    get_resolved_model_sonnet,
    get_resolved_model_haiku,
)

opus = get_resolved_model_opus()      # Full resolution
sonnet = get_resolved_model_sonnet()  # Full resolution
haiku = get_resolved_model_haiku()    # Full resolution
```

### `get_model_fallback_chain()`

Get the model fallback chain for quota exhaustion handling:

```python
from adw_modules.agent import get_model_fallback_chain

chain = get_model_fallback_chain()
# {
#   "claude-opus-4-5-20251101": "claude-sonnet-4-5-20250929",
#   "claude-sonnet-4-5-20250929": "claude-haiku-4-5-20251001",
#   "claude-haiku-4-5-20251001": "claude-haiku-4-5-20251001"
# }
```

### `get_fast_model()`

Get the fast model ID for summarization and quick operations:

```python
from adw_modules.adw_summarizer import get_fast_model

# Always uses Haiku (via get_model_id)
fast = get_fast_model()  # "claude-haiku-4-5-20251001" (or env/config override)
```

## Architecture

### Key Files Modified

**Core Implementation:**
- `adws/adw_modules/workflow_ops.py` - `get_model_id()` function
- `adws/adw_modules/agent.py` - `get_model_fallback_chain()` function
- `adws/adw_modules/adw_summarizer.py` - `get_fast_model()` function
- `adws/adw_modules/adw_agent_sdk.py` - `get_resolved_model_*()` functions

**Configuration:**
- `config.yml` - Model ID overrides
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Pydantic ModelPolicy

**Orchestrators (Updated):**
- `adws/adw_sdlc_zte_iso.py` - 6 phases
- `adws/adw_sdlc_iso.py` - 5 phases
- `adws/adw_ship_iso.py` - Shipping phase

**Workflows (Updated):**
- `adws/adw_workflows/adw_plan_build_review.py`
- `adws/adw_workflows/adw_plan_build_review_fix.py`

## Testing

Comprehensive test suite in `adws/tests/test_model_configuration.py`:

```bash
# Run all tests
python -m pytest adws/tests/test_model_configuration.py -v

# Run specific test class
python -m pytest adws/tests/test_model_configuration.py::TestModelResolution -v

# Run with coverage
python -m pytest adws/tests/test_model_configuration.py --cov=adw_modules.workflow_ops
```

Test Coverage:
- ✅ 3-tier resolution hierarchy
- ✅ Environment variable overrides
- ✅ Configuration file loading
- ✅ Model fallback chains
- ✅ Fast model resolution
- ✅ Edge cases (invalid types, partial config)

## Implementation Details

### Resolution Flow

```python
def get_model_id(model_type: str) -> str:
    # Step 1: Check environment variable
    env_var = f"ANTHROPIC_DEFAULT_{model_type.upper()}_MODEL"
    if env_var is set:
        return env_value  # ← HIGHEST PRIORITY

    # Step 2: Check config.yml
    config = load_config()
    if config["agentic"]["model_policy"][f"{model_type}_model"]:
        return config_value  # ← MEDIUM PRIORITY

    # Step 3: Return hardcoded default
    defaults = {
        "opus": "claude-opus-4-5-20251101",
        "sonnet": "claude-sonnet-4-5-20250929",
        "haiku": "claude-haiku-4-5-20251001",
    }
    return defaults[model_type]  # ← LOWEST PRIORITY
```

### Backward Compatibility

- ModelName enum values unchanged (still available as fallback)
- All existing code continues to work
- New code uses dynamic resolution functions
- Zero breaking changes

### Performance

- Config loaded once and cached (`_CONFIG_CACHE`)
- Model resolution is O(1) lookups
- Negligible overhead vs hardcoded values
- Environment variables checked at each call (allows dynamic changes)

## Migration Guide

### For Existing Projects

No changes required! The system is fully backward compatible.

### To Enable Configuration Overrides

1. **Edit config.yml:**

```yaml
agentic:
  model_policy:
    # Existing fields (unchanged)
    default: "sonnet"
    heavy: "opus"
    fallback: "haiku"

    # Add these optional fields:
    opus_model: "claude-opus-4-6"
    sonnet_model: "claude-sonnet-4-6"
    haiku_model: "claude-haiku-4-6"
```

2. **Or set environment variables:**

```bash
export ANTHROPIC_DEFAULT_OPUS_MODEL="claude-opus-4-6"
export ANTHROPIC_DEFAULT_SONNET_MODEL="claude-sonnet-4-6"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="claude-haiku-4-6"
```

3. **No code changes needed!** Everything will automatically use the configured models.

## Troubleshooting

### How to verify which model is being used

```python
from adw_modules.workflow_ops import get_model_id
import os

# Check what model will be used
print(f"Opus: {get_model_id('opus')}")
print(f"Sonnet: {get_model_id('sonnet')}")
print(f"Haiku: {get_model_id('haiku')}")

# Check environment variables
print(f"Env OPUS: {os.getenv('ANTHROPIC_DEFAULT_OPUS_MODEL', 'NOT SET')}")
print(f"Env SONNET: {os.getenv('ANTHROPIC_DEFAULT_SONNET_MODEL', 'NOT SET')}")
print(f"Env HAIKU: {os.getenv('ANTHROPIC_DEFAULT_HAIKU_MODEL', 'NOT SET')}")
```

### Models not changing

1. **Check environment variables are set correctly:**
   ```bash
   echo $ANTHROPIC_DEFAULT_OPUS_MODEL
   ```

2. **Check config.yml is in the right location:**
   - Should be at project root
   - Verify with: `ls -la config.yml`

3. **Clear any cached config:**
   ```python
   from adw_modules import workflow_ops
   workflow_ops._CONFIG_CACHE = None  # Reset cache
   ```

## Future Enhancements

Potential improvements for future versions:

- [ ] Model aliasing (e.g., `latest-opus` → current latest version)
- [ ] Regional model selection
- [ ] Rate limit configuration per model
- [ ] Cost tracking and reporting
- [ ] Automatic model switching based on token count
- [ ] Model warm-up for latency-sensitive tasks

## References

- [config.yml](config.yml) - Configuration file schema
- [adws/adw_modules/workflow_ops.py](adws/adw_modules/workflow_ops.py) - Implementation
- [adws/tests/test_model_configuration.py](adws/tests/test_model_configuration.py) - Tests
- [Claude API Documentation](https://docs.anthropic.com/)

## Questions?

For issues or questions about model configuration:
1. Check [troubleshooting](#troubleshooting) section
2. Review test cases for usage examples
3. Check environment variable names spelling
4. Verify config.yml YAML syntax
