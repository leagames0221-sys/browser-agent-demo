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

---

## 2026-05-11 — Phase 1 install layer: Ollama + uv sync + pip-audit + Playwright (session: portfolio-init)

**作業 (literal 実測値で 全項 GREEN)**:
- `winget install Ollama.Ollama --silent --accept-package-agreements --accept-source-agreements` → exit 0、 install path: `C:\Users\admin\AppData\Local\Programs\Ollama\ollama.exe` (per-user install)、 version: 0.23.1
- `OLLAMA_MODELS=D:\ollama_models` User-level 永続 env set + D:\ollama_models dir 作成 (D: drive redirect)
- `ollama pull qwen2.5:7b` → 4.7GB main layer 100% + 全 layer pull 完了 (sha256 verify 中だが DL は完成)
- `uv sync --extra dev` (UV_PROJECT_ENVIRONMENT=D:\venvs\browser-agent-demo) → exit 0、 全 deps install (browser-use + ollama + playwright + pytest + pip-audit + ruff 等)
- `uv run pip-audit --strict` → exit 0、 **"No known vulnerabilities found"** ★★★ (supply chain defense literal verified)
- `uv run playwright install chromium` → exit 0 (Chrome 自動操作 binary 配置)
- `uv.lock` 5029 行 生成 (D-NPM-3GUARD pip equivalent literal lockfile pin)

**error**: なし

**進捗**: Phase 1 自動化 step 全件 GREEN。 残 user 介入 step = Chrome `portfolio-sandbox` profile 作成 (chrome://settings/profiles)、 baseline run。

**申し送り (次 session)**:
- uv.lock commit + push、 drift-check 緑保持
- user 側 Chrome sandbox profile 作成完了後、 `uv run python examples/simple.py` で baseline 走行 (browser-use simple example が Ollama + Chrome で動くか literal verify)
- baseline 成功時、 自 domain task 設計 (Phase 2 着手 = 例: 競合 site 巡回 → CSV 出力、 30s gif 生成)
- baseline 失敗時、 logbook に literal error + 推定原因 + 修正路線 記録、 honest results section の素材化

---

## 2026-05-11 — Phase 1 baseline run #1: literal completed with honest failure mode captured (session: portfolio-init)

**作業**:
- `examples/baseline.py` 起草 (ChatOllama + qwen2.5:7b + 公開 site task)、 D-PRIOR-ART-FIRST < 20% 改造 (model 名 + task 内容のみ変更、 commit msg で browser-use@9b4b8d8 attribution)
- Chrome `portfolio-sandbox` profile 作成済 (user UI、 ログアウト状態保持)
- Ollama server alive on 127.0.0.1:11434、 qwen2.5:7b 4.68GB literal listed
- `uv run python examples/baseline.py` exit 0、 baseline.json literal written

**実測値 (artifacts/baseline.json)**:
```json
{
  "model": "qwen2.5:7b",
  "host": "ollama-local",
  "task": "visit example.com and report title + H1",
  "max_steps": 8,
  "elapsed_sec": 180.08,
  "final_result": "Max steps reached. ...",
  "is_done": true
}
```

**Judge Verdict (browser-use 内蔵 LLM judge による)**: ❌ **FAIL**

**Honest failure mode 解析 (portfolio thesis evidence)**:

1. **task 部分は literal 成功**: Judge も認定 — agent は example.com に navigate、 title + H1 を 正しく抽出済
2. **task 完了後の暴走**: agent が agent self の判断で eBay に navigate、 「items under $50 with 4+ stars」 という task に literal 存在しない検索を試行、 max_steps 8 を浪費
3. **self-report の虚偽**: final_result で 「could not navigate due to network issues」 と報告、 ただし agent log では最初に navigate 成功してた = agent の memory が破綻 (eBay の network error と最初の example.com navigation を 混同)
4. **所要時間 180 sec**: frontier API (GPT-5 等) なら 想定 5-15 sec、 local 7B は **~15-30x 遅い** + task discipline 弱い

→ portfolio README の `## Honest results` section に literal そのまま記載できる 1 級素材 ★★★:
- `Where the local 7B model holds up`: simple page extraction (example.com title + H1) literal pass
- `Where it loses badly`: task discipline (8 steps 中 5+ steps を 範囲外 task で浪費)
- `Where reasonable engineering fixes the gap`: prompt 引き締め (「STOP after first task」 等)、 max_steps 3 で abort、 ReAct system prompt 強化
- `Where it doesn't (and frontier is the right answer)`: complex multi-step tasks with reasoning

**error**: なし (exit 0、 Judge FAIL は機能 = honest evidence 取得済)

**進捗**: Phase 1 baseline literal 完了、 Phase 2 入口 = README `## Honest results` populate + baseline JSON evidence commit。 Phase 1 で全 component 動作 verified、 Phase 2 で 「task discipline 改善版 baseline_v2」 + 「自 domain task (競合 site 巡回 CSV 出力)」 + 「30s demo gif」 設計。

**申し送り (Phase 2)**:
- baseline_v2 設計: max_steps=3 + tighter system prompt + 「STOP after reporting」 enforcement
- 自 domain task 設計: portfolio context で説得力ある public-site task (例: GitHub trending 3 件の star 数取得、 Wikipedia 記事冒頭抽出 等)
- 30s gif 生成: `examples/features/video_recording.py` の Browser(record_video_dir) pattern 流用
- 数値 cell 1 件目: 「example.com title 抽出 task: success=Yes (task portion)、 Judge=FAIL (scope creep)、 180 sec、 cost=¥0」 を cost-tier table に literal populate
