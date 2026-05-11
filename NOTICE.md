# NOTICE — Derived Sources

Files in `examples/` are derived from upstream open-source projects under their respective licenses.
D-PRIOR-ART-FIRST: ゼロから生成せず、 成熟したひな形から literal 抽出 + attribution。

---

## browser-use (MIT)

- **Source**: https://github.com/browser-use/browser-use
- **Commit SHA**: `9b4b8d8054a2d23f13a141aa7c871dea1e939450`
- **License**: MIT — https://github.com/browser-use/browser-use/blob/main/LICENSE
- **Audit (D-PRIOR-ART-SECURITY-GATE)**: 2026-05-11
  - stars: 93,377
  - last push: 2026-05-11 (daily-active)
  - open issues: 228 (規模相応)
  - red flag: ZERO
- **Files derived (verbatim copies, see commit msg for derivation attribution)**:
  - `examples/models/ollama.py` — Ollama LLM integration pattern
  - `examples/features/video_recording.py` — Browser session recording (Phase 2 demo gif source)
  - `examples/simple.py` — Minimal agent loop reference
- **Modification scope**: Phase 1 = verbatim copies only. Phase 2 customization ≤ 20% (D-PRIOR-ART-FIRST 順守、 超過時は別 prior art 探索)

---

## ollama (MIT) — used as library dependency

- **Source**: https://github.com/ollama/ollama (server) + https://github.com/ollama/ollama-python (client)
- **Usage**: declared in `pyproject.toml` as `ollama>=0.4.0`
- **License**: MIT
- **No files copied** (library import only)

---

## Qwen/Qwen2.5-7B-Instruct (Apache 2.0) — used as model weight

- **Source**: https://huggingface.co/Qwen/Qwen2.5-7B-Instruct (loaded via Ollama as `qwen2.5:7b`)
- **License**: Apache 2.0
- **No model files committed** (loaded at runtime via Ollama registry)

---

## License compatibility note

This repository is MIT-licensed. All derived files are MIT (browser-use) or Apache 2.0 (Qwen model). Both are compatible with this repo's MIT license. No GPL / AGPL dependencies.
