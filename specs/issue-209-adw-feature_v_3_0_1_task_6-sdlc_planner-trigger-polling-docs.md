# Feature: Trigger Polling Configuration Documentation

## Metadata
issue_number: `209`
adw_id: `feature_v_3_0_1_task_6`
issue_json: `{"number":209,"title":"Incluir configuracion de intervalos en docs de triggers","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_v_3_0_1_task_6\n\n### Archivos a modificar\n- **Archivo raiz**: `adws/README.md`\n- **Archivo template**: `tac_bootstrap_cli/tac_bootstrap/templates/adws/README.md.j2`\n\n### Contexto\nEl README de ADWs no documenta claramente como configurar los intervalos de polling para los triggers. Los usuarios necesitan saber:\n1. Cual es el intervalo por defecto (20 segundos)\n2. Como cambiarlo via CLI (`--interval`)\n3. Si existe configuracion en `config.yml` (actualmente no, pero podria agregarse)\n\n### Ubicacion en el README\nAgregar una nueva subseccion dentro de \"## Configuration\" (aproximadamente linea 604), despues de \"### ADW Tracking\".\n\n### Contenido a agregar\n```markdown\n### Trigger Polling Configuration\n\nADW triggers use polling intervals to check GitHub for new workflow commands.\n\n#### Default Interval\nAll polling-based triggers default to **20 seconds** between checks.\n\n#### Overriding via CLI\nUse the `--interval` or `-i` flag to customize:\n\n```bash\n# Poll every 30 seconds\nuv run adw_triggers/trigger_cron.py --interval 30\n\n# Poll every 60 seconds\nuv run adw_triggers/trigger_issue_chain.py --issues 1,2,3 -i 60\n```\n\n#### Recommended Intervals\n| Use Case | Interval | Rationale |\n|----------|----------|-----------|\n| Development/Testing | 10-20s | Fast feedback during testing |\n| Production (light usage) | 30-60s | Balance responsiveness and API limits |\n| Production (heavy usage) | 60-120s | Avoid GitHub API rate limiting |\n| CI/CD Integration | Use `--once` | Single execution, no polling |\n\n#### API Rate Limiting\nGitHub's API allows 5,000 requests/hour for authenticated users. Each polling cycle makes approximately 1-3 API calls depending on open issues. With default 20s interval:\n- ~180 cycles/hour\n- ~180-540 API calls/hour\n- Safe margin for other operations\n\nFor repositories with many open issues, consider increasing the interval.\n```\n\n### Pasos a ejecutar\n1. Abrir `adws/README.md`\n2. Localizar la seccion \"## Configuration\" (aproximadamente linea 604)\n3. Despues de \"### ADW Tracking\", agregar la nueva subseccion \"### Trigger Polling Configuration\"\n4. Incluir tabla de intervalos recomendados y explicacion de rate limiting\n5. Replicar los mismos cambios en el archivo template `README.md.j2`\n\n### Criterios de aceptacion\n- [ ] El README incluye seccion \"### Trigger Polling Configuration\"\n- [ ] Documenta el valor por defecto de 20 segundos\n- [ ] Muestra ejemplos de como usar `--interval` y `-i`\n- [ ] Incluye tabla de intervalos recomendados por caso de uso\n- [ ] Menciona consideraciones de rate limiting de GitHub API\n- [ ] El template `.j2` tiene los mismos cambios\n- [ ] Verificar con:\n  ```bash\n  # Verificar que la seccion existe\n  grep -A3 \"Trigger Polling Configuration\" adws/README.md\n\n  # Verificar que menciona el default\n  grep \"20 seconds\" adws/README.md\n\n  # Verificar tabla de intervalos\n  grep -c \"Interval\" adws/README.md  # Debe ser >= 2"}`

## Feature Description
Add comprehensive documentation about trigger polling configuration to the ADWs README. Currently, users don't have clear guidance on:
- Default polling interval (20 seconds)
- How to customize intervals via CLI flags
- Recommended intervals for different use cases
- GitHub API rate limiting considerations

This documentation will help users configure polling intervals appropriately based on their use case (development, production, CI/CD) and avoid API rate limiting issues.

## User Story
As a developer using ADW triggers
I want to understand how to configure polling intervals
So that I can balance responsiveness with API rate limits and choose appropriate intervals for my use case

## Problem Statement
The ADWs README lacks documentation about trigger polling configuration. Users currently need to:
- Read the source code to discover the default 20-second interval
- Guess appropriate intervals for their use case
- Risk hitting GitHub API rate limits without understanding the implications

This creates friction in adoption and can lead to suboptimal configurations or API throttling.

## Solution Statement
Add a new "Trigger Polling Configuration" subsection within the "Configuration" section of both:
1. The root `adws/README.md` file
2. The Jinja2 template `tac_bootstrap_cli/tac_bootstrap/templates/adws/README.md.j2`

The documentation will include:
- Default interval specification
- CLI flag examples (`--interval` and `-i`)
- Recommended intervals table organized by use case
- GitHub API rate limiting calculations and considerations

## Relevant Files
Files necessary to implement the feature:

- `adws/README.md` (line ~639-667) - Root documentation file where the new subsection will be added after "### ADW Tracking" and before "### Target Branch"
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/README.md.j2` - Jinja2 template that needs identical changes to maintain consistency when generating new projects

### New Files
None. This is a documentation-only change to existing files.

## Implementation Plan

### Phase 1: Foundation
Understand the current structure of the Configuration section in both files to ensure the new subsection fits naturally with existing documentation patterns.

### Phase 2: Core Implementation
Add the "Trigger Polling Configuration" subsection with all required content:
- Default interval documentation
- CLI flag usage examples
- Recommended intervals table
- API rate limiting section

### Phase 3: Integration
Ensure both the root README and the Jinja2 template have identical changes, maintaining consistency across the documentation ecosystem.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Read current README structure
- Read `adws/README.md` around line 639-667 to understand the Configuration section format
- Identify the exact insertion point after "### ADW Tracking"
- Note any formatting patterns or conventions to follow

### Task 2: Add polling configuration section to root README
- Open `adws/README.md`
- Insert new "### Trigger Polling Configuration" subsection after "### ADW Tracking" (around line 646)
- Add all required content:
  - Default interval (20 seconds)
  - CLI override examples with both `--interval` and `-i` flags
  - Recommended intervals table with 4 use cases
  - API rate limiting calculations and guidance
- Ensure markdown formatting matches existing sections

### Task 3: Update Jinja2 template
- Read `tac_bootstrap_cli/tac_bootstrap/templates/adws/README.md.j2` to find corresponding location
- Replicate the exact same changes from Task 2
- Ensure Jinja2 template variables (if any in surrounding text) are preserved
- Verify the section fits naturally within the template structure

### Task 4: Validation
- Run verification commands from acceptance criteria:
  ```bash
  # Verify section exists
  grep -A3 "Trigger Polling Configuration" adws/README.md

  # Verify default interval documented
  grep "20 seconds" adws/README.md

  # Verify table exists (should find "Interval" multiple times)
  grep -c "Interval" adws/README.md  # Should be >= 2

  # Verify template also has changes
  grep "Trigger Polling Configuration" tac_bootstrap_cli/tac_bootstrap/templates/adws/README.md.j2
  ```
- Visually review both files to ensure formatting is consistent
- Confirm all acceptance criteria are met

## Testing Strategy

### Unit Tests
No unit tests required - this is documentation-only.

### Edge Cases
- Verify markdown table renders correctly in different viewers
- Ensure code blocks are properly formatted with syntax highlighting
- Check that line breaks and spacing match existing sections

## Acceptance Criteria
- ✅ The `adws/README.md` includes a new "### Trigger Polling Configuration" subsection
- ✅ Documentation clearly states the default interval is 20 seconds
- ✅ Examples show how to use both `--interval` and `-i` CLI flags
- ✅ Includes a complete table with 4 recommended intervals covering Development/Testing, Production (light), Production (heavy), and CI/CD use cases
- ✅ Documents GitHub API rate limiting considerations with specific calculations
- ✅ The Jinja2 template `README.md.j2` contains identical changes
- ✅ All verification commands pass:
  - `grep -A3 "Trigger Polling Configuration" adws/README.md` shows the new section
  - `grep "20 seconds" adws/README.md` finds the default interval
  - `grep -c "Interval" adws/README.md` returns >= 2 (table headers + entries)
  - `grep "Trigger Polling Configuration" tac_bootstrap_cli/tac_bootstrap/templates/adws/README.md.j2` confirms template update

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `grep -A3 "Trigger Polling Configuration" adws/README.md` - Verify section exists in root README
- `grep "20 seconds" adws/README.md` - Verify default interval documented
- `grep -c "Interval" adws/README.md` - Verify table exists (should be >= 2)
- `grep "Trigger Polling Configuration" tac_bootstrap_cli/tac_bootstrap/templates/adws/README.md.j2` - Verify template updated
- `grep -A10 "### Trigger Polling Configuration" adws/README.md` - Visual inspection of formatting
- `grep -A10 "### Trigger Polling Configuration" tac_bootstrap_cli/tac_bootstrap/templates/adws/README.md.j2` - Visual inspection of template formatting

## Notes
- This is a documentation-only change with zero code impact
- No dependencies need to be installed
- The section should be added between "### ADW Tracking" (line ~641) and "### Target Branch" (line ~647)
- Keep the content identical between root README and template to maintain consistency
- The 20-second default is hardcoded in trigger implementations, not configurable via `config.yml`
- Future enhancement could add `config.yml` support for default intervals, but that's out of scope for this task
