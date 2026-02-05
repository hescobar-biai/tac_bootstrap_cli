-- =============================================================================
-- Migration: 001_initial
-- Description: Initial schema for orchestrator database
-- Created: 2026-02-04
-- TAC Version: 0.8.0
-- =============================================================================


-- =============================================================================
-- TAC Bootstrap Orchestrator Database Schema (SQLite)
-- =============================================================================
-- Version: 0.8.0
-- Database: SQLite 3.35+
-- Purpose: Persistent state tracking for agent orchestration workflows
-- Zero-config: Auto-initializes on first access via helper function
-- Concurrency: WAL mode enabled for multiple readers + single writer
-- =============================================================================

-- Enable WAL mode for better concurrency
PRAGMA journal_mode=WAL;

-- Enable foreign key constraints (not enabled by default in SQLite)
PRAGMA foreign_keys=ON;

-- =============================================================================
-- Table 1: orchestrator_agents
-- Purpose: Agent definitions (templates) registered in the system
-- Lifecycle: Created when agent type is registered, rarely updated
-- =============================================================================
CREATE TABLE IF NOT EXISTS orchestrator_agents (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    agent_type TEXT NOT NULL,
    capabilities TEXT,
    default_model TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    CHECK (agent_type IN ('planner', 'builder', 'reviewer', 'tester', 'orchestrator', 'utility'))
);

-- =============================================================================
-- Table 2: agents
-- Purpose: Runtime agent instances (spawned from orchestrator_agents)
-- Lifecycle: Created when workflow starts, cleaned up after completion/failure
-- =============================================================================
CREATE TABLE IF NOT EXISTS agents (
    id TEXT PRIMARY KEY,
    orchestrator_agent_id TEXT NOT NULL,
    session_id TEXT NOT NULL,
    parent_agent_id TEXT,
    status TEXT NOT NULL DEFAULT 'initializing',
    context TEXT,
    config TEXT,
    started_at TEXT NOT NULL DEFAULT (datetime('now')),
    completed_at TEXT,
    cost_usd REAL DEFAULT 0.0,
    error_message TEXT,
    FOREIGN KEY (orchestrator_agent_id) REFERENCES orchestrator_agents(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_agent_id) REFERENCES agents(id) ON DELETE SET NULL,
    CHECK (status IN ('initializing', 'planning', 'executing', 'reviewing', 'completed', 'failed', 'cancelled'))
);

-- =============================================================================
-- Table 3: prompts
-- Purpose: Individual ADW/command executions within an agent's lifecycle
-- Lifecycle: Created for each prompt sent to LLM, updated with results
-- =============================================================================
CREATE TABLE IF NOT EXISTS prompts (
    id TEXT PRIMARY KEY,
    agent_id TEXT NOT NULL,
    prompt_type TEXT NOT NULL,
    prompt_name TEXT,
    prompt_text TEXT NOT NULL,
    response_text TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    model_used TEXT,
    tokens_input INTEGER DEFAULT 0,
    tokens_output INTEGER DEFAULT 0,
    cost_usd REAL DEFAULT 0.0,
    latency_ms INTEGER,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    completed_at TEXT,
    error_message TEXT,
    FOREIGN KEY (agent_id) REFERENCES agents(id) ON DELETE CASCADE,
    CHECK (prompt_type IN ('adw', 'command', 'followup', 'correction', 'tool_call')),
    CHECK (status IN ('pending', 'streaming', 'completed', 'failed', 'cancelled'))
);

-- =============================================================================
-- Table 4: agent_logs
-- Purpose: Lifecycle events for agents (state transitions, milestones)
-- Lifecycle: Append-only log, cleaned up with parent agent
-- =============================================================================
CREATE TABLE IF NOT EXISTS agent_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id TEXT NOT NULL,
    log_level TEXT NOT NULL DEFAULT 'INFO',
    log_type TEXT NOT NULL,
    message TEXT NOT NULL,
    details TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (agent_id) REFERENCES agents(id) ON DELETE CASCADE,
    CHECK (log_level IN ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')),
    CHECK (log_type IN ('state_change', 'milestone', 'error', 'performance', 'tool_call', 'cost_update'))
);

-- =============================================================================
-- Table 5: system_logs
-- Purpose: System-wide events (not tied to specific agent)
-- Lifecycle: Append-only log, managed by retention policy
-- =============================================================================
CREATE TABLE IF NOT EXISTS system_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_level TEXT NOT NULL DEFAULT 'INFO',
    component TEXT NOT NULL,
    message TEXT NOT NULL,
    details TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    CHECK (log_level IN ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'))
);

-- =============================================================================
-- Triggers
-- =============================================================================

CREATE TRIGGER IF NOT EXISTS update_orchestrator_agents_updated_at
AFTER UPDATE ON orchestrator_agents
FOR EACH ROW
BEGIN
    UPDATE orchestrator_agents
    SET updated_at = datetime('now')
    WHERE id = NEW.id;
END;

-- =============================================================================
-- Performance Indexes
-- =============================================================================

CREATE INDEX IF NOT EXISTS idx_agents_session ON agents(session_id);
CREATE INDEX IF NOT EXISTS idx_agents_orch ON agents(orchestrator_agent_id);
CREATE INDEX IF NOT EXISTS idx_prompts_agent ON prompts(agent_id);
CREATE INDEX IF NOT EXISTS idx_prompts_status ON prompts(status);
CREATE INDEX IF NOT EXISTS idx_agent_logs_agent ON agent_logs(agent_id);
CREATE INDEX IF NOT EXISTS idx_system_logs_level ON system_logs(log_level);

-- =============================================================================
-- Schema Initialization Complete
-- =============================================================================
-- Tables created: 5 (orchestrator_agents, agents, prompts, agent_logs, system_logs)
-- Triggers created: 1 (auto-update updated_at)
-- Indexes created: 6 (strategic indexes for common queries)
--
-- Next steps:
-- 1. Create Pydantic models mapping to this schema (Task 7: orch_database_models.py)
-- 2. Implement CRUD operations with aiosqlite (Task 8: adw_database.py)
-- 3. Integrate with FastAPI for web visualization (Task 12)
-- =============================================================================
