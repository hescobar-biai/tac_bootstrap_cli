from typing import TYPE_CHECKING, Optional

from .autocomplete_agent import AutocompleteAgent
from .autocomplete_models import AutocompleteResponse

if TYPE_CHECKING:
    from .logger import OrchestratorLogger
    from .websocket_manager import WebSocketManager


class AutocompleteService:
    def __init__(
        self,
        orchestrator_agent_id: str,
        logger: "OrchestratorLogger",
        working_dir: str,
        ws_manager: Optional["WebSocketManager"] = None,
    ) -> None:
        self.orchestrator_agent_id = orchestrator_agent_id
        self.logger = logger
        self.agent = AutocompleteAgent(orchestrator_agent_id, logger, working_dir, ws_manager)

    async def generate_autocomplete(
        self, user_input: str, orchestrator_agent_id: str
    ) -> AutocompleteResponse:
        try:
            if str(self.orchestrator_agent_id) != orchestrator_agent_id:
                raise ValueError("Orchestrator ID mismatch")

            items = await self.agent.generate_autocomplete(user_input)

            return AutocompleteResponse(
                status="success",
                autocompletes=items,
                total_items=len(items),
                orchestrator_agent_id=orchestrator_agent_id
            )
        except Exception as e:
            self.logger.error(f"Autocomplete generation failed: {e}")
            return AutocompleteResponse(
                status="error",
                autocompletes=[],
                total_items=0,
                orchestrator_agent_id=orchestrator_agent_id
            )

    async def update_completion_history(
        self,
        orchestrator_agent_id: str,
        completion_type: str,
        user_input_on_enter: Optional[str] = None,
        user_input_before_completion: Optional[str] = None,
        autocomplete_item: Optional[str] = None,
        reasoning: Optional[str] = None,
    ) -> None:
        """
        Update completion history with type-safe event.

        CRITICAL: Type annotations match Pydantic models for validation
        """
        try:
            self.agent.add_completion_event(
                completion_type=completion_type,
                user_input_on_enter=user_input_on_enter,
                user_input_before_completion=user_input_before_completion,
                autocomplete_item=autocomplete_item,
                reasoning=reasoning
            )
            self.logger.info(f"Updated completion history: {completion_type}")
        except Exception as e:
            self.logger.error(f"Failed to update completion history: {e}")
            raise
