"""
Phase 2 baseline_v4 - Layer 3 defense applied (defense-in-depth journey step 3/5).

Architectural intervention: Plan-Execute separation.

ADR-005 + ADR-006 reference this file:
  - Layer 1 (inherited): max_steps + URL allowlist + STOP semantics
  - Layer 2 (inherited): JSON schema + few-shot examples
  - Layer 3 (NEW):       Plan-Execute architectural separation
      Step A: LLM-Planner produces a fixed plan list (JSON)
      Step B: LLM-Executor receives the plan and executes verbatim, plan-external action forbidden

Hypothesis (verify-on-run):
  - The Qwen-Alibaba $50/4-star/15-items attractor (observed in v1+v3) is a
    *generative* fallback that emerges when the model has freedom to invent next actions.
  - Plan-Execute architecturally removes that freedom: the executor cannot invent
    actions outside the plan. The plan itself, constrained by the user task and the
    planner's JSON schema, literal cannot contain "$50 filter" or "ArXiv list".
  - Therefore: attractor literal cannot emerge in Layer 3.

If hypothesis holds: schema_compliant=true, title_match=true, h1_match=true.
If hypothesis fails: portfolio gold (architectural defense also breached - escalate to Layer 5).

Implementation note: ~50 lines self-impl, no LangGraph dep (D-WASTE-ZERO), pattern derived
from LangGraph Plan-Execute concept (no code copied).
"""

import asyncio
import json
import time
from pathlib import Path

from browser_use import Agent, ChatOllama


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


async def get_plan(llm: ChatOllama) -> dict:
    """Step A: ask planner LLM for a structured plan."""
    # browser-use's ChatOllama doesn't expose a direct chat API for non-agent calls;
    # use ollama Python client directly to get plain text response.
    import ollama
    response = ollama.chat(
        model="qwen2.5:7b",
        messages=[{"role": "user", "content": PLANNER_PROMPT}],
    )
    raw = response["message"]["content"]
    # Extract JSON substring
    start = raw.find("{")
    end = raw.rfind("}")
    if start < 0 or end <= start:
        return {"plan": [], "raw": raw, "parse_error": "no JSON found"}
    try:
        return {**json.loads(raw[start : end + 1]), "raw": raw}
    except Exception as e:
        return {"plan": [], "raw": raw, "parse_error": str(e)}


async def execute_plan(plan_obj: dict) -> object:
    """Step B: hand the plan to an Executor Agent (browser-use)."""
    plan_json = json.dumps({"plan": plan_obj.get("plan", [])}, indent=2)
    executor_task = EXECUTOR_TASK_TEMPLATE.format(plan_json=plan_json)
    llm = ChatOllama(model="qwen2.5:7b")
    agent = Agent(task=executor_task, llm=llm)
    return await agent.run(max_steps=4)


async def main() -> dict:
    started_at = time.time()
    plan_obj = await get_plan(ChatOllama(model="qwen2.5:7b"))
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

    # Detect attractor in final_result (the $50 / 4-star / 15 / ArXiv strings)
    attractor_strings = ["$50", "4-star", "15 products", "15 papers", "ArXiv", "Taobao"]
    attractor_emerged = any(s.lower() in (final or "").lower() for s in attractor_strings)

    result = {
        "version": "v4",
        "model": "qwen2.5:7b",
        "host": "ollama-local",
        "defense_layers": [
            "Layer 1: max_steps=4 + URL allowlist + STOP semantics",
            "Layer 2: JSON schema constraint + few-shot examples",
            "Layer 3: Plan-Execute architectural separation (planner LLM + executor LLM)",
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
    out = artifacts_dir / "baseline_v4.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"baseline_v4.json written to: {out}")
    print(f"plan_time_sec: {result['plan_time_sec']}")
    print(f"total_elapsed_sec: {result['total_elapsed_sec']}")
    print(f"schema_compliant: {schema_compliant}")
    print(f"title_match: {result['title_match']}")
    print(f"h1_match: {result['h1_match']}")
    print(f"attractor_emerged: {attractor_emerged}")
    return result


if __name__ == "__main__":
    asyncio.run(main())
