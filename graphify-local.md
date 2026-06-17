# Graphify Local Pilot

Graphify is approved for local pilot use only. Use it to understand code, docs, schemas, and project relationships, but keep generated output out of git until a human reviews it for sensitive data.

## Current policy

1. `graphify-out/` is local-only and ignored by git.
2. Do not commit or publish `graphify-out/` by default.
3. Review `graphify-out/GRAPH_REPORT.md`, `graphify-out/graph.json`, and `graphify-out/graph.html` before sharing externally.
4. Mixed or docs-only repositories require an LLM backend/API key for semantic extraction. Code-only repositories can be graphed without an LLM key.
5. Rollout to every project should wait until pilot quality, security review, and backend choice are settled.

## Local command

```bash
export PATH="$HOME/.local/bin:$PATH"
graphify .
```

Expected output:

```text
graphify-out/
├── graph.html
├── GRAPH_REPORT.md
└── graph.json
```

## Backend note

The current Hermes subscription/OAuth model access is not automatically exposed to the standalone Graphify CLI as provider API keys. For docs-heavy repositories, choose one backend before rollout:

- direct provider key: Gemini, OpenAI, Anthropic, DeepSeek, Moonshot/Kimi
- local/OpenAI-compatible backend: Ollama, vLLM, LM Studio, llama.cpp server

## Pilot result so far

`my-sprees` code-only pilot succeeded with Graphify 0.8.40:

- 131 nodes
- 150 links
- 9 communities
- 0 LLM token cost
- no obvious sensitive pattern hits in generated output scan

`my-sprees-docs` is docs-only, so full extraction is blocked until an LLM backend/API key is configured.
