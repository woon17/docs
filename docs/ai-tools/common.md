# Common AI Knowledge

This page collects short reference notes about common AI concepts used in this site.

## Prompt

Prompt engineering notes and patterns:

- Prompt = input + instructions + context.
- Keep context concise and structured.
- Use system and assistant roles when supported.

Examples and templates:

- Template 1: "You are an expert X. Given the following input: {{input}}. Respond with..."
- Template 2: Short few-shot examples.


## Agent

A short definition:

- Agent: an autonomous system that perceives its environment, makes decisions, and acts to achieve goals. In AI, agents may be simple rule-based programs, reinforcement learning agents, or orchestration layers that call models and tools.

## MCP

- MCP: Model Context Protocol (or "Model Control Plane" depending on context). Use this section to list what MCP means for you — orchestration, connectors, observability, and dataflow.

Example:

- Purpose: coordinate multiple models, maintain context, routing and plugin/tool control.


Combined overview of prompts, MCP and agents.

<figure>
      <img src="/ai-tools/image/prompt_mcp_agent.jpeg" alt="Prompt / MCP / Agent diagram">
      <figcaption><b>Figure 1:</b> Server architecture overview</figcaption>
</figure>
---
