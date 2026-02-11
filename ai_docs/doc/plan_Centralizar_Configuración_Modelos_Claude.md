# Plan Detallado: Centralizar Configuración de Modelos Claude

  **Fecha**: 2026-02-10                                                                                                                                                       
  **Versión Target**: 0.11.0
  **Descripción**: Centralizar la configuración de modelos Claude (Opus, Sonnet, Haiku) usando jerarquía de 3 niveles (env vars → config.yml → hardcoded defaults) para       
  permitir configuración runtime sin redeployment.                                       

  ---

  ## Assumptions

  1. **Config Cache Existe**: `_CONFIG_CACHE` ya existe en `workflow_ops.py` y puede ser reutilizado
  2. **Backward Compatibility**: Todos los cambios son 100% backward compatible (no breaking changes)
  3. **Imports Dinámicos**: Se usan imports dentro de funciones para evitar imports circulares
  4. **Template Sync**: Todos los cambios en archivos raíz se sincronizan a plantillas `.j2` simultáneamente
  5. **Tests Manuales**: Los tests son manuales, no hay suite de tests automatizados a actualizar

  ---

  ## Tasks

  ### Task 1: Extender config.yml con Model IDs

  **Classification**: [CHORE]

  **ADW Metadata**:
  - Tipo: /chore
  - Workflow: /adw_sdlc_zte_iso
  - ID: /adw_id: chore_model_config_task_01

  **Title**: Add optional model ID overrides to config.yml

  **Description**:
  1. Abre `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/config.yml`
  2. Localiza la sección `agentic.model_policy`
  3. Agrega los siguientes campos opcionales DESPUÉS de `fallback`:
     ```yaml
     agentic:
       model_policy:
         default: "sonnet"
         heavy: "opus"
         fallback: "haiku"
         # NUEVO: Fully qualified model IDs (optional)
         opus_model: "claude-opus-4-5-20251101"
         sonnet_model: "claude-sonnet-4-5-20250929"
         haiku_model: "claude-haiku-4-5-20251001"
  4. Guardar archivo

  Acceptance Criteria:
  - ✅ config.yml contiene los 3 campos nuevos: opus_model, sonnet_model, haiku_model
  - ✅ Campos están DESPUÉS de fallback
  - ✅ Valores son model IDs fully qualified

  Impacted Paths:
  - /Users/hernandoescobar/Documents/Celes/tac_bootstrap/config.yml

  ---
  Task 2: Extender ModelPolicy Pydantic con Campos Opcionales

  Classification: [CHORE]

  ADW Metadata:
  - Tipo: /chore
  - Workflow: /adw_sdlc_zte_iso
  - ID: /adw_id: chore_model_config_task_02

  Title: Add optional model ID fields to ModelPolicy Pydantic class

  Description:
  1. Abre /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/domain/models.py
  2. Localiza la clase ModelPolicy (alrededor de línea 299-307)
  3. Agrega 3 nuevos campos Optional[str] después del campo fallback:
  class ModelPolicy(BaseModel):
      default: str = Field(default="sonnet", description="Default model for standard tasks")
      heavy: str = Field(default="opus", description="Heavy model for complex tasks")
      fallback: str = Field(default="haiku", description="Fallback model for quota/rate limits")

      # NUEVO: Optional model ID overrides
      opus_model: Optional[str] = Field(
          default=None,
          description="Override Opus model ID (e.g., 'claude-opus-4-5-20251101')"
      )
      sonnet_model: Optional[str] = Field(
          default=None,
          description="Override Sonnet model ID (e.g., 'claude-sonnet-4-5-20250929')"
      )
      haiku_model: Optional[str] = Field(
          default=None,
          description="Override Haiku model ID (e.g., 'claude-haiku-4-5-20251001')"
      )
  4. Guardar archivo

  Acceptance Criteria:
  - ✅ ModelPolicy tiene 3 campos nuevos: opus_model, sonnet_model, haiku_model
  - ✅ Todos son Optional[str] con default=None
  - ✅ Tienen Field descriptions claras
  - ✅ Archivo compila sin errores

  Impacted Paths:
  - /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/domain/models.py

  ---
  Task 3: Crear Función get_model_id() en workflow_ops.py

  Classification: [FEATURE]

  ADW Metadata:
  - Tipo: /feature
  - Workflow: /adw_sdlc_zte_iso
  - ID: /adw_id: feature_model_config_task_03

  Title: Implement get_model_id() function with 3-tier resolution

  Description:
  1. Abre /Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/workflow_ops.py
  2. Ubica la línea 136 (después de imports y before existing functions)
  3. Agrega la función get_model_id() con resolución en 3 niveles:
  def get_model_id(model_type: Literal["opus", "sonnet", "haiku"]) -> str:
      """Get fully qualified model ID with 3-tier resolution.

      Resolution order:
      1. Environment variable (ANTHROPIC_DEFAULT_{TYPE}_MODEL)
      2. Config file (config.yml: agentic.model_policy.{type}_model)
      3. Hardcoded default

      Args:
          model_type: One of "opus", "sonnet", "haiku"

      Returns:
          Fully qualified model ID string (e.g., "claude-opus-4-5-20251101")
      """
      import os
      from typing import Literal

      # Tier 1: Environment variable
      env_var = f"ANTHROPIC_DEFAULT_{model_type.upper()}_MODEL"
      env_value = os.getenv(env_var)
      if env_value:
          return env_value

      # Tier 2: Config file
      config = load_config()  # Already exists in this module
      model_policy = config.get("agentic", {}).get("model_policy", {})
      config_value = model_policy.get(f"{model_type}_model")
      if config_value:
          return config_value

      # Tier 3: Hardcoded defaults
      defaults = {
          "opus": "claude-opus-4-5-20251101",
          "sonnet": "claude-sonnet-4-5-20250929",
          "haiku": "claude-haiku-4-5-20251001",
      }
      return defaults[model_type]
  4. Guardar archivo

  Acceptance Criteria:
  - ✅ Función existe y es importable
  - ✅ Maneja los 3 tipos: opus, sonnet, haiku
  - ✅ Intenta env var primero, luego config, luego defaults
  - ✅ Retorna string válido en todos los casos
  - ✅ Tiene docstring completo

  Impacted Paths:
  - /Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/workflow_ops.py

  ---
  Task 4: Refactorizar ModelName Enum a Funciones Dinámicas

  Classification: [CHORE]

  ADW Metadata:
  - Tipo: /chore
  - Workflow: /adw_sdlc_zte_iso
  - ID: /adw_id: chore_model_config_task_04

  Title: Convert ModelName enum constants to dynamic resolution functions

  Description:
  1. Abre /Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/adw_agent_sdk.py
  2. Localiza la clase ModelName(str, Enum) (alrededor de línea 43-55)
  3. Reemplaza OPUS, SONNET, HAIKU con métodos estáticos:
  class ModelName(str, Enum):
      """Available Claude models (dynamically resolved from config)."""

      @staticmethod
      def get_opus() -> str:
          """Get current Opus model ID from config/env."""
          from adw_modules.workflow_ops import get_model_id
          return get_model_id("opus")

      @staticmethod
      def get_sonnet() -> str:
          """Get current Sonnet model ID from config/env."""
          from adw_modules.workflow_ops import get_model_id
          return get_model_id("sonnet")

      @staticmethod
      def get_haiku() -> str:
          """Get current Haiku model ID from config/env."""
          from adw_modules.workflow_ops import get_model_id
          return get_model_id("haiku")
  4. Mantén backward compatibility: Los lugares que usan ModelName.OPUS.value deben seguir funcionando
  5. Guardar archivo

  Acceptance Criteria:
  - ✅ ModelName tiene 3 métodos estáticos: get_opus(), get_sonnet(), get_haiku()
  - ✅ Cada uno retorna string del get_model_id()
  - ✅ No hay hardcoded model IDs en esta clase
  - ✅ Imports dinámicos (dentro de funciones)

  Impacted Paths:
  - /Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/adw_agent_sdk.py

  ---
  Task 5: Refactorizar MODEL_FALLBACK_CHAIN a Función Dinámica

  Classification: [CHORE]

  ADW Metadata:
  - Tipo: /chore
  - Workflow: /adw_sdlc_zte_iso
  - ID: /adw_id: chore_model_config_task_05

  Title: Convert MODEL_FALLBACK_CHAIN from static dict to dynamic function

  Description:
  1. Abre /Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/agent.py
  2. Localiza la constante MODEL_FALLBACK_CHAIN (alrededor de línea 720-724)
  3. Reemplaza con función dinámica:
  def get_model_fallback_chain() -> Dict[str, Optional[str]]:
      """Get model fallback chain with resolved IDs.

      Returns:
          Dict mapping from model ID to fallback model ID
          Example: {
              "claude-opus-4-5-20251101": "claude-sonnet-4-5-20250929",
              "claude-sonnet-4-5-20250929": "claude-haiku-4-5-20251001",
              "claude-haiku-4-5-20251001": "claude-haiku-4-5-20251001"
          }
      """
      from adw_modules.workflow_ops import get_model_id

      opus = get_model_id("opus")
      sonnet = get_model_id("sonnet")
      haiku = get_model_id("haiku")

      return {
          opus: sonnet,
          sonnet: haiku,
          haiku: haiku,
      }


  def get_fallback_model(current_model: str) -> Optional[str]:
      """Get fallback model for given current model.

      Args:
          current_model: Current model ID

      Returns:
          Fallback model ID, or None if not found
      """
      chain = get_model_fallback_chain()
      return chain.get(current_model)
  4. Busca y reemplaza TODAS las referencias a MODEL_FALLBACK_CHAIN en el archivo con get_model_fallback_chain()
  5. Guardar archivo

  Acceptance Criteria:
  - ✅ Función get_model_fallback_chain() existe
  - ✅ Función get_fallback_model() existe
  - ✅ NO hay constante MODEL_FALLBACK_CHAIN
  - ✅ Todas las referencias usan la función
  - ✅ Imports dinámicos

  Impacted Paths:
  - /Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/agent.py

  ---
  Task 6: Refactorizar FAST_MODEL a Función Dinámica

  Classification: [CHORE]

  ADW Metadata:
  - Tipo: /chore
  - Workflow: /adw_sdlc_zte_iso
  - ID: /adw_id: chore_model_config_task_06

  Title: Convert FAST_MODEL from hardcoded constant to dynamic resolution

  Description:
  1. Abre /Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/adw_summarizer.py
  2. Localiza la constante FAST_MODEL (alrededor de línea 32)
  3. Reemplaza con función:
  def get_fast_model() -> str:
      """Get fast model ID for summarization (uses Haiku by default).

      Returns:
          Fully qualified Haiku model ID
      """
      from adw_modules.workflow_ops import get_model_id
      return get_model_id("haiku")


  # Backward compatibility: can still use FAST_MODEL if needed
  FAST_MODEL = get_fast_model()
  4. Busca y reemplaza TODAS las referencias a FAST_MODEL en el archivo con llamadas a get_fast_model()
  5. Guardar archivo

  Acceptance Criteria:
  - ✅ Función get_fast_model() existe
  - ✅ Retorna haiku model ID dinámicamente
  - ✅ Todas las referencias usan la función
  - ✅ Backward compatibility mantenida

  Impacted Paths:
  - /Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/adw_summarizer.py

  ---
  Task 7: Refactorizar adw_sdlc_zte_iso.py - Uso Dinámico de Modelos

  Classification: [CHORE]

  ADW Metadata:
  - Tipo: /chore
  - Workflow: /adw_sdlc_zte_iso
  - ID: /adw_id: chore_model_config_task_07

  Title: Update adw_sdlc_zte_iso.py to use dynamic model resolution

  Description:
  1. Abre /Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_sdlc_zte_iso.py
  2. Agrega import al inicio: from adw_modules.workflow_ops import get_model_id
  3. Busca TODAS las líneas con track_agent_start() que tengan model hardcoded
  4. Reemplaza patrón:
  # ANTES
  agent_id = track_agent_start(adw_id, "adw_plan_iso", model="claude-sonnet-4-5-20250929")

  # DESPUÉS
  agent_id = track_agent_start(adw_id, "adw_plan_iso", model=get_model_id("sonnet"))
  5. Identifica el tipo de modelo a usar basado en el contexto:
    - Plan/Build/Test/Review: sonnet
    - Heavy tasks (optional): opus
    - Fast tasks (optional): haiku
  6. Guardar archivo

  Acceptance Criteria:
  - ✅ Todas las llamadas track_agent_start() usan get_model_id()
  - ✅ NO hay model IDs hardcoded en track_agent_start()
  - ✅ Los tipos de modelo (sonnet/opus/haiku) son consistentes con la lógica de negocio
  - ✅ Import de get_model_id presente

  Impacted Paths:
  - /Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_sdlc_zte_iso.py

  ---
  Task 8: Refactorizar adw_sdlc_iso.py - Uso Dinámico de Modelos

  Classification: [CHORE]

  ADW Metadata:
  - Tipo: /chore
  - Workflow: /adw_sdlc_zte_iso
  - ID: /adw_id: chore_model_config_task_08

  Title: Update adw_sdlc_iso.py to use dynamic model resolution

  Description:
  1. Abre /Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_sdlc_iso.py
  2. Agrega import: from adw_modules.workflow_ops import get_model_id
  3. Busca TODAS las líneas con track_agent_start() con model hardcoded
  4. Reemplaza con get_model_id() según el patrón de Task 7
  5. Asegura consistencia de tipos de modelo
  6. Guardar archivo

  Acceptance Criteria:
  - ✅ Todas las llamadas track_agent_start() usan get_model_id()
  - ✅ NO hay model IDs hardcoded
  - ✅ Tipos de modelo son consistentes

  Impacted Paths:
  - /Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_sdlc_iso.py

  ---
  Task 9: Refactorizar adw_ship_iso.py - Uso Dinámico de Modelos

  Classification: [CHORE]

  ADW Metadata:
  - Tipo: /chore
  - Workflow: /adw_sdlc_zte_iso
  - ID: /adw_id: chore_model_config_task_09

  Title: Update adw_ship_iso.py to use dynamic model resolution

  Description:
  1. Abre /Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_ship_iso.py
  2. Agrega import: from adw_modules.workflow_ops import get_model_id
  3. Busca TODAS las líneas con track_agent_start() con model hardcoded
  4. Reemplaza con get_model_id() según patrón anterior
  5. Guardar archivo

  Acceptance Criteria:
  - ✅ Todas las llamadas track_agent_start() usan get_model_id()
  - ✅ NO hay model IDs hardcoded

  Impacted Paths:
  - /Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_ship_iso.py

  ---
  Task 10: Refactorizar adw_plan_build_review_fix.py - Review/Fix Models

  Classification: [CHORE]

  ADW Metadata:
  - Tipo: /chore
  - Workflow: /adw_sdlc_zte_iso
  - ID: /adw_id: chore_model_config_task_10

  Title: Update adw_plan_build_review_fix.py to use dynamic model resolution

  Description:
  1. Abre /Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_workflows/adw_plan_build_review_fix.py
  2. Agrega import: from adw_modules.workflow_ops import get_model_id
  3. Localiza líneas ~1184-1185 donde se asignan review_model y fix_model
  4. Reemplaza:
  # ANTES
  review_model = input_data.get("review_model", ModelName.OPUS.value)
  fix_model = input_data.get("fix_model", ModelName.OPUS.value)

  # DESPUÉS
  review_model = input_data.get("review_model", get_model_id("opus"))
  fix_model = input_data.get("fix_model", get_model_id("opus"))
  5. Guardar archivo

  Acceptance Criteria:
  - ✅ review_model y fix_model usan get_model_id("opus")
  - ✅ NO hay ModelName.OPUS.value hardcoded

  Impacted Paths:
  - /Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_workflows/adw_plan_build_review_fix.py

  ---
  Task 11: Refactorizar adw_plan_build_review.py - Review Model

  Classification: [CHORE]

  ADW Metadata:
  - Tipo: /chore
  - Workflow: /adw_sdlc_zte_iso
  - ID: /adw_id: chore_model_config_task_11

  Title: Update adw_plan_build_review.py to use dynamic model resolution

  Description:
  1. Abre /Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_workflows/adw_plan_build_review.py
  2. Agrega import: from adw_modules.workflow_ops import get_model_id
  3. Localiza línea ~982 donde se asigna review_model
  4. Reemplaza con get_model_id("opus")
  5. Guardar archivo

  Acceptance Criteria:
  - ✅ review_model usa get_model_id("opus")
  - ✅ NO hay hardcoded values

  Impacted Paths:
  - /Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_workflows/adw_plan_build_review.py

  ---
  Task 12: Crear .env.example con Variables de Entorno

  Classification: [CHORE]

  ADW Metadata:
  - Tipo: /chore
  - Workflow: /adw_sdlc_zte_iso
  - ID: /adw_id: chore_model_config_task_12

  Title: Add optional model configuration variables to .env.example

  Description:
  1. Abre /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/.env.example
  2. Localiza la sección de configuración (alrededor de línea 60)
  3. Agrega nueva sección DESPUÉS de credenciales:
  # =============================================================================
  # OPTIONAL - Claude Model Configuration
  # =============================================================================

  # Override default Claude model versions (optional)
  # If not set, uses models from config.yml or hardcoded defaults

  # ANTHROPIC_DEFAULT_OPUS_MODEL=claude-opus-4-5-20251101
  # ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-4-5-20250929
  # ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-haiku-4-5-20251001
  4. Guardar archivo

  Acceptance Criteria:
  - ✅ Sección comentada agregada al final
  - ✅ Las 3 variables están presentes
  - ✅ Tienen valores por defecto como ejemplos
  - ✅ Documentación clara

  Impacted Paths:
  - /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/.env.example

  ---
  Task 13: Sincronizar config.yml Template

  Classification: [CHORE]

  ADW Metadata:
  - Tipo: /chore
  - Workflow: /adw_sdlc_zte_iso
  - ID: /adw_id: chore_model_config_task_13

  Title: Sync config.yml.j2 template with root config.yml changes

  Description:
  1. Abre /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/config/config.yml.j2
  2. Busca la sección agentic.model_policy
  3. Aplica exactamente los mismos cambios que en Task 1 (agregar opus_model, sonnet_model, haiku_model)
  4. Guardar archivo

  Acceptance Criteria:
  - ✅ Template tiene los 3 nuevos campos
  - ✅ Orden y valores coinciden con root config.yml

  Impacted Paths:
  - /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/config/config.yml.j2

  ---
  Task 14: Sincronizar workflow_ops.py Template

  Classification: [CHORE]

  ADW Metadata:
  - Tipo: /chore
  - Workflow: /adw_sdlc_zte_iso
  - ID: /adw_id: chore_model_config_task_14

  Title: Sync workflow_ops.py.j2 template with get_model_id() function

  Description:
  1. Abre /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2
  2. Agrega la función get_model_id() exactamente como en Task 3
  3. Guardar archivo

  Acceptance Criteria:
  - ✅ Template contiene get_model_id() idéntica a root

  Impacted Paths:
  - /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2

  ---
  Task 15: Sincronizar adw_agent_sdk.py Template

  Classification: [CHORE]

  ADW Metadata:
  - Tipo: /chore
  - Workflow: /adw_sdlc_zte_iso
  - ID: /adw_id: chore_model_config_task_15

  Title: Sync adw_agent_sdk.py.j2 template with ModelName changes

  Description:
  1. Abre /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/adw_agent_sdk.py.j2
  2. Aplica cambios de Task 4 (reemplazar OPUS/SONNET/HAIKU con métodos estáticos)
  3. Guardar archivo

  Acceptance Criteria:
  - ✅ Template contiene get_opus(), get_sonnet(), get_haiku()

  Impacted Paths:
  - /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/adw_agent_sdk.py.j2

  ---
  Task 16: Sincronizar agent.py Template

  Classification: [CHORE]

  ADW Metadata:
  - Tipo: /chore
  - Workflow: /adw_sdlc_zte_iso
  - ID: /adw_id: chore_model_config_task_16

  Title: Sync agent.py.j2 template with MODEL_FALLBACK_CHAIN changes

  Description:
  1. Abre /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/agent.py.j2
  2. Aplica cambios de Task 5 (reemplazar MODEL_FALLBACK_CHAIN con get_model_fallback_chain())
  3. Guardar archivo

  Acceptance Criteria:
  - ✅ Template contiene get_model_fallback_chain() y get_fallback_model()

  Impacted Paths:
  - /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/agent.py.j2

  ---
  Task 17: Sincronizar adw_summarizer.py Template

  Classification: [CHORE]

  ADW Metadata:
  - Tipo: /chore
  - Workflow: /adw_sdlc_zte_iso
  - ID: /adw_id: chore_model_config_task_17

  Title: Sync adw_summarizer.py.j2 template with FAST_MODEL changes

  Description:
  1. Abre /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/adw_summarizer.py.j2
  2. Aplica cambios de Task 6 (reemplazar FAST_MODEL con get_fast_model())
  3. Guardar archivo

  Acceptance Criteria:
  - ✅ Template contiene get_fast_model()

  Impacted Paths:
  - /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/adw_summarizer.py.j2

  ---
  Task 18: Sincronizar adw_sdlc_zte_iso.py Template

  Classification: [CHORE]

  ADW Metadata:
  - Tipo: /chore
  - Workflow: /adw_sdlc_zte_iso
  - ID: /adw_id: chore_model_config_task_18

  Title: Sync adw_sdlc_zte_iso.py.j2 template with model resolution changes

  Description:
  1. Abre /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_sdlc_zte_iso.py.j2
  2. Aplica cambios de Task 7 (reemplazar hardcoded models con get_model_id())
  3. Guardar archivo

  Acceptance Criteria:
  - ✅ Template contiene import de get_model_id
  - ✅ Todas las llamadas track_agent_start() usan get_model_id()

  Impacted Paths:
  - /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_sdlc_zte_iso.py.j2

  ---
  Task 19: Sincronizar adw_sdlc_iso.py Template

  Classification: [CHORE]

  ADW Metadata:
  - Tipo: /chore
  - Workflow: /adw_sdlc_zte_iso
  - ID: /adw_id: chore_model_config_task_19

  Title: Sync adw_sdlc_iso.py.j2 template with model resolution changes

  Description:
  1. Abre /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_sdlc_iso.py.j2
  2. Aplica cambios de Task 8 (reemplazar hardcoded models con get_model_id())
  3. Guardar archivo

  Acceptance Criteria:
  - ✅ Template contiene import de get_model_id
  - ✅ Todas las llamadas track_agent_start() usan get_model_id()

  Impacted Paths:
  - /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_sdlc_iso.py.j2

  ---
  Task 20: Sincronizar adw_ship_iso.py Template

  Classification: [CHORE]

  ADW Metadata:
  - Tipo: /chore
  - Workflow: /adw_sdlc_zte_iso
  - ID: /adw_id: chore_model_config_task_20

  Title: Sync adw_ship_iso.py.j2 template with model resolution changes

  Description:
  1. Abre /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_ship_iso.py.j2
  2. Aplica cambios de Task 9 (reemplazar hardcoded models con get_model_id())
  3. Guardar archivo

  Acceptance Criteria:
  - ✅ Template contiene import de get_model_id
  - ✅ Todas las llamadas track_agent_start() usan get_model_id()

  Impacted Paths:
  - /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_ship_iso.py.j2

  ---
  Task 21: Sincronizar adw_plan_build_review_fix.py Template

  Classification: [CHORE]

  ADW Metadata:
  - Tipo: /chore
  - Workflow: /adw_sdlc_zte_iso
  - ID: /adw_id: chore_model_config_task_21

  Title: Sync adw_plan_build_review_fix.py.j2 template with review/fix model changes

  Description:
  1. Abre /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_workflows/adw_plan_build_review_fix.py.j2
  2. Aplica cambios de Task 10 (reemplazar review_model y fix_model defaults)
  3. Guardar archivo

  Acceptance Criteria:
  - ✅ Template usa get_model_id("opus") para review/fix defaults

  Impacted Paths:
  - /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_workflows/adw_plan_build_review_fix.py.j2

  ---
  Task 22: Sincronizar adw_plan_build_review.py Template

  Classification: [CHORE]

  ADW Metadata:
  - Tipo: /chore
  - Workflow: /adw_sdlc_zte_iso
  - ID: /adw_id: chore_model_config_task_22

  Title: Sync adw_plan_build_review.py.j2 template with review model changes

  Description:
  1. Abre /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_workflows/adw_plan_build_review.py.j2
  2. Aplica cambios de Task 11 (reemplazar review_model default)
  3. Guardar archivo

  Acceptance Criteria:
  - ✅ Template usa get_model_id("opus") para review_model

  Impacted Paths:
  - /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_workflows/adw_plan_build_review.py.j2

  ---
  Task 23: Sincronizar models.py Template

  Classification: [CHORE]

  ADW Metadata:
  - Tipo: /chore
  - Workflow: /adw_sdlc_zte_iso
  - ID: /adw_id: chore_model_config_task_23

  Title: Sync data_types.py.j2 template with ModelPolicy changes

  Description:
  1. Abre /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/data_types.py.j2
  2. Aplica cambios de Task 2 (agregar opus_model, sonnet_model, haiku_model a ModelPolicy)
  3. Guardar archivo

  Acceptance Criteria:
  - ✅ Template contiene los 3 campos opcionales en ModelPolicy

  Impacted Paths:
  - /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/data_types.py.j2

  ---
  Task 24: Actualizar CLI README con Tabla de Configuración

  Classification: [CHORE]

  ADW Metadata:
  - Tipo: /chore
  - Workflow: /adw_sdlc_zte_iso
  - ID: /adw_id: chore_model_config_task_24

  Title: Update CLI README with model configuration table

  Description:
  1. Abre /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/README.md
  2. Localiza la sección de "Configuration" o "Features" (si no existe, crea nueva sección después de "Installation")
  3. Agrega nueva subsección "### Model Configuration" con tabla:
  ### Model Configuration

  La configuración de modelos Claude se puede personalizar en 3 niveles (orden de prioridad):

  | Nivel | Fuente | Variables | Descripción |
  |-------|--------|-----------|-------------|
  | 1 (Máxima) | Variables de Entorno | `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL` | Override dinámico en runtime |
  | 2 (Media) | config.yml | `agentic.model_policy.opus_model`, `agentic.model_policy.sonnet_model`, `agentic.model_policy.haiku_model` | Configuración por proyecto |
  | 3 (Baja) | Defaults | Hardcoded en `workflow_ops.py` | Fallback final (claude-opus-4-5-20251101, etc.) |

  **Ejemplo - Usar Sonnet más nuevo localmente**:
  ```bash
  export ANTHROPIC_DEFAULT_SONNET_MODEL="claude-sonnet-4-5-20250929"
  uv run adws/adw_plan_iso.py --issue 123

  4. Guardar archivo

  Acceptance Criteria:
  - ✅ Tabla agregada en README
  - ✅ Muestra los 3 niveles de configuración
  - ✅ Incluye ejemplo práctico
  - ✅ Variables de entorno documentadas

  Impacted Paths:
  - /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/README.md

  ---
  Task 25: Actualizar CHANGELOG y Bumper Versión

  Classification: [CHORE]

  ADW Metadata:
  - Tipo: /chore
  - Workflow: /adw_sdlc_zte_iso
  - ID: /adw_id: chore_model_config_task_25

  Title: Update CHANGELOG and bump version to 0.11.0

  Description:
  1. Abre /Users/hernandoescobar/Documents/Celes/tac_bootstrap/CHANGELOG.md
  2. Agrega nueva entrada al INICIO del archivo (antes de versiones anteriores):
  ## [0.11.0] - 2026-02-10

  ### Added
  - **Model Configuration Centralization**: Centralized Claude model configuration with 3-tier resolution (environment variables → config.yml → hardcoded defaults)
  - New `get_model_id()` function in `workflow_ops.py` for dynamic model resolution
  - Optional model ID overrides in `config.yml` under `agentic.model_policy`
  - Optional `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL` environment variables
  - Dynamic model resolution in `ModelName`, `MODEL_FALLBACK_CHAIN`, and `FAST_MODEL`
  - Updated all orchestrators (`adw_sdlc_iso`, `adw_sdlc_zte_iso`, `adw_ship_iso`) to use dynamic models
  - Updated review/fix workflows to use dynamic model resolution

  ### Changed
  - Model configuration is now runtime-configurable without code changes
  - Templates synchronized with all model configuration changes
  - CLI README updated with model configuration documentation

  ### Benefits
  - ✅ Change models without redeploying code
  - ✅ Different models per environment (dev/staging/prod)
  - ✅ Cost control: quick switch to cheaper models for testing
  - ✅ Version pinning: lock to specific model versions
  - ✅ 100% backward compatible with existing projects
  3. Actualiza el número de versión en los siguientes archivos:
    - /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/__init__.py: Busca __version__ y cámbialo a "0.11.0"
    - /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/pyproject.toml: Busca version =  y cámbialo a "0.11.0"
  4. Guardar archivos

  Acceptance Criteria:
  - ✅ CHANGELOG.md contiene entrada 0.11.0
  - ✅ Entrada lista todos los cambios de forma clara
  - ✅ init.py tiene versión 0.11.0
  - ✅ pyproject.toml tiene versión 0.11.0

  Impacted Paths:
  - /Users/hernandoescobar/Documents/Celes/tac_bootstrap/CHANGELOG.md
  - /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/__init__.py
  - /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/pyproject.toml

  ---
  Parallel Execution Groups
  Grupo: P1-Config
  Tareas: 1, 2
  Cantidad: 2
  Dependencia: Ninguna
  Descripción: Configurar extensiones base (config.yml y Pydantic ModelPolicy)
  ────────────────────────────────────────
  Grupo: P2-CoreFunctions
  Tareas: 3, 4, 5, 6
  Cantidad: 4
  Dependencia: P1
  Descripción: Crear funciones centrales de resolución dinámica (get_model_id, ModelName, MODEL_FALLBACK_CHAIN, FAST_MODEL)
  ────────────────────────────────────────
  Grupo: P3-Orchestrators
  Tareas: 7, 8, 9
  Cantidad: 3
  Dependencia: P2
  Descripción: Refactorizar orchestrators para usar resolución dinámica
  ────────────────────────────────────────
  Grupo: P4-Workflows
  Tareas: 10, 11
  Cantidad: 2
  Dependencia: P2
  Descripción: Refactorizar workflows para modelos dinámicos
  ────────────────────────────────────────
  Grupo: P5-EnvAndTemplates
  Tareas: 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23
  Cantidad: 12
  Dependencia: P2
  Descripción: Crear .env.example y sincronizar todos los templates (config, modules, workflows)
  ────────────────────────────────────────
  Grupo: P6-Documentation
  Tareas: 24
  Cantidad: 1
  Dependencia: P5
  Descripción: Actualizar README.md con tabla de configuración
  ────────────────────────────────────────
  Grupo: SEQ-Final
  Tareas: 25
  Cantidad: 1
  Dependencia: Todos
  Descripción: Actualizar CHANGELOG y bumper versión a 0.11.0
  ---
  Execution Notes

  - Total Tasks: 25
  - Parallel Groups: 7 (incluyendo sequential final)
  - Estimated Duration: ~2-3 horas de ejecución paralela + 30 min para verificación
  - Critical Path: P1 → P2 → P3/P4 → P5 → P6 → SEQ-Final
  - No Breaking Changes: 100% backward compatible
  - Test Strategy: Tests manuales en cada grupo (env var resolution, config fallback, hardcoded defaults)

  ---
  Files Changed Summary

  Root Changes (13 files)

  1. config.yml
  2. adws/adw_modules/workflow_ops.py
  3. adws/adw_modules/adw_agent_sdk.py
  4. adws/adw_modules/agent.py
  5. adws/adw_modules/adw_summarizer.py
  6. adws/adw_sdlc_zte_iso.py
  7. adws/adw_sdlc_iso.py
  8. adws/adw_ship_iso.py
  9. adws/adw_workflows/adw_plan_build_review_fix.py
  10. adws/adw_workflows/adw_plan_build_review.py
  11. tac_bootstrap_cli/.env.example
  12. tac_bootstrap_cli/README.md
  13. tac_bootstrap_cli/tac_bootstrap/domain/models.py

  Template Changes (12 files)

  1. tac_bootstrap_cli/tac_bootstrap/templates/config/config.yml.j2
  2. tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2
  3. tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/adw_agent_sdk.py.j2
  4. tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/agent.py.j2
  5. tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/adw_summarizer.py.j2
  6. tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/data_types.py.j2
  7. tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_sdlc_zte_iso.py.j2
  8. tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_sdlc_iso.py.j2
  9. tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_ship_iso.py.j2
  10. tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_workflows/adw_plan_build_review_fix.py.j2
  11. tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_workflows/adw_plan_build_review.py.j2

  Version/Changelog Changes (3 files)

  1. CHANGELOG.md
  2. tac_bootstrap_cli/tac_bootstrap/init.py
  3. tac_bootstrap_cli/pyproject.toml

  TOTAL: 28 files changed