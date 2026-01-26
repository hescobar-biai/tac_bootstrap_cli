# Claude Code SDK

The Claude Code SDK enables running Claude Code as a subprocess, providing a way to build AI-powered coding assistants and tools that leverage Claude's capabilities.

The SDK is available for command line, TypeScript, and Python usage.

## Authentication

### Anthropic API key

To use the Claude Code SDK directly with Anthropic's API, we recommend creating a dedicated API key:

1. Create an Anthropic API key in the [Anthropic Console](https://console.anthropic.com/)
2. Then, set the `ANTHROPIC_API_KEY` environment variable. We recommend storing this key securely (e.g., using a Github [secret](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions))

### Third-Party API credentials

The SDK also supports third-party API providers:

- **Amazon Bedrock**: Set `CLAUDE_CODE_USE_BEDROCK=1` environment variable and configure AWS credentials
- **Google Vertex AI**: Set `CLAUDE_CODE_USE_VERTEX=1` environment variable and configure Google Cloud credentials

## Basic SDK usage

The Claude Code SDK allows you to use Claude Code in non-interactive mode from your applications.

### Command line

Here are a few basic examples for the command line SDK:

```bash
# Run a single prompt and exit (print mode)
$ claude -p "Write a function to calculate Fibonacci numbers"

# Using a pipe to provide stdin
$ echo "Explain this code" | claude -p

# Output in JSON format with metadata
$ claude -p "Generate a hello world function" --output-format json

# Stream JSON output as it arrives
$ claude -p "Build a React component" --output-format stream-json
```

### TypeScript

The TypeScript SDK is included in the main [`@anthropic-ai/claude-code`](https://www.npmjs.com/package/@anthropic-ai/claude-code) package on NPM:

```ts
import { query, type SDKMessage } from "@anthropic-ai/claude-code";

const messages: SDKMessage[] = [];

for await (const message of query({
  prompt: "Write a haiku about foo.py",
  abortController: new AbortController(),
  options: {
    maxTurns: 3,
  },
})) {
  messages.push(message);
}

console.log(messages);
```

The TypeScript SDK accepts all arguments supported by the command line SDK, as well as:

| Argument | Description | Default |
| --- | --- | --- |
| `abortController` | Abort controller | `new AbortController()` |
| `cwd` | Current working directory | `process.cwd()` |
| `executable` | Which JavaScript runtime to use | `node` when running with Node.js, `bun` when running with Bun |
| `executableArgs` | Arguments to pass to the executable | `[]` |
| `pathToClaudeCodeExecutable` | Path to the Claude Code executable | Executable that ships with `@anthropic-ai/claude-code` |

### Python

The Python SDK is available as [`claude-code-sdk`](https://github.com/anthropics/claude-code-sdk-python) on PyPI:

```bash
pip install claude-code-sdk
```

**Prerequisites:**

- Python 3.10+
- Node.js
- Claude Code CLI: `npm install -g @anthropic-ai/claude-code`

Basic usage:

```python
import anyio
from claude_code_sdk import query, ClaudeCodeOptions, Message

async def main():
    messages: list[Message] = []

    async for message in query(
        prompt="Write a haiku about foo.py",
        options=ClaudeCodeOptions(max_turns=3)
    ):
        messages.append(message)

    print(messages)

anyio.run(main)
```

The Python SDK accepts all arguments supported by the command line SDK through the `ClaudeCodeOptions` class:

```python
from claude_code_sdk import query, ClaudeCodeOptions
from pathlib import Path

options = ClaudeCodeOptions(
    max_turns=3,
    system_prompt="You are a helpful assistant",
    cwd=Path("/path/to/project"),  # Can be string or Path
    allowed_tools=["Read", "Write", "Bash"],
    permission_mode="acceptEdits"
)

async for message in query(prompt="Hello", options=options):
    print(message)
```

## Advanced usage

### Multi-turn conversations

For multi-turn conversations, you can resume conversations or continue from the most recent session:

```bash
# Continue the most recent conversation
$ claude --continue

# Continue and provide a new prompt
$ claude --continue "Now refactor this for better performance"

# Resume a specific conversation by session ID
$ claude --resume 550e8400-e29b-41d4-a716-446655440000

# Resume in print mode (non-interactive)
$ claude -p --resume 550e8400-e29b-41d4-a716-446655440000 "Update the tests"

# Continue in print mode (non-interactive)
$ claude -p --continue "Add error handling"
```

### Custom system prompts

You can provide custom system prompts to guide Claude's behavior:

```bash
# Override system prompt (only works with --print)
$ claude -p "Build a REST API" --system-prompt "You are a senior backend engineer. Focus on security, performance, and maintainability."

# System prompt with specific requirements
$ claude -p "Create a database schema" --system-prompt "You are a database architect. Use PostgreSQL best practices and include proper indexing."
```

You can also append instructions to the default system prompt:

```bash
# Append system prompt (only works with --print)
$ claude -p "Build a REST API" --append-system-prompt "After writing code, be sure to code review yourself."
```

### MCP Configuration

The Model Context Protocol (MCP) allows you to extend Claude Code with additional tools and resources from external servers. Using the `--mcp-config` flag, you can load MCP servers that provide specialized capabilities like database access, API integrations, or custom tooling.

Create a JSON configuration file with your MCP servers:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/allowed/files"
      ]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your-github-token"
      }
    }
  }
}
```

Then use it with Claude Code:

```bash
# Load MCP servers from configuration
$ claude -p "List all files in the project" --mcp-config mcp-servers.json

# Important: MCP tools must be explicitly allowed using --allowedTools
# MCP tools follow the format: mcp__$serverName__$toolName
$ claude -p "Search for TODO comments" \
  --mcp-config mcp-servers.json \
  --allowedTools "mcp__filesystem__read_file,mcp__filesystem__list_directory"
```

## Available CLI options

| Flag | Description | Example |
| --- | --- | --- |
| `--print`, `-p` | Run in non-interactive mode | `claude -p "query"` |
| `--output-format` | Specify output format ( `text`, `json`, `stream-json`) | `claude -p --output-format json` |
| `--resume`, `-r` | Resume a conversation by session ID | `claude --resume abc123` |
| `--continue`, `-c` | Continue the most recent conversation | `claude --continue` |
| `--verbose` | Enable verbose logging | `claude --verbose` |
| `--max-turns` | Limit agentic turns in non-interactive mode | `claude --max-turns 3` |
| `--system-prompt` | Override system prompt (only with `--print`) | `claude --system-prompt "Custom instruction"` |
| `--append-system-prompt` | Append to system prompt (only with `--print`) | `claude --append-system-prompt "Custom instruction"` |
| `--allowedTools` | Space-separated list of allowed tools | `claude --allowedTools mcp__slack mcp__filesystem` |
| `--disallowedTools` | Space-separated list of denied tools | `claude --disallowedTools mcp__splunk mcp__github` |
| `--mcp-config` | Load MCP servers from a JSON file | `claude --mcp-config servers.json` |
| `--permission-prompt-tool` | MCP tool for handling permission prompts (only with `--print`) | `claude --permission-prompt-tool mcp__auth__prompt` |

## Output formats

### Text output (default)

Returns just the response text:

```bash
$ claude -p "Explain file src/components/Header.tsx"
# Output: This is a React component showing...
```

### JSON output

Returns structured data including metadata:

```bash
$ claude -p "How does the data layer work?" --output-format json
```

Response format:

```json
{
  "type": "result",
  "subtype": "success",
  "total_cost_usd": 0.003,
  "is_error": false,
  "duration_ms": 1234,
  "duration_api_ms": 800,
  "num_turns": 6,
  "result": "The response text here...",
  "session_id": "abc123"
}
```

### Streaming JSON output

Streams each message as it is received:

```bash
$ claude -p "Build an application" --output-format stream-json
```

## Best practices

1. **Use JSON output format** for programmatic parsing of responses:

```bash
# Parse JSON response with jq
result=$(claude -p "Generate code" --output-format json)
code=$(echo "$result" | jq -r '.result')
cost=$(echo "$result" | jq -r '.cost_usd')
```

2. **Handle errors gracefully** - check exit codes and stderr:

```bash
if ! claude -p "$prompt" 2>error.log; then
       echo "Error occurred:" >&2
       cat error.log >&2
       exit 1
fi
```

3. **Use session management** for maintaining context in multi-turn conversations

4. **Consider timeouts** for long-running operations:

```bash
timeout 300 claude -p "$complex_prompt" || echo "Timed out after 5 minutes"
```

5. **Respect rate limits** when making multiple requests by adding delays between calls

## Related resources

- [CLI usage and controls](https://docs.anthropic.com/en/docs/claude-code/cli-reference) - Complete CLI documentation
- [GitHub Actions integration](https://docs.anthropic.com/en/docs/claude-code/github-actions) - Automate your GitHub workflow with Claude
- [Common workflows](https://docs.anthropic.com/en/docs/claude-code/common-workflows) - Step-by-step guides for common use cases
