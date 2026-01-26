# Feature: Add concise-tts.md.j2 Output Style Template

## Metadata
- **issue_number**: 235
- **adw_id**: feature_Tac_9_task_4_2_3
- **feature**: Add concise-tts output style template for TTS-compatible output format
- **status**: Planning

## Feature Description

Create a Jinja2 template for the "concise-tts" output style that produces speech-optimized output. This style bridges the concise output family with audio delivery requirements. Unlike traditional text-based styles, concise-tts prioritizes listening comprehension and natural speech pacing over extreme token efficiency. The output is designed to sound natural when read aloud by text-to-speech systems or human readers.

## User Story

**As a** Developer using Claude Code with text-to-speech integrations
**I want to** receive responses optimized for listening comprehension
**So that** I can consume Claude Code responses in audio format with natural pacing and clear pronunciation

## Problem Statement

The current output style templates (concise-ultra, concise-done) are optimized for reading or programmatic parsing. TTS systems and listeners have fundamentally different comprehension patterns:
- Listening comprehension requires natural sentence rhythm and pacing
- Technical terms need explicit spelling guidance to avoid mispronunciation
- Sentences under 20 words prevent cognitive overload during listening
- Special characters and operators confuse speech synthesis without explicit guidance
- Extreme token efficiency (concise-ultra) creates unnatural speech patterns

**Gap**: No existing output style balances conciseness with TTS clarity and listening comprehension.

## Solution Statement

Implement concise-tts as a new output style template that:
1. **Maintains brevity** within 45-55 lines (soft guideline, flexible to 60 for clarity)
2. **Optimizes for listening** with natural sentence structure and under-20-word sentences
3. **Handles special characters** explicitly by spelling out symbols and avoiding operators
4. **Uses practical code formatting** with backticks for inline code/variables
5. **Provides exception carve-outs** in Important Notes for technical accuracy
6. **Differs from concise-ultra** by prioritizing natural pacing over token efficiency

The template follows the established pattern from concise-ultra and concise-done, maintaining consistency while addressing TTS-specific requirements.

## Relevant Files

### Existing Files (for reference/pattern)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-ultra.md.j2` - Template pattern and structure
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-done.md.j2` - Alternative template example
- `.claude/output-styles/concise-ultra.md` - Rendered version (reference)

### New Files to Create
- **`tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-tts.md.j2`** - Jinja2 template (primary deliverable)
- **`.claude/output-styles/concise-tts.md`** - Rendered markdown version (rendered from template)

## Implementation Plan

### Phase 1: Foundation
- Review existing template structure (concise-ultra.md.j2)
- Understand Jinja2 template patterns used in project
- Confirm directory structure and naming conventions

### Phase 2: Core Implementation
- Create concise-tts.md.j2 template with:
  - **Response Guidelines** section optimized for TTS
  - **When to Use This Style** section with TTS use cases
  - **Example Responses** section with good/bad TTS examples
  - **Important Notes** section with TTS-specific guidance
- Ensure 45-55 line range with flexibility for clarity
- Prioritize listening comprehension over token efficiency

### Phase 3: Integration
- Render the Jinja2 template to create .claude/output-styles/concise-tts.md
- Verify file exists in both locations
- Validate against acceptance criteria

## Step by Step Tasks

### Task 1: Create concise-tts.md.j2 Template
**File**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-tts.md.j2`

**Content Structure**:
1. **Header** - Introduce concise-tts style with TTS focus
2. **Response Guidelines** - Core TTS requirements:
   - Sentences under 20 words
   - Use backticks for inline code/variables/URLs
   - Spell out single symbols and avoid operators
   - Natural pauses and phrasing
   - Avoid mathematical notation in running text
3. **When to Use This Style** - Use case guidance:
   - Voice-based interactions
   - TTS integration scenarios
   - Accessible output requirements
   - Listening-optimized workflows
4. **Example Responses** - Good/bad examples with TTS considerations
5. **Important Notes** - Exception carve-outs and guidance:
   - Break under-20-word guideline if necessary for technical accuracy
   - Correctness trumps brevity
   - Mention that slight verbosity acceptable for clarity

**Requirements**:
- Target 45-55 lines (soft guideline, allow flexibility to 60 for TTS clarity)
- Follow concise-ultra.md.j2 structure and formatting
- Use Jinja2 syntax (no dynamic variables required for this template)
- Prioritize listening comprehension over token efficiency
- Provide practical guidance for TTS delivery

### Task 2: Render Template to Markdown
**File**: `.claude/output-styles/concise-tts.md`

- Process concise-tts.md.j2 template to generate rendered output-styles/concise-tts.md
- Verify content matches template (both should be identical for static templates)

### Task 3: Validate File Existence and Content
- Confirm both files exist in correct locations
- Verify file names match specification exactly
- Check content includes all required sections

## Testing Strategy

### Static Content Validation
- File exists at `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-tts.md.j2`
- File exists at `.claude/output-styles/concise-tts.md`
- Template renders without errors
- No Jinja2 syntax errors in template

### Content Validation
- Template includes all five sections (Header, Response Guidelines, When to Use, Examples, Important Notes)
- Response Guidelines contain TTS-specific guidance
- Examples include good/bad TTS responses
- Line count in acceptable range (45-60 lines)

### Integration Validation
- CLI recognizes concise-tts as valid output style option
- Existing smoke tests pass (CLI --help)
- No regressions in other output styles

## Acceptance Criteria

✅ **File Creation**
- [ ] `tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-tts.md.j2` created with valid Jinja2 syntax
- [ ] `.claude/output-styles/concise-tts.md` rendered from template and present

✅ **Content Requirements**
- [ ] Template includes Header section introducing concise-tts style
- [ ] Response Guidelines section with sentences under 20 words
- [ ] Response Guidelines include: backtick usage, symbol spelling, operator avoidance, natural pacing
- [ ] "When to Use This Style" section with TTS-specific use cases
- [ ] Example Responses section with good/bad TTS examples
- [ ] Important Notes section with exception carve-outs for technical accuracy

✅ **Quality Metrics**
- [ ] Template is 45-55 lines (flexible to 60 if needed for TTS clarity)
- [ ] Listening comprehension prioritized over token efficiency
- [ ] Consistent formatting with existing output style templates
- [ ] No Jinja2 errors or syntax issues

✅ **Validation**
- [ ] Existing validation commands pass with zero regressions
- [ ] CLI --help works without errors
- [ ] Files match specification naming and location

## Validation Commands

Execute these commands in order to validate implementation:

```bash
# 1. Verify files exist
ls -l tac_bootstrap_cli/tac_bootstrap/templates/claude/output-styles/concise-tts.md.j2
ls -l .claude/output-styles/concise-tts.md

# 2. Verify template syntax (no errors)
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# 3. Lint check
cd tac_bootstrap_cli && uv run ruff check .

# 4. Type check
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# 5. Smoke test - CLI should recognize the style
cd tac_bootstrap_cli && uv run tac-bootstrap --help

# 6. Verify file content includes required sections
grep -c "Response Guidelines" .claude/output-styles/concise-tts.md
grep -c "When to Use This Style" .claude/output-styles/concise-tts.md
grep -c "Important Notes" .claude/output-styles/concise-tts.md
```

## Notes

### Template Structure Reference
The template follows the established pattern from concise-ultra.md.j2:
- Static markdown content (no dynamic Jinja2 variables needed)
- Five-section structure: Header → Guidelines → Use Cases → Examples → Notes
- Markdown formatting with headers, lists, and code blocks

### Key Differences from concise-ultra
- **Priority**: Listening comprehension (not extreme token efficiency)
- **Sentence Structure**: Natural pacing prioritized, under-20-word guideline
- **Special Characters**: Explicit guidance on pronunciation and TTS handling
- **Flexibility**: Allows slight verbosity (up to 60 lines) if needed for clarity

### TTS-Specific Guidance
The template should emphasize:
1. **Short sentences** (under 20 words) for cognitive processing
2. **Code backticks** as silent markers for TTS engines
3. **Spelled-out operators** (e.g., "equals sign" not "=")
4. **Natural prosody** over extreme brevity
5. **Exception handling** for technical accuracy

### No New Tests Required
Per specification, this is a static template file without code logic. Existing smoke tests and CLI validation are sufficient. No new unit tests needed.

### Future Considerations
- Monitor TTS integration adoption
- Gather feedback on sentence length preferences from TTS users
- Consider expanding to other TTS-oriented styles if needed
- May reference this template for future voice-based output modes

