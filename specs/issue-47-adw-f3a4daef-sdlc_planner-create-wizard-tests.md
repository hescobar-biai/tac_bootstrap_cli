# Feature: Crear Tests de Wizard

## Metadata
issue_number: `47`
adw_id: `f3a4daef`
issue_json: `{"number":47,"title":"TAREA 6: Crear Tests de Wizard","body":"**Archivo a crear:** `tests/test_wizard.py`\n\n**Prompt:**\n```\nCrea tests para el módulo wizard en tests/test_wizard.py.\n\nEl wizard usa Rich para prompts interactivos. Para testear:\n1. Mockear rich.prompt.Prompt\n2. Mockear rich.console.Console\n\nTests a crear:\n\n1. **test_select_from_enum**: Verificar selección de enums\n2. **test_run_init_wizard_defaults**: Wizard con valores por defecto\n3. **test_run_init_wizard_custom**: Wizard con valores custom\n4. **test_run_add_agentic_wizard**: Wizard para repos existentes\n5. **test_wizard_cancellation**: Verificar manejo de Ctrl+C\n\nUsa pytest-mock o unittest.mock para los mocks.\n\nReferencia:\n- tac_bootstrap/interfaces/wizard.py\n- Patrones de mock en tests existentes\n```\n\n**Criterios de aceptación:**\n- [ ] Al menos 5 tests\n- [ ] Mocks funcionan correctamente\n- [ ] Tests pasan sin interacción manual\n"}`

## Feature Description
Crear un archivo de tests completo para el módulo `wizard.py` que contiene las funciones interactivas de configuración del TAC Bootstrap. El wizard usa Rich para mostrar prompts interactivos en terminal, por lo que requiere mocks apropiados para poder testear sin interacción humana.

Los tests deben cubrir:
- Selección de valores enum con `select_from_enum()`
- Wizard de inicialización completo con defaults y valores custom
- Wizard para agregar agentic layer a repos existentes
- Manejo de cancelación (Ctrl+C / SystemExit)

## User Story
As a TAC Bootstrap developer
I want to have comprehensive tests for the wizard module
So that I can ensure the interactive configuration flows work correctly without manual testing

## Problem Statement
El módulo `wizard.py` contiene lógica interactiva compleja usando Rich (prompts, consoles, tablas) que actualmente no tiene tests. Esto hace que:
1. Sea difícil detectar regresiones en el flujo de configuración
2. No haya validación automática de que los wizards funcionan correctamente
3. Cambios al wizard requieran testing manual tedioso

El wizard es crítico porque es el punto de entrada principal para usuarios nuevos del CLI.

## Solution Statement
Crear `tests/test_wizard.py` con mocks de Rich para simular interacción del usuario. Usar `unittest.mock.patch` para mockear:
- `rich.prompt.Prompt.ask()` para simular respuestas del usuario
- `rich.prompt.Confirm.ask()` para simular confirmaciones
- `rich.console.Console` para evitar output en tests

Seguir los patrones existentes en `test_scaffold_service.py` y `test_cli.py` que ya usan mocks efectivamente.

## Relevant Files
Archivos necesarios para implementar la feature:

- **tac_bootstrap_cli/tac_bootstrap/interfaces/wizard.py** - Módulo a testear, contiene funciones:
  - `select_from_enum()` - Selección interactiva de enums
  - `run_init_wizard()` - Wizard para proyectos nuevos
  - `run_add_agentic_wizard()` - Wizard para repos existentes
  - `_show_config_summary()` - Helper para mostrar resumen

- **tac_bootstrap_cli/tests/test_scaffold_service.py** - Referencia para patrones de testing con fixtures y mocks
- **tac_bootstrap_cli/tests/test_plan.py** - Referencia para estructura de tests con clases
- **tac_bootstrap_cli/tac_bootstrap/domain/models.py** - Modelos usados (Language, Framework, TACConfig, etc.)

### New Files
- **tac_bootstrap_cli/tests/test_wizard.py** - Archivo principal de tests del wizard

## Implementation Plan

### Phase 1: Foundation
Preparar estructura de tests y fixtures base:
1. Crear `test_wizard.py` con imports necesarios
2. Definir fixtures para mocks de Rich (Console, Prompt, Confirm)
3. Definir fixtures para objetos de prueba (TACConfig mock, detected project mock)

### Phase 2: Core Implementation
Implementar los 5 tests principales requeridos:
1. `test_select_from_enum` - Verificar selección de enum con default
2. `test_run_init_wizard_defaults` - Wizard acepta todos los defaults
3. `test_run_init_wizard_custom` - Wizard con selecciones personalizadas
4. `test_run_add_agentic_wizard` - Wizard para repo existente
5. `test_wizard_cancellation` - Manejo de SystemExit cuando usuario cancela

### Phase 3: Integration
Agregar tests adicionales para cobertura completa:
1. Tests edge cases (enums filtrados, sin opciones válidas)
2. Tests de helpers internos (`_show_config_summary`)
3. Verificar que tests pasan en el pipeline de validación

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Crear estructura base y fixtures
- Crear archivo `tac_bootstrap_cli/tests/test_wizard.py`
- Agregar imports necesarios (pytest, unittest.mock, wizard module, domain models)
- Crear fixture `mock_console` que patchea `rich.console.Console`
- Crear fixture `mock_prompt` que patchea `rich.prompt.Prompt.ask`
- Crear fixture `mock_confirm` que patchea `rich.prompt.Confirm.ask`
- Crear fixture `sample_detected_project` con objeto mock para detected project

### Task 2: Implementar test_select_from_enum
- Crear clase `TestSelectFromEnum`
- Implementar test que verifica selección con default (Language.PYTHON)
- Mockear Prompt.ask para retornar "1" (primera opción)
- Verificar que retorna el enum correcto
- Agregar test con filtro (frameworks válidos para un language)
- Verificar que tabla se muestra con opciones correctas

### Task 3: Implementar test_run_init_wizard_defaults
- Crear clase `TestRunInitWizard`
- Implementar test que acepta todos los defaults
- Mockear Prompt.ask para retornar valores default ("1" para cada select)
- Mockear Confirm.ask para retornar True
- Verificar que TACConfig resultante tiene valores correctos
- Verificar estructura: project.name, project.language, commands, etc.

### Task 4: Implementar test_run_init_wizard_custom
- Implementar test con valores custom
- Mockear Prompt.ask con side_effect para retornar diferentes opciones
- Simular usuario que selecciona TypeScript, React, npm, etc.
- Simular usuario que customiza comandos (start, test, lint)
- Verificar que TACConfig refleja las selecciones custom

### Task 5: Implementar test_run_add_agentic_wizard
- Crear clase `TestRunAddAgenticWizard`
- Usar fixture `sample_detected_project` con valores pre-detectados
- Mockear prompts para aceptar/modificar valores detectados
- Verificar que config usa detected values como defaults
- Verificar que mode = ProjectMode.EXISTING
- Verificar que repo_path se preserva

### Task 6: Implementar test_wizard_cancellation
- Implementar test que simula usuario cancelando (Ctrl+C)
- Mockear Confirm.ask en confirmación final para retornar False
- Verificar que levanta SystemExit(0)
- Usar pytest.raises(SystemExit) para capturar la excepción
- Verificar que mensaje de "Aborted" se muestra

### Task 7: Tests adicionales y edge cases
- Test `select_from_enum` sin opciones válidas (debería raise ValueError)
- Test `select_from_enum` con filter_fn que elimina todas las opciones
- Test que verifica que console.print se llama con mensajes correctos
- Test de `_show_config_summary` para verificar tabla de resumen

### Task 8: Validación final
- Ejecutar `cd tac_bootstrap_cli && uv run pytest tests/test_wizard.py -v --tb=short`
- Verificar que al menos 5 tests pasan
- Verificar que no hay interacción manual requerida
- Ejecutar suite completa de validación (ver Validation Commands)
- Verificar que todos los criterios de aceptación se cumplen

## Testing Strategy

### Unit Tests
Los tests deben ser unitarios y enfocados:

1. **Mocking de Rich components**:
   - `@patch('tac_bootstrap.interfaces.wizard.console')` para Console
   - `@patch('tac_bootstrap.interfaces.wizard.Prompt.ask')` para prompts
   - `@patch('tac_bootstrap.interfaces.wizard.Confirm.ask')` para confirmaciones

2. **Fixtures reutilizables**:
   ```python
   @pytest.fixture
   def mock_prompt(mocker):
       return mocker.patch('tac_bootstrap.interfaces.wizard.Prompt.ask')

   @pytest.fixture
   def mock_confirm(mocker):
       return mocker.patch('tac_bootstrap.interfaces.wizard.Confirm.ask')
   ```

3. **Test organization con clases**:
   - `TestSelectFromEnum` para tests de selección enum
   - `TestRunInitWizard` para wizard de init
   - `TestRunAddAgenticWizard` para wizard add-agentic

### Edge Cases
1. **Enum sin opciones válidas**: filter_fn que elimina todas las opciones → ValueError
2. **Usuario cancela**: Confirm retorna False → SystemExit(0)
3. **Default no está en opciones filtradas**: debería usar primera opción válida
4. **Valores None en detected project**: deberían usar fallback defaults
5. **Comandos vacíos**: strings vacíos deberían ser aceptables

## Acceptance Criteria
- [x] Archivo `tests/test_wizard.py` creado con al menos 5 tests
- [x] Test `test_select_from_enum` verifica selección de enums con defaults
- [x] Test `test_run_init_wizard_defaults` verifica wizard con valores por defecto
- [x] Test `test_run_init_wizard_custom` verifica wizard con valores personalizados
- [x] Test `test_run_add_agentic_wizard` verifica wizard para repos existentes
- [x] Test `test_wizard_cancellation` verifica manejo de cancelación
- [x] Mocks de Rich funcionan correctamente (no requieren interacción manual)
- [x] Todos los tests pasan al ejecutar pytest
- [x] Tests siguen convenciones del proyecto (fixtures, clases, docstrings)
- [x] No hay regresiones en tests existentes

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/test_wizard.py -v --tb=short` - Tests del wizard
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios completos
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Patrones de Mocking de Rich
```python
from unittest.mock import MagicMock, patch
import pytest

@pytest.fixture
def mock_prompt(mocker):
    """Mock Prompt.ask to simulate user input."""
    return mocker.patch('tac_bootstrap.interfaces.wizard.Prompt.ask')

@pytest.fixture
def mock_confirm(mocker):
    """Mock Confirm.ask to simulate yes/no confirmations."""
    return mocker.patch('tac_bootstrap.interfaces.wizard.Confirm.ask')

def test_example(mock_prompt, mock_confirm):
    # Simulate user selecting option 1, then entering "test", then confirming
    mock_prompt.side_effect = ["1", "test"]
    mock_confirm.return_value = True

    result = run_init_wizard("myproject")
    assert result.project.name == "myproject"
```

### Mock de Detected Project
El wizard `run_add_agentic_wizard` recibe un objeto `detected` con atributos:
```python
class MockDetected:
    language = Language.PYTHON
    framework = Framework.FASTAPI
    package_manager = PackageManager.UV
    commands = {"start": "uv run fastapi", "test": "uv run pytest"}
    app_root = "src"
```

### Consideraciones
- Usar `pytest-mock` (mocker fixture) o `unittest.mock.patch` - ambos funcionan
- Los mocks deben patchear el path completo: `tac_bootstrap.interfaces.wizard.Prompt`
- Console output no es crítico verificar - enfocarse en lógica y resultados
- SystemExit en wizard es comportamiento esperado cuando usuario cancela
