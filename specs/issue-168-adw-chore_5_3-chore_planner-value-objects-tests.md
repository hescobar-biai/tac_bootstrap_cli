# Chore: Tests para value objects

## Metadata
issue_number: `168`
adw_id: `chore_5_3`
issue_json: `{"number":168,"title":"Tarea 5.3: Tests para value objects","body":"chore\n/adw_sdlc_zte_iso\n/adw_id: chore_5_3\n\n**Tipo**: chore\n**Ganancia**: Garantia de que la validacion de value objects funciona correctamente.\n\n**Instrucciones para el agente**:\n\n1. Crear `tac_bootstrap_cli/tests/test_value_objects.py`\n2. Tests para ProjectName:\n   - `\"My App\"` → `\"my-app\"`\n   - `\"  Hello World  \"` → `\"hello-world\"`\n   - `\"app@#$name\"` → `\"appname\"`\n   - `\"\"` → raises ValueError\n   - `\"---\"` → raises ValueError\n3. Tests para TemplatePath:\n   - `\"claude/commands/test.md.j2\"` → valido\n   - `\"../../../etc/passwd\"` → raises ValueError\n   - `\"/absolute/path\"` → raises ValueError\n4. Tests para SemanticVersion:\n   - `\"0.2.2\" < \"0.3.0\"` → True\n   - `\"1.0.0\" > \"0.99.99\"` → True\n   - `\"abc\"` → raises ValueError\n\n**Criterios de aceptacion**:\n- `uv run pytest tests/test_value_objects.py` pasa\n- Edge cases cubiertos- \n# FASE 5: Value Objects y IDK Docstrings\n\n**Objetivo**: Mejorar la calidad del codigo del CLI con value objects tipados y documentacion estandarizada.\n\n**Ganancia de la fase**: Codigo mas mantenible, menos bugs por strings invalidos, y documentacion que facilita la busqueda semantica por agentes AI.\n"}`

## Chore Description
Crear tests comprehensivos para los value objects (ProjectName, TemplatePath, SemanticVersion) que ya existen en el codebase. Los value objects fueron implementados en la tarea 5.2 (chore_5_2) y ya están integrados en el código actual en `tac_bootstrap_cli/tac_bootstrap/domain/value_objects.py`.

Los tests deben verificar:
- **Casos válidos**: Sanitización/normalización correcta de inputs válidos
- **Casos inválidos**: Rechazo de inputs inválidos con ValueError apropiado
- **API completa**: Atributos, métodos y operadores de comparación

## Relevant Files
Archivos existentes que serán probados:

- `tac_bootstrap_cli/tac_bootstrap/domain/value_objects.py` - Implementación de los value objects (ya existe, contiene ProjectName, TemplatePath, SemanticVersion)

### New Files
- `tac_bootstrap_cli/tests/test_value_objects.py` - Suite de tests comprehensiva (ya existe pero debe ser verificada)

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Verificar archivo de tests existe
- Confirmar que `tac_bootstrap_cli/tests/test_value_objects.py` ya existe
- Revisar que los tests cubren todos los casos especificados en el issue

### Task 2: Ejecutar tests de ProjectName
- Verificar sanitización básica: `"My App"` → `"my-app"`, `"  Hello World  "` → `"hello-world"`
- Verificar remoción de caracteres especiales: `"app@#$name"` → `"appname"`
- Verificar rechazo de strings vacíos: `""` → ValueError
- Verificar rechazo de solo hyphens: `"---"` → ValueError
- Verificar límite de 64 caracteres (boundary: exactamente 64 OK, 65 falla)
- Verificar edge cases: espacios múltiples, hyphens consecutivos, mayúsculas/minúsculas
- Verificar que es subclase de str

### Task 3: Ejecutar tests de TemplatePath
- Verificar paths relativos válidos: `"claude/commands/test.md.j2"` → válido
- Verificar rechazo de traversal: `"../../../etc/passwd"` → ValueError
- Verificar rechazo de paths absolutos: `"/absolute/path"` → ValueError
- Verificar paths con dot-relative: `"./templates/file"` → válido
- Verificar rechazo de strings vacíos
- Verificar paths con dots en nombres de archivo (no ..)
- Verificar que es subclase de str

### Task 4: Ejecutar tests de SemanticVersion
- Verificar parsing correcto: `SemanticVersion("1.2.3").tuple` → `(1, 2, 3)`
- Verificar comparaciones: `"0.2.2" < "0.3.0"` → True, `"1.0.0" > "0.99.99"` → True
- Verificar rechazo de formato inválido: `"abc"` → ValueError
- Verificar todos los operadores: ==, !=, <, <=, >, >=
- Verificar comparación con strings
- Verificar hash consistency para uso en sets/dicts
- Verificar sorting de versiones
- Verificar edge cases: "0.0.0", números grandes, formatos inválidos
- Verificar que es subclase de str

### Task 5: Validar cobertura de edge cases
- Confirmar que todos los edge cases mencionados en el issue están cubiertos
- Verificar tests de tipos inválidos (non-string)
- Verificar comportamiento con casos límite

### Task 6: Ejecutar validation commands
- Ejecutar todos los comandos de validación
- Confirmar cero regresiones

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/test_value_objects.py -v --tb=short` - Tests específicos
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios completos
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- Los value objects ya están implementados en `tac_bootstrap/domain/value_objects.py` (copiados de chore_5_2)
- El archivo de tests `test_value_objects.py` ya existe y contiene 398 líneas de tests comprehensivos
- Esta tarea es principalmente de verificación: confirmar que los tests existentes cubren todos los requisitos
- Los value objects heredan de `str` para compatibilidad con Pydantic v2
- ProjectName: máximo 64 caracteres, sanitización a lowercase-hyphen
- TemplatePath: validación de seguridad (no .., no paths absolutos)
- SemanticVersion: formato estricto X.Y.Z, soporte completo de comparación
