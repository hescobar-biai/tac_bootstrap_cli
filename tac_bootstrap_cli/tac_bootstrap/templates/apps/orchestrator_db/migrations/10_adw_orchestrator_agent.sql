-- ============================================================================
-- ADW ORCHESTRATOR AGENT (SEED DATA)
-- ============================================================================
-- Creates a well-known orchestrator_agent row for ADW workflows.
-- This provides a stable orchestrator_agent_id that adw_db_bridge uses
-- when creating agents during workflow execution.
--
-- Dependencies: orchestrator_agents table (migration 0)

INSERT INTO orchestrator_agents (id, status, working_dir, metadata)
VALUES (
    '00000000-0000-0000-0000-ad0000000000'::uuid,
    'idle',
    NULL,
    '{"source": "adw_db_bridge", "description": "ADW Workflow Orchestrator"}'::jsonb
) ON CONFLICT (id) DO NOTHING;
