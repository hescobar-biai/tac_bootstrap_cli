# E2B - Secure Cloud Sandboxes for AI-Generated Code

E2B is an open-source runtime for executing AI-generated code in secure cloud sandboxes. Perfect for agentic AI use cases, data analysis, code interpretation, and more.

## What is E2B?

E2B provides secure, isolated cloud sandboxes that can run AI-generated code safely. Each sandbox is a small VM that starts quickly (~150ms) and can be used for various AI applications like data analysis, visualization, coding agents, and full AI-generated apps.

### Key Features

- **Fast startup**: Sandboxes start in under 200ms (no cold starts)
- **Secure**: Powered by Firecracker microVMs for untrusted code execution
- **LLM-agnostic**: Works with OpenAI, Anthropic, Mistral, Llama, and custom models
- **Multiple languages**: Python, JavaScript, Ruby, C++, and more
- **Persistent sessions**: Up to 24-hour sandbox sessions
- **Internet access**: Full internet connectivity with public URLs
- **Package installation**: Install custom packages via pip, npm, apt-get
- **File operations**: Upload, download, and manipulate files

## Quick Start (Python)

### 1. Installation

```bash
pip install e2b-code-interpreter
```

### 2. Set Environment Variable

```bash
export E2B_API_KEY="your_api_key_here"
```

Get your API key from the [E2B Dashboard](https://www.e2b.dev/dashboard?tab=keys).

### 3. Basic Usage

```python
from e2b_code_interpreter import Sandbox

# Create a sandbox
with Sandbox() as sandbox:
    # Run Python code
    execution = sandbox.run_code("print('Hello, E2B!')")
    print(execution.text)  # Output: Hello, E2B!

    # List files in sandbox
    files = sandbox.files.list('/')
    print(files)
```

### 4. Advanced Example with Data Analysis

```python
from e2b_code_interpreter import Sandbox
import pandas as pd

with Sandbox() as sandbox:
    # Upload a CSV file
    csv_data = "name,age,city\nJohn,25,NYC\nJane,30,LA"
    sandbox.files.write('/tmp/data.csv', csv_data)

    # Analyze data with pandas
    code = """
import pandas as pd
import matplotlib.pyplot as plt

# Load and analyze data
df = pd.read_csv('/tmp/data.csv')
print("Data shape:", df.shape)
print("\\nData preview:")
print(df.head())

# Create a simple plot
plt.figure(figsize=(8, 6))
plt.bar(df['name'], df['age'])
plt.title('Age by Name')
plt.xlabel('Name')
plt.ylabel('Age')
plt.savefig('/tmp/plot.png')
print("\\nPlot saved to /tmp/plot.png")
"""

    execution = sandbox.run_code(code)
    print(execution.text)

    # Download the generated plot
    plot_data = sandbox.files.read('/tmp/plot.png')
    with open('plot.png', 'wb') as f:
        f.write(plot_data)
```

## Sandbox Management

### Create Sandbox with Custom Timeout

```python
# Python
with Sandbox(timeout=300) as sandbox:  # 5 minutes
    # Your code here
    pass

# Or extend timeout during runtime
sandbox.set_timeout(600)  # 10 minutes
```

### Sandbox Persistence (Beta)

Pause and resume sandboxes to maintain state across sessions:

```python
# Pause sandbox (saves filesystem + memory state)
sandbox_id = sandbox.pause()
print(f"Sandbox paused: {sandbox_id}")

# Resume later from exact same state
resumed_sandbox = Sandbox.resume(sandbox_id)
```

## Package Installation

### Runtime Installation

```python
with Sandbox() as sandbox:
    # Install Python packages
    sandbox.commands.run('pip install requests beautifulsoup4')

    # Install system packages
    sandbox.commands.run('apt-get update && apt-get install -y curl git')

    # Install Node.js packages
    sandbox.commands.run('npm install axios')

    # Now use the packages
    sandbox.run_code("""
import requests
response = requests.get('https://api.github.com/users/e2b-dev')
print(response.json()['name'])
""")
```

## File Operations

### Upload/Download Files

```python
with Sandbox() as sandbox:
    # Write text file
    sandbox.files.write('/tmp/hello.txt', 'Hello, World!')

    # Write binary file
    with open('local_image.png', 'rb') as f:
        image_data = f.read()
    sandbox.files.write('/tmp/image.png', image_data)

    # Read file
    content = sandbox.files.read('/tmp/hello.txt', text=True)
    print(content)

    # List directory
    files = sandbox.files.list('/tmp')
    for file in files:
        print(f"{file.name}: {file.type}")

    # Download file
    result_data = sandbox.files.read('/tmp/result.csv')
    with open('local_result.csv', 'wb') as f:
        f.write(result_data)
```

## Internet Access & Servers

Sandboxes have full internet access and can host services:

```python
with Sandbox() as sandbox:
    # Start a web server
    process = sandbox.commands.run('python -m http.server 8000', background=True)

    # Get public URL
    host = sandbox.get_host(8000)
    url = f"https://{host}"
    print(f"Server running at: {url}")

    # Make requests from outside
    import requests
    response = requests.get(url)
    print(response.text)

    # Clean up
    process.kill()
```

## LLM Provider Examples

### Anthropic Integration

```python
from anthropic import Anthropic
from e2b_code_interpreter import Sandbox

anthropic = Anthropic()

response = anthropic.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Write Python code to analyze this CSV data and create visualizations"}
    ]
)

code = response.content[0].text

with Sandbox() as sandbox:
    execution = sandbox.run_code(code)
    print(execution.text)
```

## Best Practices

### 1. Resource Management

```python
# Always use context managers
with Sandbox() as sandbox:
    # Your code here
    pass  # Sandbox automatically cleaned up

# Or explicitly kill
sandbox = Sandbox.create()
try:
    # Your code here
    pass
finally:
    sandbox.kill()
```

### 2. Error Handling

```python
with Sandbox() as sandbox:
    execution = sandbox.run_code("print(1/0)")  # This will error

    if execution.error:
        print(f"Error occurred: {execution.error}")
        print(f"Error type: {execution.error.name}")
        print(f"Error message: {execution.error.value}")
    else:
        print(f"Success: {execution.text}")
```

## Resources

- **Documentation**: https://www.e2b.dev/docs
- **GitHub**: https://github.com/e2b-dev
- **Discord Community**: https://discord.com/invite/U7KEcGErtQ
- **Dashboard**: https://www.e2b.dev/dashboard
- **Cookbook Examples**: https://github.com/e2b-dev/e2b-cookbook

E2B makes it easy to run AI-generated code safely and efficiently. Start building your AI applications with secure, scalable sandbox execution today!
