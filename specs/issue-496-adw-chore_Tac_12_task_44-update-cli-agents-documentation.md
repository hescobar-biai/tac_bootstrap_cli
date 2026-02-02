# Chore: Update CLI agents documentation

## Metadata
issue_number: `496`
adw_id: `chore_Tac_12_task_44`
issue_json: `[Task 44/49] [CHORE] Update CLI agents documentation`

## Chore Description

Update the CLI agents documentation (`tac_bootstrap_cli/docs/agents.md`) to include all 6 new TAC-12 agents that are missing from the existing documentation. The documentation should follow the existing lightweight pattern established for `docs-scraper`, `meta-agent`, and `research-docs-fetcher`.

### Missing Agents
1. **build-agent** - Parallel build workflow specialist for single file implementation
2. **playwright-validator** - E2E validation and browser automation specialist
3. **scout-report-suggest** - Codebase analysis and problem identification (sonnet model)
4. **scout-report-suggest-fast** - Fast variant of scout with haiku model
5. **meta-agent** - (Already in docs but may need review/updates)
6. **research-docs-fetcher** - (Already in docs but may need review/updates)

## Relevant Files

### Files to Modify
- `tac_bootstrap_cli/docs/agents.md` - Main agents documentation file

### Agent Definition Files (for reference)
- `.claude/agents/build-agent.md`
- `.claude/agents/playwright-validator.md`
- `.claude/agents/scout-report-suggest.md`
- `.claude/agents/scout-report-suggest-fast.md`
- `.claude/agents/meta-agent.md`
- `.claude/agents/research-docs-fetcher.md`

## Step by Step Tasks

### Task 1: Verify existing documentation
- Read the current `agents.md` file
- Identify which agents are already documented
- Note the documentation pattern and style used
- List missing agents that need to be added

### Task 2: Extract agent capabilities from definition files
- Read each missing agent definition file (`.claude/agents/`)
- Extract: agent description, model type, tools available, capabilities
- Note practical use cases from agent documentation
- Identify any unique output structures

### Task 3: Add build-agent documentation
- Create new section after `docs-scraper` section
- Include: name, description, location reference to `.claude/agents/build-agent.md (model: sonnet)`
- Add Capabilities list (file implementation, context gathering, pattern analysis, verification)
- Include practical Use cases code block
- Add Output structure section showing key deliverables

### Task 4: Add playwright-validator documentation
- Create new section after build-agent
- Include: name, description, location reference to `.claude/agents/playwright-validator.md (model: sonnet)`
- Add Capabilities list (E2E test execution, test failure handling, evidence capture, structured reporting)
- Include practical Use cases code block showing test scenarios
- Add Output structure for test results and evidence

### Task 5: Add scout-report-suggest documentation
- Create new section after playwright-validator
- Include: name, description, location reference to `.claude/agents/scout-report-suggest.md (model: sonnet)`
- Add Capabilities list (codebase analysis, issue identification, root cause analysis, resolution suggestions)
- Include practical Use cases code block
- Add "Best For" section: comprehensive analysis with detailed reasoning

### Task 6: Add scout-report-suggest-fast documentation
- Create new section after scout-report-suggest
- Include: name, description, location reference to `.claude/agents/scout-report-suggest-fast.md (model: haiku)`
- Add Capabilities list (same as scout-report-suggest but optimized for speed)
- Include practical Use cases code block
- Add "Best For" section: quick analysis when speed is prioritized over depth

### Task 7: Review and update existing agent sections
- Verify meta-agent documentation is complete and consistent
- Verify research-docs-fetcher documentation is complete and consistent
- Ensure all sections follow the same format and style

### Task 8: Update Available Agents section
- Add entries for all 6 new agents in the Available Agents table of contents
- Ensure cross-references are correct
- Verify anchor links would work properly

### Task 9: Validate documentation consistency
- Check that all agent entries follow the same structure:
  - H3 heading with agent name
  - One-line description
  - Location reference with model specified
  - Capabilities bullet list
  - Use cases code block
  - Output structure or "Best For" section
- Ensure consistent formatting and spacing throughout

### Task 10: Final verification and validation
- Run Markdown validation (check syntax is valid)
- Verify no broken references or anchors
- Ensure the document is readable and well-organized
- Check consistency with existing documentation patterns

## Validation Commands

```bash
# Validate Markdown syntax
cd tac_bootstrap_cli && python3 -m markdown docs/agents.md

# Check file exists and is readable
head -50 tac_bootstrap_cli/docs/agents.md

# Verify all agent definitions referenced exist
ls -la .claude/agents/*.md | grep -E "(build-agent|playwright-validator|scout-report-suggest|meta-agent|research-docs-fetcher)"

# Count sections to verify all 6 agents documented
grep "^### " tac_bootstrap_cli/docs/agents.md | wc -l
```

## Notes

- **Documentation Pattern**: Follow the lightweight pattern established in the existing agents.md file. Each agent gets:
  - Name and one-line description
  - Location reference with model (haiku/sonnet)
  - Bulleted capabilities
  - Code block with use cases
  - Output structure or "Best For" section

- **Model Information**: Include model type in location reference:
  - build-agent: sonnet
  - playwright-validator: sonnet
  - scout-report-suggest: sonnet
  - scout-report-suggest-fast: haiku (optimized for speed)

- **Consistency**: All 6 new agents must follow the exact same documentation format as existing agents (docs-scraper, meta-agent, research-docs-fetcher)

- **Practical Use Cases**: Each agent needs code block examples showing real-world delegation scenarios

- **Cross-references**: Update the "Available Agents" section to list all agents for easy discovery
