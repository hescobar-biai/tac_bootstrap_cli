# Feature: Implement ScaffoldService.build_plan()

## Metadata
issue_number: `28`
adw_id: `c9d3ab60`
issue_json: `{"number":28,"title":"TAREA 5.1: Implementar ScaffoldService.build_plan()","body":" Prompt para Agente\n\n## Contexto\nEl ScaffoldService es el servicio central que construye y aplica el plan de scaffolding.\nYa tenemos los modelos ScaffoldPlan, FileOperation y DirectoryOperation en domain/plan.py.\nAhora necesitamos implementar la logica que construye el plan basado en la configuracion.\n\n## Objetivo\nImplementar el metodo build_plan() que analiza la configuracion y construye un\nScaffoldPlan con todas las operaciones necesarias.\n\n## Archivo a Crear\n`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`\n\n## Contenido Completo\n\n```python\n\"\"\"Scaffold Service for building and applying generation plans.\n\nThis service is responsible for:\n1. Building a ScaffoldPlan from TACConfig\n2. Applying the plan to create directories and files\n3. Handling idempotency and existing files\n\"\"\"\nfrom dataclasses import dataclass, field\nfrom pathlib import Path\nfrom typing import List, Optional\n\nfrom tac_bootstrap.domain.models import TACConfig\nfrom tac_bootstrap.domain.plan import (\n    ScaffoldPlan,\n    FileOperation,\n    FileAction,\n    DirectoryOperation,\n)\nfrom tac_bootstrap.infrastructure.template_repo import TemplateRepository\n\n\n@dataclass\nclass ApplyResult:\n    \"\"\"Result of applying a scaffold plan.\"\"\"\n    success: bool = True\n    directories_created: int = 0\n    files_created: int = 0\n    files_skipped: int = 0\n    files_overwritten: int = 0\n    error: Optional[str] = None\n    errors: List[str] = field(default_factory=list)\n\n\nclass ScaffoldService:\n    \"\"\"Service for building and applying scaffold plans.\n\n    Example:\n        service = ScaffoldService()\n        plan = service.build_plan(config)\n        result = service.apply_plan(plan, output_dir, config)\n    \"\"\"\n\n    def __init__(self, template_repo: Optional[TemplateRepository] = None):\n        \"\"\"Initialize scaffold service.\n\n        Args:\n            template_repo: Template repository (created if not provided)\n        \"\"\"\n        self.template_repo = template_repo or TemplateRepository()\n\n    def build_plan(\n        self,\n        config: TACConfig,\n        existing_repo: bool = False,\n    ) -> ScaffoldPlan:\n        \"\"\"Build a scaffold plan from configuration.\n\n        Args:\n            config: TAC configuration\n            existing_repo: Whether scaffolding into existing repo\n\n        Returns:\n            ScaffoldPlan with all operations to perform\n        \"\"\"\n        plan = ScaffoldPlan()\n\n        # Add directory structure\n        self._add_directories(plan, config)\n\n        # Add Claude configuration files\n        self._add_claude_files(plan, config, existing_repo)\n\n        # Add ADW files\n        self._add_adw_files(plan, config, existing_repo)\n\n        # Add script files\n        self._add_script_files(plan, config, existing_repo)\n\n        # Add config files\n        self._add_config_files(plan, config, existing_repo)\n\n        # Add structure READMEs\n        self._add_structure_files(plan, config, existing_repo)\n\n        return plan\n\n    def _add_directories(self, plan: ScaffoldPlan, config: TACConfig) -> None:\n        \"\"\"Add directory operations to plan.\"\"\"\n        directories = [\n            (\".claude\", \"Claude Code configuration\"),\n            (\".claude/commands\", \"Slash commands\"),\n            (\".claude/hooks\", \"Execution hooks\"),\n            (\".claude/hooks/utils\", \"Hook utilities\"),\n            (config.paths.adws_dir, \"AI Developer Workflows\"),\n            (f\"{config.paths.adws_dir}/adw_modules\", \"ADW shared modules\"),\n            (f\"{config.paths.adws_dir}/adw_triggers\", \"ADW triggers\"),\n            (config.paths.specs_dir, \"Specifications\"),\n            (config.paths.logs_dir, \"Execution logs\"),\n            (config.paths.scripts_dir, \"Utility scripts\"),\n            (config.paths.prompts_dir, \"Prompt templates\"),\n            (f\"{config.paths.prompts_dir}/templates\", \"Document templates\"),\n            (\"agents\", \"ADW agent state\"),\n            (config.paths.worktrees_dir, \"Git worktrees\"),\n            (\"app_docs\", \"Application documentation\"),\n            (\"ai_docs\", \"AI-generated documentation\"),\n        ]\n\n        for path, reason in directories:\n            plan.add_directory(path, reason)\n\n    def _add_claude_files(\n        self, plan: ScaffoldPlan, config: TACConfig, existing_repo: bool\n    ) -> None:\n        \"\"\"Add .claude/ configuration files.\"\"\"\n        action = FileAction.CREATE if not existing_repo else FileAction.SKIP\n\n        # Settings\n        plan.add_file(\n            \".claude/settings.json\",\n            action=action,\n            template=\"claude/settings.json.j2\",\n            reason=\"Claude Code settings and permissions\",\n        )\n\n        # Commands - all slash commands\n        commands = [\n            \"prime\", \"start\", \"build\", \"test\", \"lint\",\n            \"feature\", \"bug\", \"chore\", \"patch\",\n            \"implement\", \"commit\", \"pull_request\",\n            \"review\", \"document\", \"health_check\",\n            \"prepare_app\", \"install\", \"track_agentic_kpis\",\n        ]\n\n        for cmd in commands:\n            plan.add_file(\n                f\".claude/commands/{cmd}.md\",\n                action=action,\n                template=f\"claude/commands/{cmd}.md.j2\",\n                reason=f\"/{cmd} slash command\",\n            )\n\n        # Hooks\n        hooks = [\n            (\"pre_tool_use.py\", \"Pre-execution validation\"),\n            (\"post_tool_use.py\", \"Post-execution logging\"),\n            (\"stop.py\", \"Session cleanup\"),\n        ]\n\n        for hook, reason in hooks:\n            plan.add_file(\n                f\".claude/hooks/{hook}\",\n                action=action,\n                template=f\"claude/hooks/{hook}.j2\",\n                reason=reason,\n                executable=True,\n            )\n\n        # Hook utils\n        plan.add_file(\n            \".claude/hooks/utils/__init__.py\",\n            action=action,\n            template=\"claude/hooks/utils/__init__.py.j2\",\n            reason=\"Hook utilities package\",\n        )\n        plan.add_file(\n            \".claude/hooks/utils/constants.py\",\n            action=action,\n            template=\"claude/hooks/utils/constants.py.j2\",\n            reason=\"Shared constants for hooks\",\n        )\n\n    def _add_adw_files(\n        self, plan: ScaffoldPlan, config: TACConfig, existing_repo: bool\n    ) -> None:\n        \"\"\"Add adws/ workflow files.\"\"\"\n        action = FileAction.CREATE if not existing_repo else FileAction.SKIP\n        adws_dir = config.paths.adws_dir\n\n        # README\n        plan.add_file(\n            f\"{adws_dir}/README.md\",\n            action=action,\n            template=\"adws/README.md.j2\",\n            reason=\"ADW documentation\",\n        )\n\n        # Modules\n        modules = [\n            (\"__init__.py\", \"Package init\"),\n            (\"agent.py\", \"Claude Code wrapper\"),\n            (\"state.py\", \"State persistence\"),\n            (\"git_ops.py\", \"Git operations\"),\n            (\"workflow_ops.py\", \"Workflow orchestration\"),\n        ]\n\n        for module, reason in modules:\n            plan.add_file(\n                f\"{adws_dir}/adw_modules/{module}\",\n                action=action,\n                template=f\"adws/adw_modules/{module}.j2\",\n                reason=reason,\n            )\n\n        # Workflows\n        workflows = [\n            (\"adw_sdlc_iso.py\", \"SDLC workflow (isolated)\"),\n            (\"adw_patch_iso.py\", \"Patch workflow (isolated)\"),\n        ]\n\n        for workflow, reason in workflows:\n            plan.add_file(\n                f\"{adws_dir}/{workflow}\",\n                action=action,\n                template=f\"adws/{workflow}.j2\",\n                reason=reason,\n                executable=True,\n            )\n\n        # Triggers\n        plan.add_file(\n            f\"{adws_dir}/adw_triggers/__init__.py\",\n            action=action,\n            template=\"adws/adw_triggers/__init__.py.j2\",\n            reason=\"Triggers package\",\n        )\n        plan.add_file(\n            f\"{adws_dir}/adw_triggers/trigger_cron.py\",\n            action=action,\n            template=\"adws/adw_triggers/trigger_cron.py.j2\",\n            reason=\"Cron-based task polling\",\n            executable=True,\n        )\n\n    def _add_script_files(\n        self, plan: ScaffoldPlan, config: TACConfig, existing_repo: bool\n    ) -> None:\n        \"\"\"Add scripts/ utility files.\"\"\"\n        action = FileAction.CREATE if not existing_repo else FileAction.SKIP\n        scripts_dir = config.paths.scripts_dir\n\n        scripts = [\n            (\"start.sh\", \"Application starter\"),\n            (\"test.sh\", \"Test runner\"),\n            (\"lint.sh\", \"Linter runner\"),\n            (\"build.sh\", \"Build script\"),\n        ]\n\n        for script, reason in scripts:\n            plan.add_file(\n                f\"{scripts_dir}/{script}\",\n                action=action,\n                template=f\"scripts/{script}.j2\",\n                reason=reason,\n                executable=True,\n            )\n\n    def _add_config_files(\n        self, plan: ScaffoldPlan, config: TACConfig, existing_repo: bool\n    ) -> None:\n        \"\"\"Add configuration files.\"\"\"\n        action = FileAction.CREATE if not existing_repo else FileAction.SKIP\n\n        # config.yml - always create/overwrite to capture user settings\n        plan.add_file(\n            \"config.yml\",\n            action=FileAction.OVERWRITE if existing_repo else FileAction.CREATE,\n            template=\"config/config.yml.j2\",\n            reason=\"TAC Bootstrap configuration\",\n        )\n\n        # .mcp.json\n        plan.add_file(\n            \".mcp.json\",\n            action=action,\n            template=\"config/.mcp.json.j2\",\n            reason=\"MCP server configuration\",\n        )\n\n        # .gitignore - append if exists\n        plan.add_file(\n            \".gitignore\",\n            action=FileAction.PATCH if existing_repo else FileAction.CREATE,\n            template=\"config/.gitignore.j2\",\n            reason=\"Git ignore patterns\",\n        )\n\n    def _add_structure_files(\n        self, plan: ScaffoldPlan, config: TACConfig, existing_repo: bool\n    ) -> None:\n        \"\"\"Add README files for directory structure.\"\"\"\n        action = FileAction.CREATE if not existing_repo else FileAction.SKIP\n\n        structure_readmes = [\n            (f\"{config.paths.specs_dir}/README.md\", \"structure/specs/README.md.j2\"),\n            (\"app_docs/README.md\", \"structure/app_docs/README.md.j2\"),\n            (\"ai_docs/README.md\", \"structure/ai_docs/README.md.j2\"),\n        ]\n\n        for path, template in structure_readmes:\n            plan.add_file(\n                path,\n                action=action,\n                template=template,\n                reason=\"Directory documentation\",\n            )\n\n    def apply_plan(\n        self,\n        plan: ScaffoldPlan,\n        output_dir: Path,\n        config: TACConfig,\n        force: bool = False,\n    ) -> ApplyResult:\n        \"\"\"Apply a scaffold plan to create files and directories.\n\n        Args:\n            plan: The scaffold plan to apply\n            output_dir: Target directory\n            config: Configuration for template rendering\n            force: Overwrite existing files\n\n        Returns:\n            ApplyResult with statistics and any errors\n        \"\"\"\n        from tac_bootstrap.infrastructure.fs import FileSystem\n\n        result = ApplyResult()\n        fs = FileSystem()\n        template_context = {\"config\": config}\n\n        # Create directories first\n        for dir_op in plan.directories:\n            dir_path = output_dir / dir_op.path\n            try:\n                fs.ensure_directory(dir_path)\n                result.directories_created += 1\n            except Exception as e:\n                result.errors.append(f\"Failed to create {dir_op.path}: {e}\")\n\n        # Process files\n        for file_op in plan.files:\n            file_path = output_dir / file_op.path\n\n            try:\n                # Determine action based on existence and force flag\n                if file_path.exists() and file_op.action == FileAction.CREATE:\n                    if not force:\n                        result.files_skipped += 1\n                        continue\n                    # Force mode - treat as overwrite\n                    actual_action = FileAction.OVERWRITE\n                else:\n                    actual_action = file_op.action\n\n                if actual_action == FileAction.SKIP:\n                    result.files_skipped += 1\n                    continue\n\n                # Render content\n                if file_op.template:\n                    content = self.template_repo.render(\n                        file_op.template, template_context\n                    )\n                elif file_op.content:\n                    content = file_op.content\n                else:\n                    content = \"\"\n\n                # Apply based on action\n                if actual_action == FileAction.PATCH:\n                    fs.append_file(file_path, content)\n                else:\n                    fs.write_file(file_path, content)\n\n                # Make executable if needed\n                if file_op.executable:\n                    fs.make_executable(file_path)\n\n                if actual_action == FileAction.OVERWRITE and file_path.exists():\n                    result.files_overwritten += 1\n                else:\n                    result.files_created += 1\n\n            except Exception as e:\n                result.errors.append(f\"Failed to create {file_op.path}: {e}\")\n\n        # Set success based on errors\n        if result.errors:\n            result.success = False\n            result.error = f\"{len(result.errors)} error(s) occurred\"\n\n        return result\n```\n\n## Criterios de Aceptacion\n1. [ ] build_plan() genera plan completo con ~50+ operaciones\n2. [ ] Directorios se agregan en orden correcto\n3. [ ] Archivos .claude/ incluyen settings, commands y hooks\n4. [ ] Archivos adws/ incluyen modules y workflows\n5. [ ] Scripts son marcados como ejecutables\n6. [ ] apply_plan() crea estructura correctamente\n\n## Comandos de Verificacion\n```bash\ncd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli\n\n# Test build_plan\nuv run python -c \"\nfrom tac_bootstrap.application.scaffold_service import ScaffoldService\nfrom tac_bootstrap.domain.models import *\n\nservice = ScaffoldService()\nconfig = TACConfig(\n    project=ProjectSpec(name='test', language=Language.PYTHON, package_manager=PackageManager.UV),\n    commands=CommandsSpec(start='uv run python -m app', test='uv run pytest'),\n    claude=ClaudeConfig(settings=ClaudeSettings(project_name='test'))\n)\n\nplan = service.build_plan(config)\nprint(plan.summary)\nprint(f'Directories: {plan.total_directories}')\nprint(f'Files: {plan.total_files}')\n\"\n```\n\n## NO hacer\n- No crear los archivos reales aun (eso es apply_plan)\n- No implementar FileSystem aun (siguiente tarea)\n```"}`

## Feature Description

Implementar el servicio central `ScaffoldService` en la capa de aplicación que construye y aplica planes de scaffolding completos para generar la estructura de Agentic Layer en proyectos target. Este servicio es el corazón del generador TAC Bootstrap, responsable de orquestar la creación de ~50+ archivos y ~16 directorios basándose en la configuración TACConfig del usuario.

El servicio implementa dos métodos clave:
1. `build_plan()`: Analiza TACConfig y construye un ScaffoldPlan con todas las operaciones de archivos/directorios necesarias
2. `apply_plan()`: Ejecuta el plan para crear físicamente la estructura de archivos con idempotencia y manejo de errores

Esta implementación sigue arquitectura DDD clean: ScaffoldService en application layer orquesta domain models (ScaffoldPlan, FileOperation, DirectoryOperation) e infrastructure components (TemplateRepository, FileSystem) sin acoplarse a detalles de persistencia.

## User Story

As a **TAC Bootstrap CLI generator**
I want to **build comprehensive scaffolding plans from user configuration**
So that **I can preview all operations before execution, handle idempotency correctly, and generate complete Agentic Layer structures with proper templates rendered**

## Problem Statement

El CLI necesita generar estructuras de Agentic Layer completas para proyectos target, pero actualmente:

1. No existe lógica centralizada para determinar qué archivos y directorios crear basado en TACConfig
2. No hay distinción entre proyectos nuevos vs existentes (different file actions needed)
3. No existe preview capability - los usuarios no pueden ver qué se creará antes de ejecutar
4. No hay manejo de idempotencia - ¿qué pasa si archivos ya existen?
5. No hay orquestación de templates - cada archivo necesita template correcto renderizado con contexto apropiado
6. No hay manejo de permisos ejecutables para scripts y hooks
7. No hay diferenciación de acciones: CREATE, OVERWRITE, PATCH, SKIP para diferentes tipos de archivos

La generación de ~50+ archivos con lógica condicional compleja (existing_repo flag, templates Jinja2, permisos, configuración paths dinámica) requiere servicio robusto con separation of concerns.

## Solution Statement

Implementar `ScaffoldService` completo en `tac_bootstrap/application/scaffold_service.py` con:

### 1. ApplyResult Dataclass
- Estructura para resultados de aplicación de plan
- Tracking de estadísticas: directories_created, files_created, files_skipped, files_overwritten
- Lista de errores detallada para debugging
- Success flag y mensaje de error general

### 2. ScaffoldService Class
**Constructor:**
- Acepta TemplateRepository opcional (DI pattern)
- Crea TemplateRepository default si no provisto

**build_plan() Method:**
- Parámetros: `config: TACConfig`, `existing_repo: bool = False`
- Retorna: `ScaffoldPlan` completo con todas operaciones
- Lógica delegada a 6 métodos privados especializados:
  - `_add_directories()`: 16 directorios core
  - `_add_claude_files()`: .claude/settings.json, 18 commands, 3 hooks, 2 hook utils
  - `_add_adw_files()`: README, 5 modules, 2 workflows, 2 triggers
  - `_add_script_files()`: 4 bash scripts (start, test, lint, build)
  - `_add_config_files()`: config.yml, .mcp.json, .gitignore
  - `_add_structure_files()`: 3 README files para documentación de directorios

**_add_directories():**
- Itera lista de tuples (path, reason)
- Usa config.paths dinámico (adws_dir, specs_dir, logs_dir, scripts_dir, prompts_dir, worktrees_dir)
- Añade directorios fijos: .claude/, agents/, app_docs/, ai_docs/

**_add_claude_files():**
- Action: CREATE para proyectos nuevos, SKIP para existing (no sobrescribir configuración existente)
- Settings: .claude/settings.json
- Commands: Loop sobre 18 comandos (prime, start, build, test, lint, feature, bug, chore, patch, implement, commit, pull_request, review, document, health_check, prepare_app, install, track_agentic_kpis)
- Hooks: pre_tool_use.py, post_tool_use.py, stop.py (todos executable=True)
- Hook utils: __init__.py, constants.py

**_add_adw_files():**
- Action: CREATE para nuevos, SKIP para existing
- README.md con documentación completa
- Modules: __init__.py, agent.py, state.py, git_ops.py, workflow_ops.py
- Workflows: adw_sdlc_iso.py, adw_patch_iso.py (ambos executable=True)
- Triggers: __init__.py, trigger_cron.py (executable=True)

**_add_script_files():**
- Action: CREATE para nuevos, SKIP para existing
- Scripts: start.sh, test.sh, lint.sh, build.sh (todos executable=True)
- Usa config.paths.scripts_dir dinámico

**_add_config_files():**
- config.yml: ALWAYS OVERWRITE para capturar user settings actualizados
- .mcp.json: CREATE para nuevos, SKIP para existing
- .gitignore: PATCH para existing (append patterns), CREATE para nuevos

**_add_structure_files():**
- README files para specs/, app_docs/, ai_docs/
- Documentan propósito de cada directorio
- Guías para organizadores de contenido

**apply_plan() Method:**
- Parámetros: `plan: ScaffoldPlan`, `output_dir: Path`, `config: TACConfig`, `force: bool = False`
- Retorna: `ApplyResult` con estadísticas y errores
- Lazy import de FileSystem (TAREA 5.2 - next task)
- Lógica:
  1. Crear todos directorios primero (orden importante)
  2. Procesar cada file operation:
     - Determinar acción efectiva basado en existence + force flag
     - SKIP si action=SKIP
     - Render template o usar content estático
     - Aplicar acción: write_file() o append_file()
     - Make executable si requerido
     - Track estadísticas
  3. Collect errores sin abortar (resilient execution)
  4. Retornar ApplyResult completo

### 3. Template Context
- Todos templates renderizan con `{"config": config}`
- Templates acceden configuración como `{{ config.project.name }}`, `{{ config.commands.start }}`

### 4. Error Handling
- Try/catch por directorio y archivo individual
- Errores no abortan proceso completo (resilient)
- ApplyResult.errors lista todos problemas para review
- Success=False si cualquier error ocurrió

## Relevant Files

Archivos necesarios para implementar la feature:

### Domain Models (Read)
- `tac_bootstrap/domain/models.py` - TACConfig, ProjectSpec, PathsSpec, CommandsSpec y todos los enums
- `tac_bootstrap/domain/plan.py` - ScaffoldPlan, FileOperation, DirectoryOperation, FileAction

### Infrastructure (Read)
- `tac_bootstrap/infrastructure/template_repo.py` - TemplateRepository para rendering

### Documentation (Read)
- `PLAN_TAC_BOOTSTRAP.md` - Plan maestro, contexto de TAREA 5.1
- `app_docs/feature-72bb26fe-scaffolding-plan-models.md` - Modelos de plan
- `app_docs/feature-d2f77c7a-jinja2-template-infrastructure.md` - Template infrastructure

### New Files
- `tac_bootstrap/application/scaffold_service.py` - Servicio completo a crear (provided in issue body)

## Implementation Plan

### Phase 1: Service Foundation
Crear estructura básica del servicio con ApplyResult y constructor

### Phase 2: Build Plan Logic
Implementar build_plan() y todos los métodos _add_*() para construcción de plan completo

### Phase 3: Apply Plan Logic
Implementar apply_plan() con rendering de templates, creación de archivos/directorios, y manejo de errores

## Step by Step Tasks

### Task 1: Create scaffold_service.py file with ApplyResult and ScaffoldService class structure
- Create `/Volumes/MAc1/Celes/tac_bootstrap/trees/c9d3ab60/tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- Add module docstring explaining service responsibilities
- Import required dependencies: dataclass, field, Path, List, Optional, TACConfig, ScaffoldPlan, FileOperation, FileAction, DirectoryOperation, TemplateRepository
- Define ApplyResult dataclass with fields: success, directories_created, files_created, files_skipped, files_overwritten, error, errors
- Define ScaffoldService class with docstring and example
- Implement __init__() accepting optional TemplateRepository and creating default if not provided

### Task 2: Implement build_plan() method and _add_directories()
- Implement build_plan() method signature accepting config and existing_repo flag
- Create ScaffoldPlan instance
- Implement _add_directories() method:
  - Create list of 16 directory tuples with (path, reason)
  - Use config.paths dynamic values (adws_dir, specs_dir, logs_dir, scripts_dir, prompts_dir, worktrees_dir)
  - Add fixed directories: .claude/, agents/, app_docs/, ai_docs/
  - Loop and call plan.add_directory() for each
- Call _add_directories() from build_plan()

### Task 3: Implement _add_claude_files() method
- Determine action based on existing_repo flag (CREATE if new, SKIP if existing)
- Add .claude/settings.json with template
- Add 18 slash commands in loop:
  - Commands list: prime, start, build, test, lint, feature, bug, chore, patch, implement, commit, pull_request, review, document, health_check, prepare_app, install, track_agentic_kpis
  - Template path pattern: `claude/commands/{cmd}.md.j2`
  - Reason: `/{cmd} slash command`
- Add 3 hooks with tuples (filename, reason):
  - pre_tool_use.py, post_tool_use.py, stop.py
  - All with executable=True
  - Template path pattern: `claude/hooks/{hook}.j2`
- Add 2 hook utils:
  - .claude/hooks/utils/__init__.py
  - .claude/hooks/utils/constants.py
- Call from build_plan()

### Task 4: Implement _add_adw_files() method
- Determine action based on existing_repo flag
- Get adws_dir from config.paths
- Add README.md for ADW documentation
- Add 5 modules in loop with tuples (filename, reason):
  - __init__.py, agent.py, state.py, git_ops.py, workflow_ops.py
  - Template path pattern: `adws/adw_modules/{module}.j2`
  - Path pattern: `{adws_dir}/adw_modules/{module}`
- Add 2 workflows with tuples (filename, reason):
  - adw_sdlc_iso.py, adw_patch_iso.py
  - Both executable=True
  - Template path pattern: `adws/{workflow}.j2`
  - Path pattern: `{adws_dir}/{workflow}`
- Add 2 trigger files:
  - adw_triggers/__init__.py
  - adw_triggers/trigger_cron.py (executable=True)
- Call from build_plan()

### Task 5: Implement _add_script_files() and _add_config_files() methods
- Implement _add_script_files():
  - Determine action based on existing_repo flag
  - Get scripts_dir from config.paths
  - Add 4 scripts in loop with tuples (filename, reason):
    - start.sh, test.sh, lint.sh, build.sh
    - All executable=True
    - Template path pattern: `scripts/{script}.j2`
    - Path pattern: `{scripts_dir}/{script}`
- Implement _add_config_files():
  - Add config.yml with OVERWRITE action if existing_repo, CREATE if new (always capture latest settings)
  - Add .mcp.json with CREATE/SKIP based on existing_repo
  - Add .gitignore with PATCH action if existing_repo (append), CREATE if new
- Call both from build_plan()

### Task 6: Implement _add_structure_files() method
- Determine action based on existing_repo flag
- Create list of structure README tuples (file_path, template_path):
  - specs/README.md → structure/specs/README.md.j2
  - app_docs/README.md → structure/app_docs/README.md.j2
  - ai_docs/README.md → structure/ai_docs/README.md.j2
- Use config.paths.specs_dir for dynamic specs path
- Loop and add files with reason="Directory documentation"
- Call from build_plan()

### Task 7: Implement apply_plan() method
- Define method signature accepting plan, output_dir, config, force flag
- Create ApplyResult instance
- Add lazy import: `from tac_bootstrap.infrastructure.fs import FileSystem`
- Create FileSystem instance
- Prepare template_context dict: `{"config": config}`
- Loop through plan.directories:
  - Construct full dir_path: output_dir / dir_op.path
  - Try: fs.ensure_directory(dir_path), increment directories_created
  - Except: append error to result.errors
- Loop through plan.files:
  - Construct full file_path: output_dir / file_op.path
  - Try:
    - Determine actual_action based on file existence and force flag
    - Skip if actual_action is SKIP
    - Render content from template if file_op.template, else use file_op.content or empty string
    - Apply action: fs.append_file() if PATCH, else fs.write_file()
    - Make executable if file_op.executable
    - Track statistics based on actual_action
  - Except: append error to result.errors
- Set result.success = False if any errors occurred
- Set result.error summary message
- Return result

### Task 8: Run validation commands and verify acceptance criteria
- Verify build_plan() generates plan with ~50+ operations
- Verify directories are added in correct order
- Verify .claude/ files include settings, commands, and hooks
- Verify adws/ files include modules and workflows
- Verify scripts are marked as executable
- Verify apply_plan() structure is correct (will test execution in TAREA 5.2 when FileSystem exists)
- Run command: `cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli && uv run python -c "from tac_bootstrap.application.scaffold_service import ScaffoldService; from tac_bootstrap.domain.models import *; service = ScaffoldService(); config = TACConfig(project=ProjectSpec(name='test', language=Language.PYTHON, package_manager=PackageManager.UV), commands=CommandsSpec(start='uv run python -m app', test='uv run pytest'), claude=ClaudeConfig(settings=ClaudeSettings(project_name='test'))); plan = service.build_plan(config); print(plan.summary); print(f'Directories: {plan.total_directories}'); print(f'Files: {plan.total_files}')"`
- Verify output shows correct counts: ~16 directories, ~50+ files
- Run type checking: `cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli && uv run mypy tac_bootstrap/application/scaffold_service.py`
- Run linting: `cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli && uv run ruff check tac_bootstrap/application/scaffold_service.py`

## Testing Strategy

### Unit Tests
No crear tests unitarios formales aún (FASE 7), pero validar manualmente:
- build_plan() con config mínimo retorna ScaffoldPlan válido
- Plan contiene ~16 directorios
- Plan contiene ~50+ archivos
- existing_repo=True cambia acciones correctamente (CREATE → SKIP)
- config.yml siempre OVERWRITE, .gitignore PATCH en existing repos
- Scripts y hooks tienen executable=True
- Template paths son correctos

### Edge Cases
- Config con paths customizados (adws_dir="workflows", scripts_dir="bin")
- Config con comandos vacíos (lint="", build="")
- existing_repo=True vs False diferencias en FileAction
- force=True override de CREATE actions

## Acceptance Criteria

1. build_plan() genera plan completo con ~50+ file operations y ~16 directory operations
2. Directorios se agregan en orden correcto (parent antes que child)
3. Archivos .claude/ incluyen settings.json, 18 comandos slash, 3 hooks, 2 hook utils
4. Archivos adws/ incluyen README, 5 modules, 2 workflows, 2 triggers
5. Scripts son marcados como executable=True (start.sh, test.sh, lint.sh, build.sh)
6. Hooks son marcados como executable=True (pre_tool_use.py, post_tool_use.py, stop.py)
7. Workflows son marcados como executable=True (adw_sdlc_iso.py, adw_patch_iso.py)
8. config.yml usa FileAction.OVERWRITE cuando existing_repo=True
9. .gitignore usa FileAction.PATCH cuando existing_repo=True
10. Otros archivos usan FileAction.SKIP cuando existing_repo=True
11. apply_plan() tiene estructura correcta con try/except por operación
12. ApplyResult tracking estadísticas correctas
13. Template rendering usa context {"config": config}
14. Paths dinámicos usan config.paths correctamente

## Validation Commands

Ejecutar todos los comandos para validar con cero regresiones:

```bash
cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli

# Verify scaffold_service module import
uv run python -c "from tac_bootstrap.application.scaffold_service import ScaffoldService, ApplyResult; print('✓ Module imports successfully')"

# Test build_plan() generates correct plan
uv run python -c "
from tac_bootstrap.application.scaffold_service import ScaffoldService
from tac_bootstrap.domain.models import *

service = ScaffoldService()
config = TACConfig(
    project=ProjectSpec(name='test', language=Language.PYTHON, package_manager=PackageManager.UV),
    commands=CommandsSpec(start='uv run python -m app', test='uv run pytest'),
    claude=ClaudeConfig(settings=ClaudeSettings(project_name='test'))
)

plan = service.build_plan(config)
print(f'Plan Summary: {plan.summary}')
print(f'Total Directories: {plan.total_directories}')
print(f'Total Files: {plan.total_files}')
print(f'Files to Create: {len(plan.get_files_to_create())}')
print(f'Files to Skip: {len(plan.get_files_skipped())}')
print(f'Executable Files: {len(plan.get_executable_files())}')

# Verify counts
assert plan.total_directories >= 16, 'Should have at least 16 directories'
assert plan.total_files >= 50, 'Should have at least 50 files'
print('✓ Plan generation successful')
"

# Test build_plan() with existing_repo=True
uv run python -c "
from tac_bootstrap.application.scaffold_service import ScaffoldService
from tac_bootstrap.domain.models import *

service = ScaffoldService()
config = TACConfig(
    project=ProjectSpec(name='test', language=Language.PYTHON, package_manager=PackageManager.UV),
    commands=CommandsSpec(start='uv run python -m app', test='uv run pytest'),
    claude=ClaudeConfig(settings=ClaudeSettings(project_name='test'))
)

plan = service.build_plan(config, existing_repo=True)
print(f'Existing Repo Plan: {plan.summary}')
print(f'Files to Skip: {len(plan.get_files_skipped())}')
print(f'Files to Patch: {len(plan.get_files_to_patch())}')
print(f'Files to Overwrite: {len(plan.get_files_to_overwrite())}')

# Verify config.yml is overwritten
config_yml_op = next(f for f in plan.files if f.path == 'config.yml')
assert config_yml_op.action.value == 'overwrite', 'config.yml should be overwritten in existing repo'

# Verify .gitignore is patched
gitignore_op = next(f for f in plan.files if f.path == '.gitignore')
assert gitignore_op.action.value == 'patch', '.gitignore should be patched in existing repo'

print('✓ Existing repo plan generation successful')
"

# Type checking
uv run mypy tac_bootstrap/application/scaffold_service.py

# Linting
uv run ruff check tac_bootstrap/application/scaffold_service.py

# Format check
uv run ruff format --check tac_bootstrap/application/scaffold_service.py
```

## Notes

### Implementation Notes
- Esta es TAREA 5.1 de PLAN_TAC_BOOTSTRAP.md (FASE 5: Servicios de Scaffolding)
- El servicio NO crea archivos físicos aún - solo construye el plan
- apply_plan() usa FileSystem que se implementará en TAREA 5.2 (siguiente)
- Por ahora apply_plan() tendrá lazy import de FileSystem
- Templates Jinja2 ya existen en tac_bootstrap/templates/ (creados en FASE 3)
- El código completo está provisto en issue body - copiar exactamente como está

### Next Steps After This Feature
- TAREA 5.2: Implementar FileSystem service (fs.py) con métodos:
  - ensure_directory(), write_file(), append_file(), make_executable()
- TAREA 5.3: Implementar DetectService para auto-detección de proyectos existentes
- TAREA 6.1: Integrar ScaffoldService con CLI commands (init, add-agentic)

### Dependencies Required
Ya instaladas en pyproject.toml (TAREA 2.1):
- jinja2 (template rendering via TemplateRepository)
- pydantic (TACConfig models)
- pathlib (Path handling)

### Template Expectations
Todos los templates deben existir en `tac_bootstrap/templates/`:
- claude/settings.json.j2
- claude/commands/*.md.j2 (18 comandos)
- claude/hooks/*.py.j2 (3 hooks)
- claude/hooks/utils/*.py.j2 (2 utils)
- adws/README.md.j2
- adws/adw_modules/*.py.j2 (5 modules)
- adws/*.py.j2 (2 workflows)
- adws/adw_triggers/*.py.j2 (2 triggers)
- scripts/*.sh.j2 (4 scripts)
- config/config.yml.j2, config/.mcp.json.j2, config/.gitignore.j2
- structure/specs/README.md.j2, structure/app_docs/README.md.j2, structure/ai_docs/README.md.j2

Si algún template falta, TemplateRepository.render() lanzará TemplateNotFoundError - esto es esperado y será manejado en apply_plan() try/except.

### Performance Considerations
- build_plan() es operation de construcción en memoria - muy rápida
- apply_plan() será I/O bound (TAREA 5.2) - minimizar syscalls con batch operations
- Template rendering lazy (solo cuando apply_plan() ejecuta)
- Preview capability allows dry-run sin filesystem writes
