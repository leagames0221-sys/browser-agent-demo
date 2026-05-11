# browser-agent-demo — spec

## 機能 list

- F-001: browser-use + Ollama Qwen2.5 で local LLM 駆動の browser agent を実行
- F-002: baseline task (browser-use 同梱 eval) が green に到達
- F-003: 自 domain task 1 件実装 (例: 競合 site 巡回 → CSV 出力)、 成功率 95%+
- F-004: 30 秒 demo gif を自動生成 (browser-use 同梱 `gif-of-agent.py` 流用)
- F-005: drift CI が README claims を 100% verify

## 非機能要件

- API 課金: 0 円 (local LLM のみ、 GitHub Models / Anthropic API 一切不使用)
- consumer laptop (Windows 11 / 16GB+ RAM) で完走
- Chrome 別 profile (`portfolio-sandbox`) に隔離、 prod 認証情報 混入禁止
- task 成功率 ≥ 95% (10 試行中 9 件以上 green)
- 平均所要時間 ≤ 60 秒 / task

## 依存

- 外部 OSS: `github.com/browser-use/browser-use` (MIT)、 `github.com/ollama/ollama` (MIT)
- LLM: `qwen2.5:7b` Q4_K_M (~5GB DL、 consumer GPU で推論可)
- Browser: Chromium via Playwright (browser-use 経由)
- CI: GitHub Actions (free tier)

## 完了条件 (acceptance criteria)

- AC-1: `python examples/run_self_task.py` で 自 domain task が成功率 95%+ に到達
- AC-2: `python examples/gif_demo.py` で 30 秒 gif が出力 dir に literal 生成
- AC-3: `pytest` で全 test green
- AC-4: `pip-audit` で high severity issue 0 件
- AC-5: GitHub Actions の drift-check workflow が green
- AC-6: README `## Verified state` section の各項目が drift-check と一致
- AC-7: Dependabot enabled、 weekly schedule 配信確認

## Phase 進行

- Phase 0 (current): scaffold + drift CI + memory_bank + ARA/Security/.gitignore 配線
- Phase 1: browser-use clone → audit → 自 repo に literal 抽出、 Ollama install、 baseline eval green
- Phase 2: 自 domain task 実装 + gif 生成 + 数値計測 + README populate
- Phase 3: craftstack 統合 (上位 fold + GitHub Profile + social distribution)
