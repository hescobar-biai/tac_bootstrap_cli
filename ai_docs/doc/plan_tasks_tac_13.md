# TAC-13: Agent Experts Implementation Plan

## Assumptions

1. **Scope**: Implementing TAC-13 Agent Experts pattern in tac_bootstrap with focus on self-improving expertise files, meta-agentics, and basic orchestration patterns
2. **Priority**: Starting with agent expert foundation (expertise files + self-improve + question patterns), then meta-agentics, followed by CLI integration
3. **First Domains**: CLI Expert, ADW Expert, and Commands Expert as initial agent expert implementations
4. **Orchestration**: Basic multi-agent patterns without full WebSocket/database infrastructure (defer to future release)
5. **Version Bump**: MINOR version increase (0.7.0 → 0.8.0) due to significant new capabilities

---

## Tasks

### [CHORE] Task 1: Create TAC-13 documentation in ai_docs

**Workflow Metadata:**
```
/chore
/adw_sdlc_zte_iso
/adw_id: chore_Tac_13_Task_1
```

**Description:**
Create comprehensive documentation for TAC-13 concepts, patterns, and implementation guide.

**Technical Steps:**

1. **Create documentation file**:
   ```bash
   # Path
   /Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/Tac-13-agent-experts.md
   ```

2. **Document core concepts with examples**:

   **Section 1: The Problem**
   ```markdown
   ## The Problem TAC-13 Solves

   **Agents forget and don't learn.**

   - TAC-9/10/12 improved workflows, but each execution starts from zero
   - Memory files require manual updates
   - Generic agents rebuild understanding every time

   TAC-13 introduces: **Agents that learn automatically from each execution**
   ```

   **Section 2: Agent Experts - Act → Learn → Reuse Loop**
   ```markdown
   ## Agent Experts: Self-Improving Agents

   ### The 3-Step Loop

   1. **Act**: Execute task (build, modify, query)
   2. **Learn**: Self-improve prompt updates expertise.yaml automatically
   3. **Reuse**: Next execution uses expertise as starting point

   ### Difference from Generic Agents

   | Generic Agent | Agent Expert |
   |--------------|--------------|
   | Search codebase every time | Reads expertise first |
   | No memory between runs | Maintains mental model |
   | Manual knowledge transfer | Automatic learning |
   | 100% context window usage | 20% expertise + 80% specific task |
   ```

   **Section 3: Expertise Files as Mental Models**
   ```markdown
   ## Expertise Files: The Mental Model

   **Not source of truth** - A working memory structure that validates against code

   ### Example Structure (expertise.yaml):

   \`\`\`yaml
   overview:
     description: "Brief system description"
     key_files: ["path/to/file1.py", "path/to/file2.py"]

   core_implementation:
     component_name:
       location: "path/to/component.py"
       key_functions:
         - name: "function_name"
           line_start: 45
           line_end: 78
           logic: "What it does"

   schema_structure:  # If applicable
     tables: ["table1", "table2"]
     relationships: "How they connect"

   key_operations:
     operation_category:
       description: "What this category handles"
       files: ["file1.py", "file2.py"]
       patterns: "Common patterns used"

   best_practices:
     - "Do X when Y"
     - "Avoid Z because W"

   known_issues:
     - issue: "Description"
       workaround: "Solution"
   \`\`\`

   ### Constraints:
   - **Max 1000 lines** (enforced by self-improve)
   - **Valid YAML** (validated on every update)
   - **Compressed format** (YAML preferred over JSON for space)
   ```

   **Section 4: Self-Improving Template Metaprompts**
   ```markdown
   ## Self-Improving Template Metaprompts

   ### Definition

   A **self-improving template metaprompt** is:
   - **Metaprompt**: Prompt that builds other prompts
   - **Template**: Has specific purpose and structure
   - **Self-improving**: Updates itself/related files with new info

   ### The 7-Phase Self-Improve Workflow

   \`\`\`
   Phase 1: Check git diff (conditional)
      ↓
   Phase 2: Read current expertise.yaml
      ↓
   Phase 3: Validate expertise vs actual codebase
      ↓
   Phase 4: Identify discrepancies
      ↓
   Phase 5: Update expertise.yaml
      ↓
   Phase 6: Enforce line limit (<1000 lines)
      ↓
   Phase 7: Validate YAML syntax
   \`\`\`

   ### Example Self-Improve Prompt Structure:

   \`\`\`markdown
   ---
   allowed-tools: Read, Grep, Glob, Bash, Edit, Write, TodoWrite
   description: Self-improve CLI expertise by validating against codebase
   argument-hint: [check_git_diff] [focus_area]
   ---

   ## Variables
   - CHECK_GIT_DIFF: $1 (default: false)
   - FOCUS_AREA: $2 (default: empty)
   - EXPERTISE_FILE: .claude/commands/experts/cli/expertise.yaml
   - MAX_LINES: 1000

   ## Workflow

   ### Phase 1: Check Git Diff (Conditional)
   IF CHECK_GIT_DIFF is true:
     - Run: git diff HEAD
     - Identify changed files in CLI domain
     - Note: This focuses the update

   ### Phase 2: Read Current Expertise
   - Read EXPERTISE_FILE
   - Parse YAML structure
   - Identify current documented areas

   [... continues with all 7 phases ...]
   \`\`\`
   ```

   **Section 5: Meta-Agentics**
   ```markdown
   ## Meta-Agentics: System That Builds System

   ### Three Types

   1. **Meta-Prompts**: Prompts that generate other prompts
      - Input: Description of desired command
      - Output: Complete .md slash command file

   2. **Meta-Agents**: Agents that generate other agents
      - Input: Description of desired agent behavior
      - Output: Complete .md agent definition file

   3. **Meta-Skills**: Skills with progressive disclosure
      - Level 1: Metadata (always loaded)
      - Level 2: Instructions (loaded on trigger)
      - Level 3: Resources (loaded as needed)

   ### Why Meta-Agentics Matter

   "Build the system that builds the system"

   - Faster agentic layer development
   - Consistent patterns across generated artifacts
   - Less manual template maintenance
   ```

   **Section 6: When to Use Agent Experts**
   ```markdown
   ## When to Use Agent Experts

   ### ✅ Use Agent Experts For:

   - **Billing Systems**: High-risk, money-saving potential
   - **Security-Critical Code**: Authentication, authorization, encryption
   - **Complex Niche Systems**: Deep interconnections, non-obvious relationships
   - **Large Codebases**: Where connections span many files
   - **High Error Rate Areas**: Generic agents repeatedly fail

   ### ❌ Don't Use Agent Experts For:

   - Code that doesn't evolve
   - Brand-new, generic codebases
   - When YOU don't have a mental model yet
   - Simple 1-2 file problems

   ### Decision Framework

   | Question | Answer | Use Expert? |
   |----------|--------|-------------|
   | Does this area change frequently? | Yes | ✅ |
   | Are there non-obvious connections? | Yes | ✅ |
   | Is the cost of errors high? | Yes | ✅ |
   | Is it simple and self-contained? | Yes | ❌ |
   | Am I still learning this area? | Yes | ❌ |
   ```

   **Section 7: Examples from TAC-13 Codebase**
   ```markdown
   ## Real Examples from TAC-13

   ### Database Expert
   - **Location**: `/Volumes/MAc1/Celes/TAC/tac-13/.claude/commands/experts/database/`
   - **Expertise Size**: 413 lines YAML
   - **Coverage**: PostgreSQL async operations, schema, connection pool
   - **Use Case**: Answer database questions without searching codebase

   ### Websocket Expert
   - **Location**: `/Volumes/MAc1/Celes/TAC/tac-13/.claude/commands/experts/websocket/`
   - **Expertise Size**: 650 lines YAML
   - **Coverage**: Backend-frontend websocket communication
   - **Use Case**: Plan → Build → Improve workflow for websocket features

   ### Product Expert (Shopping Example)
   - **Use Case**: Per-user adaptive UI/UX
   - **Pattern**: User action → Learn preferences → Generate personalized UI
   - **Scaling**: One expertise file per user
   ```

3. **Reference TAC-13 source implementations**:
   - Link to `/Volumes/MAc1/Celes/TAC/tac-13/.claude/commands/experts/`
   - Include actual expertise.yaml snippets
   - Reference video timestamps from Tac-13_1.md and Tac-13_2.md

4. **Add troubleshooting section**:
   ```markdown
   ## Troubleshooting

   ### False Expertise
   - **Problem**: Agent updates expertise incorrectly
   - **Solution**: Run self-improve with focus_area, validate manually
   - **Prevention**: Strict validation in Phase 7

   ### Expertise Bloat
   - **Problem**: Expertise file exceeds 1000 lines
   - **Solution**: Enforce MAX_LINES in self-improve, compress format
   - **Prevention**: Use YAML, avoid verbose descriptions

   ### Too Granular
   - **Problem**: Expertise is line-by-line documentation
   - **Solution**: Focus on patterns, not implementation details
   - **Prevention**: Prompt engineering in self-improve
   ```

**Acceptance Criteria:**
- ✅ Documentation covers all 7 core concepts with examples
- ✅ Includes 3+ concrete code examples from TAC-13 codebase
- ✅ References specific files with line numbers from `/Volumes/MAc1/Celes/TAC/tac-13/`
- ✅ Provides decision framework table with 5+ criteria
- ✅ Includes troubleshooting section with 3+ common issues
- ✅ File is 500-800 lines of well-structured markdown
- ✅ All code blocks are properly formatted with syntax highlighting

**Validation Commands:**
```bash
# Verify file exists and is valid markdown
test -f /Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/Tac-13-agent-experts.md && echo "✓ File exists"

# Check line count (should be 500-800)
wc -l /Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/Tac-13-agent-experts.md

# Verify YAML examples are valid
grep -A 20 '```yaml' /Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/Tac-13-agent-experts.md | python3 -c "import yaml, sys; yaml.safe_load(sys.stdin)"
```

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/Tac-13-agent-experts.md`

---

### [FEATURE] Task 2: Create expertise file structure documentation

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_13_Task_2
```

**Description:**
Document the standard structure for expertise.yaml files used by agent experts.

**Technical Steps:**

1. **Create documentation file**:
   ```bash
   /Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/expertise-file-structure.md
   ```

2. **Define complete YAML schema with examples**:

   **Full Schema Template:**
   ```yaml
   overview:
     description: "One-sentence description of what this expert covers"
     key_files:
       - "path/to/main/file1.py"
       - "path/to/main/file2.py"
     total_files: 15
     last_updated: "2026-02-03"

   core_implementation:
     component_name_1:
       location: "path/to/component.py"
       description: "What this component does"
       key_classes:
         - name: "ClassName"
           line_start: 10
           line_end: 150
           purpose: "Core responsibility"
           key_methods:
             - name: "method_name"
               line_start: 45
               line_end: 78
               signature: "def method_name(self, arg1: str, arg2: int) -> bool"
               logic: "High-level what it does (not line-by-line)"
               dependencies: ["OtherClass", "external_lib"]
       key_functions:
         - name: "standalone_function"
           line_start: 200
           line_end: 250
           signature: "def standalone_function(config: Config) -> Result"
           logic: "What it does and why"

     component_name_2:
       # ... same structure ...

   schema_structure:  # Optional: for database/API experts
     tables:
       - name: "table_name"
         primary_key: "id"
         columns: ["col1", "col2", "col3"]
         relationships:
           - table: "related_table"
             type: "one_to_many"
             foreign_key: "related_id"
     views:
       - name: "view_name"
         query_logic: "Aggregates X from Y"

   key_operations:
     operation_category_1:
       description: "What this category handles"
       files:
         - "path/to/handler.py"
         - "path/to/utils.py"
       workflow: |
         1. Entry point: function_a() in handler.py:45
         2. Validation: function_b() in utils.py:120
         3. Processing: function_c() in handler.py:89
         4. Response: function_d() in handler.py:150
       patterns:
         - "Pattern 1: Use X when Y"
         - "Pattern 2: Avoid Z because W"
       examples:
         - description: "Common use case"
           code_reference: "handler.py:45-78"

   data_flow:  # Optional: for complex systems
     input: "Where data enters"
     transformations:
       - step: "Transformation 1"
         location: "file.py:100"
       - step: "Transformation 2"
         location: "file.py:200"
     output: "Where data exits"

   performance_tuning:
     bottlenecks:
       - location: "file.py:500"
         issue: "N+1 query problem"
         solution: "Use bulk loading"
     optimizations:
       - "Connection pool: min=5, max=20"
       - "Cache TTL: 300 seconds"

   best_practices:
     dos:
       - "Do X when implementing Y"
       - "Always validate Z before W"
     donts:
       - "Don't use A because B"
       - "Avoid C in production (use D instead)"

   known_issues:
     - issue: "Description of known limitation"
       workaround: "How to work around it"
       tracking: "Issue #123 or TODO location"

   recent_changes:  # Auto-updated by self-improve
     - date: "2026-02-03"
       description: "Added new validation logic"
       files: ["validator.py"]
     - date: "2026-02-01"
       description: "Refactored database connections"
       files: ["db.py", "pool.py"]
   ```

3. **Provide 3 complete examples**:

   **Example 1: CLI Expert (tac-bootstrap)**
   ```yaml
   overview:
     description: "tac-bootstrap CLI for generating agentic layers"
     key_files:
       - "tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py"
       - "tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py"
     total_files: 8
     last_updated: "2026-02-03"

   core_implementation:
     cli_interface:
       location: "tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py"
       description: "Typer CLI commands"
       key_functions:
         - name: "init"
           line_start: 25
           line_end: 45
           signature: "def init(name: str, language: Optional[str] = None)"
           logic: "Creates new project with wizard or options"
         - name: "add_agentic"
           line_start: 50
           line_end: 80
           signature: "def add_agentic(dry_run: bool = False)"
           logic: "Adds agentic layer to existing project"

     scaffold_service:
       location: "tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py"
       description: "Core template rendering and file generation"
       key_classes:
         - name: "ScaffoldService"
           line_start: 15
           line_end: 300
           key_methods:
             - name: "_add_claude_code_commands"
               line_start: 150
               line_end: 200
               logic: "Registers all command templates for rendering"
             - name: "render_template"
               line_start: 220
               line_end: 250
               logic: "Renders Jinja2 template with config variables"

   key_operations:
     template_registration:
       description: "How templates are registered and rendered"
       workflow: |
         1. ScaffoldService.__init__ loads config
         2. _add_claude_code_commands() registers templates via plan.add_file()
         3. Each template gets: action, template path, reason
         4. render_template() processes .j2 files with config variables
       files:
         - "scaffold_service.py"
       patterns:
         - "Use plan.add_file(action='create', template='path.j2')"
         - "Template variables: {{ config.project.name }}"

   best_practices:
     dos:
       - "Register templates in _add_claude_code_commands method"
       - "Use action='skip_if_exists' for seed files like expertise.yaml"
       - "Always provide a 'reason' parameter for clarity"
     donts:
       - "Don't hardcode project names in templates"
       - "Avoid complex logic in Jinja2 templates"
   ```

   **Example 2: ADW Expert**
   ```yaml
   overview:
     description: "AI Developer Workflows for SDLC automation"
     key_files:
       - "adws/adw_sdlc_iso.py"
       - "adws/adw_modules/workflow_ops.py"
       - "adws/adw_modules/state.py"
     total_files: 12

   core_implementation:
     state_management:
       location: "adws/adw_modules/state.py"
       key_classes:
         - name: "ADWState"
           line_start: 20
           line_end: 150
           key_methods:
             - name: "save"
               line_start: 80
               logic: "Persists state to .adw_state.json"
             - name: "load"
               line_start: 95
               logic: "Loads state from previous run"

     workflow_orchestration:
       location: "adws/adw_modules/workflow_ops.py"
       key_functions:
         - name: "run_phase"
           line_start: 50
           line_end: 100
           logic: "Executes workflow phase (clarify/plan/build/test/review/ship)"
         - name: "detect_relevant_docs"
           line_start: 200
           line_end: 300
           logic: "TAC-9 integration: auto-detects ai_docs to load"

   key_operations:
     sdlc_workflow:
       description: "Full SDLC automation workflow"
       workflow: |
         1. Fetch issue from GitHub
         2. Detect relevant docs (TAC-9)
         3. Clarify requirements
         4. Plan implementation
         5. Build with /build_w_report (TAC-10)
         6. Test
         7. Review
         8. Document
         9. Ship (commit, PR, merge)
       files:
         - "adw_sdlc_iso.py"
         - "adw_sdlc_zte_iso.py"

   best_practices:
     dos:
       - "Use ADWState for persistence across phases"
       - "Always detect_relevant_docs before planning"
       - "Track KPIs after each workflow completion"
   ```

   **Example 3: Commands Expert**
   ```yaml
   overview:
     description: "Slash command structure and patterns"
     key_files:
       - ".claude/commands/*.md"
     total_files: 25+

   core_implementation:
     command_structure:
       description: "Standard slash command file format"
       components:
         yaml_frontmatter:
           required_fields:
             - allowed-tools: "List of tool names"
             - description: "One-line description"
             - argument-hint: "[arg1] [arg2]"
           optional_fields:
             - model: "sonnet|opus|haiku"
         markdown_sections:
           - "## Purpose"
           - "## Variables"
           - "## Instructions"
           - "## Workflow"
           - "## Report"

     variable_injection:
       patterns:
         dynamic_variables:
           - "$1, $2, $3": "Positional arguments"
           - "$ARGUMENTS": "All arguments as string"
         static_variables:
           - "{{ config.project.name }}": "From config.yml"
           - "{{ config.commands.test }}": "Command definitions"

   key_operations:
     command_creation:
       workflow: |
         1. Define YAML frontmatter
         2. Document purpose
         3. List variables with defaults
         4. Write workflow steps (numbered)
         5. Define report format
       examples:
         - description: "Simple read-only command"
           code_reference: ".claude/commands/question.md"
         - description: "Build command with subagents"
           code_reference: ".claude/commands/build.md"

   best_practices:
     dos:
       - "Use argument-hint to document expected arguments"
       - "Number workflow steps for clarity"
       - "Specify model when opus/haiku is needed"
     donts:
       - "Don't create commands without allowed-tools"
       - "Avoid hardcoding paths (use variables)"
   ```

4. **Document validation requirements**:

   ```markdown
   ## Validation Requirements

   ### Mandatory Checks

   1. **Valid YAML Syntax**
      ```bash
      # Validation command
      python3 -c "import yaml; yaml.safe_load(open('expertise.yaml'))"
      ```
      - Must parse without errors
      - No duplicate keys
      - Proper indentation (2 spaces)

   2. **Line Limit: Max 1000 Lines**
      ```bash
      # Check line count
      wc -l expertise.yaml
      ```
      - Rationale: Context window protection
      - Enforcement: Self-improve Phase 6
      - If exceeded: Compress, remove low-value details

   3. **Required Top-Level Keys**
      - `overview` (mandatory)
      - `core_implementation` (mandatory)
      - At least ONE of: `key_operations`, `schema_structure`, `data_flow`

   4. **File References Must Exist**
      ```bash
      # Verify all referenced files exist
      grep -oP 'location: "\K[^"]+' expertise.yaml | while read f; do
        test -f "$f" && echo "✓ $f" || echo "✗ MISSING: $f"
      done
      ```

   ### Best Practice Checks

   1. **Line Numbers Are Accurate**
      - Validate line_start < line_end
      - Verify lines exist in referenced files

   2. **Descriptions Are Concise**
      - Avoid line-by-line documentation
      - Focus on "what and why", not "how"

   3. **Recent Updates Tracked**
      - `recent_changes` should have 3-5 latest entries
      - Dates in YYYY-MM-DD format
   ```

5. **Add rationale for 1000-line limit**:

   ```markdown
   ## Why 1000 Lines?

   ### Context Window Economics

   - Claude Sonnet: 200K context window
   - Typical prompt: 5K tokens
   - Expertise file (1000 lines YAML): ~4-6K tokens
   - Leaves: ~190K tokens for codebase exploration

   ### Performance Impact

   | Expertise Size | Context Usage | Remaining for Code |
   |----------------|---------------|-------------------|
   | 500 lines | 2-3K tokens | ~195K tokens | ✅ Ideal |
   | 1000 lines | 4-6K tokens | ~190K tokens | ✅ Good |
   | 2000 lines | 8-12K tokens | ~180K tokens | ⚠️ Acceptable |
   | 5000 lines | 20-30K tokens | ~170K tokens | ❌ Too much |

   ### Compression Strategies

   When approaching limit:
   1. Use YAML (not JSON) - 20-30% smaller
   2. Remove outdated `recent_changes` entries
   3. Consolidate similar patterns
   4. Reference line ranges instead of listing every function
   5. Focus on non-obvious knowledge (skip obvious patterns)
   ```

**Acceptance Criteria:**
- ✅ Complete YAML schema with all 10 sections documented
- ✅ 3 complete examples (CLI, ADW, Commands) totaling 150+ lines each
- ✅ Validation section with 4+ runnable bash commands
- ✅ Line limit rationale with context window calculations table
- ✅ Compression strategies documented with 5+ techniques
- ✅ File is 400-600 lines of structured markdown

**Validation Commands:**
```bash
# Verify file exists
test -f /Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/expertise-file-structure.md && echo "✓ File exists"

# Check line count
wc -l /Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/expertise-file-structure.md

# Verify all YAML examples are valid
grep -Pzo '```yaml\n(.*?\n)*?```' /Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/expertise-file-structure.md | python3 -c "import yaml, sys; [yaml.safe_load(block.split('```yaml\n')[1].split('\n```')[0]) for block in sys.stdin.read().split('```yaml') if block.strip()]"
```

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/expertise-file-structure.md`

---

### [FEATURE] Task 3: Create agent experts directory structure

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_13_Task_3
```

**Description:**
Create base directory structure for storing agent expert definitions in the repository.

**Technical Steps:**
1. Create directory: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/`
2. Create subdirectories for initial experts:
   - `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/cli/`
   - `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/adw/`
   - `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/commands/`
3. Create `.gitkeep` files in each subdirectory to preserve structure

**Acceptance Criteria:**
- Directory structure exists and is committed
- Structure matches TAC-13 patterns
- Ready for expert implementation files

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/cli/.gitkeep`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/adw/.gitkeep`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/commands/.gitkeep`

---

### [FEATURE] Task 4: Create CLI expert - question prompt

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_13_Task_4
```

**Description:**
Create question prompt for CLI expert that reads expertise and answers questions about tac-bootstrap CLI.

**Technical Steps:**

1. **Create prompt file with complete implementation**:

   **File**: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/cli/question.md`

   **Complete Content**:
   ```markdown
   ---
   allowed-tools: Bash, Read, Grep, Glob, TodoWrite
   description: Answer questions about tac-bootstrap CLI without coding
   argument-hint: [question]
   model: sonnet
   ---

   # CLI Expert: Question Mode

   ## Purpose

   Answer questions about the tac-bootstrap CLI by leveraging the CLI expert's mental model (expertise file) and validating assumptions against the actual codebase.

   This is a **read-only** command - no code modifications allowed.

   ## Variables

   - **USER_QUESTION**: `$1` (required) - The question to answer
   - **EXPERTISE_PATH**: `.claude/commands/experts/cli/expertise.yaml` (static)
   - **CLI_ROOT**: `tac_bootstrap_cli/tac_bootstrap/` (static)

   ## Instructions

   You are the CLI Expert. You have a deep mental model of the tac-bootstrap CLI stored in your expertise file. Use this knowledge to answer questions quickly and accurately.

   **Key Principles:**
   1. Start with expertise (mental model)
   2. Validate against actual code (source of truth)
   3. Report with evidence (file references + line numbers)
   4. Never guess - if unsure, read the code

   ## Workflow

   ### Phase 1: Read Expertise File

   1. Read the expertise file to understand your mental model:
      ```bash
      # Read CLI expert's mental model
      cat .claude/commands/experts/cli/expertise.yaml
      ```

   2. Parse the expertise for relevant information:
      - Review `overview` section for high-level context
      - Check `core_implementation` for component details
      - Examine `key_operations` for workflow patterns
      - Note any `known_issues` or `best_practices`

   3. Identify which sections of expertise are relevant to USER_QUESTION

   ### Phase 2: Validate Expertise Against Codebase

   **CRITICAL**: The expertise file is a mental model, NOT source of truth. Always validate assumptions against actual code.

   1. Based on USER_QUESTION and expertise, identify files to read:
      ```bash
      # Example: If question is about template registration
      cat tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
      ```

   2. Cross-reference expertise claims with actual code:
      - Verify function signatures match
      - Confirm line numbers are accurate
      - Check for recent changes not yet in expertise

   3. Use Grep/Glob if searching is needed:
      ```bash
      # Example: Find all template registrations
      grep -n "plan.add_file" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
      ```

   4. Note any discrepancies:
      - Expertise outdated? Document for self-improve
      - Missing information? Note gaps
      - Contradictions? Trust code over expertise

   ### Phase 3: Report Findings

   Provide a comprehensive answer structured as follows:

   #### 1. Direct Answer
   - Answer USER_QUESTION clearly and concisely
   - Lead with the most important information

   #### 2. Evidence from Code
   - Provide file paths and line numbers
   - Include relevant code snippets
   - Format: `file_path:line_start-line_end`

   Example:
   ```
   Template registration happens in ScaffoldService._add_claude_code_commands():
   - Location: scaffold_service.py:150-200
   - Pattern: plan.add_file(action="create", template="path.j2", reason="...")
   ```

   #### 3. Context and Relationships
   - Explain how this fits into the larger system
   - Mention related components or patterns
   - Reference expertise sections if helpful

   #### 4. Examples (if applicable)
   - Provide concrete usage examples
   - Show command-line invocations
   - Include expected outputs

   #### 5. Additional Notes
   - Mention any caveats or edge cases
   - Reference best practices from expertise
   - Note any known issues

   #### 6. Discrepancies (if any)
   - Report any differences between expertise and actual code
   - Format: "Expertise says X, but code shows Y"
   - Recommend running self-improve if significant gaps exist

   ## Report Format

   ```
   ## Answer: [USER_QUESTION]

   ### Direct Answer
   [Clear, concise answer]

   ### Evidence
   - **File**: [path:line_start-line_end]
     ```[language]
     [relevant code snippet]
     ```
   - **File**: [path:line_start-line_end]
     [description]

   ### Context
   [How this fits into the system]

   ### Examples
   ```bash
   [example command or usage]
   ```

   ### Additional Notes
   - [Note 1]
   - [Note 2]

   ### Expertise Status
   ✅ Expertise is accurate
   OR
   ⚠️ Expertise needs update: [describe discrepancy]
   ```

   ## Example Execution

   **Question**: "How does template registration work in scaffold_service?"

   **Expected Report**:
   ```
   ## Answer: How does template registration work in scaffold_service?

   ### Direct Answer
   Template registration in ScaffoldService uses a centralized `plan.add_file()` pattern. All command templates are registered in the `_add_claude_code_commands()` method, which is called during scaffold initialization.

   ### Evidence
   - **File**: scaffold_service.py:150-200
     ```python
     def _add_claude_code_commands(self, plan: ScaffoldPlan) -> None:
         """Register all command templates."""
         plan.add_file(
             action="create",
             template="claude/commands/prime.md.j2",
             path=".claude/commands/prime.md",
             reason="Prime command for context loading"
         )
         # ... more registrations
     ```

   - **File**: scaffold_service.py:220-250
     ```python
     def render_template(self, template_path: str, context: dict) -> str:
         """Render Jinja2 template with config variables."""
         env = Environment(loader=FileSystemLoader(self.templates_dir))
         template = env.get_template(template_path)
         return template.render(**context)
     ```

   ### Context
   The registration pattern follows a two-step process:
   1. **Registration Phase**: `_add_claude_code_commands()` builds a plan of files to create
   2. **Rendering Phase**: `render_template()` processes each .j2 file with config variables

   This separation allows for dry-run mode and better error handling.

   ### Examples
   ```python
   # Register a new template
   plan.add_file(
       action="create",  # or "skip_if_exists" for seed files
       template="claude/commands/my-command.md.j2",
       path=".claude/commands/my-command.md",
       reason="My custom command"
   )
   ```

   ### Additional Notes
   - Use `action="skip_if_exists"` for seed files like expertise.yaml
   - Template variables: `{{ config.project.name }}`, `{{ config.commands.test }}`
   - All templates must be in `tac_bootstrap_cli/tac_bootstrap/templates/`

   ### Expertise Status
   ✅ Expertise is accurate (validated against scaffold_service.py)
   ```

   ## Success Criteria

   Your response is successful if:
   1. ✅ USER_QUESTION is answered completely
   2. ✅ All claims are backed by file references
   3. ✅ Code snippets include file paths and line numbers
   4. ✅ No code modifications were made
   5. ✅ Any expertise discrepancies are reported
   ```

2. **Reference TAC-13 implementation**:
   - Pattern from: `/Volumes/MAc1/Celes/TAC/tac-13/.claude/commands/experts/database/question.md`
   - Adapt for tac-bootstrap CLI domain
   - Keep 3-phase structure: Read → Validate → Report

3. **Ensure read-only behavior**:
   - Only allowed-tools: Bash, Read, Grep, Glob, TodoWrite
   - No Edit, Write, or code modification tools
   - Bash only for validation commands (grep, cat, wc)

**Acceptance Criteria:**
- ✅ Prompt file is 150-200 lines of markdown
- ✅ YAML frontmatter includes exactly: allowed-tools, description, argument-hint, model
- ✅ Workflow has 3 phases with numbered steps
- ✅ Report format is clearly defined with example
- ✅ File references format is specified: `path:line_start-line_end`
- ✅ Read-only behavior is enforced (no Edit/Write tools)
- ✅ Example execution shows complete workflow

**Validation Commands:**
```bash
# Verify file exists
test -f /Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/cli/question.md && echo "✓ File exists"

# Check frontmatter is valid YAML
head -10 /Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/cli/question.md | python3 -c "import yaml, sys; yaml.safe_load(sys.stdin)"

# Verify only read-only tools are allowed
grep "allowed-tools:" /Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/cli/question.md | grep -v "Edit\|Write" && echo "✓ Read-only"

# Check line count (should be 150-200)
wc -l /Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/cli/question.md
```

**Test Command:**
```bash
# Test the command after creation
cd /Users/hernandoescobar/Documents/Celes/tac_bootstrap
/experts:cli:question "How does template registration work?"
```

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/cli/question.md`

---

### [FEATURE] Task 5: Create CLI expert - self-improve prompt

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_13_Task_5
```

**Description:**
Create self-improve prompt for CLI expert that validates and updates expertise file using the 7-phase TAC-13 pattern.

**Technical Steps:**

1. **Create self-improve prompt with complete 7-phase implementation**:

   **File**: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/cli/self-improve.md`

   **Complete Content**:
   ```markdown
   ---
   allowed-tools: Read, Grep, Glob, Bash, Edit, Write, TodoWrite
   description: Self-improve CLI expertise by validating against codebase
   argument-hint: [check_git_diff] [focus_area]
   model: sonnet
   ---

   # CLI Expert: Self-Improve Mode

   ## Purpose

   Maintain and update the CLI expert's mental model (expertise.yaml) by validating it against the actual codebase and incorporating new knowledge.

   This is the **Learn** step in the Act → Learn → Reuse loop.

   ## Variables

   - **CHECK_GIT_DIFF**: `$1` (default: `false`) - If `true`, focus on recently changed files
   - **FOCUS_AREA**: `$2` (default: empty) - Optional area to focus on (e.g., "templates", "scaffold_service", "cli_commands")
   - **EXPERTISE_FILE**: `.claude/commands/experts/cli/expertise.yaml` (static)
   - **CLI_ROOT**: `tac_bootstrap_cli/tac_bootstrap/` (static)
   - **MAX_LINES**: `1000` (static)

   ## Instructions

   You are the CLI Expert updating your mental model. Follow the 7-phase workflow strictly:

   1. **Check git diff** (if requested)
   2. **Read current expertise**
   3. **Validate against codebase**
   4. **Identify discrepancies**
   5. **Update expertise**
   6. **Enforce line limit**
   7. **Validate YAML syntax**

   **Key Principles:**
   - Expertise is a mental model, NOT source of truth
   - Focus on patterns and high-value knowledge
   - Keep under 1000 lines (compress if needed)
   - Always validate YAML syntax before finishing

   ## Workflow

   ### Phase 1: Check Git Diff (Conditional)

   **Execute only if CHECK_GIT_DIFF is `true`**

   1. Run git diff to see recent changes:
      ```bash
      # Check unstaged changes
      git diff HEAD -- tac_bootstrap_cli/

      # Check staged changes
      git diff --cached -- tac_bootstrap_cli/

      # Check last commit
      git log -1 --stat --oneline -- tac_bootstrap_cli/
      ```

   2. Identify changed files in CLI domain:
      ```bash
      # List changed files
      git diff --name-only HEAD -- tac_bootstrap_cli/
      ```

   3. Note focus areas based on changes:
      - If `scaffold_service.py` changed → focus on template registration
      - If `cli.py` changed → focus on CLI commands
      - If `templates/` changed → focus on template patterns
      - If `domain/` changed → focus on data models

   4. Update FOCUS_AREA internally based on findings

   **If CHECK_GIT_DIFF is `false`**: Skip to Phase 2

   ### Phase 2: Read Current Expertise

   1. Read the existing expertise file:
      ```bash
      cat .claude/commands/experts/cli/expertise.yaml
      ```

   2. Parse the structure:
      - Note `last_updated` date
      - Review all `core_implementation` components
      - Check `key_operations` workflows
      - Review `recent_changes` entries

   3. Identify sections to validate:
      - If FOCUS_AREA is set: prioritize that section
      - Otherwise: validate all sections systematically

   4. Track current line count:
      ```bash
      wc -l .claude/commands/experts/cli/expertise.yaml
      ```

   ### Phase 3: Validate Expertise Against Codebase

   **Systematic validation of expertise claims**

   1. **Validate Overview Section**:
      ```bash
      # Check if key_files exist and are current
      for file in $(grep -A 10 "key_files:" .claude/commands/experts/cli/expertise.yaml | grep "- " | sed 's/.*- "\(.*\)"/\1/'); do
          test -f "$file" && echo "✓ $file" || echo "✗ MISSING: $file"
      done
      ```

   2. **Validate Core Implementation**:
      ```bash
      # For each component in core_implementation
      # Example: Validate scaffold_service component

      # Read the actual file
      cat tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py

      # Check if documented classes exist
      grep -n "class ScaffoldService" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py

      # Verify method signatures
      grep -n "def _add_claude_code_commands" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py

      # Check line numbers are accurate
      sed -n '150,200p' tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
      ```

   3. **Validate Key Operations**:
      ```bash
      # Verify workflow patterns described in expertise
      # Example: Template registration workflow

      # Find actual registration calls
      grep -n "plan.add_file" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py

      # Verify pattern matches expertise description
      grep -A 3 "plan.add_file" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
      ```

   4. **Discover New Information**:
      ```bash
      # Find files not yet documented
      find tac_bootstrap_cli/tac_bootstrap -name "*.py" | grep -v __pycache__

      # Check for new important functions
      grep -rn "^def " tac_bootstrap_cli/tac_bootstrap/application/
      grep -rn "^class " tac_bootstrap_cli/tac_bootstrap/domain/
      ```

   5. **Check for Architectural Changes**:
      - New modules or packages?
      - Moved files?
      - Refactored functions?
      - New patterns introduced?

   ### Phase 4: Identify Discrepancies

   **Document ALL differences between expertise and reality**

   Create a discrepancies report:

   ```markdown
   ## Discrepancies Found

   ### Outdated Information
   - [ ] Expertise says: "X is at line 100"
         Reality: X is at line 120 (moved due to new imports)

   - [ ] Expertise documents: method_old()
         Reality: method_old() was renamed to method_new()

   ### Missing Information
   - [ ] New file added: `templates/claude/commands/new-command.md.j2`
         Not documented in expertise

   - [ ] New method in ScaffoldService: `_add_tac_13_templates()`
         Should be documented in key_operations

   ### Incorrect Information
   - [ ] Expertise: "Template registration uses pattern X"
         Reality: Pattern changed to Y in recent refactor

   ### Gaps in Coverage
   - [ ] No documentation for: `infrastructure/filesystem.py`
   - [ ] Missing workflow: "How entity generation works"
   ```

   ### Phase 5: Update Expertise File

   **Apply updates based on discrepancies**

   1. **Update Overview** (if needed):
      ```yaml
      overview:
        description: "Updated description if system changed"
        key_files:
          - "add new important files"
          - "remove obsolete files"
        last_updated: "2026-02-03"  # Always update date
      ```

   2. **Update Core Implementation**:
      ```yaml
      core_implementation:
        scaffold_service:
          location: "tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py"
          key_methods:
            - name: "_add_claude_code_commands"
              line_start: 150  # Update if moved
              line_end: 200
              signature: "def _add_claude_code_commands(self, plan: ScaffoldPlan) -> None"
              logic: "Registers all command templates using plan.add_file() pattern"
            - name: "_add_tac_13_templates"  # NEW method found
              line_start: 205
              line_end: 230
              signature: "def _add_tac_13_templates(self, plan: ScaffoldPlan) -> None"
              logic: "Registers TAC-13 agent expert templates"
      ```

   3. **Update Key Operations**:
      ```yaml
      key_operations:
        template_registration:
          workflow: |
            1. ScaffoldService.__init__ loads config
            2. _add_claude_code_commands() registers base templates
            3. _add_tac_13_templates() registers expert templates  # UPDATED
            4. Each template: action, template path, reason
            5. render_template() processes .j2 files
      ```

   4. **Add Recent Changes**:
      ```yaml
      recent_changes:
        - date: "2026-02-03"
          description: "Added TAC-13 agent expert templates"
          files: ["scaffold_service.py", "templates/claude/commands/experts/"]
        - date: "2026-02-01"
          description: "Refactored template registration pattern"
          files: ["scaffold_service.py"]
        # Keep only 5 most recent entries
      ```

   5. **Use Edit tool for updates**:
      ```bash
      # Update specific sections using Edit tool
      # Example: Update line numbers for a method
      ```

   6. **Or use Write tool for major changes**:
      ```bash
      # If expertise needs significant restructuring, rewrite entire file
      ```

   ### Phase 6: Enforce Line Limit

   **Ensure expertise stays under 1000 lines**

   1. Check current line count:
      ```bash
      wc -l .claude/commands/experts/cli/expertise.yaml
      ```

   2. **If under 1000 lines**: Proceed to Phase 7

   3. **If over 1000 lines**: Compress using these strategies:

      **Strategy 1: Remove Old Recent Changes**
      ```yaml
      recent_changes:
        # Keep only 3-5 most recent, remove older ones
        - date: "2026-02-03"
          description: "Latest change"
      ```

      **Strategy 2: Consolidate Similar Patterns**
      ```yaml
      # Before (verbose):
      key_methods:
        - name: "method_a"
          line_start: 10
          logic: "Does X"
        - name: "method_b"
          line_start: 20
          logic: "Does X"

      # After (consolidated):
      key_methods:
        - pattern: "X-type methods"
          instances: ["method_a:10", "method_b:20"]
          logic: "Does X"
      ```

      **Strategy 3: Use Line Ranges Instead of Details**
      ```yaml
      # Before:
      key_methods:
        - name: "method_1"
          line_start: 10
          line_end: 20
        - name: "method_2"
          line_start: 25
          line_end: 35

      # After:
      key_methods_range:
        lines: "10-35"
        count: 2
        purpose: "Helper methods for X"
      ```

      **Strategy 4: Remove Obvious Information**
      ```yaml
      # Remove patterns that are self-evident from code
      # Keep only non-obvious knowledge and relationships
      ```

   4. After compression, verify:
      ```bash
      wc -l .claude/commands/experts/cli/expertise.yaml
      # Must be <= 1000
      ```

   ### Phase 7: Validate YAML Syntax

   **Final validation before finishing**

   1. Validate YAML syntax:
      ```bash
      python3 -c "import yaml; yaml.safe_load(open('.claude/commands/experts/cli/expertise.yaml'))"
      ```

   2. **If validation passes**:
      ```
      ✓ YAML syntax is valid
      ```

   3. **If validation fails**:
      - Read error message
      - Fix syntax errors (indentation, quotes, colons)
      - Re-run validation
      - Repeat until valid

   4. Verify structure:
      ```bash
      # Check required top-level keys exist
      grep -E "^(overview|core_implementation|key_operations):" .claude/commands/experts/cli/expertise.yaml
      ```

   5. Final checks:
      ```bash
      # Line count
      lines=$(wc -l < .claude/commands/experts/cli/expertise.yaml)
      echo "✓ Line count: $lines / 1000"

      # YAML valid
      python3 -c "import yaml; yaml.safe_load(open('.claude/commands/experts/cli/expertise.yaml'))" && echo "✓ Valid YAML"

      # Required keys present
      grep -q "^overview:" .claude/commands/experts/cli/expertise.yaml && echo "✓ Has overview"
      grep -q "^core_implementation:" .claude/commands/experts/cli/expertise.yaml && echo "✓ Has core_implementation"
      ```

   ## Report Format

   Provide a detailed report of the self-improve run:

   ```markdown
   # CLI Expert Self-Improve Report

   ## Execution Summary
   - **Date**: 2026-02-03
   - **Check Git Diff**: [true/false]
   - **Focus Area**: [area or "full validation"]
   - **Duration**: [X] phases completed

   ## Phase 1: Git Diff Analysis
   [If CHECK_GIT_DIFF was true]
   - Changed files: [list]
   - Focus areas identified: [areas]

   ## Phase 2: Current Expertise Review
   - Last updated: [date from expertise]
   - Line count: [X] / 1000
   - Sections reviewed: [list]

   ## Phase 3: Validation Results
   - Files validated: [count]
   - Methods verified: [count]
   - Patterns checked: [count]

   ## Phase 4: Discrepancies Found
   ### Outdated Information
   - [Item 1]
   - [Item 2]

   ### Missing Information
   - [Item 1]
   - [Item 2]

   ### Incorrect Information
   - [Item 1]

   ## Phase 5: Updates Applied
   - Overview: [updated/unchanged]
   - Core Implementation: [X updates]
   - Key Operations: [X updates]
   - Recent Changes: [added entry]

   Specific updates:
   1. [Update description]
   2. [Update description]

   ## Phase 6: Line Limit Enforcement
   - Before: [X] lines
   - After: [Y] lines
   - Status: ✅ Under 1000 / ⚠️ Compressed to fit

   Compression applied:
   - [Strategy used if compressed]

   ## Phase 7: Validation
   - YAML syntax: ✅ Valid
   - Required keys: ✅ Present
   - Line count: ✅ [Y] / 1000

   ## Recommendations
   - [Any recommendations for manual review]
   - [Suggestions for next self-improve run]

   ## Next Steps
   - Run `/experts:cli:question` to verify updated expertise
   - Consider self-improve again after next major CLI changes
   ```

   ## Success Criteria

   Self-improve is successful if:
   1. ✅ All 7 phases completed
   2. ✅ Expertise is valid YAML
   3. ✅ Line count ≤ 1000
   4. ✅ All discrepancies documented and addressed
   5. ✅ `last_updated` field updated to current date
   6. ✅ Report is comprehensive and actionable
   ```

2. **Reference TAC-13 implementation**:
   - Pattern from: `/Volumes/MAc1/Celes/TAC/tac-13/.claude/commands/experts/database/self-improve.md`
   - Adapt 7-phase workflow for CLI domain
   - Include compression strategies from TAC-13 video (Tac-13_2.md)

3. **Include validation commands throughout**:
   - Each phase has concrete bash commands
   - YAML validation in Phase 7
   - Line count checks in Phase 6

**Acceptance Criteria:**
- ✅ Prompt file is 300-400 lines of markdown
- ✅ All 7 phases are detailed with numbered steps
- ✅ Each phase includes bash command examples
- ✅ Compression strategies documented with 4+ techniques
- ✅ YAML validation command is explicit
- ✅ Report format includes all 7 phase summaries
- ✅ Variables use defaults correctly (CHECK_GIT_DIFF defaults to false)

**Validation Commands:**
```bash
# Verify file exists
test -f /Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/cli/self-improve.md && echo "✓ File exists"

# Check frontmatter
head -10 /Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/cli/self-improve.md | python3 -c "import yaml, sys; yaml.safe_load(sys.stdin)"

# Verify all 7 phases are present
grep -c "### Phase [1-7]:" /Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/cli/self-improve.md
# Should output: 7

# Check Edit and Write tools are allowed
grep "allowed-tools:" /Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/cli/self-improve.md | grep -E "Edit.*Write" && echo "✓ Can modify files"

# Check line count
wc -l /Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/cli/self-improve.md
```

**Test Command:**
```bash
# Test self-improve after creation
cd /Users/hernandoescobar/Documents/Celes/tac_bootstrap
/experts:cli:self-improve false "scaffold_service"
```

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/cli/self-improve.md`

---

### [FEATURE] Task 6: Create CLI expert - initial expertise file

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_13_Task_6
```

**Description:**
Create initial expertise.yaml file for CLI expert by running self-improve from blank state.

**Technical Steps:**
1. Create empty `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/cli/expertise.yaml`
2. Execute self-improve prompt to populate expertise
3. Expert should document:
   - CLI structure: `tac_bootstrap_cli/tac_bootstrap/`
   - Domain models: `domain/` (Config, Project, CommandConfig)
   - Application services: `application/scaffold_service.py`
   - Infrastructure: `infrastructure/` (template rendering, filesystem)
   - Interfaces: `interfaces/cli.py` (Typer commands)
   - Templates: `templates/` organization
4. Include key operations with file paths and line numbers
5. Document template registration pattern in scaffold_service.py

**Acceptance Criteria:**
- Expertise file is valid YAML
- Under 1000 lines
- Documents CLI architecture accurately
- References correct file paths and line numbers
- Follows expertise-file-structure.md schema

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/cli/expertise.yaml`

---

### [FEATURE] Task 7: Create ADW expert - question prompt

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_13_Task_7
```

**Description:**
Create question prompt for ADW expert that answers questions about AI Developer Workflows.

**Technical Steps:**
1. Create `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/adw/question.md`
2. Define YAML frontmatter:
   ```yaml
   allowed-tools: Bash, Read, Grep, Glob, TodoWrite
   description: Answer questions about ADW workflows without coding
   argument-hint: [question]
   ```
3. Implement 3-phase workflow (read expertise → validate → report)
4. Use variables: `USER_QUESTION: $1`, `EXPERTISE_PATH: .claude/commands/experts/adw/expertise.yaml`

**Acceptance Criteria:**
- Follows TAC-13 question pattern
- Validates expertise against ADW implementations
- Reports on workflow patterns and integration

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/adw/question.md`

---

### [FEATURE] Task 8: Create ADW expert - self-improve prompt

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_13_Task_8
```

**Description:**
Create self-improve prompt for ADW expert.

**Technical Steps:**
1. Create `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/adw/self-improve.md`
2. Define YAML frontmatter (same pattern as CLI expert)
3. Implement 7-phase workflow
4. Variables: `CHECK_GIT_DIFF: $1`, `FOCUS_AREA: $2`, `EXPERTISE_FILE: .claude/commands/experts/adw/expertise.yaml`, `MAX_LINES: 1000`

**Acceptance Criteria:**
- Follows TAC-13 7-phase pattern
- Enforces constraints
- Focus areas: state management, GitHub integration, workflow orchestration

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/adw/self-improve.md`

---

### [FEATURE] Task 9: Create ADW expert - initial expertise file

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_13_Task_9
```

**Description:**
Create initial expertise.yaml file for ADW expert.

**Technical Steps:**
1. Create empty `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/adw/expertise.yaml`
2. Execute self-improve to populate
3. Expert should document:
   - ADW workflows: `adws/adw_*_iso.py` patterns
   - Modules: `adws/adw_modules/` (state, workflow_ops, git_ops, github, agent)
   - State management: ADWState class and persistence
   - GitHub integration: issue fetching, PR creation, comments
   - Orchestration: plan → build → test → review → document → ship
   - TAC-9 (ai_docs), TAC-10 (build_w_report), TAC-12 (scout, parallel)
4. Include key functions with file paths and signatures

**Acceptance Criteria:**
- Valid YAML under 1000 lines
- Documents all ADW patterns
- References TAC-9, TAC-10, TAC-12 integrations
- Accurate file paths and line numbers

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/adw/expertise.yaml`

---

### [FEATURE] Task 10: Create Commands expert - question prompt

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_13_Task_10
```

**Description:**
Create question prompt for Commands expert that answers questions about slash commands.

**Technical Steps:**
1. Create `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/commands/question.md`
2. Define YAML frontmatter (same pattern as other experts)
3. Implement 3-phase workflow
4. Use variables: `USER_QUESTION: $1`, `EXPERTISE_PATH: .claude/commands/experts/commands/expertise.yaml`

**Acceptance Criteria:**
- Follows TAC-13 question pattern
- Answers questions about command structure, variables, workflows

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/commands/question.md`

---

### [FEATURE] Task 11: Create Commands expert - self-improve prompt

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_13_Task_11
```

**Description:**
Create self-improve prompt for Commands expert.

**Technical Steps:**
1. Create `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/commands/self-improve.md`
2. Define YAML frontmatter (same pattern)
3. Implement 7-phase workflow
4. Variables: `CHECK_GIT_DIFF: $1`, `FOCUS_AREA: $2`, `EXPERTISE_FILE: .claude/commands/experts/commands/expertise.yaml`, `MAX_LINES: 1000`

**Acceptance Criteria:**
- Follows TAC-13 7-phase pattern
- Focus areas: command syntax, variable injection, workflow patterns

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/commands/self-improve.md`

---

### [FEATURE] Task 12: Create Commands expert - initial expertise file

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_13_Task_12
```

**Description:**
Create initial expertise.yaml file for Commands expert.

**Technical Steps:**
1. Create empty `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/commands/expertise.yaml`
2. Execute self-improve to populate
3. Expert should document:
   - Command structure: YAML frontmatter + Markdown body
   - Variables: dynamic (`$1`, `$2`) vs static
   - Allowed-tools: tool specifications
   - Workflow sections: numbered steps
   - Report sections: output format specifications
   - Examples section: 2-4 concrete use cases
4. Document 25+ existing commands in `.claude/commands/`

**Acceptance Criteria:**
- Valid YAML under 1000 lines
- Documents command syntax patterns
- References existing commands with examples
- Explains variable injection patterns

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/commands/expertise.yaml`

---

### [FEATURE] Task 13: Create meta-prompt generator command

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_13_Task_13
```

**Description:**
Create meta-prompt command that generates new slash commands from user descriptions. This is "prompts that create prompts" - the foundation of meta-agentics.

**Technical Steps:**

1. **Create meta-prompt generator with complete implementation**:

   **File**: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/meta-prompt.md`

   **Complete Content**:
   ```markdown
   ---
   allowed-tools: Write, Read, Glob, Grep, TodoWrite
   description: Generate a new slash command from user description
   argument-hint: [command_description]
   model: opus
   ---

   # Meta-Prompt: Slash Command Generator

   ## Purpose

   Generate a complete, production-ready slash command (.md file) from a natural language description.

   This is a **meta-prompt** - a prompt that creates other prompts.

   ## Variables

   - **USER_PROMPT_REQUEST**: `$ARGUMENTS` (required) - Description of desired command
   - **OUTPUT_DIR**: `.claude/commands/` (static)
   - **COMMAND_NAME**: (derived from request)

   ## Instructions

   You are a meta-prompt generator. Your job is to create slash commands that follow tac_bootstrap standards exactly.

   **Key Principles:**
   1. Study existing commands to understand patterns
   2. Generate commands that are immediately usable
   3. Follow exact structure: YAML frontmatter + Purpose + Variables + Instructions + Workflow + Report
   4. Choose appropriate tools based on command purpose
   5. Never create commands that duplicate existing ones

   ## Workflow

   ### Phase 1: Analyze User Request

   1. Parse USER_PROMPT_REQUEST to understand intent:
      - What is the command supposed to do?
      - Is it read-only or does it modify code?
      - Does it spawn subagents?
      - What domain does it operate in?

   2. Study existing commands for patterns:
      ```bash
      # List all existing commands
      ls -1 .claude/commands/*.md | grep -v "experts/"

      # Read similar commands
      # If request is about "testing" → read test.md, test_e2e.md
      # If request is about "building" → read build.md, build_w_report.md
      # If request is about "questions" → read question.md
      ```

   3. Extract key requirements:
      - **Input**: What arguments does it need?
      - **Output**: What should it produce?
      - **Constraints**: Read-only? Requires validation?
      - **Complexity**: Simple single-agent or orchestration?

   ### Phase 2: Determine Command Structure

   1. **Choose Command Name**:
      - Use kebab-case: `my-command`
      - Be descriptive but concise
      - Check for conflicts:
        ```bash
        test -f .claude/commands/<proposed-name>.md && echo "⚠️ Already exists"
        ```

   2. **Select Allowed Tools**:

      **Read-Only Commands**:
      - Tools: `Bash, Read, Grep, Glob, TodoWrite`
      - Examples: question, prime, find_and_summarize

      **Code Modification Commands**:
      - Tools: `Read, Grep, Glob, Edit, Write, Bash, TodoWrite`
      - Examples: patch, bug, feature

      **Orchestration Commands**:
      - Tools: `Task, Read, Write, Grep, Glob, TodoWrite`
      - Examples: build, scout_plan_build, parallel_subagents

      **Validation Commands**:
      - Tools: `Bash, Read, Grep, Glob, TodoWrite`
      - Examples: test, lint, github_check

   3. **Choose Model**:
      - `sonnet`: Default (most commands)
      - `opus`: Complex planning, orchestration, meta-agentics
      - `haiku`: Simple read-only, quick tasks

   4. **Define Arguments**:
      - Positional: `$1, $2, $3`
      - All args: `$ARGUMENTS`
      - Format: `[required_arg] [optional_arg]`

   ### Phase 3: Generate Command File

   **Template Structure**:

   ```markdown
   ---
   allowed-tools: [Tool1, Tool2, ...]
   description: [One-line description - be specific]
   argument-hint: [arg1] [arg2]
   model: [sonnet|opus|haiku]
   ---

   # [Command Name]

   ## Purpose

   [2-3 sentence description of what this command does and why it exists]

   [If command has specific use cases, list them]

   ## Variables

   - **VARIABLE_NAME**: `$1` (required/optional) - Description with default if applicable
   - **ANOTHER_VAR**: `$2` (default: `value`) - Description
   - **STATIC_VAR**: `fixed/path` (static) - Description

   ## Instructions

   [High-level instructions for the agent executing this command]

   **Key Principles:**
   1. [Principle 1]
   2. [Principle 2]
   3. [Principle 3]

   [Any important context the agent needs]

   ## Workflow

   ### Step 1: [First Step Name]

   [Detailed description of what to do]

   1. [Sub-step 1]
      ```bash
      # Example command
      ```

   2. [Sub-step 2]

   3. [Sub-step 3]

   ### Step 2: [Second Step Name]

   [Continue with all necessary steps...]

   ### Step N: [Final Step Name]

   [Completion actions]

   ## Report Format

   [Define the expected output format]

   ```
   # [Command Name] Report

   ## [Section 1]
   [Expected content]

   ## [Section 2]
   [Expected content]
   ```

   ## Success Criteria

   [List of checkboxes for success]

   1. ✅ [Criterion 1]
   2. ✅ [Criterion 2]
   3. ✅ [Criterion 3]
   ```

   **Example Generation**:

   If USER_PROMPT_REQUEST is: "Create a command that finds TODOs in code and summarizes them"

   Generate:
   ```markdown
   ---
   allowed-tools: Bash, Read, Grep, Glob, TodoWrite
   description: Find and summarize TODO comments in codebase
   argument-hint: [directory]
   model: sonnet
   ---

   # Find TODOs

   ## Purpose

   Scan the codebase for TODO, FIXME, and HACK comments, then provide a prioritized summary with file locations and context.

   Useful for:
   - Pre-release audits
   - Sprint planning
   - Technical debt tracking

   ## Variables

   - **DIRECTORY**: `$1` (default: `.`) - Directory to scan
   - **OUTPUT_FILE**: `agents/todo_summary.md` (static)

   ## Instructions

   You are a TODO detective. Find all TODO/FIXME/HACK comments, understand their context, and provide actionable recommendations.

   **Key Principles:**
   1. Search recursively, respect .gitignore
   2. Include surrounding code for context
   3. Categorize by urgency and type
   4. Never modify code (read-only)

   ## Workflow

   ### Step 1: Scan for TODOs

   1. Find all TODO comments:
      ```bash
      grep -rn "TODO:\|FIXME:\|HACK:" "$DIRECTORY" \
        --include="*.py" --include="*.js" --include="*.ts" \
        | grep -v node_modules | grep -v .git
      ```

   2. Count findings:
      ```bash
      total=$(grep -rc "TODO:\|FIXME:\|HACK:" "$DIRECTORY" | awk -F: '{sum+=$2} END {print sum}')
      echo "Found $total TODOs"
      ```

   ### Step 2: Analyze Context

   1. For each TODO found:
      - Read surrounding 5 lines for context
      - Identify component/module
      - Assess urgency based on keywords

   2. Categorize:
      - **Critical**: Security, data loss, blocking
      - **High**: Performance, user experience
      - **Medium**: Refactoring, optimization
      - **Low**: Nice-to-have, documentation

   ### Step 3: Generate Summary Report

   Write to OUTPUT_FILE with structure below.

   ## Report Format

   ```markdown
   # TODO Summary Report

   **Date**: [current date]
   **Scanned**: [directory]
   **Total Found**: [count]

   ## Critical Priority (Security/Blocking)
   - [ ] **File**: path/to/file.py:45
     **TODO**: Fix SQL injection vulnerability
     **Context**: User input not sanitized
     **Recommendation**: Use parameterized queries

   ## High Priority (Performance/UX)
   [...]

   ## Medium Priority (Refactoring)
   [...]

   ## Low Priority (Documentation)
   [...]

   ## Statistics
   - Critical: X
   - High: Y
   - Medium: Z
   - Low: W
   ```

   ## Success Criteria

   1. ✅ All TODOs found and categorized
   2. ✅ Context provided for each item
   3. ✅ Priorities assigned correctly
   4. ✅ Report written to agents/todo_summary.md
   5. ✅ No code modifications made
   ```

   ### Phase 4: Validate Generated Command

   1. **Check File Structure**:
      - ✅ YAML frontmatter is valid
      - ✅ All required sections present
      - ✅ Workflow steps are numbered
      - ✅ Report format is defined

   2. **Verify Tool Selection**:
      - Tools match command purpose
      - No Write/Edit in read-only commands
      - Task tool for orchestration

   3. **Test Argument Parsing**:
      - Variables are documented
      - Defaults are specified
      - Argument-hint matches variables

   4. **Quality Checks**:
      - Description is specific (not generic)
      - Examples include actual bash commands
      - Success criteria are measurable

   ### Phase 5: Write Command File

   1. Determine final filename:
      ```bash
      COMMAND_FILE=".claude/commands/${COMMAND_NAME}.md"
      ```

   2. Write the generated command:
      ```bash
      # Use Write tool to create the file
      ```

   3. Validate syntax:
      ```bash
      # Check YAML frontmatter
      head -10 "$COMMAND_FILE" | python3 -c "import yaml, sys; yaml.safe_load(sys.stdin)"
      ```

   4. Report creation:
      ```
      ✅ Created: .claude/commands/${COMMAND_NAME}.md
      ```

   ## Report Format

   ```markdown
   # Meta-Prompt Generation Report

   ## User Request
   "[USER_PROMPT_REQUEST]"

   ## Analysis
   - **Command Type**: [read-only/modification/orchestration]
   - **Complexity**: [simple/moderate/complex]
   - **Domain**: [testing/building/analyzing/...]

   ## Generated Command
   - **Name**: [command-name]
   - **File**: .claude/commands/[command-name].md
   - **Model**: [sonnet/opus/haiku]
   - **Tools**: [list]

   ## Structure
   - ✅ YAML frontmatter
   - ✅ Purpose section
   - ✅ Variables section (X variables)
   - ✅ Instructions section
   - ✅ Workflow section (X steps)
   - ✅ Report format
   - ✅ Success criteria

   ## Validation
   - ✅ YAML syntax valid
   - ✅ Tools appropriate for purpose
   - ✅ Arguments documented
   - ✅ Workflow has examples
   - ✅ Report format is clear

   ## Usage
   \`\`\`bash
   # Execute the new command
   /[command-name] [arguments]
   \`\`\`

   ## Next Steps
   - Test the command with sample inputs
   - Consider adding to README documentation
   - Create corresponding Jinja2 template if for tac-bootstrap generator
   ```

   ## Success Criteria

   1. ✅ Command file created in .claude/commands/
   2. ✅ YAML frontmatter is valid
   3. ✅ All required sections present (6 sections)
   4. ✅ Workflow has numbered steps with examples
   5. ✅ Tools match command purpose
   6. ✅ File is immediately usable as slash command
   7. ✅ Report documents generation process
   ```

2. **Reference TAC-13 meta-prompt implementation**:
   - Pattern from: `/Volumes/MAc1/Celes/TAC/tac-13/.claude/commands/meta_prompt.md`
   - Study existing tac_bootstrap commands as templates
   - Ensure generated commands match established patterns

3. **Include command pattern examples**:
   - Read-only: question.md, scout.md
   - Modification: patch.md, feature.md
   - Orchestration: build.md, scout_plan_build.md

**Acceptance Criteria:**
- ✅ Meta-prompt file is 250-350 lines of markdown
- ✅ Generates commands with exact tac_bootstrap structure
- ✅ Includes complete example generation (TODO finder)
- ✅ Tool selection logic is documented with examples
- ✅ Validation phase checks YAML syntax
- ✅ Output is immediately usable without manual editing
- ✅ Report documents generation rationale

**Validation Commands:**
```bash
# Verify meta-prompt exists
test -f /Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/meta-prompt.md && echo "✓ File exists"

# Check frontmatter
head -10 /Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/meta-prompt.md | python3 -c "import yaml, sys; yaml.safe_load(sys.stdin)"

# Verify model is opus (for complex generation)
grep "^model: opus" /Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/meta-prompt.md && echo "✓ Uses opus"

# Check line count
wc -l /Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/meta-prompt.md
```

**Test Command:**
```bash
# Test meta-prompt generation
cd /Users/hernandoescobar/Documents/Celes/tac_bootstrap
/meta-prompt "Create a command that finds unused imports in Python files"

# Verify generated command
test -f .claude/commands/find-unused-imports.md && echo "✓ Command generated"
```

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/meta-prompt.md`

---

### [FEATURE] Task 14: Create meta-agent generator command

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_13_Task_14
```

**Description:**
Create meta-agent command that generates new agent definitions from user descriptions.

**Technical Steps:**
1. Create `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/meta-agent.md`
2. Define YAML frontmatter:
   ```yaml
   allowed-tools: Write, Edit, Read, Glob
   description: Generate a new agent definition from user description
   argument-hint: [agent_description]
   model: opus
   ```
3. Implement workflow:
   - Phase 1: Analyze user's agent description
   - Phase 2: Determine tools, model, personality
   - Phase 3: Generate agent following standard template
   - Phase 4: Write to `.claude/agents/<name>.md`
4. Enforce exact format:
   - YAML frontmatter (name, description, tools, model, color)
   - Purpose section
   - Instructions section
   - Workflow section
   - Report section
5. Variables: `AGENT_DESCRIPTION: $ARGUMENTS`, `AGENT_OUTPUT_PATH: .claude/agents/<name>.md`

**Acceptance Criteria:**
- Generates valid agent files
- Output is immediately usable
- Includes personality and behavior patterns
- Follows agent definition schema

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/meta-agent.md`

---

### [FEATURE] Task 15: Create meta-skill documentation

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_13_Task_15
```

**Description:**
Document meta-skill pattern and progressive disclosure approach for skills.

**Technical Steps:**
1. Create `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/meta-skill-pattern.md`
2. Document 3-level progressive disclosure:
   - Level 1: Metadata (name, description) - always loaded
   - Level 2: Instructions (SKILL.md main body) - loaded when triggered
   - Level 3: Resources (linked files) - loaded as needed
3. Document skill structure:
   - YAML frontmatter (name, description)
   - Purpose section
   - When to Use section
   - Instructions section
   - Linked resources (reference files, scripts)
4. Include examples: processing-pdfs, start-orchestrator
5. Document discovery pattern (project vs personal skills)
6. Best practices: keep SKILL.md under 500 lines, use gerund naming

**Acceptance Criteria:**
- Explains progressive disclosure clearly
- Includes concrete examples
- Provides creation workflow
- Documents discovery mechanism

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/ai_docs/doc/meta-skill-pattern.md`

---

### [FEATURE] Task 16: Create agent expert orchestrator command

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_13_Task_16
```

**Description:**
Create command that orchestrates agent experts in plan → build → improve workflow.

**Technical Steps:**
1. Create `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/expert-orchestrate.md`
2. Define YAML frontmatter:
   ```yaml
   allowed-tools: Task, Read, Write
   description: Orchestrate agent expert through plan-build-improve workflow
   argument-hint: [expert_domain] [task_description]
   model: opus
   ```
3. Implement 3-step orchestration:
   - Step 1: Create Plan (spawn subagent with `/experts:[domain]:plan [task]`)
   - Step 2: Build (spawn subagent with `/build [path_to_plan]`)
   - Step 3: Self-Improve (spawn subagent with `/experts:[domain]:self-improve true`)
4. Compile report from all 3 steps
5. Variables: `EXPERT_DOMAIN: $1`, `TASK_DESCRIPTION: $2`

**Acceptance Criteria:**
- Spawns 3 subagents in sequence
- Each step gets complete instructions
- Final report synthesizes all outputs
- Follows TAC-13 plan-build-improve pattern

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/expert-orchestrate.md`

---

### [FEATURE] Task 17: Create parallel expert scaling command

**Workflow Metadata:**
```
/feature
/adw_sdlc_zte_iso
/adw_id: feature_Tac_13_Task_17
```

**Description:**
Create command that scales agent experts in parallel (3, 5, 10+ instances).

**Technical Steps:**
1. Create `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/expert-parallel.md`
2. Define YAML frontmatter:
   ```yaml
   allowed-tools: Task, Read, Write
   description: Scale agent experts in parallel for high-confidence results
   argument-hint: [expert_domain] [task] [num_agents]
   model: opus
   ```
3. Implement workflow:
   - Phase 1: Validate num_agents (3-10 range)
   - Phase 2: Spawn N parallel agents with same task
   - Phase 3: Monitor execution
   - Phase 4: Synthesize results (aggregate common themes, identify conflicts, prioritize consensus)
4. Variables: `EXPERT_DOMAIN: $1`, `TASK: $2`, `NUM_AGENTS: $3 default to 3`

**Acceptance Criteria:**
- Spawns 3-10 agents in parallel
- All agents execute simultaneously (non-blocking)
- Synthesis identifies common themes and conflicts
- Reports consensus recommendations

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/expert-parallel.md`

---

### [CHORE] Task 18: Create agent expert template (CLI) for tac-bootstrap generator

**Workflow Metadata:**
```
/chore
/adw_sdlc_zte_iso
/adw_id: chore_Tac_13_Task_18
```

**Description:**
Create Jinja2 template for CLI expert that gets generated when users run `tac-bootstrap add-agentic`.

**Technical Steps:**
1. Create `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/.gitkeep`
2. Create `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/question.md.j2`
   - Template variables: `{{ config.project.name }}`, `{{ config.project.language }}`
   - Generalized version of CLI expert question prompt
3. Create `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/self-improve.md.j2`
   - Generalized version of CLI expert self-improve prompt
4. Create `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/expertise.yaml.j2`
   - Seed template with project-specific placeholders

**Acceptance Criteria:**
- Templates use Jinja2 variables correctly
- Generated files are valid and immediately usable
- Templates adapt to project configuration

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/question.md.j2`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/self-improve.md.j2`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/expertise.yaml.j2`

---

### [CHORE] Task 19: Create meta-prompt template for tac-bootstrap generator

**Workflow Metadata:**
```
/chore
/adw_sdlc_zte_iso
/adw_id: chore_Tac_13_Task_19
```

**Description:**
Create Jinja2 template for meta-prompt command.

**Technical Steps:**
1. Create `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-prompt.md.j2`
2. Copy content from base repository's meta-prompt.md
3. Add minimal Jinja2 variables if needed (project name, etc.)
4. Ensure template is project-agnostic (works for any language/framework)

**Acceptance Criteria:**
- Template generates valid meta-prompt command
- Works across all project types
- Output is immediately functional

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-prompt.md.j2`

---

### [CHORE] Task 20: Create meta-agent template for tac-bootstrap generator

**Workflow Metadata:**
```
/chore
/adw_sdlc_zte_iso
/adw_id: chore_Tac_13_Task_20
```

**Description:**
Create Jinja2 template for meta-agent command.

**Technical Steps:**
1. Create `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-agent.md.j2`
2. Copy content from base repository's meta-agent.md
3. Ensure project-agnostic
4. Validate output format matches agent schema

**Acceptance Criteria:**
- Template generates valid meta-agent command
- Output creates properly formatted agent definitions
- Works for all project configurations

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-agent.md.j2`

---

### [CHORE] Task 21: Create expert-orchestrate template for tac-bootstrap generator

**Workflow Metadata:**
```
/chore
/adw_sdlc_zte_iso
/adw_id: chore_Tac_13_Task_21
```

**Description:**
Create Jinja2 template for expert orchestrator command.

**Technical Steps:**
1. Create `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-orchestrate.md.j2`
2. Copy content from base repository's expert-orchestrate.md
3. Ensure template works with any expert domain
4. Validate subagent spawning syntax

**Acceptance Criteria:**
- Template generates valid orchestrator command
- Works with multiple expert domains
- Proper Task tool usage for subagents

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-orchestrate.md.j2`

---

### [CHORE] Task 22: Create expert-parallel template for tac-bootstrap generator

**Workflow Metadata:**
```
/chore
/adw_sdlc_zte_iso
/adw_id: chore_Tac_13_Task_22
```

**Description:**
Create Jinja2 template for parallel expert scaling command.

**Technical Steps:**
1. Create `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-parallel.md.j2`
2. Copy content from base repository's expert-parallel.md
3. Ensure synthesis logic is clear and actionable
4. Validate parallel Task tool invocation pattern

**Acceptance Criteria:**
- Template generates valid parallel command
- Spawns multiple agents correctly
- Synthesis step aggregates results properly

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-parallel.md.j2`

---

### [CHORE] Task 23: Register agent expert templates in scaffold_service.py

**Workflow Metadata:**
```
/chore
/adw_sdlc_zte_iso
/adw_id: chore_Tac_13_Task_23
```

**Description:**
Register all new agent expert templates in the scaffold service so they are generated when users run `tac-bootstrap add-agentic`.

**Technical Steps:**
1. Open `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
2. In the `_add_claude_code_commands()` method, add template registration for:
   - `.claude/commands/experts/cli/question.md` (template: `claude/commands/experts/cli/question.md.j2`)
   - `.claude/commands/experts/cli/self-improve.md` (template: `claude/commands/experts/cli/self-improve.md.j2`)
   - `.claude/commands/experts/cli/expertise.yaml` (template: `claude/commands/experts/cli/expertise.yaml.j2`)
   - `.claude/commands/meta-prompt.md` (template: `claude/commands/meta-prompt.md.j2`)
   - `.claude/commands/meta-agent.md` (template: `claude/commands/meta-agent.md.j2`)
   - `.claude/commands/expert-orchestrate.md` (template: `claude/commands/expert-orchestrate.md.j2`)
   - `.claude/commands/expert-parallel.md` (template: `claude/commands/expert-parallel.md.j2`)
3. Each registration should use `plan.add_file()` with:
   - `action="create"` (or `action="skip_if_exists"` for expertise.yaml seed)
   - `template="<path to .j2>"`
   - `reason="<short description>"`

**Acceptance Criteria:**
- All 7 new templates are registered
- Templates are rendered when `add-agentic` is executed
- Output files are placed in correct directories
- No duplicate registrations

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`

---

### [CHORE] Task 24: Update CLI README with Agent Experts section

**Workflow Metadata:**
```
/chore
/adw_sdlc_zte_iso
/adw_id: chore_Tac_13_Task_24
```

**Description:**
Add comprehensive documentation for Agent Experts (TAC-13) to the CLI README.

**Technical Steps:**
1. Open `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/README.md`
2. Add new section after "Intelligent Documentation Loading (TAC-9)":
   ```markdown
   ### Agent Experts (TAC-13)
   ```
3. Document:
   - What are agent experts (Act → Learn → Reuse loop)
   - Self-improving template metaprompts concept
   - Expertise files as mental models
   - When to use agent experts vs generic agents
4. Include usage examples:
   ```bash
   # Query CLI expert
   /experts:cli:question "How does template registration work?"

   # Self-improve CLI expert after code changes
   /experts:cli:self-improve true

   # Orchestrate expert through full workflow
   /expert-orchestrate cli "Add new template for hooks"

   # Scale experts in parallel for high-confidence results
   /expert-parallel cli "Review scaffold service logic" 5
   ```
5. Add table of included experts:

| Expert Domain | Expertise Coverage | Commands |
|---------------|-------------------|----------|
| `cli` | tac-bootstrap CLI, templates, scaffold service | `/experts:cli:question`, `/experts:cli:self-improve` |
| `adw` (optional) | AI Developer Workflows, state management | `/experts:adw:question`, `/experts:adw:self-improve` |
| `commands` (optional) | Slash command structure, variables | `/experts:commands:question`, `/experts:commands:self-improve` |

6. Document meta-agentics:
   - `/meta-prompt` - Generate new slash commands
   - `/meta-agent` - Generate new agent definitions
   - Progressive disclosure for skills

**Acceptance Criteria:**
- Section is clear and actionable
- Examples are concrete and copy-pasteable
- Table is properly formatted
- Integrates seamlessly with existing README structure
- Matches style of other feature sections

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/README.md`

---

### [CHORE] Task 25: Update main README with TAC-13 reference

**Workflow Metadata:**
```
/chore
/adw_sdlc_zte_iso
/adw_id: chore_Tac_13_Task_25
```

**Description:**
Add TAC-13 reference to main tac_bootstrap README.

**Technical Steps:**
1. Open `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/README.md`
2. Update feature list to include:
   ```markdown
   - **Agent Experts (TAC-13)**: Self-improving agents with expertise files
   ```
3. Add to `.claude/commands/` description:
   ```markdown
   - **Agent Experts**: Self-improving domain experts with mental models
   ```
4. Update course reference section to mention TAC-13

**Acceptance Criteria:**
- TAC-13 is clearly mentioned
- Links to documentation are correct
- Integrates with existing content

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/README.md`

---

### [CHORE] Task 26: Create AI docs keyword mappings for TAC-13

**Workflow Metadata:**
```
/chore
/adw_sdlc_zte_iso
/adw_id: chore_Tac_13_Task_26
```

**Description:**
Add TAC-13 documentation topics to the auto-detection keyword mappings.

**Technical Steps:**
1. Open `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/workflow_ops.py`
2. In the `detect_relevant_docs()` function, add new keyword mappings:
   ```python
   "Tac-13-agent-experts": ["agent expert", "expertise file", "self-improving", "mental model", "act learn reuse"],
   "expertise-file-structure": ["expertise yaml", "expertise structure", "expertise schema"],
   "meta-skill-pattern": ["meta-skill", "progressive disclosure", "skill levels"],
   ```
3. Sync to template: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2`

**Acceptance Criteria:**
- Keywords trigger auto-loading of TAC-13 docs
- Dynamic scanning still works for custom docs
- Template is synchronized

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/workflow_ops.py`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2`

---

### [CHORE] Task 27: Update CHANGELOG and bump version to 0.8.0

**Workflow Metadata:**
```
/chore
/adw_sdlc_zte_iso
/adw_id: chore_Tac_13_Task_27
```

**Description:**
Update CHANGELOG with all TAC-13 features and bump version to 0.8.0.

**Technical Steps:**
1. Open `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/CHANGELOG.md`
2. Add new section at top:
   ```markdown
   ## [0.8.0] - 2026-02-03

   ### Added - TAC-13: Agent Experts

   **Core Capabilities:**
   - Agent experts with self-improving expertise files (Act → Learn → Reuse loop)
   - Self-improving template metaprompts for domain specialization
   - Mental model pattern: expertise.yaml files that validate against codebase
   - Question prompts: Answer domain questions by reading expertise + validating against code
   - Self-improve prompts: 7-phase workflow (check diff → validate → update → enforce limits)

   **Agent Experts Included:**
   - CLI Expert: tac-bootstrap CLI, templates, scaffold service
   - (Optional) ADW Expert: AI Developer Workflows, state management, GitHub integration
   - (Optional) Commands Expert: Slash command structure, variables, workflows

   **Meta-Agentics:**
   - `/meta-prompt`: Generate new slash commands from descriptions
   - `/meta-agent`: Generate new agent definitions from descriptions
   - Meta-skill pattern documentation (progressive disclosure)

   **Orchestration:**
   - `/expert-orchestrate`: Plan → Build → Improve workflow for agent experts
   - `/expert-parallel`: Scale experts in parallel (3-10 instances) for high-confidence results

   **Documentation:**
   - Comprehensive TAC-13 guide in ai_docs/doc/
   - Expertise file structure documentation
   - Meta-skill pattern guide
   - Auto-detection keywords for TAC-13 docs

   **Templates:**
   - CLI expert templates (question, self-improve, expertise seed)
   - Meta-prompt template
   - Meta-agent template
   - Expert orchestration templates

   ### Changed
   - Updated README with Agent Experts section and usage examples
   - Enhanced AI docs auto-detection with TAC-13 keywords
   ```
3. Update version references in:
   - `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/README.md` (installation commands)
   - `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/pyproject.toml` (version field)
   - `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/__init__.py` (if version constant exists)

**Acceptance Criteria:**
- CHANGELOG accurately summarizes all TAC-13 changes
- Version bumped to 0.8.0 across all files
- Follows semantic versioning (MINOR bump for new features)
- CHANGELOG is human-readable and marketing-friendly

**Impacted Paths:**
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/CHANGELOG.md`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/README.md`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/pyproject.toml`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/__init__.py`

---

## Parallel Execution Groups

| Grupo | Tareas | Cantidad | Dependencia | Descripción |
|-------|--------|----------|-------------|-------------|
| P1 | 1, 2, 3 | 3 | Ninguna | Documentation foundation (TAC-13 concepts, expertise structure, directory setup) |
| P2 | 4, 5, 7, 8, 10, 11 | 6 | P1 | Create expert prompts (question + self-improve for CLI, ADW, Commands) |
| P3 | 6, 9, 12 | 3 | P2 | Generate initial expertise files by running self-improve prompts |
| P4 | 13, 14, 15, 16, 17 | 5 | P1 | Create meta-agentic commands and orchestration patterns |
| P5 | 18, 19, 20, 21, 22 | 5 | P2, P4 | Create Jinja2 templates for all new commands and experts |
| P6 | 23, 26 | 2 | P5 | Register templates in scaffold service and update keyword mappings |
| P7 | 24, 25 | 2 | P3, P4 | Update documentation (README updates for CLI and main repo) |
| SEQ | 27 | 1 | TODOS | CHANGELOG and version bump to 0.8.0 (MUST BE LAST) |

**Execution Notes:**
- P1-P7 can have tasks executed in parallel within each group
- Each group depends on completion of previous groups
- SEQ group (Task 27) must execute ONLY after all other tasks complete
- Total estimated tasks: 27 (26 implementation + 1 CHANGELOG)

---

**End of Plan**
