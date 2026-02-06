# /// script
# dependencies = ["pytest>=8.0", "pytest-asyncio>=0.23", "aiosqlite>=0.19.0"]
# ///
"""
Pytest Configuration and Fixtures for ADW Tests

This module provides shared fixtures for testing ADW modules:
- Database fixtures with isolated temp databases
- WebSocket server fixtures
- Mock agent SDK responses
- Workflow state fixtures
"""

import asyncio
import os
import sys
import tempfile
from pathlib import Path
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio

# Add adws directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


# ============================================================================
# Async Event Loop Configuration
# ============================================================================

@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# ============================================================================
# Database Fixtures
# ============================================================================

@pytest_asyncio.fixture
async def temp_db_path() -> AsyncGenerator[str, None]:
    """Create a temporary database file path."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    yield db_path
    # Cleanup
    try:
        os.unlink(db_path)
        # Also remove WAL and SHM files if they exist
        for ext in ["-wal", "-shm"]:
            wal_path = db_path + ext
            if os.path.exists(wal_path):
                os.unlink(wal_path)
    except Exception:
        pass


@pytest_asyncio.fixture
async def db_manager(temp_db_path: str) -> AsyncGenerator:
    """Create a DatabaseManager with a temporary database."""
    from adw_modules.adw_database import DatabaseManager

    manager = DatabaseManager(temp_db_path)
    await manager.connect()
    yield manager
    await manager.close()


@pytest_asyncio.fixture
async def db_with_agent(db_manager) -> AsyncGenerator[tuple, None]:
    """Create a DatabaseManager with a pre-created orchestrator agent and runtime agent."""
    # Create orchestrator agent definition
    orch_agent_id = await db_manager.create_orchestrator_agent(
        name="test-scout-agent",
        description="Test scout agent for unit tests",
        agent_type="utility",
        capabilities="codebase_exploration,issue_detection",
        default_model="claude-sonnet-4-5"
    )

    # Create runtime agent instance
    agent_id = await db_manager.create_agent(
        orchestrator_agent_id=orch_agent_id,
        session_id="test-session-001",
        status="executing"
    )

    yield db_manager, orch_agent_id, agent_id


# ============================================================================
# WebSocket Fixtures
# ============================================================================

@pytest_asyncio.fixture
async def ws_manager() -> AsyncGenerator:
    """Create a WebSocket ConnectionManager."""
    from adw_modules.adw_websockets import ConnectionManager

    manager = ConnectionManager()
    yield manager


@pytest_asyncio.fixture
async def ws_server(ws_manager) -> AsyncGenerator[tuple, None]:
    """Start a WebSocket server on a random available port."""
    from adw_modules.adw_websockets import start_server, stop_server
    import socket

    # Find an available port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        port = s.getsockname()[1]

    server_task, manager = await start_server(host="127.0.0.1", port=port)
    yield server_task, manager, port
    await stop_server(server_task)


# ============================================================================
# Agent SDK Fixtures
# ============================================================================

@pytest.fixture
def mock_query_options():
    """Create mock QueryOptions for testing."""
    from adw_modules.adw_agent_sdk import QueryOptions, ModelName

    return QueryOptions(
        model=ModelName.SONNET,
        allowed_tools=["Read", "Glob", "Grep"],
        max_turns=10,
    )


@pytest.fixture
def sample_token_usage():
    """Create sample TokenUsage for testing."""
    from adw_modules.adw_agent_sdk import TokenUsage

    return TokenUsage(
        input_tokens=1000,
        output_tokens=500,
        cache_read_input_tokens=200,
        cache_creation_input_tokens=50,
    )


# ============================================================================
# Workflow State Fixtures
# ============================================================================

@pytest.fixture
def temp_state_dir() -> Generator[str, None, None]:
    """Create a temporary directory for ADW state files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_adw_state(temp_state_dir: str):
    """Create a sample ADW state for testing."""
    from adw_modules.state import ADWState

    state = ADWState(
        adw_id="test-adw-001",
        state_dir=temp_state_dir
    )
    state.set("issue_number", "123")
    state.set("branch_name", "feature/test-branch")
    state.set("model_set", "base")
    return state


# ============================================================================
# Mock Data Fixtures
# ============================================================================

@pytest.fixture
def sample_agent_log():
    """Sample agent log entry for testing."""
    return {
        "agent_id": "550e8400-e29b-41d4-a716-446655440000",
        "log_level": "INFO",
        "log_type": "milestone",
        "message": "Agent completed code analysis",
        "details": {"files_analyzed": 42, "duration_ms": 1250}
    }


@pytest.fixture
def sample_websocket_event():
    """Sample WebSocket event for testing."""
    from adw_modules.adw_websockets import WebSocketEvent

    return WebSocketEvent(
        event_type="agent_started",
        agent_id="550e8400-e29b-41d4-a716-446655440000",
        message="Scout agent started exploration",
        metadata={"model": "claude-sonnet-4-5", "files_queued": 10}
    )
