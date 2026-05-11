# SETUP — Phase 1 install runbook

> consumer laptop (Windows 11) で zero-credit-card constraint 下に install する literal 手順。
> Linux / macOS でも同等 path (winget → curl/brew、 PowerShell → bash) で再現可能。

## Prerequisites

- Windows 11 (or Linux / macOS)
- Python 3.12+ (`python --version` で確認)
- [uv](https://github.com/astral-sh/uv) installed (`uv --version` で確認)
- Git (`git --version` で確認)
- Chrome browser installed
- D: drive (or any drive) with ≥10GB free for `.venv` and Ollama models

## Step 1. Ollama install

```powershell
# Windows (winget、 UAC prompt 1 回)
winget install Ollama.Ollama --silent

# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh
```

**Verify**:
```powershell
ollama --version
```

## Step 2. Pull Qwen2.5-7B model

```powershell
# Optional: redirect Ollama model storage to D: drive (Windows)
$env:OLLAMA_MODELS = "D:\ollama_models"
[Environment]::SetEnvironmentVariable("OLLAMA_MODELS", "D:\ollama_models", "User")

# Pull the Q4_K_M quantized 7B model (~5GB)
ollama pull qwen2.5:7b
```

**Verify**:
```powershell
ollama list
# Expected: qwen2.5:7b row visible
```

## Step 3. Create Chrome sandbox profile

Open Chrome → click profile icon (top right) → "Add" → enter name `portfolio-sandbox` → finish.

**Why**: AI agent will drive the browser. Using a separate profile prevents accidentally interacting with your prod accounts (gmail, banking, etc.). Do NOT log into any real accounts in this sandbox profile.

**Verify**: Chrome menu shows two profiles, `portfolio-sandbox` is selectable.

## Step 4. Python deps install (uv + D: venv)

```powershell
# Redirect venv to D: drive to preserve C: capacity
$env:UV_PROJECT_ENVIRONMENT = "D:\venvs\browser-agent-demo"

cd C:\Users\admin\projects\portfolio\browser-agent-demo
uv sync
```

**Verify**:
```powershell
uv run python -c "import browser_use; print(browser_use.__version__)"
```

## Step 5. Supply chain audit (D-NPM-3GUARD pip equivalent)

```powershell
uv run pip-audit --strict
```

**Pass condition**: high severity 0 件、 fail-on-high 自動化済。

## Step 6. Playwright Chromium install

```powershell
uv run playwright install chromium
```

## Step 7. Baseline run (browser-use simple example via Ollama)

```powershell
uv run python examples/simple.py
```

**Pass condition**: agent successfully completes the baseline task (defined in `examples/simple.py`).

## Cleanup (Phase 3 後 = portfolio 配信完了後)

D: drive footprint を全削除して C: 容量回復:
```powershell
Remove-Item -Recurse -Force D:\venvs\browser-agent-demo
Remove-Item -Recurse -Force D:\ollama_models
winget uninstall Ollama.Ollama
```

Portfolio repo は GitHub に literal 残るので、 portfolio として常時稼働。 再走したい時は本 SETUP.md の通り再 install。

## Troubleshooting

- **winget UAC prompt blocked**: run PowerShell as admin、 or use Ollama portable .exe from https://ollama.com/download
- **Ollama port conflict**: stop other Ollama instances (`ollama ps` → `ollama stop <model>`)
- **`uv sync` fails on torch**: torch wheel may not match Python version、 specify `--python-version 3.12`
- **Chrome sandbox profile not isolated enough**: Phase 1 で issue 発生時 Docker chromium に upgrade、 ADR で literal 記録
