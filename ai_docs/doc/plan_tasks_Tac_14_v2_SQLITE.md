# Plan TAC-14 v2: SQLite First Approach

## Justificación del Cambio

**Problema original**: El plan TAC-14 v1 propone PostgreSQL como base de datos, lo cual requiere:
- Instalación y configuración de PostgreSQL 14+
- Setup de credenciales y permisos
- Conocimiento de administración de bases de datos
- Configuración de conexiones y pooling

**Solución propuesta**: Usar SQLite para v0.8.0 (primera versión de TAC-14)

## Ventajas de SQLite para v1

1. **Zero Configuration**: No requiere instalación ni servidor separado
2. **Portabilidad**: Base de datos en un solo archivo (.db)
3. **Simplicidad**: Perfecto para desarrollo local y testing
4. **Sin barreras de entrada**: Funciona out-of-the-box
5. **Suficiente para v1**: Soporta todas las features necesarias para orchestrator local
6. **Fácil migración**: Se puede migrar a PostgreSQL en v0.9.0 si se necesita scale

## Cambios al Plan Original

### FASE 5: Database-Backed ADWs (Class 3)

#### Tarea 6 - MODIFICADA
**[FEATURE] Implementar Database Schema SQLite (BASE + TEMPLATES)**

**Cambios**:
```diff
+ Crear schema SQLite con sqlite3

+ Archivo: schema_orchestrator.sqlite (SQLite dialect)

+ Usar tipos SQLite nativos
```

**Schema SQLite adaptado**:
```sql
-- orchestrator_agents table
CREATE TABLE orchestrator_agents (
    id TEXT PRIMARY KEY,  -- UUID as TEXT
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    status TEXT DEFAULT 'active',
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

-- agents table (runtime instances)
CREATE TABLE agents (
    id TEXT PRIMARY KEY,
    orchestrator_agent_id TEXT NOT NULL,
    session_id TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at TEXT DEFAULT (datetime('now')),
    started_at TEXT,
    completed_at TEXT,
    FOREIGN KEY (orchestrator_agent_id) REFERENCES orchestrator_agents(id)
);

-- prompts table (ADW executions)
CREATE TABLE prompts (
    id TEXT PRIMARY KEY,
    agent_id TEXT NOT NULL,
    content TEXT NOT NULL,
    response TEXT,
    status TEXT DEFAULT 'pending',
    tokens_input INTEGER DEFAULT 0,
    tokens_output INTEGER DEFAULT 0,
    cost_usd REAL DEFAULT 0.0,
    created_at TEXT DEFAULT (datetime('now')),
    completed_at TEXT,
    FOREIGN KEY (agent_id) REFERENCES agents(id)
);

-- agent_logs table
CREATE TABLE agent_logs (
    id TEXT PRIMARY KEY,
    agent_id TEXT NOT NULL,
    log_type TEXT NOT NULL,  -- 'step_start', 'step_end', 'event'
    message TEXT NOT NULL,
    metadata TEXT,  -- JSON as TEXT
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (agent_id) REFERENCES agents(id)
);

-- system_logs table
CREATE TABLE system_logs (
    id TEXT PRIMARY KEY,
    log_level TEXT NOT NULL,  -- 'info', 'warning', 'error'
    message TEXT NOT NULL,
    source TEXT,
    metadata TEXT,  -- JSON as TEXT
    created_at TEXT DEFAULT (datetime('now'))
);

-- Indexes for performance
CREATE INDEX idx_agents_orchestrator_agent_id ON agents(orchestrator_agent_id);
CREATE INDEX idx_agents_session_id ON agents(session_id);
CREATE INDEX idx_prompts_agent_id ON prompts(agent_id);
CREATE INDEX idx_agent_logs_agent_id ON agent_logs(agent_id);
CREATE INDEX idx_agent_logs_created_at ON agent_logs(created_at);
CREATE INDEX idx_system_logs_created_at ON system_logs(created_at);
```

**Rutas impactadas**:
```
adws/schema/schema_orchestrator.sqlite  [CREAR]
adws/schema/migrations/                 [CREAR]
adws/schema/README.md                   [MODIFICAR - setup SQLite]
```

---

#### Tarea 7 - MODIFICADA
**[FEATURE] Implementar Database Models para SQLite (BASE + TEMPLATES)**

**Cambios**:
```diff
+ field_validator para UUID como string, Decimal como float
+ json_encoders para SQLite types
```

**Ejemplo de modelo adaptado**:
```python
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import json

class OrchestratorAgent(BaseModel):
    """Orchestrator Agent model for SQLite."""
    id: str = Field(..., description="UUID as string")
    name: str
    description: Optional[str] = None
    status: str = "active"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator('id')
    def validate_uuid(cls, v):
        """Validate UUID format (stored as TEXT in SQLite)."""
        import uuid
        try:
            uuid.UUID(v)
            return v
        except ValueError:
            raise ValueError("Invalid UUID format")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
```

---

#### Tarea 8 - MODIFICADA
**[FEATURE] Implementar Database Operations con sqlite3/aiosqlite (BASE + TEMPLATES)**

**Cambios principales**:
```diff

+ aiosqlite para SQLite asíncrono
+ Connection pooling simple con aiosqlite
+ SQLite queries (? placeholders)
+ SELECT last_insert_rowid() (SQLite)
```

**Ejemplo de CRUD adaptado**:
```python
import aiosqlite
import json
from typing import Optional, List
from datetime import datetime
import uuid

class DatabaseManager:
    """Database operations manager for SQLite."""

    def __init__(self, db_path: str = "orchestrator.db"):
        self.db_path = db_path
        self.conn: Optional[aiosqlite.Connection] = None

    async def connect(self):
        """Initialize database connection."""
        self.conn = await aiosqlite.connect(self.db_path)
        self.conn.row_factory = aiosqlite.Row  # Dict-like rows
        await self._init_schema()

    async def close(self):
        """Close database connection."""
        if self.conn:
            await self.conn.close()

    async def _init_schema(self):
        """Initialize database schema if not exists."""
        with open("adws/schema/schema_orchestrator.sqlite", "r") as f:
            schema = f.read()
        await self.conn.executescript(schema)
        await self.conn.commit()

    # CRUD for orchestrator_agents
    async def create_orchestrator_agent(
        self,
        name: str,
        description: Optional[str] = None
    ) -> str:
        """Create new orchestrator agent."""
        agent_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()

        await self.conn.execute(
            """
            INSERT INTO orchestrator_agents (id, name, description, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (agent_id, name, description, now, now)
        )
        await self.conn.commit()
        return agent_id

    async def get_orchestrator_agent(self, agent_id: str) -> Optional[dict]:
        """Get orchestrator agent by ID."""
        async with self.conn.execute(
            "SELECT * FROM orchestrator_agents WHERE id = ?",
            (agent_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None

    async def list_orchestrator_agents(self) -> List[dict]:
        """List all orchestrator agents."""
        async with self.conn.execute(
            "SELECT * FROM orchestrator_agents ORDER BY created_at DESC"
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    # CRUD for agents (runtime instances)
    async def create_agent(
        self,
        orchestrator_agent_id: str,
        session_id: str
    ) -> str:
        """Create new agent instance."""
        agent_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()

        await self.conn.execute(
            """
            INSERT INTO agents (id, orchestrator_agent_id, session_id, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (agent_id, orchestrator_agent_id, session_id, now)
        )
        await self.conn.commit()
        return agent_id

    # ... más métodos CRUD para prompts, logs, etc.
```

**Dependencies**:
```python
# PEP 723 dependency (en adw_database.py)
# /// script
# dependencies = ["aiosqlite>=0.19.0"]
# ///
```

---

#### Tarea 9 - MODIFICADA
**[FEATURE] Implementar Database Logging con SQLite (BASE + TEMPLATES)**

**Cambios**:
```diff
+ Logging asíncrono con aiosqlite

+ JSON serialization con TEXT field
```

**Ejemplo de logging adaptado**:
```python
import json
from datetime import datetime
import uuid

async def log_agent_event(
    db: DatabaseManager,
    agent_id: str,
    log_type: str,
    message: str,
    metadata: Optional[dict] = None
):
    """Log agent event to database."""
    log_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()
    metadata_json = json.dumps(metadata) if metadata else None

    await db.conn.execute(
        """
        INSERT INTO agent_logs (id, agent_id, log_type, message, metadata, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (log_id, agent_id, log_type, message, metadata_json, now)
    )
    await db.conn.commit()
```

---

### FASE 7: Orchestrator Web Application

#### Tarea 12 - MODIFICADA
**[FEATURE] Implementar Orchestrator Backend con SQLite (BASE + TEMPLATES)**

**Cambios**:
```diff
+ SQLite connection en FastAPI

+ DATABASE_URL=sqlite:///./orchestrator.db

- asyncpg dependencies
+ aiosqlite dependencies
```

**FastAPI app adaptado**:
```python
from fastapi import FastAPI, WebSocket
from contextlib import asynccontextmanager
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../adws"))
from adw_modules.adw_database import DatabaseManager

# Database instance
db_manager: DatabaseManager = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for database connection."""
    global db_manager

    # Startup: Initialize database
    db_manager = DatabaseManager("orchestrator.db")
    await db_manager.connect()

    yield

    # Shutdown: Close database
    await db_manager.close()

app = FastAPI(
    title="TAC Bootstrap Orchestrator",
    version="0.8.0",
    lifespan=lifespan
)

@app.get("/api/agents")
async def list_agents():
    """List all orchestrator agents."""
    agents = await db_manager.list_orchestrator_agents()
    return {"agents": agents}

# ... más endpoints ...
```

**Environment variables (.env.sample)**:
```bash
# Database
DATABASE_PATH=orchestrator.db

# WebSocket
WEBSOCKET_PORT=8765

# Web UI
WEB_UI_PORT=5173
```

---

### FASE 10: Utility Scripts

#### Tarea 19 - MODIFICADA
**[FEATURE] Implementar Utility Scripts simplificados (BASE + TEMPLATES)**

**Cambios**:
```diff
+ scripts/setup_database.sh (SQLite init - muy simple)

+ Solo crear archivo .db y ejecutar schema
```

**Script simplificado**:
```bash
#!/bin/bash
# setup_database.sh - Initialize SQLite database

set -e

DB_PATH="${1:-orchestrator.db}"
SCHEMA_FILE="adws/schema/schema_orchestrator.sqlite"

echo "🔧 Setting up SQLite database..."

# Check if schema file exists
if [ ! -f "$SCHEMA_FILE" ]; then
    echo "❌ Error: Schema file not found: $SCHEMA_FILE"
    exit 1
fi

# Remove existing database if it exists
if [ -f "$DB_PATH" ]; then
    echo "⚠️  Existing database found. Removing..."
    rm "$DB_PATH"
fi

# Create new database and apply schema
echo "📝 Creating database and applying schema..."
sqlite3 "$DB_PATH" < "$SCHEMA_FILE"

echo "✅ Database initialized successfully: $DB_PATH"
echo "   Tables created: orchestrator_agents, agents, prompts, agent_logs, system_logs"
```

---

## Migration Path: SQLite → PostgreSQL (v0.9.0)

Para usuarios que eventualmente necesiten scale, documentar path de migración:

### Cuándo migrar a PostgreSQL:
- Multiple usuarios concurrentes (>10)
- Volumen alto de logs (>1M registros)
- Necesidad de replicación
- Deployment en producción con alta disponibilidad

### Script de migración:
```bash
#!/bin/bash
# migrate_sqlite_to_postgresql.sh

# 1. Dump SQLite data
sqlite3 orchestrator.db .dump > dump.sql

# 2. Convert SQLite → PostgreSQL dialect
# (usar herramienta como pgloader)
pgloader orchestrator.db postgresql://user:pass@localhost/orchestrator

# 3. Verify data integrity
# ... validation scripts ...
```

---

## Actualización de Supuestos (Assumptions)

**Original**:
```
1. PostgreSQL disponible: Se asume PostgreSQL 14+ instalado y accesible
```

**Actualizado**:
```
1. SQLite disponible: Se asume Python 3.10+ con sqlite3 incluido (viene por defecto)
2. PostgreSQL opcional: Para v0.9.0+ se puede migrar a PostgreSQL si se necesita scale
```

---

## Actualización de Dependencies

**Original**:
```python
# Python dependencies
asyncpg>=0.29.0  # PostgreSQL async driver
```

**Actualizado**:
```python
# Python dependencies
aiosqlite>=0.19.0  # SQLite async driver (mucho más liviano)
```

---

## Resumen de Beneficios

### Para Usuarios (v0.8.0 con SQLite):
✅ Zero setup - funciona out-of-the-box
✅ Sin barreras de entrada - no requiere PostgreSQL
✅ Portabilidad - archivo único .db
✅ Ideal para desarrollo local y testing
✅ Suficiente para mayoría de casos de uso

### Para Mantenedores:
✅ Menos complejidad en setup scripts
✅ Menos soporte técnico requerido
✅ Tests más rápidos (sin Docker/PostgreSQL)
✅ CI/CD más simple

### Path Forward:
- **v0.8.0 (TAC-14 v1)**: SQLite como default
- **v0.9.0 (TAC-14 v2)**: PostgreSQL como opción para producción/scale
- **Ambos soportados**: Abstracción en database layer permite ambos backends

---

## Conclusión

**Recomendación**: Implementar TAC-14 v1 (v0.8.0) con SQLite first approach.

**Razón**: Maximiza adopción reduciendo barreras de entrada, mientras mantiene todas las features de Class 3 (Orchestrator). PostgreSQL queda como upgrade path opcional para usuarios avanzados en v0.9.0.

**Esfuerzo de cambio**: Mínimo - la mayoría del código es agnóstico a la base de datos gracias a la capa de abstracción (DatabaseManager).
