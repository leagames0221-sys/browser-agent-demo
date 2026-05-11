# Active Context — browser-agent-demo

## Current phase

**Phase 2 (in progress)** — Defense-in-depth journey 3/5 complete (v1, v2, v3 literal ran with JSON evidence). v4 (Plan-Execute) + v5 (frontier fallback) await next session.

## Current focus

Phase 2 v1+v2+v3 literal 実走完了 + JSON evidence + Honest results section populated。 portfolio narrative: 「prompt engineering 限界の literal 実測 evidence → architectural intervention 必要性 (v4 で verify) → frontier fallback (v5)」 の 3 段 journey の 1 段目完了。

**Phase 2 実測値 summary** (artifacts/baseline{,_v2,_v3}.json に literal evidence):
- v1 (no defense): 180s, FAIL, eBay rogue navigation
- v2 (Layer 1: step cap + STOP semantics): 86s, FAIL, ArXiv 15 papers fabrication
- v3 (Layer 1+2: JSON schema + few-shot): 94s, FAIL, $50/4-star/15-items attractor 再発 (v1 と同型 pattern)

**Key honest finding (portfolio gold)**: Qwen 2.5-7B has a training-data attractor that prompt engineering (Layer 1+2) cannot suppress. Architectural intervention (Layer 3 Plan-Execute) is the literal next path.

## Next concrete steps (Phase 2 continuation)

### baseline_v4 (Layer 3: Plan-Execute architectural separation)

仮説: training-data attractor は plan に literal 入らない (plan に "extract title + h1, return JSON" だけ書ける) → executor が plan 外行動 architecturally 不可能化 → $50/4-star fabrication が emerge できない。

設計:
1. LLM #1 (planner): task を読み、 plan list を JSON 出力 (`["navigate example.com", "extract title", "extract h1", "return JSON", "done"]`)
2. LLM #2 (executor): plan の各 step を 1 step ずつ execute、 plan 外 action 禁止 (browser-use Agent を step 制限で起動 + plan を tool call hint として注入)
3. 評価: schema_compliant + title_match + h1_match を計測、 v3 と直接比較

実装は 自前 50 行 程度の wrapper、 LangGraph 等 OSS 不要 (D-WASTE-ZERO 順守)、 commit msg に prior art note (`pattern derived from LangGraph Plan-Execute concept`).

### baseline_v5 (Layer 5: GitHub Models frontier fallback)

- GitHub Models 経由で GPT-5 / Claude Sonnet 4.6 を同 task に投入 (CC 不要、 free tier)
- v4 の Plan-Execute pattern に frontier model を literal 適用
- cost-tier table 完成: Qwen local v1-v4 + frontier v5 の 5 cell + 所要時間 + cost を JSON evidence 由来自動生成

### Phase 3 (Phase 2 完了後)

- craftstack integration: 上位 fold に 2 repo link + thesis 1 行 + 数値 summary
- r/LocalLLaMA + Hacker News 投稿 (defense-in-depth journey は community 反応強い領域)

## Blockers

なし (Phase 1 着手 OK)。

## Out of scope (current phase)

- 自 domain task 実装 (Phase 2)
- 30s gif 生成 (Phase 2)
- 数値 (成功率 / 所要時間) の README populate (Phase 2)
- craftstack 統合 (Phase 3)
