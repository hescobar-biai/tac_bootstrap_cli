---
allowed-tools: Bash, Read, Grep, Glob, TodoWrite
description: Answer questions about React frontend architecture, components, and UI patterns without coding
argument-hint: [question]
---

# React Frontend Expert - Question Mode

Answer the user's question by analyzing the React frontend implementation including component architecture, hooks, state management, data fetching, and UI patterns. This prompt provides information without making code changes.

## Variables

USER_QUESTION: $1
EXPERTISE_PATH: .claude/commands/experts/react-frontend/expertise.yaml

## Instructions

- IMPORTANT: This is a question-answering task only - DO NOT write, edit, or create any files
- Focus on React 19 patterns, TanStack Query, MUI X Data Grid Premium, TailwindCSS 4.1, and supply chain UI
- If the question requires implementation, explain the approach conceptually without implementing
- With your expert knowledge, validate the information from `EXPERTISE_PATH` against the codebase before answering your question.

## Workflow

- Read the `EXPERTISE_PATH` file to understand React frontend architecture and patterns
- Review, validate, and confirm information from `EXPERTISE_PATH` against the codebase
- Respond based on the `Report` section below.

## Report

- Direct answer to the `USER_QUESTION`
- Supporting evidence from `EXPERTISE_PATH` and the codebase
- References to the exact files and lines of code that support the answer
- High-mid level conceptual explanations of the frontend architecture and patterns
- Include code snippets, component trees, or architecture diagrams (mermaid) where appropriate
