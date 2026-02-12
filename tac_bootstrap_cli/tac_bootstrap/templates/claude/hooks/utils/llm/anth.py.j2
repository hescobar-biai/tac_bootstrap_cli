#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "anthropic",
#     "python-dotenv",
# ]
# ///

import os
import sys
from dotenv import load_dotenv
from pathlib import Path
import yaml


def get_haiku_model():
    """
    Get Haiku model ID with 3-tier resolution.

    Resolution order:
    1. Environment variable (ANTHROPIC_DEFAULT_HAIKU_MODEL) - highest priority
    2. config.yml: agentic.model_policy.haiku_model
    3. Hardcoded default - fallback
    """
    # Tier 1: Environment variable
    env_model = os.getenv('ANTHROPIC_DEFAULT_HAIKU_MODEL')
    if env_model:
        return env_model

    # Tier 2: Load from config.yml if available
    try:
        # Try to find config.yml in common locations
        config_paths = [
            Path.cwd() / "config.yml",
            Path.home() / ".config" / "tac" / "config.yml",
            Path(__file__).parent.parent.parent.parent.parent / "config.yml",
        ]

        for config_path in config_paths:
            if config_path.exists():
                with open(config_path) as f:
                    config_data = yaml.safe_load(f)
                    if config_data:
                        model = config_data.get("agentic", {}).get("model_policy", {}).get("haiku_model")
                        if model:
                            return model
    except Exception:
        pass  # Fall through to hardcoded default

    # Tier 3: Hardcoded default
    return "claude-3-5-haiku-20241022"


def prompt_llm(prompt_text):
    """
    Base Anthropic LLM prompting method using fastest model.

    Args:
        prompt_text (str): The prompt to send to the model

    Returns:
        str: The model's response text, or None if error
    """
    load_dotenv()

    api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_AUTH_TOKEN")
    if not api_key:
        return None

    try:
        import anthropic

        # Resolve base_url: env var -> config.yml
        base_url = os.getenv("ANTHROPIC_BASE_URL")
        if not base_url:
            try:
                config_paths = [
                    Path.cwd() / "config.yml",
                    Path(__file__).parent.parent.parent.parent.parent / "config.yml",
                ]
                for cp in config_paths:
                    if cp.exists():
                        with open(cp) as f:
                            cfg = yaml.safe_load(f) or {}
                        base_url = cfg.get("agentic", {}).get("model_policy", {}).get("base_url")
                        if base_url:
                            break
            except Exception:
                pass
        client = anthropic.Anthropic(api_key=api_key, base_url=base_url) if base_url else anthropic.Anthropic(api_key=api_key)

        message = client.messages.create(
            model=get_haiku_model(),  # Fastest Anthropic model (dynamically resolved)
            max_tokens=100,
            temperature=0.7,
            messages=[{"role": "user", "content": prompt_text}],
        )

        return message.content[0].text.strip()

    except Exception:
        return None


def generate_completion_message():
    """
    Generate a completion message using Anthropic LLM.

    Returns:
        str: A natural language completion message, or None if error
    """
    engineer_name = os.getenv("ENGINEER_NAME", "").strip()

    if engineer_name:
        name_instruction = f"Sometimes (about 30% of the time) include the engineer's name '{engineer_name}' in a natural way."
        examples = f"""Examples of the style: 
- Standard: "Work complete!", "All done!", "Task finished!", "Ready for your next move!"
- Personalized: "{engineer_name}, all set!", "Ready for you, {engineer_name}!", "Complete, {engineer_name}!", "{engineer_name}, we're done!" """
    else:
        name_instruction = ""
        examples = """Examples of the style: "Work complete!", "All done!", "Task finished!", "Ready for your next move!" """

    prompt = f"""Generate a short, friendly completion message for when an AI coding assistant finishes a task. 

Requirements:
- Keep it under 10 words
- Make it positive and future focused
- Use natural, conversational language
- Focus on completion/readiness
- Do NOT include quotes, formatting, or explanations
- Return ONLY the completion message text
{name_instruction}

{examples}

Generate ONE completion message:"""

    response = prompt_llm(prompt)

    # Clean up response - remove quotes and extra formatting
    if response:
        response = response.strip().strip('"').strip("'").strip()
        # Take first line if multiple lines
        response = response.split("\n")[0].strip()

    return response


def main():
    """Command line interface for testing."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--completion":
            message = generate_completion_message()
            if message:
                print(message)
            else:
                print("Error generating completion message")
        else:
            prompt_text = " ".join(sys.argv[1:])
            response = prompt_llm(prompt_text)
            if response:
                print(response)
            else:
                print("Error calling Anthropic API")
    else:
        print("Usage: ./anth.py 'your prompt here' or ./anth.py --completion")


if __name__ == "__main__":
    main()