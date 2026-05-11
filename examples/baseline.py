"""
Phase 1 baseline — zero-CC / consumer-laptop literal verify.

Selected under: zero credit card + consumer laptop + public-site only + drift-CI enforced.
LLM = local Ollama qwen2.5:7b (no paid API).
Browser = Playwright-managed Chromium (isolated from system Chrome profiles).
Task = visit example.com and report page title (public deterministic site).

Attribution: integration pattern derived from browser-use@9b4b8d8054a2 examples/models/ollama.py (MIT).
This file is our own customization (≤20% modification per D-PRIOR-ART-FIRST):
  - model name changed to qwen2.5:7b (the model we literally pulled)
  - task changed to a deterministic public-site target for reproducibility
"""

import asyncio
import json
import time
from pathlib import Path

from browser_use import Agent, ChatOllama


async def main() -> dict:
    started_at = time.time()
    llm = ChatOllama(model="qwen2.5:7b")
    agent = Agent(
        task="Visit https://example.com and report the page title (exact text) and the first H1 heading text.",
        llm=llm,
    )
    history = await agent.run(max_steps=8)
    elapsed = time.time() - started_at

    # Extract a reproducible summary
    result = {
        "model": "qwen2.5:7b",
        "host": "ollama-local",
        "task": "visit example.com and report title + H1",
        "max_steps": 8,
        "elapsed_sec": round(elapsed, 2),
        "final_result": str(history.final_result()) if hasattr(history, "final_result") else None,
        "is_done": bool(history.is_done()) if hasattr(history, "is_done") else None,
    }

    # Persist JSON evidence (drift-CI will verify in Phase 2)
    artifacts_dir = Path(__file__).parent.parent / "artifacts"
    artifacts_dir.mkdir(exist_ok=True)
    out = artifacts_dir / "baseline.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n=== baseline.json written to {out} ===")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


if __name__ == "__main__":
    asyncio.run(main())
