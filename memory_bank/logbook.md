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
