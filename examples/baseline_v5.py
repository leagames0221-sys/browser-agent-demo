"""
Phase 2 baseline_v5 - Layer 5 defense applied (defense-in-depth journey step 5/5, final).

Frontier-model fallback via GitHub Models free tier.

ADR-005 + ADR-006 reference this file:
  - Layer 1+2+3 (inherited): max_steps + URL allowlist + STOP + JSON schema + Plan-Execute
  - Layer 5 (NEW):           Frontier LLM via GitHub Models marketplace (zero credit card)
      - Endpoint: https://models.github.ai/inference (OpenAI-compatible)
      - Auth: GITHUB_TOKEN (gh auth token, free tier)
      - Model: openai/gpt-4.1-mini (frontier-tier, recent, cost-effective at free tier)

Hypothesis (verify-on-run):
  - The Qwen-Alibaba $50/4-star/Walmart attractor (observed in v1+v3+v4) does NOT exist
    in OpenAI training data (different corpus composition, different RLHF).
  - Frontier model has better instruction-following + can respect Plan-Execute pattern.
  - Therefore: schema_compliant=True, title_match=True, h1_match=True is the literal target.

Constraint compliance:
  - zero credit card: GitHub Models free tier, no CC required (only GitHub PAT)
  - consumer laptop: API call only, no local compute
  - public source only: example.com (same as v1-v4)
  - drift-CI enforced: extends to baseline_v5.json

Attribution: Plan-Execute pattern shared with v4. ChatOpenAI integration follows
browser-use@9b4b8d8 examples (MIT). GitHub Models endpoint per
https://docs.github.com/en/github-models (free tier).
"""

import asyncio
import json
import os
import subprocess
import time
from pathlib import Path

from browser_use import Agent, ChatOpenAI


def get_github_token() -> str:
    """Pull the GitHub token from gh CLI auth (already authenticated)."""
    return subprocess.check_output(["gh", "auth", "token"], text=True).strip()


PLANNER_PROMPT = """\
You are a PLANNER. Read the user task below and output a JSON plan as a list of strings.
Each string is one concrete action. Do NOT execute; only plan.

User task: Visit https://example.com once and extract two fields - the page title
(exact text of <title>) and the first <h1> heading text. Return as JSON
{"title": "...", "h1": "..."} and stop.

Output ONLY valid JSON in this exact shape:
{"plan": ["action 1 string", "action 2 string", ..., "call done with the JSON result"]}

Constraints:
- Maximum 4 actions in the plan
- Allowed URLs: https://example.com only
- Final action must be: call done with the extracted {"title": ..., "h1": ...}
"""

EXECUTOR_TASK_TEMPLATE = """\
You are an EXECUTOR. Follow this exact plan from the PLANNER. Execute each action verbatim.
Do NOT add actions not in the plan. Do NOT navigate to URLs not in the plan.
After the last plan action, immediately call done() and STOP.

PLAN (JSON):
{plan_json}

Allowed URLs: https://example.com only. Plan-external actions = task failure.
Output the final extracted data as JSON: {{"title": "<title>", "h1": "<h1>"}}.
"""

FRONTIER_MODEL = "openai/gpt-4.1-mini"
GITHUB_MODELS_ENDPOINT = "https://models.github.ai/inference"


def make_llm() -> ChatOpenAI:
    """Construct a ChatOpenAI pointed at GitHub Models (free tier, zero CC)."""
    token = get_github_token()
    return ChatOpenAI(
        model=FRONTIER_MODEL,
        api_key=token,
        base_url=GITHUB_MODELS_ENDPOINT,
    )


async def get_plan() -> dict:
    """Planner step using frontier model via direct OpenAI client (no Agent loop)."""
    from openai import OpenAI

    token = get_github_token()
    client = OpenAI(api_key=token, base_url=GITHUB_MODELS_ENDPOINT)
    response = client.chat.completions.create(
        model=FRONTIER_MODEL,
        messages=[{"role": "user", "content": PLANNER_PROMPT}],
    )
    raw = response.choices[0].message.content
    start = raw.find("{")
    end = raw.rfind("}")
    if start < 0 or end <= start:
        return {"plan": [], "raw": raw, "parse_error": "no JSON found"}
    try:
        return {**json.loads(raw[start : end + 1]), "raw": raw}
    except Exception as e:
        return {"plan": [], "raw": raw, "parse_error": str(e)}


async def execute_plan(plan_obj: dict):
    """Executor: browser-use Agent with frontier LLM."""
    plan_json = json.dumps({"plan": plan_obj.get("plan", [])}, indent=2)
    executor_task = EXECUTOR_TASK_TEMPLATE.format(plan_json=plan_json)
    llm = make_llm()
    agent = Agent(task=executor_task, llm=llm)
    return await agent.run(max_steps=4)


async def main() -> dict:
    started_at = time.time()
    plan_obj = await get_plan()
    plan_time = time.time() - started_at

    history = await execute_plan(plan_obj)
    total_time = time.time() - started_at

    final = str(history.final_result()) if hasattr(history, "final_result") else None

    schema_compliant = False
    parsed_title = None
    parsed_h1 = None
    if final:
        try:
            start = final.find("{")
            end = final.rfind("}")
            if start >= 0 and end > start:
                obj = json.loads(final[start : end + 1])
                if isinstance(obj, dict) and "title" in obj and "h1" in obj:
                    schema_compliant = True
                    parsed_title = obj.get("title")
                    parsed_h1 = obj.get("h1")
        except Exception:
            schema_compliant = False

    attractor_strings = ["$50", "4-star", "15 products", "15 papers", "ArXiv", "Walmart", "eBay", "Taobao"]
    attractor_emerged = any(s.lower() in (final or "").lower() for s in attractor_strings)

    result = {
        "version": "v5",
        "model": FRONTIER_MODEL,
        "host": "github-models-free-tier",
        "endpoint": GITHUB_MODELS_ENDPOINT,
        "credit_card_required": False,
        "defense_layers": [
            "Layer 1: max_steps + URL allowlist + STOP semantics",
            "Layer 2: JSON schema constraint + few-shot examples",
            "Layer 3: Plan-Execute architectural separation",
            "Layer 5: Frontier model (openai/gpt-4.1-mini) via GitHub Models free tier",
        ],
        "task_summary": "visit example.com, return {title, h1} as JSON, then STOP",
        "plan_obj": plan_obj,
        "plan_time_sec": round(plan_time, 2),
        "total_elapsed_sec": round(total_time, 2),
        "final_result": final,
        "is_done": bool(history.is_done()) if hasattr(history, "is_done") else None,
        "schema_compliant": schema_compliant,
        "parsed_title": parsed_title,
        "parsed_h1": parsed_h1,
        "expected_title": "Example Domain",
        "expected_h1": "Example Domain",
        "title_match": parsed_title == "Example Domain" if parsed_title else False,
        "h1_match": parsed_h1 == "Example Domain" if parsed_h1 else False,
        "attractor_emerged": attractor_emerged,
        "attractor_strings_checked": attractor_strings,
    }

    artifacts_dir = Path(__file__).parent.parent / "artifacts"
    artifacts_dir.mkdir(exist_ok=True)
    out = artifacts_dir / "baseline_v5.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"baseline_v5.json written to: {out}")
    print(f"model: {FRONTIER_MODEL}")
    print(f"plan_time_sec: {result['plan_time_sec']}")
    print(f"total_elapsed_sec: {result['total_elapsed_sec']}")
    print(f"schema_compliant: {schema_compliant}")
    print(f"title_match: {result['title_match']}")
    print(f"h1_match: {result['h1_match']}")
    print(f"attractor_emerged: {attractor_emerged}")
    return result


if __name__ == "__main__":
    asyncio.run(main())
