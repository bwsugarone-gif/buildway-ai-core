# PHASE 0.5D — Production UI Cleanup QA Notes

**Date:** 2026-05-27 (Final Blocker Fix)
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
- Production default: checkbox is NOT rendered; `dev_mode` is directly set to `False` (not `setdefault`)
- Enable via: `BUILDWAY_DEV_MODE=true` environment variable

### C. Traditional Chinese Localization (Full)

**LABELS dictionary (繁體中文):**
- `db_hosted` → `"Buildway 託管"`
- `db_client` → `"客戶現有資料庫 API"`

**AI Model page:**
- API key warning → 繁中
- Client-owned key recommendation → 繁中
- `Custom Model Name` / `Enter model name` → `自訂模型名稱` / `輸入模型名稱`
- `Endpoint Path` → `Endpoint 路徑`
- Error messages (Missing Base URL / API key / Model Name) → 繁中
- Save success / caption → 繁中
- Test connection spinner → 繁中

**Database page:**
- Warning message → 繁中
- Radio label → 繁中
- Hosted mode description → 繁中
- Client mode description → 繁中
- `Database Provider` selectbox → uses `L["db_provider"]`

**Tenant page:**
- Save success caption → 繁中

**KB page:**
- Embedding provider metric label → `嵌入模型`
- Index progress / summary metrics → 繁中
- Clear all button → 繁中
- Search results → 繁中

**CRM page:**
- Model "Not set" → `未設定`
- Spinner → 繁中
- Warnings / errors → 繁中
- Reply metadata captions (Source, KB Context, Confidence) → 繁中

### D. Cache Clear (One-time)
```python
if st.session_state.get("force_ui_refresh", True):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.session_state["force_ui_refresh"] = False
```
Runs once per session on first load only.

### E. WhatsApp Demo
- `inject_global_css()` applied after `set_page_config()`
- `layout="centered"` preserved
- All UI text in Traditional Chinese

---

## Known Limitations

### ⚠️ Fork / GitHub Badge (Streamlit Community Cloud)

**Status: Cannot be fully hidden by app-level CSS.**

The Fork button and GitHub icon shown in the top-right corner of Streamlit Community Cloud deployments are **injected by the hosting layer as a DOM overlay**, outside the normal Streamlit app DOM. App-injected CSS via `st.markdown()` cannot reliably target or remove these elements.

**What app CSS can hide:**
- Deploy button (`.stDeployButton`)
- Kebab menu (`button[kind="header"]`)
- Toolbar (`[data-testid="stToolbar"]`)
- Status widget (`[data-testid="stStatusWidget"]`)

**What app CSS cannot hide:**
- Streamlit Community Cloud Fork badge
- GitHub repository link badge

**Production recommendation:**
To fully remove all Streamlit chrome including the Fork/GitHub badge, deploy to a self-hosted environment:
- Google Cloud Run
- Railway / Render / Fly.io
- VPS / Docker
- Any custom domain deployment

These environments do not inject the Community Cloud hosting badge and allow full Streamlit chrome suppression via `config.toml` (`toolbarMode = "minimal"` or `"viewer"`).

---

## Syntax Check
```
python -m py_compile apps/streamlit_demo/app.py              → PASSED
python -m py_compile apps/streamlit_demo/pages/whatsapp_demo.py → PASSED
```

---

## Files Modified
- `apps/streamlit_demo/app.py`
- `apps/streamlit_demo/pages/whatsapp_demo.py`
- `docs/PHASE_0_5D_UI_QA.md`

## Files NOT Modified (protected)
- `core/rag/retriever.py`
- `core/agents/provider_router.py`
- All confidence / source weighting / Gemini logic
- All RAG / KB logic
- All CRM business logic
