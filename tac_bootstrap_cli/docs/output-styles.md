# Output Styles

Output styles control Claude's response format and token usage, enabling optimization for different use cases.

## Overview

Output styles are markdown files that instruct Claude how to format responses. They're useful for:
- Reducing token consumption
- Optimizing for TTS (text-to-speech)
- Structuring output for parsing
- Adapting verbosity to context

## Available Styles

### Concise Styles

#### concise-done

Minimal responses with "Done." confirmations.

**Location:** `.claude/output-styles/concise-done.md`

**Behavior:**
- Responds with "Done." after completing tasks
- Minimal explanations
- Maximum token savings

**Use case:** Batch operations, automated workflows

**Example output:**
```
Done.
```

#### concise-ultra

Ultra-minimal responses under 50 tokens.

**Location:** `.claude/output-styles/concise-ultra.md`

**Behavior:**
- Responses limited to ~50 tokens
- Essential information only
- No elaboration

**Use case:** High-volume operations, CI/CD pipelines

**Example output:**
```
Created auth module. 3 files added.
```

#### concise-tts

Optimized for text-to-speech output.

**Location:** `.claude/output-styles/concise-tts.md`

**Behavior:**
- Natural spoken language
- No code blocks or formatting
- Punctuation optimized for speech
- Avoids acronyms and abbreviations

**Use case:** Voice assistants, accessibility, audio summaries

**Example output:**
```
I've created the authentication service. It includes login, logout, and token refresh endpoints. The tests are passing.
```

### Verbose Styles

#### verbose-bullet-points

Detailed responses in bullet-point format.

**Location:** `.claude/output-styles/verbose-bullet-points.md`

**Behavior:**
- Comprehensive explanations
- Organized bullet points
- Clear section headers
- Step-by-step breakdowns

**Use case:** Documentation, learning, code reviews

**Example output:**
```
## Changes Made

### Authentication Module
- Created `src/auth/service.py`
  - Implements JWT token generation
  - Handles password hashing with bcrypt
  - Includes refresh token logic

### API Endpoints
- Added routes in `src/auth/routes.py`
  - POST /login - User authentication
  - POST /logout - Session termination
  - POST /refresh - Token renewal

### Tests
- Added 12 unit tests
- All tests passing
```

#### verbose-yaml-structured

YAML-formatted output for machine parsing.

**Location:** `.claude/output-styles/verbose-yaml-structured.md`

**Behavior:**
- Structured YAML format
- Machine-parseable
- Consistent schema
- Detailed metadata

**Use case:** Automation, reporting, data extraction

**Example output:**
```yaml
task:
  status: completed
  type: feature_implementation

changes:
  - file: src/auth/service.py
    action: created
    lines: 145
    description: JWT authentication service

  - file: src/auth/routes.py
    action: created
    lines: 78
    description: FastAPI auth endpoints

tests:
  total: 12
  passed: 12
  failed: 0

summary: Authentication module implemented with JWT support
```

## Using Output Styles

### Via settings.local.json

Create `.claude/settings.local.json` to set default style:

```json
{
  "output_style": "concise-done"
}
```

### Via Command

Reference style in slash commands:

```markdown
---
output-style: concise-ultra
---

# Command content...
```

### Dynamically

Request style change in conversation:

```
Use the concise-tts output style for this session
```

## Configuration

### settings.local.json

Override default settings locally (not committed to git):

```json
{
  "output_style": "verbose-bullet-points",
  "preferences": {
    "verbosity": "detailed",
    "format": "markdown"
  }
}
```

### Per-Command Override

Commands can specify their output style:

```markdown
---
description: Quick status check
output-style: concise-ultra
---

# Status Command
Report current project status.
```

## Creating Custom Styles

### Style Structure

```markdown
# Style Name

## Response Guidelines

- Guideline 1
- Guideline 2

## Format Rules

- Format rule 1
- Format rule 2

## Examples

### Example 1
Input: [example input]
Output: [example output]

### Example 2
Input: [example input]
Output: [example output]
```

### Location

Add custom styles to `.claude/output-styles/`:

```
.claude/
└── output-styles/
    ├── concise-done.md
    ├── concise-ultra.md
    ├── concise-tts.md
    ├── verbose-bullet-points.md
    ├── verbose-yaml-structured.md
    └── my-custom-style.md
```

## Token Optimization

### Comparison

| Style | Avg Tokens | Use Case |
|-------|------------|----------|
| concise-done | ~5 | Batch automation |
| concise-ultra | ~50 | High-volume ops |
| concise-tts | ~100 | Voice output |
| verbose-bullet-points | ~300 | Documentation |
| verbose-yaml-structured | ~250 | Machine parsing |

### Best Practices

1. **Default to concise** for automated workflows
2. **Use verbose** for learning and documentation
3. **Use YAML** when output needs parsing
4. **Use TTS** for voice interfaces
5. **Create custom styles** for specific needs

## Integration with Hooks

Output styles can be dynamically selected by hooks:

```python
# In a hook, set output style based on context
def select_style(context):
    if context.get('automated'):
        return 'concise-done'
    elif context.get('voice_output'):
        return 'concise-tts'
    else:
        return 'verbose-bullet-points'
```

## Style Precedence

1. Command-level `output-style` (highest)
2. Session override
3. `settings.local.json`
4. Default (verbose-bullet-points)
