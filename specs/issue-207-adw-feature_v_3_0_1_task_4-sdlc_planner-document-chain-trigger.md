# Feature: Document trigger_issue_chain.py in ADWs README

## Metadata
issue_number: `207`
adw_id: `feature_v_3_0_1_task_4`
issue_json: `{"number":207,"title":"Documentar el trigger de cadena en el README de ADWs","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_v_3_0_1_task_4\n\n## Archivos a modificar\n- **Archivo raiz**: `adws/README.md`\n- **Archivo template**: `tac_bootstrap_cli/tac_bootstrap/templates/adws/README.md.j2`\n\n### Contexto\nEl README actual de ADWs documenta `trigger_cron.py` y `trigger_webhook.py`, pero no incluye documentacion para `trigger_issue_chain.py`. Los usuarios necesitan saber como usar este trigger para procesar issues en orden secuencial.\n\n### Ubicacion en el README\nAgregar una nueva subseccion dentro de \"### Automation Triggers\" (linea ~333), despues de la documentacion de `trigger_cron.py`.\n\n### Contenido a agregar\n```markdown\n#### trigger_issue_chain.py - Sequential Issue Processing\nProcesses issues in a specific order, waiting for each to close before starting the next.\n\n**Usage:**\n```bash\n# Process issues 123, 456, 789 in order\nuv run adw_triggers/trigger_issue_chain.py 123 456 789\n\n# Using comma-separated format\nuv run adw_triggers/trigger_issue_chain.py --issues 123,456,789\n\n# Custom polling interval (default: 20 seconds)\nuv run adw_triggers/trigger_issue_chain.py --issues 123,456,789 --interval 30\n\n# Single check cycle (for testing)\nuv run adw_triggers/trigger_issue_chain.py --issues 123,456,789 --once\n```\n\n**Behavior:**\n- Only processes the first OPEN issue in the chain\n- Waits for issue N to be CLOSED before processing issue N+1\n- Polls GitHub at configurable intervals to check issue status\n- Supports all workflow triggers (adw_plan_iso, adw_sdlc_iso, etc.)\n\n**Use Cases:**\n- Processing dependent issues in sequence\n- Ensuring ordered feature implementation\n- Batch processing with dependencies between tasks\n\n**Example Workflow:**\n1. Create issues #10, #11, #12 with dependencies\n2. Run: `uv run adw_triggers/trigger_issue_chain.py --issues 10,11,12`\n3. Trigger starts processing #10\n4. When #10 is closed (manually or by merged PR), trigger processes #11\n5. Process continues until all issues are closed\n```\n\n### Pasos a ejecutar\n1. Abrir `adws/README.md`\n2. Localizar la seccion \"### Automation Triggers\" (aproximadamente linea 333)\n3. Despues del bloque de `trigger_cron.py` y antes de `trigger_webhook.py`, insertar la nueva seccion documentando `trigger_issue_chain.py`\n4. Asegurar que el formato markdown es consistente con el resto del documento\n5. Replicar los mismos cambios en el archivo template `README.md.j2`\n\n### Criterios de aceptacion\n- [ ] El README incluye seccion completa para `trigger_issue_chain.py`\n- [ ] La documentacion explica el comportamiento de espera hasta cierre del issue anterior\n- [ ] Incluye al menos 4 ejemplos de comando (posicional, --issues, --interval, --once)\n- [ ] Describe los casos de uso principales\n- [ ] El formato es consistente con el resto del README\n- [ ] El template `.j2` tiene los mismos cambios\n- [ ] Verificar con:\n  ```bash\n  # Verificar que la seccion existe\n  grep -A5 \"trigger_issue_chain.py\" adws/README.md\n\n  # Verificar ejemplos de comando\n  grep \"\\-\\-issues\" adws/README.md | head -3"}`

## Feature Description
This feature adds comprehensive documentation for the `trigger_issue_chain.py` automation trigger to the ADWs README files. The chain trigger is a sequential issue processing system that processes a specific ordered list of GitHub issues, waiting for each to close before starting the next. Currently, the README documents `trigger_cron.py` and `trigger_webhook.py` but lacks documentation for this important third trigger type.

## User Story
As a developer using TAC Bootstrap's ADW system
I want to understand how to use the chain trigger for sequential issue processing
So that I can automate the processing of dependent issues in the correct order

## Problem Statement
The ADWs README currently documents two automation triggers (`trigger_cron.py` and `trigger_webhook.py`) but is missing documentation for `trigger_issue_chain.py`. This creates a gap in the user documentation, as developers cannot discover or understand how to use the chain trigger for sequential issue processing without reading the source code. The trigger provides valuable functionality for processing dependent issues in order, ensuring issue N is closed before issue N+1 begins processing.

## Solution Statement
Add a new subsection documenting `trigger_issue_chain.py` within the "Automation Triggers" section of both the root `adws/README.md` and the template `tac_bootstrap_cli/tac_bootstrap/templates/adws/README.md.j2`. The documentation will include usage examples, behavior description, use cases, and a complete workflow example. The new section will be positioned after `trigger_cron.py` and before `trigger_webhook.py` to maintain logical ordering.

## Relevant Files
Files necessary for implementing the feature:

- `adws/README.md` (lines 333-374) - Root README file where documentation will be added in the "Automation Triggers" section
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/README.md.j2` - Template version that generates ADWs README for new projects, needs identical changes
- `adws/adw_triggers/trigger_issue_chain.py` - Source code reference to verify documented behavior is accurate

### New Files
None. This feature only modifies existing documentation files.

## Implementation Plan

### Phase 1: Foundation
Review the existing README structure and the `trigger_issue_chain.py` implementation to ensure documentation accuracy. Verify the exact line locations in both files where the new section should be inserted.

### Phase 2: Core Implementation
Add the new documentation section for `trigger_issue_chain.py` to both `adws/README.md` and the template `README.md.j2`. The documentation will include:
- Section title and description
- Four usage examples (positional args, --issues, --interval, --once)
- Behavior bullet points
- Use cases
- Complete workflow example

### Phase 3: Integration
Verify the documentation integrates seamlessly with surrounding sections and maintains consistent formatting with the existing trigger documentation.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Review existing README structure
- Read `adws/README.md` lines 333-374 to understand current "Automation Triggers" section structure
- Review how `trigger_cron.py` and `trigger_webhook.py` are documented
- Identify the exact insertion point (after `trigger_cron.py`, before `trigger_webhook.py`)
- Verify formatting patterns (heading levels, code block styles, bullet point format)

### Task 2: Verify trigger_issue_chain.py functionality
- Read `adws/adw_triggers/trigger_issue_chain.py` to confirm:
  - Command-line argument patterns (positional, --issues, --interval, --once)
  - Default polling interval (20 seconds)
  - Sequential processing behavior (only first open issue)
  - Workflow support (all ADW workflows)

### Task 3: Add documentation to adws/README.md
- Open `adws/README.md`
- Locate line ~351 (end of trigger_cron.py section, before trigger_webhook.py)
- Insert new section with heading: `#### trigger_issue_chain.py - Sequential Issue Processing`
- Add description: "Processes issues in a specific order, waiting for each to close before starting the next."
- Add **Usage:** section with 4 code examples:
  - Positional arguments: `uv run adw_triggers/trigger_issue_chain.py 123 456 789`
  - CSV format: `uv run adw_triggers/trigger_issue_chain.py --issues 123,456,789`
  - Custom interval: `uv run adw_triggers/trigger_issue_chain.py --issues 123,456,789 --interval 30`
  - Once mode: `uv run adw_triggers/trigger_issue_chain.py --issues 123,456,789 --once`
- Add **Behavior:** section with 4 bullet points about processing logic
- Add **Use Cases:** section with 3 bullet points
- Add **Example Workflow:** section with 5-step numbered list

### Task 4: Replicate changes to template README.md.j2
- Open `tac_bootstrap_cli/tac_bootstrap/templates/adws/README.md.j2`
- Verify this is a template version (much shorter, only 44 lines)
- Note: Template has different structure, only includes basic ADWs structure
- Determine if template needs update or if it's intentionally minimal
- If template should match root README structure: add equivalent section with Jinja2 template variables where appropriate
- If template is minimal by design: document decision in Notes section

### Task 5: Verify formatting consistency
- Compare new section formatting with `trigger_cron.py` and `trigger_webhook.py` sections
- Ensure heading levels match (####)
- Verify code block formatting uses bash syntax highlighting
- Check bullet point style consistency
- Ensure spacing between sections matches existing patterns

### Task 6: Execute validation commands and verify acceptance criteria
- Run: `grep -A5 "trigger_issue_chain.py" adws/README.md` to verify section exists
- Run: `grep "\-\-issues" adws/README.md | head -3` to verify examples exist
- Verify all acceptance criteria:
  - README includes complete section for trigger_issue_chain.py
  - Documentation explains wait-until-close behavior
  - Includes at least 4 command examples
  - Describes main use cases
  - Format is consistent with rest of README
  - Template .j2 has matching changes (or design decision documented)

## Testing Strategy

### Unit Tests
No unit tests required. This is a documentation-only change.

### Edge Cases
- Verify markdown renders correctly with nested code blocks
- Ensure grep validation commands work as specified
- Check that new section doesn't break existing table of contents (if present)

## Acceptance Criteria
- [ ] The `adws/README.md` includes complete section for `trigger_issue_chain.py` in "Automation Triggers"
- [ ] Documentation explains sequential processing behavior (waits for issue N to close before processing N+1)
- [ ] Includes exactly 4 command usage examples (positional, --issues, --interval, --once)
- [ ] Describes at least 3 use cases for the chain trigger
- [ ] Markdown formatting is consistent with existing trigger documentation sections
- [ ] Template `README.md.j2` has matching changes or decision about template structure is documented
- [ ] Command `grep -A5 "trigger_issue_chain.py" adws/README.md` returns the new section
- [ ] Command `grep "\-\-issues" adws/README.md | head -3` returns at least 3 examples

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `grep -A5 "trigger_issue_chain.py" adws/README.md` - Verify section exists in root README
- `grep "\-\-issues" adws/README.md | head -3` - Verify --issues flag examples
- `grep -A5 "trigger_issue_chain.py" tac_bootstrap_cli/tac_bootstrap/templates/adws/README.md.j2 || echo "Template verification needed"` - Check template

## Notes
- The template `README.md.j2` is significantly shorter (44 lines) than the root `adws/README.md`. During implementation, need to determine if:
  1. Template should be expanded to match root README structure, or
  2. Template is intentionally minimal and only root README needs update
- The chain trigger (`trigger_issue_chain.py`) is a 417-line Python script with comprehensive functionality
- Default polling interval is 20 seconds as confirmed in source code line 361
- The trigger only processes issues assigned to the current GitHub user (line 125)
- Documentation should emphasize sequential processing: only the first open issue in the chain is processed
