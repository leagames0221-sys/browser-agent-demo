# Active Context — browser-agent-demo

## Current phase

**Phase 1** — Prior art clone + audit + Ollama install + baseline eval (next session に着手予定)

## Current focus

Phase 0 完了 (drift-check workflow success run 25669533542)、 次 session の Phase 1 着手準備。

## Next concrete steps (Phase 1)

1. `~/tmp/prior-art/browser-use/` に隔離 clone (`git clone https://github.com/browser-use/browser-use.git`)
2. audit: star 数 / 直近 commit / open Issues 確認、 LICENSE = MIT verify、 red flag ZERO 確認後採用
3. Ollama install: `winget install Ollama.Ollama` (Windows installer)、 `ollama pull qwen2.5:7b` (~5GB DL)
4. Chrome 別 profile `portfolio-sandbox` 作成 (chrome://settings/profiles)、 dummy 認証情報のみ投入
5. 必要 file 抽出: `examples/models/ollama.py` + `examples/gif-of-agent.py` + `examples/use-cases/<1 件>` を自 repo に literal copy、 commit msg `derived from browser-use@<sha>`
6. pip 配線: `pyproject.toml` 起草、 `uv sync`、 `uv.lock` commit、 `pip-audit` CI step 追加、 `.github/dependabot.yml` for pip 配線
7. baseline 走行: 抽出した example が Ollama + Chrome sandbox profile で literal 動くか実測
8. README の Status を Phase 1 に更新、 drift-check workflow の Phase 0 expectation を Phase 1 用に拡張

## Blockers

なし (Phase 1 着手 OK)。

## Out of scope (current phase)

- 自 domain task 実装 (Phase 2)
- 30s gif 生成 (Phase 2)
- 数値 (成功率 / 所要時間) の README populate (Phase 2)
- craftstack 統合 (Phase 3)
