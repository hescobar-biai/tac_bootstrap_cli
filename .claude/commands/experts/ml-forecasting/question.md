---
allowed-tools: Bash, Read, Grep, Glob, TodoWrite
description: Answer questions about demand forecasting, ML pipelines, and model evaluation without coding
argument-hint: [question]
model: sonnet
---

# NOTE: Model "sonnet" uses 3-tier resolution:
#   1. ANTHROPIC_DEFAULT_SONNET_MODEL (env var) - highest priority
#   2. config.yml agentic.model_policy.sonnet_model - project config
#   3. Hardcoded default "claude-sonnet-4-5-20250929" - fallback
# See .claude/MODEL_RESOLUTION.md for details


# ML Forecasting Expert - Question Mode

Answer the user's question by analyzing the ML forecasting implementation including model pipelines, feature engineering, evaluation metrics, and deployment patterns. This prompt provides information without making code changes.

## Variables

USER_QUESTION: $1
EXPERTISE_PATH: .claude/commands/experts/ml-forecasting/expertise.yaml

## Instructions

- IMPORTANT: This is a question-answering task only - DO NOT write, edit, or create any files
- Focus on demand forecasting methods, feature engineering, model evaluation, and pipeline design
- If the question requires implementation, explain the approach conceptually without implementing
- With your expert knowledge, validate the information from `EXPERTISE_PATH` against the codebase before answering your question.

## Workflow

- Read the `EXPERTISE_PATH` file to understand ML forecasting architecture and patterns
- Review, validate, and confirm information from `EXPERTISE_PATH` against the codebase
- Respond based on the `Report` section below.

## Report

- Direct answer to the `USER_QUESTION`
- Supporting evidence from `EXPERTISE_PATH` and the codebase
- References to the exact files and lines of code that support the answer
- High-mid level conceptual explanations of the ML architecture and patterns
- Include code snippets, model comparisons, or architecture diagrams (mermaid) where appropriate
