# BITS Agentic AI Exercises

Completed exercises for Weeks 1 and 2 of the BITS Pilani Dubai Agentic AI
Engineering course.

## Topics

- **Week 1:** assistant versus agent, LLM limitations, agent anatomy, agent
  loops, reflection, safe multi-tool execution, and native function calling.
- **Week 2:** tool schemas, structured tool calls, reusable tool agents, robust
  external API tools, multi-API agents, and webhook-driven automation.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and configure one provider. Week 2 native tool calling supports
OpenAI, Groq, or Ollama through the OpenAI-compatible API shape.

Run an exercise from the repository root, for example:

```bash
python "Week 1/skeleton/04_agent_loop.py"
python "Week 2/skeleton/03_tool_calling_agent.py"
```

The Open-Meteo exercises require internet access but no API key. The webhook
exercise uses a local mock unless `WEBHOOK_URL` is configured.
