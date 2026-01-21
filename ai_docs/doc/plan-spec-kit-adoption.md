# Plan de Adopción: Conceptos de spec-kit para TAC Bootstrap CLI

**Fecha:** 2026-01-21
**Referencia:** https://github.com/github/spec-kit
**Estado:** Planificado

## Resumen Ejecutivo

Después de investigar spec-kit de GitHub, se identificaron 3 conceptos valiosos para adoptar en TAC Bootstrap CLI. Este documento contiene las tareas priorizadas con prompts ejecutables para cada una.

---

## Tarea 1: Checklist de Validación en /review (Prioridad ALTA)

### Descripción
Extender el comando `/review` para generar checklists de validación automáticos basados en la especificación. Concepto inspirado en `/speckit.checklist` - "unit tests para requisitos en inglés".

### Beneficio
- Validación sistemática antes de ship
- Reduce bugs escapados a producción
- Documenta criterios de aceptación verificables

### Prompt para Ejecutar

```
Necesito extender el comando /review en TAC Bootstrap CLI para que genere un checklist de validación automático.

El checklist debe:
1. Leer el archivo de especificación (spec file)
2. Extraer los requisitos y criterios de aceptación
3. Generar una lista de verificación con formato:
   - [ ] Requisito 1 - Descripción
   - [ ] Requisito 2 - Descripción
   ...
4. Incluir validaciones técnicas automáticas:
   - [ ] Tests pasan
   - [ ] Linting sin errores
   - [ ] Build exitoso
5. Guardar el checklist en el mismo directorio que el spec

Archivos a modificar:
- tac_bootstrap_cli/tac_bootstrap/templates/commands/review.md.j2
- Posiblemente crear un nuevo template para el checklist

El output del checklist debe poder usarse como comentario en GitHub PR.
```

### Archivos Involucrados
- `templates/commands/review.md.j2`
- Nuevo: `templates/checklist.md.j2` (opcional)

### Criterios de Aceptación
- [ ] `/review` genera checklist basado en spec
- [ ] Checklist incluye requisitos del spec
- [ ] Checklist incluye validaciones técnicas
- [ ] Formato compatible con GitHub markdown

---

## Tarea 2: Constitution/Principios Gobernantes en /prime (Prioridad MEDIA)

### Descripción
Extender el comando `/prime` para generar un archivo `constitution.md` que defina los principios gobernantes del proyecto. Inspirado en `/speckit.constitution`.

### Beneficio
- Consistencia en decisiones de desarrollo
- Onboarding más rápido para nuevos agentes/desarrolladores
- Reglas claras para code review

### Prompt para Ejecutar

```
Necesito extender el comando /prime en TAC Bootstrap CLI para que genere un archivo de constitution/principios gobernantes.

El archivo constitution.md debe incluir secciones para:
1. **Principios de Código**
   - Estilo de código preferido
   - Patrones a usar/evitar
   - Convenciones de naming

2. **Estándares de Testing**
   - Cobertura mínima esperada
   - Tipos de tests requeridos
   - Estrategia de mocking

3. **Arquitectura**
   - Estructura de carpetas
   - Separación de responsabilidades
   - Dependencias permitidas

4. **UX/DX Guidelines**
   - Manejo de errores
   - Mensajes al usuario
   - Documentación requerida

5. **Performance**
   - Límites aceptables
   - Optimizaciones requeridas

Archivos a modificar:
- tac_bootstrap_cli/tac_bootstrap/templates/commands/prime.md.j2
- Crear nuevo template: templates/constitution.md.j2

El constitution debe ser parametrizable con {{ config.* }} para adaptarse a cada proyecto generado.
```

### Archivos Involucrados
- `templates/commands/prime.md.j2`
- Nuevo: `templates/constitution.md.j2`

### Criterios de Aceptación
- [ ] `/prime` genera `constitution.md` en el proyecto
- [ ] Constitution tiene las 5 secciones definidas
- [ ] Valores parametrizables con config
- [ ] Otros comandos pueden referenciar el constitution

---

## Tarea 3: Fase de Clarificación en ADW Planning (Prioridad BAJA)

### Descripción
Añadir una fase opcional de clarificación en `adw_plan_iso.py` que identifique ambigüedades en el issue antes de generar el plan. Inspirado en `/speckit.clarify`.

### Beneficio
- Reduce implementaciones incorrectas
- Fuerza definición clara de requisitos
- Documenta decisiones tomadas

### Prompt para Ejecutar

```
Necesito añadir una fase de clarificación opcional en el workflow adw_plan_iso.py de TAC Bootstrap CLI.

La fase de clarificación debe:
1. Analizar el issue de GitHub buscando:
   - Requisitos ambiguos o vagos
   - Información faltante
   - Decisiones técnicas no especificadas
   - Casos edge no definidos

2. Si encuentra ambigüedades:
   - Generar lista de preguntas específicas
   - Postear comentario en el issue pidiendo clarificación
   - Pausar el workflow hasta obtener respuestas
   - O continuar con assumptions documentadas

3. Documentar clarificaciones:
   - Guardar preguntas y respuestas en el spec
   - Incluir assumptions tomadas

Archivos a modificar:
- tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_plan_iso.py.j2
- Posiblemente adw_modules/workflow_ops.py.j2

El flag --skip-clarify debe permitir saltar esta fase si no se necesita.
```

### Archivos Involucrados
- `templates/adws/adw_plan_iso.py.j2`
- `templates/adws/adw_modules/workflow_ops.py.j2`

### Criterios de Aceptación
- [ ] adw_plan_iso tiene fase de clarificación
- [ ] Detecta ambigüedades en issues
- [ ] Puede postear preguntas en GitHub
- [ ] Flag --skip-clarify funciona
- [ ] Clarificaciones se documentan en spec

---

## Orden de Ejecución Recomendado

| # | Tarea | Prioridad | Dependencias | Esfuerzo |
|---|-------|-----------|--------------|----------|
| 1 | Checklist en /review | Alta | Ninguna | Medio |
| 2 | Constitution en /prime | Media | Ninguna | Medio |
| 3 | Clarify en ADW | Baja | Ninguna | Alto |

## Notas

- Las tareas son independientes y pueden ejecutarse en cualquier orden
- Se recomienda empezar por Checklist por su alto impacto inmediato
- Constitution mejora la consistencia a largo plazo
- Clarify es nice-to-have, ya tenemos AskUserQuestion para esto

## Conceptos NO Adoptados (y por qué)

| Concepto | Razón para NO adoptar |
|----------|----------------------|
| Namespace `/speckit.*` | Nuestros comandos directos son más intuitivos |
| Multi-agente (17+) | TAC Bootstrap optimizado para Claude Code |
| Estructura rígida de carpetas | Nuestra estructura es más flexible |
| `/speckit.tasks` separado | Ya integrado en nuestro /implement |
