# System Patterns — browser-agent-demo

## Drift prevention pattern

**Goal**: README claims ↔ code reality の literal 同期を CI で構造的に強制。

**Mechanism**:
1. README に `## Verified state` table 配置、 各 claim が drift-check で verify されるか明記
2. `.github/workflows/drift-check.yml` が push / PR 毎に走り、 claim mismatch で CI fail
3. claim 追加時は drift-check.yml にも対応 verify step を追加 (PR で同時 review)
4. `git pre-commit` hook (Phase 1 で install) が local commit 時点で同等 check

**Invariant**: claim を README に書く = drift-check 拡張を同 PR に含める。 違反 = CI fail = merge 不可。

---

## Memory Bank pattern (D-HANDOFF-DUTY literal 順守)

**Goal**: AI multi-session で 「前任 session が何をして、 次が何をすべきか」 が literal 引継ぎ可能。

**5 file 役割分担**:
- `logbook.md`: 時系列 append-only、 session 毎の作業 / error / 進捗 / 申し送り
- `activeContext.md`: current phase + 今 focus + 次の concrete step (上書き型)
- `decisionLog.md`: ADR、 重要決定の Context / Decision / Consequences / Verify
- `productContext.md`: what / why / target / success signals (頻繁更新しない)
- `systemPatterns.md`: how、 再利用可能な技術 pattern (本 file)

**Session 開始 protocol**: activeContext → logbook 末尾 § → decisionLog (必要 ADR のみ)
**Session 終了 protocol**: logbook append、 ADR 発生時 decisionLog 新規、 focus 変更時 activeContext 更新

---

## Prior art adoption pattern (D-PRIOR-ART-FIRST literal 順守)

**Step**:
1. 候補 OSS を `~/tmp/prior-art/<repo>/` に隔離 clone (採用前 audit zone)
2. star 数 / 直近 commit / Issues red flag scan (D-PRIOR-ART-SECURITY-GATE)
3. LICENSE 確認 (MIT / Apache-2.0 / BSD のみ採用可、 GPL / AGPL は portfolio で慎重判断)
4. `examples/` から自 task に近い 3-5 file 選定
5. 自 repo に copy、 commit msg に `derived from <repo>@<sha>` literal 記録
6. 改造範囲 20% 以内に literal 制限 (超える = ひな形不適合、 別 prior art 探す)
7. baseline eval (元 repo の test) が自 repo でも green になるか literal 検証

**Invariant**: ゼロ生成は M0 立証責任、 「ない」 ことを literal 示せない限り採用見送り。

---

## Sandbox pattern (D-NEW-PJ-SANDBOX-CHECK literal 順守)

**Goal**: AI が browser を触る ≒ 誤操作で prod 認証情報 / 重要 data を leak する risk を構造的に隔離。

**Mechanism**:
- Chrome 別 profile `portfolio-sandbox` を OS level で作成、 dummy 認証情報のみ投入
- `chrome_profile/` を `.gitignore` で除外、 commit 混入物理的に不可
- AI agent 実行時は 常に sandbox profile を明示指定、 default profile fallback 禁止
- 信頼 site list (許可ドメイン) を `config/allowlist.yml` (Phase 1 で実装) で literal 制限

**Limit**: OS-level isolation 100% ではない (process 共有あり)、 完全 isolation 要件時のみ Docker 化検討。 個人 demo scope では Chrome 別 profile で 90% 防御達成 ★★ tier。

---

## Phase gate pattern

各 Phase end は 「測れる完成品」 で gate される、 次 Phase 着手前に literal verify:
- Phase 0: drift-check workflow green on first push
- Phase 1: `pytest` 全 green + baseline task 成功
- Phase 2: success rate ≥ 95% + 30s gif 生成 + README 数値 populate
- Phase 3: craftstack 上位 fold link active + social 3 channel 配信
