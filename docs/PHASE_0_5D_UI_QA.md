# PHASE 0.5D — Production UI Cleanup QA Notes

**Date:** 2026-05-27  
**Status:** Completed

---

## Changes Applied

### A. Global CSS (`inject_global_css()`)
- Defined in both `app.py` and `pages/whatsapp_demo.py`
- Called immediately after `st.set_page_config()`
- Targets: `stToolbar`, `stDecoration`, `stHeader`, `stDeployButton`, `button[kind="header"]`, `baseButton-headerNoPadding`, `stStatusWidget`, `header`, `footer`, `#MainMenu`
- Sidebar navigation is NOT affected

### B. Developer Mode
- Wrapped in `os.getenv("BUILDWAY_DEV_MODE", "false").lower() == "true"`
- Default production: checkbox hidden, `dev_mode` defaults to `False`
- Enable via: `export BUILDWAY_DEV_MODE=true` (or set in `.env`)

### C. Traditional Chinese Localization
Replaced all remaining hardcoded English labels:
- AI Model page: `Available Now` → `目前支援`, `Coming Soon` → `即將支援`
- KB page: `Embedding Provider` → `嵌入模型`, `Indexing documents` → `索引文件中`, `Total Files/Indexed/Failed/Chunks Added` → 中文, `Clear All Documents` → `清除所有文件`, `Search` results → 中文
- CRM page: `Not set` → `未設定`, `No AI model configured` → 中文, `Generating AI draft` → `AI 正在生成回覆草稿`, `Source/KB Context/Confidence` captions → 中文, `empty response` error → 中文
- CRM page: `Please enter a customer message` → 中文

### D. Cache Clear (One-time)
```python
if st.session_state.get("force_ui_refresh", True):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.session_state["force_ui_refresh"] = False
```
Runs once per session on first load only.

### E. WhatsApp Demo
- `inject_global_css()` added after `set_page_config()`
- `layout="centered"` preserved
- All UI text already in Traditional Chinese

---

## Known Limitations

### Fork / GitHub Icon (Top-right toolbar)
The Streamlit `stToolbar` / `baseButton-headerNoPadding` CSS selectors reliably hide the **Deploy** button and **kebab menu (⋮)** in most Streamlit versions.

However, the **Fork** button and **GitHub icon** are injected by Streamlit Community Cloud's hosting layer as an overlay — these elements are rendered **outside the normal Streamlit DOM** and cannot be reliably hidden via CSS injected through `st.markdown()`.

**Workaround options (not implemented in this phase):**
1. Use Streamlit's native `hide_streamlit_style` via `config.toml` — already set to `toolbarMode = "minimal"` in `.streamlit/config.toml`
2. For full removal: deploy to a custom hosting environment (not Streamlit Community Cloud), or use Streamlit's enterprise/private deployment which allows full toolbar suppression
3. Streamlit >= 1.28 introduced `st.set_page_config(menu_items={})` which can remove some menu items but not the Fork/GitHub badge from Community Cloud

**Status:** CSS selectors applied as best-effort. Full suppression of Fork/GitHub Community Cloud badge requires infrastructure-level change.

---

## Syntax Check
```
python -m py_compile apps/streamlit_demo/app.py       → PASSED
python -m py_compile apps/streamlit_demo/pages/whatsapp_demo.py → PASSED
```

---

## Files Modified
- `apps/streamlit_demo/app.py`
- `apps/streamlit_demo/pages/whatsapp_demo.py`

## Files NOT Modified (protected)
- `core/rag/retriever.py`
- `core/agents/provider_router.py`
- All confidence / source weighting / Gemini logic
- All RAG / KB logic
- All CRM business logic
