# Logbook — browser-agent-demo

> Append-only chronological event log. Latest entry at bottom.
> Each entry: timestamp / session / 作業 / error / 進捗 / 申し送り.

---

## 2026-05-11 — Phase 0 install (session: portfolio-init)

**作業**:
- `~/projects/portfolio/` parent dir 作成
- GitHub repo `leagames0221-sys/browser-agent-demo` を PUBLIC + MIT で create + clone (gh CLI 経由)
- Tier 2 scaffold install: CLAUDE.md / spec.md / README.md / .gitignore / .github/workflows/drift-check.yml
- Memory Bank (Cline pattern) 5 file 配置
- .claude/{skills,agents,commands,hooks}/ dir 構造作成

**error**: なし

**進捗**: Phase 0 scaffold install 完了見込、 initial commit + push 待ち

**申し送り (次 session への引継)**:
- Phase 0 end gate = drift-check workflow が initial push で green になるか実測
- 次 session で Phase 1 着手: browser-use を `~/tmp/prior-art/` に隔離 clone → audit → 必要 file 抽出 → 自 repo に literal 配置 (commit msg に `derived from browser-use@<sha>`)
- Ollama install (Windows installer)、 `qwen2.5:7b` Q4_K_M pull (~5GB)
- baseline eval green になるまで literal iterate

---

## 2026-05-11 — Phase 0 closure verified (session: portfolio-init)

**作業**:
- initial commit (e4ac5bc → 9c46a64) push 完了、 10 file changes
- drift-check workflow run 25669533542 = **success** (15s で 全 check pass、 evidence: `gh run list --repo leagames0221-sys/browser-agent-demo`)
- PJ_REGISTRY.yaml に `browser_agent_demo` entry 登録済

**Phase 0 end gate**: ✅ 達成

**Phase 0 → Phase 1 引継**:
- Phase 1 entry point: browser-use を `~/tmp/prior-art/browser-use/` に隔離 clone → star/commit/Issues audit (D-PRIOR-ART-SECURITY-GATE)
- Ollama install (`winget install Ollama.Ollama` で Windows installer literal 取得)、 `ollama pull qwen2.5:7b`
- Chrome 別 profile `portfolio-sandbox` 作成 (chrome://settings/profiles)、 dummy 認証情報のみ投入
- 自 repo 内に `examples/baseline.py` (browser-use 公式 example の literal 抽出 + commit msg attribution) で baseline 走行
- pip 依存配線時 `pip-audit` + Dependabot for pip (.github/dependabot.yml) を Phase 1 内で apply

---

## 2026-05-11 — Portfolio unifying thesis 確定 (session: portfolio-init)

**作業**:
- user 提案 「全 free 制約下で best」 を portfolio unifying thesis として literal 採用
- README 上位 fold に `## Selected under` section literal 追加 (4 constraint: zero CC / consumer laptop / public source / drift-CI enforced)
- README に `## Why this is the literal best under the constraint set` section literal 追加 (5 row 選定 vs 却下 alternatives table)
- README 上部に 3 constraint badge (shields.io) 追加
- portfolio category: **constraint-optimized AI engineering** に literal 確定
- drift-check workflow 拡張: Selected under section + 4 constraint 文字列 + portfolio category line + Why best section + Rejected alternatives column の literal 存在 verify (8 step → 10 step)

**Thesis (literal 永続記録)**:
> Constraint-optimized AI engineering — best possible AI systems under (1) zero credit card, (2) consumer laptop, (3) public source / OSS only, (4) drift-CI enforced。 cross-repo (browser-agent-demo + longctx-bench-honest) で unifying narrative。 採用 / 受託 共通の signal axis: 「制約下で最善を出す engineer」。

**進捗**: thesis literal 確定 + drift-check 拡張完了見込、 commit + push + 再 verify 待ち

**申し送り (次 session)**:
- Phase 1 着手時、 全 ADR の Context section に `(constraint: zero CC / consumer laptop / public source / drift-CI)` を literal 明記、 thesis を ADR 単位でも literal 反映
- craftstack 上位 fold は Phase 3 で同 thesis を hub message として配置 (2 repo + thesis 1 行)

---

## 2026-05-11 — Phase 1 prep: supply chain defense + D: disk redirect (session: portfolio-init)

**作業**:
- D: drive 環境変数 set (HF_HOME=D:\hf_cache + HF_HUB_CACHE=D:\hf_cache\hub) + D:\hf_cache\hub + D:\venvs dir 作成
- C: drive 45.6GB free (9.6%) = Windows safe zone 危険水域、 D: 182.7GB free に literal 逃して回避
- pyproject.toml skeleton 配置: browser-use>=0.4 + ollama>=0.4 + playwright>=1.49 + anyio + dev (pytest + pip-audit + ruff)
- .github/dependabot.yml 配線 (pip ecosystem + github-actions ecosystem、 weekly schedule)
- drift-check workflow 拡張: pyproject.toml metadata + dependabot.yml pip ecosystem + pip-audit declared verify の 3 step 追加 (12 step → 15 step)
- README 「Disk layout (consumer laptop constraint)」 section 追加、 D: venv path + Lifecycle (Phase 2 後 D: 削除 OK) 明記

**Rationale (5 site WebSearch + WebFetch evidence)**:
- supply chain defense layer (pyproject + dependabot + pip-audit) は **install と同 commit / 同 PR で literal 配線必須**、 後付け = D-DRIFT-PREVENT-INFRA literally too late 違反
- D: redirect は consumer laptop constraint (D-CONSUMER-HW) の literal 実装、 C: 9.6% free を 維持しつつ 15GB model + 5GB venv を D: 受け止め

**進捗**: Phase 1 prep 配線完了見込、 commit + push + drift-check 再 verify 待ち

**申し送り (次 session = Phase 1 heavy install)**:
- Ollama install: `winget install Ollama.Ollama --silent` (admin UAC prompt 可能性 ★★)
- `ollama pull qwen2.5:7b` (~5GB、 OLLAMA_MODELS env で D: redirect 検討)
- Chrome 別 profile `portfolio-sandbox` 作成 (chrome://settings/profiles)
- browser-use の `examples/models/ollama.py` + `examples/features/video_recording.py` を 自 repo `examples/` に literal copy、 commit msg `derived from browser-use@<sha>`
- `uv sync` (UV_PROJECT_ENVIRONMENT=D:\venvs\browser-agent-demo set 後) で deps install + uv.lock commit
- baseline 走行 (browser-use simple example が Ollama + Chrome sandbox で動くか literal verify)

---

## 2026-05-11 — Phase 1 extract: browser-use 3 file 抽出 + NOTICE + SETUP runbook (session: portfolio-init)

**作業**:
- prior art audit verified: browser-use 93,377★ MIT (last push: today 2026-05-11)、 SHA `9b4b8d8054a2d23f13a141aa7c871dea1e939450`
- `examples/` dir に literal 抽出 (verbatim copies、 改造 0%):
  - `examples/models/ollama.py` — Ollama LLM integration
  - `examples/features/video_recording.py` — session recording (Phase 2 demo gif source)
  - `examples/simple.py` — minimal agent loop reference
- `NOTICE.md` 配置: derived sources attribution + audit log + license compatibility note
- `SETUP.md` 配置: Phase 1 install runbook (Ollama winget + Chrome sandbox profile + uv sync with D: venv + pip-audit + baseline run)
- env verified: WSL2 Ubuntu v2 already installed、 huggingface_hub 1.10.2 in system Python (hf command available)

**error**: なし (verbatim copy 成功、 NOTICE / SETUP markdown 書き込み 成功)

**進捗**: Phase 1 file extract + docs 配線完了見込、 commit + push 待ち。 Ollama install + Chrome profile + baseline 走行は user 介入 step (UAC + Chrome UI)。

**申し送り (次 session = Ollama install + baseline 走行)**:
- user 側で SETUP.md Step 1-3 実行 (winget install Ollama + ollama pull qwen2.5:7b + Chrome `portfolio-sandbox` profile 作成)
- 自動化可能 step: SETUP.md Step 4-7 (uv sync + pip-audit + playwright install + baseline run)
- baseline 完走後、 README Status を Phase 1 → Phase 2 候補に更新、 cost-tier table の Qwen 列 第 1 cell に baseline 数値 populate
