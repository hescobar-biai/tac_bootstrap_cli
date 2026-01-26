# OpenAI Developer Quickstart

Take your first steps with the OpenAI API.

The OpenAI API provides a simple interface to state-of-the-art AI models for text generation, natural language processing, computer vision, and more.

## Generate text from a model

### Python

```python
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-4.1",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)
```

### JavaScript

```javascript
import OpenAI from "openai";
const client = new OpenAI();

const response = await client.responses.create({
    model: "gpt-4.1",
    input: "Write a one-sentence bedtime story about a unicorn."
});

console.log(response.output_text);
```

### cURL

```bash
curl "https://api.openai.com/v1/responses" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -d '{
        "model": "gpt-4.1",
        "input": "Write a one-sentence bedtime story about a unicorn."
    }'
```

### Data retention for model responses

Response objects are saved for 30 days by default. They can be viewed in the dashboard logs page or retrieved via the API. You can disable this behavior by setting `store` to `false` when creating a Response.

OpenAI does not use data sent via API to train our models without your explicit consent.

## Analyze image inputs

You can provide image inputs to the model as well. Scan receipts, analyze screenshots, or find objects in the real world with computer vision.

### Python

```python
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-4.1",
    input=[
        {"role": "user", "content": "what teams are playing in this image?"},
        {
            "role": "user",
            "content": [
                {
                    "type": "input_image",
                    "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/3b/LeBron_James_Layup_%28Cleveland_vs_Brooklyn_2018%29.jpg"
                }
            ]
        }
    ]
)

print(response.output_text)
```

## Extend the model with tools

Give the model access to new data and capabilities using tools. You can either call your own custom code, or use one of OpenAI's powerful built-in tools.

### Get information from the Internet

```python
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-4.1",
    tools=[{"type": "web_search_preview"}],
    input="What was a positive news story from today?"
)

print(response.output_text)
```

## Deliver blazing fast AI experiences

Using either the Realtime API or server-sent streaming events, you can build high performance, low-latency experiences for your users.

### Stream server-sent events from the API

```python
from openai import OpenAI
client = OpenAI()

stream = client.responses.create(
    model="gpt-4.1",
    input=[
        {
            "role": "user",
            "content": "Say 'double bubble bath' ten times fast.",
        },
    ],
    stream=True,
)

for event in stream:
    print(event)
```

## Build agents

Use the OpenAI platform to build agents capable of taking action—like controlling computers—on behalf of your users.

### Build a language triage agent

```python
from agents import Agent, Runner
import asyncio

spanish_agent = Agent(
    name="Spanish agent",
    instructions="You only speak Spanish.",
)

english_agent = Agent(
    name="English agent",
    instructions="You only speak English",
)

triage_agent = Agent(
    name="Triage agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[spanish_agent, english_agent],
)

async def main():
    result = await Runner.run(triage_agent, input="Hola, ¿cómo estás?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

## Explore further

- **Go deeper with prompting and text generation** - Learn more about prompting, message roles, and building conversational apps like chat bots.
- **Analyze the content of images** - Learn to use image inputs to the model and extract meaning from images.
- **Generate structured JSON data from the model** - Generate JSON data from the model that conforms to a JSON schema you specify.
- **Call custom code to help generate a response** - Empower the model to invoke your own custom code to help generate a response.
- **Search the web or use your own data in responses** - Try out powerful built-in tools to extend the capabilities of the models.
- **Build agents** - Explore interfaces to build powerful AI agents that can take action on behalf of users.
- **Full API Reference** - View the full API reference for the OpenAI platform.
