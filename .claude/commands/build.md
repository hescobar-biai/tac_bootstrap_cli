# Build - Sequential Plan Implementation

Implement a plan file sequentially, step-by-step, with clear progress tracking and validation.

## Variables
- $ARGUMENTS: Optional path to plan file (defaults to specs/plan.md or auto-detects first specs/issue-*.md)

## Instructions

Follow these steps in order to implement the plan:

### Step 1: Locate Plan File
- If $ARGUMENTS is provided, use that as the plan file path
- Otherwise, check if `specs/plan.md` exists
- If not, find the first `specs/issue-*.md` file in the specs directory
- If no plan file found, report error and stop

### Step 2: Read and Parse Plan
- Read the complete plan file
- Identify all implementation steps/tasks
- Understand dependencies between steps
- Note any special requirements or constraints

### Step 3: Ultrathink
Think carefully about the implementation approach:
- Review the architecture and design patterns required
- Consider edge cases and potential issues
- Plan the order of operations
- Identify validation points
- Understand acceptance criteria

### Step 4: Execute Sequentially
Implement each step one at a time:
- Show clear progress for each step (e.g., "Step 1/5: Creating models...")
- Complete each step fully before moving to the next
- Verify each step works before proceeding
- Use appropriate tools (Read, Write, Edit, Bash, etc.)
- Follow best practices and coding standards

### Step 5: Error Handling
If any step fails:
- STOP immediately - do not continue to next steps
- Report which step failed (e.g., "Failed at Step 3/5")
- Provide clear error message with details
- Show what was completed successfully before failure
- Suggest how to fix the error if possible

### Step 6: Completion Report
After successful implementation, display:
- Implementation status (success or failed at step X)
- Number of steps completed (e.g., "5/5 steps completed")
- Changes made using `git diff --stat`
- Summary of what was implemented

## Report

Provide a comprehensive report:

### Status
- [ ] Success: All steps completed
- [ ] Failed: Stopped at step X/Y

### Progress
- Steps completed: X/Y
- Files modified: (from git diff --stat)
- Lines changed: (from git diff --stat)

### Changes
```
git diff --stat output here
```

### Summary
- Bullet point list of what was implemented
- Any issues encountered and how they were resolved
- Next steps (if applicable)

### Recommendation
If successful, consider running:
- `/test` - Validate implementation with tests
- `/review` - Review code quality and patterns

## Orchestration Patterns

Para construir múltiples archivos en paralelo con agentes especializados, considera usar patrones de orquestación:

- [build-agent](./../agents/build-agent.md) - Agente especializado en implementar un archivo específico basado en instrucciones detalladas y contexto
- [orch_scout_and_build](./orch_scout_and_build.md) - Workflow simplificado que orquesta exploración scout y construcción directa

Usa comandos directos (como este) para construcción secuencial. Usa orquestación con build-agents para construcción paralela de múltiples archivos.
