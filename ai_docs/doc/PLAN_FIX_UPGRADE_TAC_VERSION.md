# Plan: Fix tac-bootstrap upgrade - Campo tac_version vs version

## Problema

El comando `tac-bootstrap upgrade` falla con:
```
Error loading config: 1 validation error for TACConfig
tac_version
  Extra inputs are not permitted
```

**Causa raíz:**
- Template genera `tac_version` en config.yml
- Modelo TACConfig espera `version`
- `extra="forbid"` rechaza campos desconocidos

---

## Tareas

### Tarea 1: Cambiar template config.yml.j2 de tac_version a version `/bug`

**Archivos a modificar**:
1. `tac_bootstrap_cli/tac_bootstrap/templates/config/config.yml.j2` (template)

**Prompt para el agente**:

```
Abre el archivo tac_bootstrap_cli/tac_bootstrap/templates/config/config.yml.j2

Busca la línea que contiene:
tac_version: "{{ config.version }}"

Reemplázala con:
version: "{{ config.version }}"

Este cambio hace que nuevos proyectos generen el campo correcto que el modelo TACConfig espera.

## Verificación

Ejecuta: cd tac_bootstrap_cli && uv run pytest tests/ -q
Todos los tests deben pasar (o mostrar errores relacionados con tests que esperan tac_version).
```

---

### Tarea 2: Agregar normalización en upgrade_service.py `/bug`

**Archivos a modificar**:
1. `tac_bootstrap_cli/tac_bootstrap/application/upgrade_service.py` (base)

**Prompt para el agente**:

```
Abre el archivo tac_bootstrap_cli/tac_bootstrap/application/upgrade_service.py

Busca el método que carga la configuración del proyecto target. Puede llamarse `_load_config`, `load_existing_config`, o similar.

Antes de parsear el YAML a TACConfig, agrega normalización para compatibilidad hacia atrás:

1. Busca donde se hace algo como:
   config_data = yaml.safe_load(f)

2. Después de esa línea, agrega:
   # Normalize legacy field names for compatibility
   if "tac_version" in config_data and "version" not in config_data:
       config_data["version"] = config_data.pop("tac_version")

Esto permite que proyectos viejos con tac_version se actualicen correctamente.

## Verificación

Ejecuta: cd tac_bootstrap_cli && uv run pytest tests/test_upgrade_service.py -v
```

---

### Tarea 3: Actualizar tests que esperan tac_version `/chore`

**Archivos a modificar**:
1. `tac_bootstrap_cli/tests/test_scaffold_service.py` (base)
2. `tac_bootstrap_cli/tests/test_upgrade_service.py` (base)

**Prompt para el agente**:

```
Busca en los archivos de tests referencias a "tac_version" y cámbialas a "version":

## ARCHIVO 1: tac_bootstrap_cli/tests/test_scaffold_service.py

Busca líneas como:
- assert "tac_version" in parsed
- assert parsed["tac_version"] == "0.2.0"

Reemplázalas con:
- assert "version" in parsed
- assert parsed["version"] == "0.2.0"

## ARCHIVO 2: tac_bootstrap_cli/tests/test_upgrade_service.py

Busca cualquier referencia a "tac_version" y cámbiala a "version".

## Verificación

Ejecuta: cd tac_bootstrap_cli && uv run pytest tests/ -v -k "version or scaffold or upgrade"
Todos los tests deben pasar.
```

---

### Tarea 4: Ejecutar todos los tests `/chore`

**Prompt para el agente**:

```
Ejecuta todos los tests del proyecto:

cd tac_bootstrap_cli && uv run pytest tests/ -v

Si hay errores:
1. Lee el mensaje de error completo
2. Identifica si es por tac_version → version
3. Corrige el archivo afectado
4. Vuelve a ejecutar los tests

Todos los tests deben pasar (307 tests).
```

---

### Tarea 5: Prueba manual del upgrade `/chore`

**Prompt para el agente**:

```
Realiza una prueba manual del upgrade:

1. Ve al proyecto de prueba que tiene tac_version en su config.yml:
   cd /Users/hernandoescobar/Documents/Celes/tac-test

2. Verifica el contenido actual de config.yml:
   cat config.yml | head -10

3. Ejecuta el upgrade:
   tac-bootstrap upgrade

4. Verifica que:
   - El upgrade detecta la versión correcta
   - No hay error de "Extra inputs are not permitted"
   - El upgrade completa exitosamente
   - config.yml ahora tiene "version" en lugar de "tac_version"

5. Reporta el resultado:
   - Si funciona: confirma que el fix está completo
   - Si falla: describe el error exacto
```

---

### Tarea 6: Actualizar CHANGELOG.md `/chore`

**Archivos a modificar**:
1. `/Volumes/MAc1/Celes/tac_bootstrap/CHANGELOG.md`

**Prompt para el agente**:

```
Abre el archivo /Volumes/MAc1/Celes/tac_bootstrap/CHANGELOG.md

Agrega una nueva entrada para la versión 0.2.2 al inicio (después de # Changelog):

## [0.2.2] - 2026-01-22

### Fixed
- `tac-bootstrap upgrade` now works with projects using legacy `tac_version` field
- Config field normalized from `tac_version` to `version` for consistency

### Changed
- Template `config.yml.j2` now generates `version` instead of `tac_version`
- Upgrade service normalizes legacy field names automatically

---

No modifiques las entradas existentes (0.2.1, 0.2.0, 0.1.0).
```

---

## Verificación Final

Después de completar todas las tareas:

- [ ] Template genera `version` (no `tac_version`)
- [ ] upgrade_service.py normaliza `tac_version` → `version`
- [ ] Tests actualizados para esperar `version`
- [ ] Todos los 307 tests pasan
- [ ] Prueba manual de upgrade exitosa
- [ ] CHANGELOG actualizado con v0.2.2

---

## Respuestas a Ambigüedades

| Pregunta | Respuesta |
|----------|-----------|
| ¿Mantener compatibilidad con tac_version? | Sí. Normalizar en upgrade_service. |
| ¿Qué si el proyecto ya tiene version? | No hacer nada. Solo normalizar si tiene tac_version. |
| ¿Actualizar pyproject.toml version? | No. Solo CHANGELOG. La versión del paquete es 0.2.0. |
| ¿Crear migration script? | No. La normalización en upgrade es suficiente. |
