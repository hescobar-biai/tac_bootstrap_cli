# MCP Python SDK

**Python implementation of the Model Context Protocol (MCP)**

The Model Context Protocol allows applications to provide context for LLMs in a standardized way, separating the concerns of providing context from the actual LLM interaction. This Python SDK implements the full MCP specification, making it easy to:

- Build MCP clients that can connect to any MCP server
- Create MCP servers that expose resources, prompts and tools
- Use standard transports like stdio, SSE, and Streamable HTTP
- Handle all MCP protocol messages and lifecycle events

## Installation

### Adding MCP to your python project

We recommend using [uv](https://docs.astral.sh/uv/) to manage your Python projects.

If you haven't created a uv-managed project yet, create one:

```bash
uv init mcp-server-demo
cd mcp-server-demo
```

Then add MCP to your project dependencies:

```bash
uv add "mcp[cli]"
```

Alternatively, for projects using pip for dependencies:

```bash
pip install "mcp[cli]"
```

## Quickstart

Let's create a simple MCP server that exposes a calculator tool and some data:

```python
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

# Add a prompt
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."
```

You can install this server in Claude Desktop and interact with it right away by running:

```bash
uv run mcp install server.py
```

Alternatively, you can test it with the MCP Inspector:

```bash
uv run mcp dev server.py
```

## What is MCP?

The Model Context Protocol (MCP) lets you build servers that expose data and functionality to LLM applications in a secure, standardized way. Think of it like a web API, but specifically designed for LLM interactions. MCP servers can:

- Expose data through **Resources** (think of these sort of like GET endpoints; they are used to load information into the LLM's context)
- Provide functionality through **Tools** (sort of like POST endpoints; they are used to execute code or otherwise produce a side effect)
- Define interaction patterns through **Prompts** (reusable templates for LLM interactions)
- And more!

## Core Concepts

### Server

The FastMCP server is your core interface to the MCP protocol. It handles connection management, protocol compliance, and message routing.

### Resources

Resources are how you expose data to LLMs. They're similar to GET endpoints in a REST API - they provide data but shouldn't perform significant computation or have side effects:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="Resource Example")

@mcp.resource("file://documents/{name}")
def read_document(name: str) -> str:
    """Read a document by name."""
    # This would normally read from disk
    return f"Content of {name}"

@mcp.resource("config://settings")
def get_settings() -> str:
    """Get application settings."""
    return """{
  "theme": "dark",
  "language": "en",
  "debug": false
}"""
```

### Tools

Tools let LLMs take actions through your server. Unlike resources, tools are expected to perform computation and have side effects:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="Tool Example")

@mcp.tool()
def sum(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@mcp.tool()
def get_weather(city: str, unit: str = "celsius") -> str:
    """Get weather for a city."""
    # This would normally call a weather API
    return f"Weather in {city}: 22 degrees {unit[0].upper()}"
```

### Prompts

Prompts are reusable templates that help LLMs interact with your server effectively:

```python
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP(name="Prompt Example")

@mcp.prompt(title="Code Review")
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"

@mcp.prompt(title="Debug Assistant")
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]
```

### Context

The Context object is automatically injected into tool and resource functions that request it via type hints. It provides access to MCP capabilities like logging, progress reporting, resource reading, user interaction, and request metadata.

```python
from mcp.server.fastmcp import Context, FastMCP

mcp = FastMCP(name="Context Example")

@mcp.tool()
async def my_tool(x: int, ctx: Context) -> str:
    """Tool that uses context capabilities."""
    await ctx.info(f"Processing {x}")
    await ctx.report_progress(progress=0.5, total=1.0, message="Halfway done")
    return f"Processed {x}"
```

## Running Your Server

### Development Mode

The fastest way to test and debug your server is with the MCP Inspector:

```bash
uv run mcp dev server.py

# Add dependencies
uv run mcp dev server.py --with pandas --with numpy

# Mount local code
uv run mcp dev server.py --with-editable .
```

### Claude Desktop Integration

Once your server is ready, install it in Claude Desktop:

```bash
uv run mcp install server.py

# Custom name
uv run mcp install server.py --name "My Analytics Server"

# Environment variables
uv run mcp install server.py -v API_KEY=abc123 -v DB_URL=postgres://...
uv run mcp install server.py -f .env
```

### Direct Execution

For advanced scenarios like custom deployments:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My App")

@mcp.tool()
def hello(name: str = "World") -> str:
    """Say hello to someone."""
    return f"Hello, {name}!"

def main():
    """Entry point for the direct execution server."""
    mcp.run()

if __name__ == "__main__":
    main()
```

Run it with:

```bash
python server.py
# or
uv run mcp run server.py
```

## MCP Primitives

The MCP protocol defines three core primitives that servers can implement:

| Primitive | Control | Description | Example Use |
| --- | --- | --- | --- |
| Prompts | User-controlled | Interactive templates invoked by user choice | Slash commands, menu options |
| Resources | Application-controlled | Contextual data managed by the client application | File contents, API responses |
| Tools | Model-controlled | Functions exposed to the LLM to take actions | API calls, data updates |

## Documentation

- [Model Context Protocol documentation](https://modelcontextprotocol.io/)
- [Model Context Protocol specification](https://spec.modelcontextprotocol.io/)
- [Officially supported servers](https://github.com/modelcontextprotocol/servers)
- [GitHub Repository](https://github.com/modelcontextprotocol/python-sdk)

## License

This project is licensed under the MIT License.
