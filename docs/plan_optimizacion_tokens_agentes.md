# Plan para optimizar el uso de tokens (agentes que disparan flujos ADW)

## Objetivo
Reducir **tokens de entrada/salida y costo** en los flujos orquestados (p. ej. `adw_sdlc_iso.py` → plan/build/test/review/document) **sin cambiar la lógica** de los workflows ni degradar la calidad de los resultados.

## No negociables (guardrails)
- Mantener la misma secuencia de fases y criterios de éxito.
- No “recortar” contexto crítico: requisitos, criterios de aceptación, constraints, decisiones ya tomadas, y cambios de código relevantes.
- Cualquier optimización debe ser **medible** y reversible (feature flag / configuración / rollout por etapas).

## Baseline y medición (lo que ya existe)
En ADW ya se guarda un resumen por agente en `ADWState.get_token_summary()` y se publica en el issue al final del SDLC.

**Acciones de baseline (1 día):**
1. Elegir 5–10 issues representativos (chore/bug/feature, chicos y medianos).
2. Ejecutar flujos con el estado/plantillas actuales y archivar:
   - `## 📊 Token Usage Summary` final
   - breakdown por agente
   - tiempo total (si aplica)
3. Definir métricas objetivo:
   - `-25%` tokens de entrada totales
   - `-15%` tokens de salida totales
   - **0 regresiones** en calidad (PR válido, tests, review y docs coherentes)

## Principios de ahorro (sin perder calidad)
1. **Contexto mínimo suficiente**: pasar a cada agente solo lo necesario para su decisión.
2. **Reuso determinístico**: evitar volver a enviar el mismo contexto en múltiples fases.
3. **Salida estructurada y corta**: exigir formato y límites claros por fase (sin prosa).
4. **Gating inteligente**: ejecutar sub-agentes “caros” (expertos, deep review) solo cuando hay señal real de riesgo/ambigüedad.
5. **Compresión con trazabilidad**: resumir sin perder hechos/decisiones, y conservar enlaces a fuentes (archivos, PR, commits).

---

## Propuesta por capas (quick wins → cambios estructurales)

### Capa 1 — Quick wins (1–2 días)
**1) Contratos de salida por fase (format + límites)**
- Planner: salida en JSON (o markdown mínimo) con: objetivo, scope, pasos, riesgos, criterios de aceptación, archivos a tocar.
- Implementor: checklist + lista de archivos y cambios (sin repetir plan).
- Tester: solo fallas + comandos + hipótesis (sin re-explicar el sistema).
- Reviewer: hallazgos priorizados (P0–P3) + acciones concretas.
- Document: cambios de docs en bullets + “qué se documentó” (no narración).

**2) “No repitas contexto” como regla explícita**
Agregar instrucción fija a los prompts: “No re-escribas el issue; referencia por título/ID; usa solo deltas”.

**3) Minimizar el payload del issue siempre**
Ya existe `get_minimal_issue_json()` con truncado. Extender el criterio de “mínimo” a otras fases:
- No pasar bodies completos, comentarios enteros, ni logs completos si no son necesarios.
- Para errores: pasar **solo el snippet** relevante (stacktrace recortado + comando que falla).

**4) Respuestas con “fallback de detalle”**
Pedir output corto por defecto, con la regla: “si falta info, pregunta / genera clarifications, no inventes”.

### Capa 2 — Reuso de contexto entre fases (2–4 días)
**5) Context bundle persistente (por ADW y por tópico)**
Objetivo: que el “contexto común” viaje como un **bundle corto** en vez de duplicarse.

Estructura sugerida:
- `agents/context_bundles/{adw_id}/issue_facts.md`
- `agents/context_bundles/{adw_id}/decisions.md`
- `agents/context_bundles/{adw_id}/repo_constraints.md`
- `agents/context_bundles/{topic}.md` (digests de docs recurrentes)

Regla: cada fase solo adjunta:
- el bundle (o referencias a él),
- cambios desde la última fase (diff),
- y el objetivo específico de la fase.

**6) Compresión de docs (TAC-9)**
Actualmente se detectan tópicos y se cargan docs. Optimizar el “doc payload”:
- Convertir docs a “digest” de 0.5–2 páginas por tópico (definiciones, APIs, convenciones del repo).
- Guardar el digest (cache) y pasar solo eso a los agentes.
- Mantener trazabilidad: “digest deriva de `ai_docs/<...>` y `docs/<...>`”.

### Capa 3 — Gating y ejecución selectiva (3–6 días)
**7) Gating para “expert system”**
Hoy se consulta expertos solo en Plan y Review (bueno). Siguiente paso: consultarlos solo si:
- el issue tiene ambigüedad alta (clarify detecta “critical”),
- o el cambio toca áreas sensibles (auth, pagos, migraciones, infra),
- o la PR supera cierto umbral (archivos tocados, diff grande).

**8) “Two-pass” solo cuando aporta**
En vez de pedir siempre “plan completo + implementación completa”:
- Pass 1 (barato): outline + riesgos + decisiones pendientes.
- Pass 2 (caro): solo si el outline quedó aprobado / sin dudas.

### Capa 4 — Gobernanza de prompts y control de drift (continuo)
**9) Prompt blocks estables para aprovechar caching**
Para modelos/CLIs que soportan cacheo (p. ej. tokens de “cache read/creation”):
- Mantener el preámbulo del prompt **idéntico** entre runs.
- Separar “instrucciones fijas” de “variables” (issue/context) y poner variables al final.
- Evitar timestamps/IDs variables dentro del bloque fijo.

**10) Observabilidad y alertas**
Crear una tabla simple por ejecución:
- tokens por fase
- top 3 agentes más caros
- causa probable (docs, logs, repetición, salida extensa)
Acción: cada sprint atacar el top 1.

---

## Checklist de implementación (orden recomendado)
1. Definir contratos de salida por fase (plantillas de prompts).
2. Introducir bundle mínimo por ADW (facts/decisions).
3. Digests por tópico de docs (cacheado).
4. Gating de expertos por señal (ambigüedad/riesgo).
5. Estandarizar prompts para caching y “no repetición”.

## Validación (A/B sin riesgo)
Para cada cambio:
- Ejecutar 3–5 issues del baseline.
- Comparar:
  - tokens totales
  - tokens por agente
  - calidad (PR compila, tests, review útil, docs correctas)
- Si hay regresión: rollback del cambio o ajustar límites (no forzar recortes).

## Resultado esperado (realista)
- Menos duplicación de issue/docs entre fases.
- Salidas más cortas pero más accionables.
- Mayor reuso de contexto (bundles/digests).
- Reducción significativa de costo sin sacrificar calidad.

---

## Dónde aplicar (mapeo a este repo)
- Plantillas de salida (para forzar brevedad y estructura):
  - `prompts/templates/plan.md` (limitar “Context” a bullets; prohibir repetir el issue; exigir “Files to Modify” sin explicación larga).
  - `prompts/templates/review.md` (formato tabular + top hallazgos; recortar secciones narrativas).
  - `prompts/templates/bug.md`, `prompts/templates/feature.md`, `prompts/templates/chore.md` (mismo patrón: output corto + deltas).
- Orquestación y minimización de payload:
  - `adws/adw_modules/workflow_ops.py` (ya existe `MAX_ISSUE_BODY_LENGTH` y `get_minimal_issue_json()`; extender el enfoque “mínimo” a cualquier otro payload que se inyecte a agentes).
- Persistencia/reuso de contexto:
  - `adws/adw_modules/state.py` (ya guarda `ai_docs_context` y `loaded_docs_topic`; usarlo como “source of truth” para evitar recargar docs en cada fase).
  - `agents/context_bundles/` (existe el directorio; usarlo para digests y bundles por ejecución/tópico).
- Observabilidad:
  - `ADWState.get_token_summary()` (usar el breakdown como KPI principal; agregar tabla histórica fuera del runtime si se necesita).

---

## Mejoras generales de la app (sin afectar calidad)
Además de optimizar tokens, estas mejoras suben DX/robustez y ayudan indirectamente a gastar menos:

1. **Configuración centralizada**
   - Un único config (YAML/ENV) para: modelos por fase, límites de payload/logs, gating de expertos, thresholds de diff, etc.

2. **Modo `--dry-run` y `--resume`**
   - `--dry-run`: mostrar qué fases se ejecutarían y con qué inputs (sin llamadas a agentes).
   - `--resume`: reanudar desde la última fase exitosa usando `agents/{adw_id}/adw_state.json` (evita re-ejecuciones caras).

3. **CLI más consistente**
   - `--help` homogéneo, errores accionables, y un resumen final estándar (rutas, artefactos, comandos, próximos pasos).

4. **Observabilidad “de verdad”**
   - Historial por ADW: tokens/costo/tiempo por fase; top agentes más caros; “causa probable” (docs/logs/repetición/diff).

5. **Bundles de contexto first-class**
   - Generación automática de `agents/context_bundles/{adw_id}/` (facts/decisions/digests) y consumo por fase basado en deltas.

6. **Gating más fino**
   - Expertos/review profundo solo con señal (ambigüedad alta, áreas sensibles, diff grande, tests fallando), configurable.

7. **Seguridad y prevención de loops**
   - Sanitizar/redactar secretos en payloads y logs; endurecer protección anti-webhook-loop.

8. **Contratos de output + validación**
   - Formatos estrictos por fase (JSON/markdown corto), validación de esquema y “fail fast” si no cumple.
