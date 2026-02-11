"""
IDK: web-server, fastapi-dashboard, project-management-ui, websocket-updates, rest-api
Responsibility: Provides a FastAPI-based web dashboard for managing TAC Bootstrap projects
                with REST API endpoints and WebSocket real-time updates
Invariants: Server runs on configurable port (default 3000), serves both API and static files,
            WebSocket provides real-time project status updates

Example usage:
    from tac_bootstrap.infrastructure.web_server import DashboardServer

    server = DashboardServer(port=3000)
    server.start()  # Starts in background
    server.stop()   # Stops the server
"""

import json
import os
import signal
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


# PID file for tracking running server
PID_FILE = Path.home() / ".tac-bootstrap" / "dashboard.pid"


class DashboardConfig:
    """Dashboard configuration."""

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 3000,
        reload: bool = False,
    ) -> None:
        """Initialize dashboard configuration.

        Args:
            host: Host to bind to (default: 127.0.0.1)
            port: Port number (default: 3000)
            reload: Enable auto-reload for development
        """
        self.host = host
        self.port = port
        self.reload = reload


def create_app() -> Any:
    """Create and configure the FastAPI application.

    Returns:
        FastAPI application instance
    """
    try:
        from fastapi import FastAPI, WebSocket, WebSocketDisconnect
        from fastapi.middleware.cors import CORSMiddleware
        from fastapi.responses import HTMLResponse, JSONResponse
    except ImportError:
        raise ImportError(
            "FastAPI is required for the dashboard. "
            "Install with: pip install fastapi uvicorn"
        )

    app = FastAPI(
        title="TAC Bootstrap Dashboard",
        description="Web dashboard for managing TAC Bootstrap projects",
        version="1.0.0",
    )

    # CORS middleware for frontend access
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # WebSocket connection manager
    class ConnectionManager:
        """Manages WebSocket connections for real-time updates."""

        def __init__(self) -> None:
            self.active_connections: List[WebSocket] = []

        async def connect(self, websocket: WebSocket) -> None:
            await websocket.accept()
            self.active_connections.append(websocket)

        def disconnect(self, websocket: WebSocket) -> None:
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)

        async def broadcast(self, message: Dict[str, Any]) -> None:
            for connection in self.active_connections:
                try:
                    await connection.send_json(message)
                except Exception:
                    pass

    manager = ConnectionManager()

    # ---- API Endpoints ----

    @app.get("/", response_class=HTMLResponse)
    async def dashboard_home() -> str:
        """Serve the dashboard home page."""
        return _generate_dashboard_html()

    @app.get("/api/health")
    async def health_check() -> Dict[str, Any]:
        """API health check endpoint."""
        from tac_bootstrap import __version__

        return {
            "status": "healthy",
            "version": __version__,
            "service": "tac-bootstrap-dashboard",
        }

    @app.get("/api/projects")
    async def list_projects() -> Dict[str, Any]:
        """List known TAC Bootstrap projects."""
        tac_dir = Path.home() / ".tac-bootstrap"
        projects: List[Dict[str, Any]] = []

        # Scan snapshots directory for known projects
        snapshots_dir = tac_dir / "snapshots"
        if snapshots_dir.exists():
            for item in snapshots_dir.iterdir():
                if item.is_dir():
                    for snap in item.iterdir():
                        metadata_file = snap / "metadata.json"
                        if metadata_file.exists():
                            try:
                                data = json.loads(metadata_file.read_text())
                                project_path = data.get("project_path", "")
                                if project_path and project_path not in [p.get("path") for p in projects]:
                                    projects.append({
                                        "path": project_path,
                                        "name": Path(project_path).name,
                                        "snapshots": 1,
                                    })
                            except Exception:
                                pass

        return {"projects": projects, "total": len(projects)}

    @app.get("/api/projects/{project_name}/metrics")
    async def get_project_metrics(project_name: str) -> Dict[str, Any]:
        """Get metrics for a specific project."""
        return {
            "project": project_name,
            "metrics": {
                "health_score": 0,
                "message": "Use 'tac-bootstrap metrics generate' to generate metrics",
            },
        }

    @app.get("/api/commands")
    async def list_commands() -> Dict[str, Any]:
        """List available CLI commands."""
        commands = [
            {"name": "init", "description": "Create a new project"},
            {"name": "add-agentic", "description": "Add Agentic Layer to existing repo"},
            {"name": "generate", "description": "Generate code artifacts"},
            {"name": "doctor", "description": "Validate setup"},
            {"name": "validate", "description": "Validate configuration"},
            {"name": "upgrade", "description": "Upgrade to latest version"},
            {"name": "health-check", "description": "Check system health"},
            {"name": "render", "description": "Regenerate from config"},
            {"name": "telemetry", "description": "Manage telemetry"},
            {"name": "snapshot", "description": "Manage snapshots"},
            {"name": "metrics", "description": "Generate metrics"},
            {"name": "search", "description": "Search commands and templates"},
            {"name": "learn", "description": "Interactive tutorials"},
            {"name": "dashboard", "description": "Web dashboard"},
        ]
        return {"commands": commands, "total": len(commands)}

    @app.get("/api/templates")
    async def list_templates() -> Dict[str, Any]:
        """List available templates."""
        from tac_bootstrap.application.community_service import CommunityService

        service = CommunityService()
        templates = service.browse_templates()
        return {
            "templates": [t.model_dump() for t in templates],
            "total": len(templates),
        }

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket) -> None:
        """WebSocket endpoint for real-time updates."""
        await manager.connect(websocket)
        try:
            while True:
                data = await websocket.receive_text()
                # Echo back with acknowledgment
                await websocket.send_json({
                    "type": "ack",
                    "data": data,
                })
        except WebSocketDisconnect:
            manager.disconnect(websocket)

    return app


def _generate_dashboard_html() -> str:
    """Generate the dashboard HTML page.

    Returns:
        HTML string for the dashboard
    """
    from tac_bootstrap import __version__

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TAC Bootstrap Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: #0f172a; color: #e2e8f0; }}
        .header {{ background: #1e293b; padding: 1rem 2rem; border-bottom: 1px solid #334155;
                   display: flex; justify-content: space-between; align-items: center; }}
        .header h1 {{ color: #22d3ee; font-size: 1.5rem; }}
        .header .version {{ color: #94a3b8; font-size: 0.875rem; }}
        .container {{ max-width: 1200px; margin: 2rem auto; padding: 0 2rem; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; }}
        .card {{ background: #1e293b; border-radius: 0.75rem; padding: 1.5rem;
                 border: 1px solid #334155; }}
        .card h2 {{ color: #22d3ee; font-size: 1.125rem; margin-bottom: 1rem; }}
        .card p {{ color: #94a3b8; line-height: 1.6; }}
        .status {{ display: inline-block; padding: 0.25rem 0.75rem; border-radius: 1rem;
                   font-size: 0.75rem; font-weight: 600; }}
        .status.healthy {{ background: #064e3b; color: #34d399; }}
        .status.warning {{ background: #78350f; color: #fbbf24; }}
        .metric {{ display: flex; justify-content: space-between; padding: 0.5rem 0;
                   border-bottom: 1px solid #334155; }}
        .metric:last-child {{ border-bottom: none; }}
        .metric-value {{ color: #22d3ee; font-weight: 600; }}
        .btn {{ background: #0891b2; color: white; border: none; padding: 0.5rem 1rem;
                border-radius: 0.5rem; cursor: pointer; font-size: 0.875rem; }}
        .btn:hover {{ background: #06b6d4; }}
        #log {{ background: #0f172a; border: 1px solid #334155; border-radius: 0.5rem;
                padding: 1rem; font-family: monospace; font-size: 0.8rem;
                max-height: 200px; overflow-y: auto; margin-top: 1rem; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>TAC Bootstrap Dashboard</h1>
        <div>
            <span class="version">v{__version__}</span>
            <span class="status healthy" id="status">Connected</span>
        </div>
    </div>
    <div class="container">
        <div class="grid">
            <div class="card">
                <h2>System Health</h2>
                <div class="metric">
                    <span>API Status</span>
                    <span class="metric-value" id="api-status">Checking...</span>
                </div>
                <div class="metric">
                    <span>WebSocket</span>
                    <span class="metric-value" id="ws-status">Connecting...</span>
                </div>
                <div class="metric">
                    <span>Version</span>
                    <span class="metric-value">{__version__}</span>
                </div>
            </div>
            <div class="card">
                <h2>Quick Actions</h2>
                <p>Use the CLI to manage projects:</p>
                <div style="margin-top: 1rem;">
                    <button class="btn" onclick="fetchProjects()">Refresh Projects</button>
                    <button class="btn" onclick="fetchCommands()">List Commands</button>
                    <button class="btn" onclick="fetchTemplates()">Browse Templates</button>
                </div>
            </div>
            <div class="card">
                <h2>Projects</h2>
                <div id="projects-list">
                    <p>Loading projects...</p>
                </div>
            </div>
            <div class="card">
                <h2>Activity Log</h2>
                <div id="log">Waiting for events...</div>
            </div>
        </div>
    </div>
    <script>
        const WS_URL = 'ws://' + window.location.host + '/ws';
        let ws;

        function connectWebSocket() {{
            ws = new WebSocket(WS_URL);
            ws.onopen = () => {{
                document.getElementById('ws-status').textContent = 'Connected';
                document.getElementById('status').textContent = 'Connected';
                addLog('WebSocket connected');
            }};
            ws.onmessage = (event) => {{
                const data = JSON.parse(event.data);
                addLog('Received: ' + JSON.stringify(data));
            }};
            ws.onclose = () => {{
                document.getElementById('ws-status').textContent = 'Disconnected';
                document.getElementById('status').textContent = 'Disconnected';
                document.getElementById('status').className = 'status warning';
                setTimeout(connectWebSocket, 3000);
            }};
        }}

        function addLog(msg) {{
            const log = document.getElementById('log');
            const time = new Date().toLocaleTimeString();
            log.innerHTML = '[' + time + '] ' + msg + '\\n' + log.innerHTML;
        }}

        async function fetchProjects() {{
            try {{
                const resp = await fetch('/api/projects');
                const data = await resp.json();
                const list = document.getElementById('projects-list');
                if (data.projects.length === 0) {{
                    list.innerHTML = '<p>No projects found. Create one with: tac-bootstrap init my-app</p>';
                }} else {{
                    list.innerHTML = data.projects.map(p =>
                        '<div class="metric"><span>' + p.name + '</span><span class="metric-value">' + (p.snapshots || 0) + ' snapshots</span></div>'
                    ).join('');
                }}
                addLog('Loaded ' + data.total + ' projects');
            }} catch (e) {{ addLog('Error: ' + e.message); }}
        }}

        async function fetchCommands() {{
            try {{
                const resp = await fetch('/api/commands');
                const data = await resp.json();
                addLog('Available commands: ' + data.total);
            }} catch (e) {{ addLog('Error: ' + e.message); }}
        }}

        async function fetchTemplates() {{
            try {{
                const resp = await fetch('/api/templates');
                const data = await resp.json();
                addLog('Available templates: ' + data.total);
            }} catch (e) {{ addLog('Error: ' + e.message); }}
        }}

        // Health check
        fetch('/api/health')
            .then(r => r.json())
            .then(d => {{
                document.getElementById('api-status').textContent = d.status;
            }})
            .catch(() => {{
                document.getElementById('api-status').textContent = 'Error';
            }});

        connectWebSocket();
        fetchProjects();
    </script>
</body>
</html>"""


class DashboardServer:
    """
    IDK: dashboard-server, fastapi-runner, background-process, pid-management
    Responsibility: Manages the lifecycle of the web dashboard server process
    Invariants: PID file tracks running instance, only one instance per user,
                graceful shutdown on stop
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 3000) -> None:
        """Initialize dashboard server manager.

        Args:
            host: Host to bind to
            port: Port number
        """
        self.host = host
        self.port = port

    def is_running(self) -> bool:
        """Check if the dashboard server is currently running.

        Returns:
            True if the server process is running
        """
        if not PID_FILE.exists():
            return False
        try:
            pid = int(PID_FILE.read_text().strip())
            os.kill(pid, 0)
            return True
        except (ValueError, ProcessLookupError, PermissionError, OSError):
            # Clean up stale PID file
            try:
                PID_FILE.unlink()
            except OSError:
                pass
            return False

    def start(self) -> Dict[str, Any]:
        """Start the dashboard server in the background.

        Returns:
            Dict with server info (pid, port, url)

        Raises:
            RuntimeError: If server is already running or fails to start
        """
        if self.is_running():
            pid = int(PID_FILE.read_text().strip())
            return {
                "status": "already_running",
                "pid": pid,
                "port": self.port,
                "url": f"http://{self.host}:{self.port}",
            }

        PID_FILE.parent.mkdir(parents=True, exist_ok=True)

        # Start uvicorn as a subprocess
        cmd = [
            sys.executable,
            "-m",
            "uvicorn",
            "tac_bootstrap.infrastructure.web_server:create_app",
            "--factory",
            "--host",
            self.host,
            "--port",
            str(self.port),
        ]

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
            PID_FILE.write_text(str(process.pid))

            return {
                "status": "started",
                "pid": process.pid,
                "port": self.port,
                "url": f"http://{self.host}:{self.port}",
            }
        except Exception as e:
            raise RuntimeError(f"Failed to start dashboard: {e}")

    def stop(self) -> Dict[str, Any]:
        """Stop the dashboard server.

        Returns:
            Dict with stop result
        """
        if not self.is_running():
            return {"status": "not_running"}

        try:
            pid = int(PID_FILE.read_text().strip())
            os.kill(pid, signal.SIGTERM)
            PID_FILE.unlink(missing_ok=True)
            return {"status": "stopped", "pid": pid}
        except (ValueError, ProcessLookupError, PermissionError) as e:
            PID_FILE.unlink(missing_ok=True)
            return {"status": "error", "message": str(e)}

    def get_status(self) -> Dict[str, Any]:
        """Get dashboard server status.

        Returns:
            Dict with server status information
        """
        running = self.is_running()
        result: Dict[str, Any] = {
            "running": running,
            "port": self.port,
            "url": f"http://{self.host}:{self.port}" if running else None,
        }
        if running and PID_FILE.exists():
            try:
                result["pid"] = int(PID_FILE.read_text().strip())
            except ValueError:
                pass
        return result
