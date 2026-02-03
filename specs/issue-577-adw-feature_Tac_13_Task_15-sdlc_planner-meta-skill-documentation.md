# Feature: Meta-Skill Pattern Documentation

## Metadata
issue_number: `577`
adw_id: `feature_Tac_13_Task_15`
issue_json: `{"number": 577, "title": "[TAC-13] Task 15: Create meta-skill documentation", "body": "**Workflow Metadata:**\n```\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_13_Task_15\n```\n\n**Description:**\nDocument meta-skill pattern and progressive disclosure approach for skills.\n\n**Technical Steps:**\n1. Create `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/meta-skill-pattern.md`\n2. Document 3-level progressive disclosure:\n   - Level 1: Metadata (name, description) - always loaded\n   - Level 2: Instructions (SKILL.md main body) - loaded when triggered\n   - Level 3: Resources (linked files) - loaded as needed\n3. Document skill structure:\n   - YAML frontmatter (name, description)\n   - Purpose section\n   - When to Use section\n   - Instructions section\n   - Linked resources (reference files, scripts)\n4. Include examples: processing-pdfs, start-orchestrator\n5. Document discovery pattern (project vs personal skills)\n6. Best practices: keep SKILL.md under 500 lines, use gerund naming\n\n**Acceptance Criteria:**\n- Explains progressive disclosure clearly\n- Includes concrete examples\n- Provides creation workflow\n- Documents discovery mechanism\n\n**Impacted Paths:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/meta-skill-pattern.md`"}`

## Feature Description

Document the meta-skill pattern - a sophisticated approach to organizing agent knowledge using progressive disclosure and SKILL.md files. Skills are composable, reusable agent workflows that can be discovered at project or personal levels, triggered by user actions or patterns, and load only necessary context through a 3-level progressive disclosure mechanism.

This documentation will serve as:
1. Reference guide for creating new skills following TAC patterns
2. Educational resource explaining the progressive disclosure philosophy
3. Implementation guide with concrete examples from existing skills (create-crud-entity, generating-fractal-docs)
4. Discovery mechanism documentation (project vs personal skills)

## User Story

As a TAC Bootstrap developer or agent
I want comprehensive documentation on the meta-skill pattern
So that I can create well-structured, efficient skills that follow progressive disclosure principles and integrate seamlessly with the TAC ecosystem

## Problem Statement

TAC-13 introduces meta-agentic patterns including skills, but there's no comprehensive documentation explaining:
- What skills are and how they differ from commands or ADWs
- The 3-level progressive disclosure mechanism (metadata → instructions → resources)
- Standard SKILL.md structure and frontmatter format
- Discovery patterns (project vs personal skills)
- Best practices (file size limits, naming conventions, gerund naming)
- How to create new skills from scratch

Without this documentation, developers and agents lack guidance for creating consistent, efficient skills.

## Solution Statement

Create `ai_docs/doc/meta-skill-pattern.md` that comprehensively documents:

1. **Progressive Disclosure Model**: Explain the 3 levels and why this approach optimizes context window usage
2. **SKILL.md Structure**: Document YAML frontmatter schema and markdown sections
3. **Concrete Examples**: Analyze existing skills (create-crud-entity, generating-fractal-docs) as reference implementations
4. **Discovery Mechanism**: Explain how skills are discovered at project and personal levels
5. **Creation Workflow**: Step-by-step guide for generating new skills
6. **Best Practices**: Size limits (500 lines), naming (gerund form), and organization patterns

## Relevant Files

Existing documentation and examples to analyze:

### Existing Skills (Examples to Reference)
- `ai_docs/doc/create-crud-entity/SKILL.md` - Complex skill with templates, shows full structure
- `ai_docs/doc/create-crud-entity/generating-fractal-docs/SKILL.md` - Nested skill example

### Related Documentation
- `ai_docs/doc/plan_tasks_tac_13.md` - TAC-13 task definitions (Task 15 at line 800+)
- `ai_docs/doc/Tac-13_1.md` - Agent experts concepts
- `ai_docs/doc/expertise-file-structure.md` - Similar progressive disclosure pattern for expertise files
- `.claude/commands/meta-prompt.md` - Meta-prompt pattern (similar concept)

### Commands for Comparison
- `.claude/commands/feature.md` - Command structure for comparison
- `.claude/commands/implement.md` - Another command example

### New Files
- `ai_docs/doc/meta-skill-pattern.md` - Main documentation file to create

## Implementation Plan

### Phase 1: Research and Analysis
Analyze existing skills and related patterns to extract common structures and best practices.

### Phase 2: Document Core Concepts
Write the progressive disclosure model explanation, skill philosophy, and comparison with commands/ADWs.

### Phase 3: Structure and Examples
Document SKILL.md structure with annotated examples from existing skills.

### Phase 4: Discovery and Creation Workflow
Document how skills are discovered and provide step-by-step creation guide.

## Step by Step Tasks

### Task 1: Analyze Existing Skills
- Read `ai_docs/doc/create-crud-entity/SKILL.md` completely
- Read `ai_docs/doc/create-crud-entity/generating-fractal-docs/SKILL.md` completely
- Extract common patterns: frontmatter structure, section organization, file size
- Note differences between simple and complex skills
- Identify progressive disclosure levels in practice

### Task 2: Create Documentation File Structure
- Create `ai_docs/doc/meta-skill-pattern.md`
- Define table of contents with main sections:
  - Introduction (What are Skills?)
  - Progressive Disclosure Model (3 Levels)
  - SKILL.md Structure (Frontmatter + Sections)
  - Discovery Mechanism (Project vs Personal)
  - Creation Workflow (Step-by-Step)
  - Examples (Annotated from Existing Skills)
  - Best Practices (Size, Naming, Organization)
  - Comparison (Skills vs Commands vs ADWs)

### Task 3: Write Progressive Disclosure Documentation
- Document Level 1: Metadata (name, description in frontmatter) - always loaded
- Document Level 2: Instructions (main SKILL.md body) - loaded when triggered
- Document Level 3: Resources (linked templates, scripts, docs) - loaded as needed
- Explain context window optimization benefits
- Include diagram or table showing token usage per level

### Task 4: Document SKILL.md Structure
- Document YAML frontmatter schema:
  - `name`: kebab-case skill identifier
  - `description`: One-line trigger description
  - Optional fields: `allowed-tools`, custom fields
- Document standard markdown sections:
  - Purpose/Quick Start
  - When to Use
  - Instructions/Workflow
  - Templates/Resources (if applicable)
  - Best Practices
- Include annotated frontmatter examples

### Task 5: Add Concrete Examples
- Example 1: `create-crud-entity` (complex skill with templates)
  - Annotate frontmatter
  - Highlight progressive disclosure in practice
  - Show linked resources pattern
- Example 2: `generating-fractal-docs` (nested skill)
  - Annotate frontmatter with allowed-tools
  - Show script bundling pattern
- Reference hypothetical examples: processing-pdfs, start-orchestrator

### Task 6: Document Discovery Mechanism
- Explain project-level skills discovery (repo-specific)
- Explain personal-level skills discovery (user-specific across projects)
- Document trigger patterns (keywords, user requests)
- Explain skill name resolution
- Include discovery algorithm or flowchart

### Task 7: Write Creation Workflow
- Step 1: Identify skill purpose and scope
- Step 2: Choose skill name (gerund form: creating-X, processing-Y)
- Step 3: Write frontmatter (name, description, optional fields)
- Step 4: Structure main sections (Purpose, When to Use, Instructions)
- Step 5: Create linked resources if needed (templates/, scripts/)
- Step 6: Validate size (<500 lines for main SKILL.md)
- Step 7: Test discovery and triggering
- Include checklist for skill creation

### Task 8: Document Best Practices
- Size limit: SKILL.md main file should be <500 lines
  - Rationale: Context window efficiency
  - Strategy: Use progressive disclosure, link to resources instead of inlining
- Naming convention: Use gerund form (creating-X, processing-Y, generating-Z)
- Organization: Group related resources in skill subdirectory
- Frontmatter: Keep description concise but trigger-rich
- Linked resources: Use relative paths, organize by type (templates/, scripts/, docs/)
- Testing: Verify skill can be discovered and loads correctly

### Task 9: Add Skills vs Commands vs ADWs Comparison
- Create comparison table with columns:
  - Purpose
  - File structure
  - Discovery mechanism
  - Context loading
  - Typical size
  - Use cases
- Clarify when to use each pattern
- Highlight progressive disclosure advantage of skills

### Task 10: Validate Documentation
- Verify all sections in table of contents are complete
- Check that both example skills are referenced with analysis
- Confirm progressive disclosure is explained at 3 levels
- Validate discovery mechanism is documented
- Ensure creation workflow has 7+ actionable steps
- Check best practices section has 5+ guidelines
- Verify file size is reasonable (400-800 lines recommended)
- Run markdown linting if available

## Testing Strategy

### Content Validation
- All 3 progressive disclosure levels explained with context window benefits
- SKILL.md frontmatter schema documented with all fields
- At least 2 concrete example skills analyzed (create-crud-entity, generating-fractal-docs)
- Discovery mechanism documented for both project and personal levels
- Creation workflow has minimum 7 steps
- Best practices include size limit (500 lines), gerund naming, organization patterns

### Structure Validation
- Table of contents matches actual sections
- All frontmatter examples are valid YAML
- All file paths referenced exist or are marked as hypothetical
- Markdown renders correctly (headings, code blocks, tables)

### Acceptance Criteria Validation
From issue:
- ✅ Explains progressive disclosure clearly (3 levels with token usage)
- ✅ Includes concrete examples (create-crud-entity, generating-fractal-docs)
- ✅ Provides creation workflow (step-by-step guide)
- ✅ Documents discovery mechanism (project vs personal)

## Acceptance Criteria

### Functional Criteria
1. **Progressive Disclosure Documented**
   - All 3 levels explained (metadata, instructions, resources)
   - Context window optimization benefits clearly stated
   - Token usage comparison table or diagram included

2. **SKILL.md Structure Complete**
   - YAML frontmatter schema documented
   - All standard markdown sections explained
   - Annotated examples provided

3. **Concrete Examples Included**
   - `create-crud-entity` analyzed with annotations
   - `generating-fractal-docs` analyzed with annotations
   - Hypothetical examples referenced (processing-pdfs, start-orchestrator)

4. **Discovery Mechanism Explained**
   - Project-level discovery documented
   - Personal-level discovery documented
   - Trigger patterns explained

5. **Creation Workflow Provided**
   - Minimum 7 actionable steps
   - Checklist format for easy reference
   - Validation step included

6. **Best Practices Documented**
   - Size limit: SKILL.md <500 lines
   - Naming: Gerund form (creating-X, processing-Y)
   - Organization patterns
   - Resource linking strategies

### Quality Criteria
- Documentation is clear, concise, and actionable
- Examples are realistic and directly drawn from codebase
- File size is 400-800 lines (comprehensive but focused)
- Markdown is well-structured with proper headings and formatting

## Validation Commands

Validate the created documentation:

```bash
# 1. Verify file exists
test -f ai_docs/doc/meta-skill-pattern.md && echo "✅ File created" || echo "❌ File missing"

# 2. Check line count (should be 400-800 lines)
wc -l ai_docs/doc/meta-skill-pattern.md

# 3. Verify table of contents sections exist
for section in "Introduction" "Progressive Disclosure" "SKILL.md Structure" "Discovery Mechanism" "Creation Workflow" "Examples" "Best Practices"; do
  grep -q "# $section\|## $section" ai_docs/doc/meta-skill-pattern.md && echo "✅ $section section found" || echo "⚠️  $section section missing"
done

# 4. Verify concrete examples are referenced
grep -q "create-crud-entity" ai_docs/doc/meta-skill-pattern.md && echo "✅ create-crud-entity example found" || echo "❌ Missing example"
grep -q "generating-fractal-docs" ai_docs/doc/meta-skill-pattern.md && echo "✅ generating-fractal-docs example found" || echo "❌ Missing example"

# 5. Verify progressive disclosure levels documented
grep -q "Level 1.*Metadata" ai_docs/doc/meta-skill-pattern.md && echo "✅ Level 1 documented" || echo "❌ Level 1 missing"
grep -q "Level 2.*Instructions" ai_docs/doc/meta-skill-pattern.md && echo "✅ Level 2 documented" || echo "❌ Level 2 missing"
grep -q "Level 3.*Resources" ai_docs/doc/meta-skill-pattern.md && echo "✅ Level 3 documented" || echo "❌ Level 3 missing"

# 6. Check frontmatter examples are valid YAML (if they exist)
grep -Pzo '```yaml\n(.*?\n)*?```' ai_docs/doc/meta-skill-pattern.md > /dev/null 2>&1 && echo "✅ YAML examples found" || echo "⚠️  No YAML examples (might be intentional)"

# 7. Verify best practices section exists
grep -q "Best Practices\|best practices" ai_docs/doc/meta-skill-pattern.md && echo "✅ Best practices documented" || echo "❌ Best practices missing"

# 8. Markdown validation (basic)
grep -q "^#" ai_docs/doc/meta-skill-pattern.md && echo "✅ Markdown headers found" || echo "❌ No markdown structure"
```

## Notes

### Relationship to Existing Patterns

**Skills vs Commands**:
- Commands are single markdown files in `.claude/commands/`
- Skills are directories with SKILL.md + optional resources
- Skills use progressive disclosure, commands load entirely
- Skills can bundle templates/scripts, commands typically don't

**Skills vs Expertise Files**:
- Both use progressive disclosure philosophy
- Expertise files (expertise.yaml) store agent mental models
- Skills (SKILL.md) define reusable workflows with resources
- Expertise is data, skills are procedures

**Skills vs ADWs**:
- ADWs (AI Developer Workflows) are Python scripts for complex automation
- Skills are markdown-based, simpler, more composable
- ADWs handle orchestration, skills handle focused tasks
- Both can invoke each other

### Implementation Considerations

1. **Examples Must Be Real**: Reference actual files in codebase (`create-crud-entity`, `generating-fractal-docs`), not hypothetical examples only
2. **Progressive Disclosure is Key**: This is the core differentiator - must be explained thoroughly with token usage benefits
3. **Gerund Naming**: Emphasize this convention (creating-X, processing-Y, generating-Z) for consistency
4. **Size Discipline**: 500-line limit for SKILL.md is critical for context efficiency - document rationale clearly

### Future Enhancements

- Skill template generator (meta-meta-prompt)
- Automated skill discovery testing
- Skill composition patterns (skills calling skills)
- Integration with MCP skill protocol
