---
doc_type: feature
adw_id: feature_Tac_9_task_4_2_3
date: 2026-01-25
idk:
  - output-styles
  - text-to-speech
  - accessibility
  - jinja2-templates
  - listening-comprehension
  - tts-optimization
tags:
  - feature
  - templates
  - accessibility
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-tts.md.j2
  - .claude/output-styles/concise-tts.md
---

# Concise TTS Output Style Template

**ADW ID:** feature_Tac_9_task_4_2_3
**Date:** 2026-01-25
**Specification:** [issue-235-adw-feature_Tac_9_task_4_2_3-sdlc_planner-add-concise-tts-template.md](../specs/issue-235-adw-feature_Tac_9_task_4_2_3-sdlc_planner-add-concise-tts-template.md)

## Overview

This feature implements a new Jinja2 template for the "concise-tts" output style, enabling text-to-speech and listening-optimized responses. Unlike existing concise output styles that prioritize extreme token efficiency, concise-tts balances brevity with natural speech pacing and clarity, making responses accessible for audio consumption and voice interfaces.

## What Was Built

- **Concise TTS Jinja2 Template** - Static template file defining TTS-optimized output guidelines
- **Rendered Markdown Output Style** - Generated markdown file for Claude Code integration
- **TTS-Specific Guidance** - Comprehensive guidelines for speech-friendly formatting

### Key Components

- Response Guidelines optimized for listening comprehension (sentences under 20 words)
- TTS use cases and when to apply the output style
- Good/bad examples highlighting TTS pronunciation challenges
- Important notes with exception carve-outs for technical accuracy

## Technical Implementation

### Files Created

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-tts.md.j2` - Jinja2 template source (44 lines)
- `.claude/output-styles/concise-tts.md` - Rendered static markdown output

### Template Structure

The template follows the established pattern from existing output style templates (concise-ultra, concise-done) with a five-section structure:

1. **Header** - Introduces the concise-tts style with TTS focus
2. **Response Guidelines** - Core TTS requirements:
   - Sentence length constraints (under 20 words)
   - Code and variable formatting with backticks
   - Symbol spelling guidance (e.g., "equals sign" instead of "=")
   - Natural pacing and phrase breaks
   - Technical abbreviation expansion

3. **When to Use This Style** - Use case guidance for:
   - Text-to-speech system integration
   - Voice interface applications
   - Accessibility for visually impaired users
   - Listening-prioritized workflows

4. **Example Responses** - Good/bad TTS examples demonstrating:
   - Natural listening patterns ("slash home slash user")
   - Control key naming ("Control C")
   - Clear boolean expressions
   - Anti-patterns with symbols and operators

5. **Important Notes** - Exception handling and priorities:
   - Listening comprehension prioritized over brevity
   - Flexibility for technical accuracy
   - Correctness first principle
   - Up-to-60-line flexibility for clarity

### Design Decisions

**Listening Comprehension First**: Unlike `concise-ultra` which optimizes for token efficiency, this template prioritizes natural speech patterns and cognitive processing during listening.

**TTS-Specific Techniques**:
- Backtick usage provides silent markers for TTS engines
- Spelled-out operators prevent mispronunciation
- Short sentences reduce cognitive load during listening
- Natural pauses replace extreme brevity

**Flexibility for Accuracy**: Template allows up to 60 lines (vs. 45-55 guideline) to prioritize correctness and technical clarity over absolute brevity.

## How to Use

### For Users

The concise-tts output style is available as a Claude Code output style option. Select it when:

1. Consuming responses via text-to-speech systems
2. Listening rather than reading responses
3. Working with voice interfaces or accessibility features
4. Natural prosody matters more than extreme brevity

### For Developers

The template is located in the TAC Bootstrap project's output-styles directory:

```bash
# View the Jinja2 template
cat tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-tts.md.j2

# View the rendered output style
cat .claude/output-styles/concise-tts.md
```

## Configuration

No additional configuration required. The template is static markdown content without Jinja2 variables. It integrates with existing Claude Code output style infrastructure automatically.

## Testing

Verify the implementation with these commands:

```bash
# Verify both files exist
ls -l tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-tts.md.j2
ls -l .claude/output-styles/concise-tts.md
```

Validate content includes required sections:

```bash
# Check for all required sections
grep "Response Guidelines" .claude/output-styles/concise-tts.md
grep "When to Use This Style" .claude/output-styles/concise-tts.md
grep "Example Responses" .claude/output-styles/concise-tts.md
grep "Important Notes" .claude/output-styles/concise-tts.md
```

Verify template syntax:

```bash
# Run existing test suite (no new tests required)
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Check for linting issues:

```bash
# Lint check
cd tac_bootstrap_cli && uv run ruff check .
```

## Notes

### Design Principles

**Consistency**: The template follows established patterns from existing output style templates, maintaining UI/UX consistency across output styles.

**Accessibility First**: Prioritizes listening comprehension and accessibility, filling a gap in the existing output style portfolio.

**Correctness Over Brevity**: Allows flexibility in line count and sentence length to ensure technical accuracy is never compromised.

### Differences from Existing Styles

| Aspect | Concise Ultra | Concise TTS |
|--------|---------------|------------|
| Priority | Token efficiency | Listening comprehension |
| Sentence Length | Flexible | Under 20 words (guideline) |
| Symbol Handling | Implicit | Spelled out for TTS |
| Line Count | 45-55 | 45-55 (flexible to 60) |
| Use Case | Written, programmatic | Spoken, voice interfaces |

### Future Considerations

- Monitor TTS adoption and gather user feedback
- Consider expanding voice-based output style family
- Evaluate sentence length preferences from TTS user communities
- Reference this template for future accessibility-focused features

### Related Output Styles

This feature complements existing output style templates:
- `concise-ultra.md.j2` - Extreme token efficiency
- `concise-done.md.j2` - Done/completion-focused output

The concise-tts template fills an important accessibility and accessibility niche for voice-based consumption.
