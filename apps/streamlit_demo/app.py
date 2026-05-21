# -*- coding: utf-8 -*-
"""
apps/streamlit_demo/app.py
Buildway AI Core — SaaS Onboarding Demo (Phase 0.4A)
CRM AI Reply Workflow MVP: real OpenAI API reply with session state.
API keys never stored or committed.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st

st.set_page_config(
    page_title="Buildway AI Core",
    page_icon="🤖",
    layout="wide",
)

# ──────────────────────────────────────────────
# UI Dictionary (i18n skeleton)
# ──────────────────────────────────────────────
LABELS = {
    "繁體中文": {
        "nav_home": "主頁",
        "nav_tenant": "Tenant 設定",
        "nav_ai": "AI Model 設定",
        "nav_db": "Database 設定",
        "nav_kb": "Knowledge Base",
        "nav_crm": "CRM",
        "nav_logs": "Usage Logs",
        "login_title": "Client Login Portal",
        "login_email": "Email",
        "login_password": "Password",
        "login_btn": "登入",
        "login_forgot": "忘記密碼？",
        "login_coming": "登入功能將於 Phase 0.4 推出。",
        "login_demo_note": "Demo 模式：無需登入。",
        "company_name": "Company Name",
        "industry": "Industry",
        "contact_email": "Contact Email",
        "channel": "Default Channel",
        "save_profile": "儲存 Tenant 資料",
        "ai_provider": "AI Provider",
        "model_name": "Model Name",
        "api_key": "API Key",
        "base_url": "Base URL",
        "save_ai": "儲存 AI 設定",
        "db_mode": "Database 模式",
        "db_hosted": "Buildway Hosted",
        "db_client": "Client Existing Database API",
        "db_url": "Database URL",
        "service_key": "API Key / Service Key",
        "readonly_ep": "Read-only API Endpoint（選填）",
        "notes": "備註",
        "qdrant_url": "Qdrant URL",
        "qdrant_key": "Qdrant API Key",
        "collection": "Collection Name",
        "save_db": "儲存 Database 設定",
        "customer_ref": "Customer Ref",
        "customer_msg": "Customer Message",
        "save_session": "儲存 Customer Session",
        "cost_model_title": "SaaS Cost Model",
        "platform_summary": "Platform Summary",
    },
    "简体中文": {
        "nav_home": "主页",
        "nav_tenant": "Tenant 设置",
        "nav_ai": "AI Model 设置",
        "nav_db": "Database 设置",
        "nav_kb": "Knowledge Base",
        "nav_crm": "CRM",
        "nav_logs": "Usage Logs",
        "login_title": "Client Login Portal",
        "login_email": "Email",
        "login_password": "Password",
        "login_btn": "登录",
        "login_forgot": "忘记密码？",
        "login_coming": "登录功能将于 Phase 0.4 推出。",
        "login_demo_note": "Demo 模式：无需登录。",
        "company_name": "Company Name",
        "industry": "Industry",
        "contact_email": "Contact Email",
        "channel": "Default Channel",
        "save_profile": "保存 Tenant 资料",
        "ai_provider": "AI Provider",
        "model_name": "Model Name",
        "api_key": "API Key",
        "base_url": "Base URL",
        "save_ai": "保存 AI 设置",
        "db_mode": "Database 模式",
        "db_hosted": "Buildway Hosted",
        "db_client": "Client Existing Database API",
        "db_url": "Database URL",
        "service_key": "API Key / Service Key",
        "readonly_ep": "Read-only API Endpoint（选填）",
        "notes": "备注",
        "qdrant_url": "Qdrant URL",
        "qdrant_key": "Qdrant API Key",
        "collection": "Collection Name",
        "save_db": "保存 Database 设置",
        "customer_ref": "Customer Ref",
        "customer_msg": "Customer Message",
        "save_session": "保存 Customer Session",
        "cost_model_title": "SaaS Cost Model",
        "platform_summary": "Platform Summary",
    },
    "English": {
        "nav_home": "Home",
        "nav_tenant": "Tenant Setup",
        "nav_ai": "AI Model Setup",
        "nav_db": "Database Setup",
        "nav_kb": "Knowledge Base",
        "nav_crm": "CRM Demo",
        "nav_logs": "Usage Logs",
        "login_title": "Client Login Portal",
        "login_email": "Email",
        "login_password": "Password",
        "login_btn": "Login",
        "login_forgot": "Forgot password?",
        "login_coming": "Authentication system coming in Phase 0.4.",
        "login_demo_note": "Demo mode: no login required.",
        "company_name": "Company Name",
        "industry": "Industry",
        "contact_email": "Contact Email",
        "channel": "Default Channel",
        "save_profile": "Save Tenant Profile",
        "ai_provider": "AI Provider",
        "model_name": "Model Name",
        "api_key": "API Key",
        "base_url": "Base URL",
        "save_ai": "Save AI Config",
        "db_mode": "Database Mode",
        "db_hosted": "Buildway Hosted",
        "db_client": "Client Existing Database API",
        "db_url": "Database URL",
        "service_key": "API Key / Service Key",
        "readonly_ep": "Read-only API Endpoint (optional)",
        "notes": "Notes",
        "qdrant_url": "Qdrant URL",
        "qdrant_key": "Qdrant API Key",
        "collection": "Collection Name",
        "save_db": "Save Database Config",
        "customer_ref": "Customer Ref",
        "customer_msg": "Customer Message",
        "save_session": "Save Customer Session",
        "cost_model_title": "SaaS Cost Model",
        "platform_summary": "Platform Summary",
    },
}

# ──────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────
LOGO_PATH = Path(__file__).parent.parent.parent / "assets" / "logo.png"

with st.sidebar:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=120)
    else:
        st.markdown("### Buildway")
    st.markdown("**Buildway Tech (HK) Limited**")
    st.caption("AI Core SaaS Platform")
    st.divider()

    lang = st.selectbox("Language / 語言", ["繁體中文", "简体中文", "English"], index=0)
    L = LABELS[lang]

    st.divider()

    page = st.radio(
        "Navigation",
        [
            L["nav_home"],
            L["nav_tenant"],
            L["nav_ai"],
            L["nav_db"],
            L["nav_kb"],
            L["nav_crm"],
            L["nav_logs"],
        ],
        label_visibility="collapsed",
    )

# ──────────────────────────────────────────────
# CRM AI helpers (Phase 0.4B) — defined at module level
# ──────────────────────────────────────────────
CRM_SYSTEM_PROMPT = (
    "You are a professional foreign trade sales assistant. "
    "Generate concise and professional English customer replies. "
    "Avoid hallucination. "
    "If information is missing, ask politely for clarification. "
    "Keep replies business-friendly."
)


def _ensure_ai_state_defaults() -> None:
    st.session_state.setdefault("ai_provider", "OpenAI")
    st.session_state.setdefault("ai_model", "gpt-4o-mini")
    st.session_state.setdefault("ai_api_key", "")
    st.session_state["ai_configured"] = bool(st.session_state.get("ai_api_key"))


def _call_openai(api_key: str, model: str, user_message: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": CRM_SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.7,
        presence_penalty=0.2,
        timeout=30,
    )
    return response.choices[0].message.content or ""


def _generate_ai_reply(api_key: str, model: str, message: str) -> str:
    return _call_openai(api_key, model, message)


def _format_ai_api_error(exc: Exception) -> str:
    err = str(exc)
    err_lower = err.lower()
    exc_name = exc.__class__.__name__.lower()
    if "auth" in err_lower or "api_key" in err_lower or "401" in err_lower:
        return f"Invalid API key: {err}"
    if "quota" in err_lower or "insufficient_quota" in err_lower or "billing" in err_lower:
        return f"Quota exceeded: {err}"
    if "timeout" in err_lower or "timed out" in err_lower or "timeout" in exc_name:
        return f"Timeout: {err}"
    if (
        "model" in err_lower
        and ("not found" in err_lower or "unavailable" in err_lower or "does not exist" in err_lower)
    ) or "notfound" in exc_name:
        return f"Model unavailable: {err}"
    return f"OpenAI API error: {err}"


# ──────────────────────────────────────────────
# Page: Home
# ──────────────────────────────────────────────
if page == L["nav_home"]:
    st.title("Buildway AI Core")
    st.caption("Buildway Tech (HK) Limited — Multi-industry AI SaaS Platform")

    # 1. Client Login Portal
    st.subheader(L["login_title"])
    with st.container(border=True):
        st.warning(L["login_coming"])
        st.caption(L["login_demo_note"])
        login_col1, login_col2 = st.columns(2)
        with login_col1:
            st.text_input(L["login_email"], placeholder="admin@yourcompany.com", disabled=True)
        with login_col2:
            st.text_input(L["login_password"], type="password", placeholder="••••••••", disabled=True)
        st.button(L["login_btn"], disabled=True)
        st.markdown(f"_{L['login_forgot']}_")
        st.markdown("""
Coming in Phase 0.4:
- Admin login
- Staff login
- Tenant isolation
- Role-based permission
""")

    st.divider()

    # 2. Platform Summary
    st.subheader(L["platform_summary"])
    st.markdown(
        "Buildway AI Core is a general AI operation platform supporting multiple industry verticals. "
        "Each client runs as an isolated Tenant with their own Knowledge Base, AI Model API key, "
        "and CRM workflow."
    )

    # 3. Core Modules
    st.subheader("Core Modules")
    st.markdown("""
| Module | Path | Description |
|---|---|---|
| Session Memory | `core/memory/base.py` | Tenant-isolated session storage |
| RAG Manager | `core/rag/base.py` | Knowledge Base retrieval |
| Tenant Context | `core/tenant/context.py` | Multi-tenant isolation |
| Config Loader | `core/config.py` | Env-based config (no hardcoded keys) |
| Agent Router | `core/agents/` | Generic agent routing framework |
| Action Manager | `core/actions/` | Action item tracking |
| Report Generator | `core/reports/` | Output generation |
| Workflow Tracker | `core/workflow/` | Workflow step tracking |
""")

    # 4. Verticals
    st.subheader("Verticals")
    st.markdown("""
| Vertical | Path | Status |
|---|---|---|
| CRM | `verticals/crm/` | Active Demo |
| Construction | `verticals/construction/` | Existing vertical |
| Document AI | `verticals/document_ai/` | Placeholder |
| ERP | `verticals/erp/` | Placeholder |
""")

    st.divider()

    # 5. SaaS Cost Model (bottom)
    st.subheader(L["cost_model_title"])
    with st.container(border=True):
        st.markdown("""
**A. Buildway Hosted**
Buildway provides hosting, Tenant database, Vector DB and platform maintenance.
Client pays monthly SaaS fee. Usage beyond included quota may be charged separately.

**B. Client Existing Database API**
Client provides Database / ERP / CRM API. Buildway only connects to client API.
Client keeps full data ownership.

**C. AI Model API**
Client provides OpenAI / Claude / Gemini / DeepSeek API key, or
Buildway can provide managed AI usage as optional paid add-on.

**D. WhatsApp API**
Client owns WhatsApp Business API and Meta account.
Buildway integrates the Webhook and workflow.
""")

# ──────────────────────────────────────────────
# Page: Tenant Setup
# ──────────────────────────────────────────────
elif page == L["nav_tenant"]:
    st.title(L["nav_tenant"])

    with st.form("tenant_form"):
        company_name = st.text_input(L["company_name"], value="Demo Trading Company")
        industry = st.text_input(L["industry"], value="Foreign Trade")
        contact_email = st.text_input(L["contact_email"], value="admin@example.com")
        default_channel = st.selectbox(L["channel"], ["WhatsApp", "Email", "Web Chat"], index=0)
        save_tenant = st.form_submit_button(L["save_profile"])

    if save_tenant:
        st.success(f"{L['save_profile']}: **{company_name}** | {industry} | {default_channel}")
        st.caption("In production, stored in tenants table with unique tenant_id.")

# ──────────────────────────────────────────────
# Page: AI Model Setup
# ──────────────────────────────────────────────
elif page == L["nav_ai"]:
    _ensure_ai_state_defaults()
    st.title(L["nav_ai"])

    st.warning(
        "API keys are stored in session memory only. "
        "Keys are never written to disk, logged, or committed. "
        "Session is cleared when the browser tab is closed."
    )
    st.info(
        "Client-owned API key is recommended to avoid mixed Token billing. "
        "Buildway-managed AI usage can be provided as a paid add-on."
    )

    # Provider selection (outside form so model list updates immediately)
    provider = st.selectbox(
        L["ai_provider"],
        ["OpenAI"],
        index=0,
        key="ai_provider_select",
    )

    OPENAI_MODELS = ["gpt-4o-mini", "gpt-4.1-mini"]

    with st.form("ai_model_form"):
        current_model = st.session_state.get("ai_model", OPENAI_MODELS[0])
        model_name = st.selectbox(
            L["model_name"],
            OPENAI_MODELS,
            index=OPENAI_MODELS.index(current_model) if current_model in OPENAI_MODELS else 0,
        )
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-... (session only, never stored)",
        )

        save_ai = st.form_submit_button(L["save_ai"])

    if save_ai:
        if api_key_input:
            # Store in session_state — never written to disk
            st.session_state["ai_provider"] = provider
            st.session_state["ai_model"] = model_name
            st.session_state["ai_api_key"] = api_key_input
            st.session_state["ai_configured"] = True
            st.success(f"{provider} configured — model: `{model_name}`")
            st.caption("Key stored in session memory only. Not saved to disk or database.")
        else:
            st.session_state["ai_configured"] = False
            st.error("API Key is required.")

    st.divider()
    configured = bool(st.session_state.get("ai_api_key"))
    st.session_state["ai_configured"] = configured
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(L["ai_provider"], st.session_state.get("ai_provider", "Not set"))
    with c2:
        st.metric(L["model_name"], st.session_state.get("ai_model", "Not set"))
    with c3:
        st.metric("Status", "Ready" if configured else "Not configured")

# ──────────────────────────────────────────────
# Page: Database Setup
# ──────────────────────────────────────────────
elif page == L["nav_db"]:
    st.title(L["nav_db"])

    st.warning(
        "API keys are not stored in this demo version. "
        "Production version will store encrypted keys in a secure backend."
    )

    st.subheader(L["db_mode"])
    db_mode = st.radio(
        "Choose database mode:",
        [L["db_hosted"], L["db_client"]],
        index=0,
        label_visibility="collapsed",
    )

    if db_mode == L["db_hosted"]:
        st.info(
            f"**{L['db_hosted']}** — No external Database is required from client. "
            "Database / Vector DB / storage are provided under Buildway SaaS plan."
        )
        st.caption("Cost responsibility: included in monthly SaaS plan / subject to quota.")
        st.markdown(
            "> Client does not need to prepare a database server. "
            "Client still needs to prepare business data such as FAQ, product catalog and reply templates."
        )
    else:
        st.caption("Connect your existing Database API.")

        with st.form("db_form"):
            db_provider = st.selectbox(
                "Database Provider",
                ["Supabase", "PostgreSQL", "Firebase", "Custom REST API"],
            )
            db_url = st.text_input(
                L["db_url"],
                placeholder="https://xxxx.supabase.co or postgresql://...",
            )
            db_service_key = st.text_input(
                L["service_key"],
                type="password",
                placeholder="(never stored or committed)",
            )
            db_readonly_endpoint = st.text_input(
                L["readonly_ep"],
                placeholder="https://xxxx.supabase.co/rest/v1",
            )
            db_notes = st.text_area(L["notes"], placeholder="e.g. project name, region", height=60)

            st.divider()
            st.markdown("**Vector Database (Qdrant)**")
            qdrant_url = st.text_input(
                L["qdrant_url"],
                placeholder="https://your-qdrant-instance.com or http://localhost:6333",
            )
            qdrant_api_key = st.text_input(
                L["qdrant_key"],
                type="password",
                placeholder="(never stored or committed)",
            )
            collection_name = st.text_input(L["collection"], value="crm_knowledge_base")
            save_db = st.form_submit_button(L["save_db"])

        if save_db:
            if db_url or qdrant_url:
                st.success(f"{L['save_db']} (demo — not stored anywhere).")
                if db_url:
                    st.info(f"DB: `{db_provider}` — URL configured")
                if qdrant_url:
                    st.info(f"Qdrant: collection `{collection_name}` — URL configured")
            else:
                st.warning("No Database URL provided. Using placeholder mode.")

# ──────────────────────────────────────────────
# Page: Knowledge Base
# ──────────────────────────────────────────────
elif page == L["nav_kb"]:
    st.title(L["nav_kb"])

    kb_col1, kb_col2, kb_col3 = st.columns(3)
    with kb_col1:
        st.metric("FAQ", "Not connected")
    with kb_col2:
        st.metric("Product Catalog", "Not connected")
    with kb_col3:
        st.metric("Reply Templates", "Not connected")

    st.info(
        "Phase 1 Knowledge Base — Only the following documents are needed:\n\n"
        "- FAQ\n- Product Catalog\n- MOQ / Shipping Terms / Payment Terms\n- Reply Templates"
    )

    st.divider()

    # FAQ Data Template
    st.subheader("FAQ Data Template")
    st.markdown(
        "Prepare your FAQ as an Excel or CSV file with the following columns. "
        "This is the recommended format for building the RAG Knowledge Base."
    )
    st.markdown("""
| Column | Description |
|---|---|
| Category | Topic group, e.g. MOQ, Shipping, Payment |
| Question | Customer question text |
| Standard Answer | Approved reply for this question |
| Can Auto Reply | Yes / No — whether AI can reply without human review |
| Need Human Approval | Yes / No — whether staff must approve before sending |
| Risk Level | Low / Medium / High |
| Notes | Internal notes, e.g. "Do not quote exact price" |
""")

    st.markdown("**Example row:**")
    st.code(
        "Category: MOQ\n"
        "Question: What is your MOQ?\n"
        "Standard Answer: Our MOQ depends on product model. Please share the model number and quantity for confirmation.\n"
        "Can Auto Reply: Yes\n"
        "Need Human Approval: No\n"
        "Risk Level: Low\n"
        "Notes: Do not quote exact price.",
        language="text",
    )
    st.caption("Recommended format: Excel (.xlsx) or CSV. Minimum 20 Q&A pairs for Phase 1.")

    st.divider()
    st.subheader("Upload Documents (Demo)")
    st.caption(
        "Demo mode supports small files only. "
        "Recommended test file size: under 20MB. "
        "Large files such as 200MB will be handled in production by background ingestion."
    )
    uploaded = st.file_uploader(
        "Upload FAQ / Product Catalog / Templates",
        type=["pdf", "txt", "docx", "csv", "xlsx"],
        accept_multiple_files=True,
    )
    if uploaded:
        for f in uploaded:
            size_mb = f.size / (1024 * 1024)
            if size_mb > 20:
                st.warning(
                    f"`{f.name}` ({size_mb:.1f} MB) — File too large for demo mode. "
                    "Production version will support large file ingestion via cloud storage."
                )
            else:
                st.info(f"`{f.name}` ({size_mb:.1f} MB) — received (demo: not processed or stored)")
        st.caption("In Phase 1, files will be chunked and indexed into Qdrant per tenant_id.")

# ──────────────────────────────────────────────
# Page: CRM Demo  (Phase 0.4B — Real AI API)
# ──────────────────────────────────────────────
elif page == L["nav_crm"]:

    # ── Session state init ────────────────────────
    _ensure_ai_state_defaults()
    if "crm_reply" not in st.session_state:
        st.session_state["crm_reply"] = ""
    if "crm_reply_source" not in st.session_state:
        st.session_state["crm_reply_source"] = ""
    if "crm_message" not in st.session_state:
        st.session_state["crm_message"] = "Hi, what is your MOQ and delivery time?"

    st.title("CRM AI Assist")
    st.caption(
        "Tenant: Demo Trading Company  |  Industry: Foreign Trade  |  Channel: WhatsApp"
    )

    # ── AI status banner ──────────────────────────
    ai_configured = bool(st.session_state.get("ai_api_key"))
    st.session_state["ai_configured"] = ai_configured
    st.subheader("Current AI Status")
    status_col1, status_col2, status_col3 = st.columns(3)
    with status_col1:
        st.metric("Provider", st.session_state.get("ai_provider", "OpenAI"))
    with status_col2:
        st.metric("Model", st.session_state.get("ai_model", "gpt-4o-mini"))
    with status_col3:
        st.metric("API", "configured" if ai_configured else "Not configured")
    if ai_configured:
        st.success(
            f"AI Model ready: **{st.session_state.get('ai_provider')}** — "
            f"`{st.session_state.get('ai_model')}`"
        )
    else:
        st.warning("No AI model configured. Please complete AI Model Setup first.")

    # ── Customer message input ────────────────────
    st.subheader("Customer Message")
    customer_input = st.text_area(
        "customer_input",
        value=st.session_state["crm_message"],
        height=110,
        label_visibility="collapsed",
        placeholder="Paste or type the customer message here...",
    )

    btn_col1, btn_col2 = st.columns([3, 1])
    with btn_col1:
        generate_clicked = st.button(
            "Generate Draft Reply", type="primary", use_container_width=True
        )
    with btn_col2:
        clear_clicked = st.button("Clear", use_container_width=True)

    if clear_clicked:
        st.session_state["crm_reply"] = ""
        st.session_state["crm_reply_source"] = ""
        st.session_state["crm_message"] = ""
        st.rerun()

    if generate_clicked:
        if not customer_input.strip():
            st.warning("Please enter a customer message before generating.")
        else:
            st.session_state["crm_message"] = customer_input
            if ai_configured:
                with st.spinner("Generating AI draft..."):
                    try:
                        reply = _generate_ai_reply(
                            api_key=st.session_state["ai_api_key"],
                            model=st.session_state["ai_model"],
                            message=customer_input,
                        )
                        if reply:
                            st.session_state["crm_reply"] = reply
                            st.session_state["crm_reply_source"] = "OpenAI API"
                        else:
                            st.error("AI returned an empty response. Please try again.")
                    except Exception as e:
                        st.error(_format_ai_api_error(e))
            else:
                st.session_state["crm_reply"] = ""
                st.session_state["crm_reply_source"] = ""
                st.error("No AI model configured. Please complete AI Model Setup first.")

    # ── Draft reply output panel ──────────────────
    if st.session_state["crm_reply"]:
        st.divider()
        st.subheader("Draft Reply")

        with st.container(border=True):
            st.markdown(
                "<div style='font-family: Arial, sans-serif; font-size: 14px; "
                "line-height: 1.8; white-space: pre-wrap; padding: 4px 0;'>"
                + st.session_state["crm_reply"].replace("\n", "<br>")
                + "</div>",
                unsafe_allow_html=True,
            )

        action_col1, action_col2 = st.columns(2)
        with action_col1:
            src = st.session_state.get("crm_reply_source", "")
            st.caption(f"Source: {src}" if src else "")
        with action_col2:
            if st.button("Copy Reply", use_container_width=True):
                st.toast("Reply copied (browser clipboard integration coming in Phase 0.5).")

    st.divider()

    # ── Customer memory panel ─────────────────────
    st.subheader("Customer Memory")
    mem_col1, mem_col2, mem_col3 = st.columns(3)
    with mem_col1:
        st.text_area("Customer Summary", value="(Not connected)", height=80, disabled=True)
    with mem_col2:
        st.text_area("Last Inquiry", value="(Not connected)", height=80, disabled=True)
    with mem_col3:
        st.text_area("Follow-up Status", value="(Not connected)", height=80, disabled=True)
    st.caption("Customer memory will be stored per tenant_id in Supabase in Phase 1.")

    st.divider()

    # ── Save session ──────────────────────────────
    st.subheader(L["save_session"])
    with st.form("session_form"):
        customer_ref = st.text_input(L["customer_ref"], value="CUST-001")
        customer_message_save = st.text_input(
            L["customer_msg"],
            value=st.session_state.get("crm_message", "What is your MOQ?"),
        )
        submitted = st.form_submit_button(L["save_session"])

    if submitted:
        try:
            from core.memory.session_memory import save_session, load_sessions
            sid = save_session(
                project_ref=customer_ref,
                file_names=[],
                file_types=[],
                selected_agents=["crm_agent"],
                risk_level="low",
                analysis_summary="CRM demo session.",
                question=customer_message_save,
            )
            st.success(f"Session saved: `{sid}`")
            sessions = load_sessions(project_ref=customer_ref)
            st.write(f"Total sessions for `{customer_ref}`: {len(sessions)}")
            if sessions:
                st.json(sessions[0])
        except Exception as e:
            st.warning(f"Session memory not connected (expected in skeleton): {e}")
            st.info(
                f"Would save: customer_ref=`{customer_ref}`, "
                f"message=`{customer_message_save}`"
            )

# ──────────────────────────────────────────────
# Page: Usage Logs
# ──────────────────────────────────────────────
elif page == L["nav_logs"]:
    st.title(L["nav_logs"])
    st.info("Usage logs will be populated once AI Model is connected.")

    import pandas as pd
    st.dataframe(
        pd.DataFrame({
            "Date": ["—", "—", "—"],
            "Tenant": ["Demo Trading Company", "—", "—"],
            "Provider": ["OpenAI", "—", "—"],
            "Tokens Used": [0, 0, 0],
            "Estimated Cost (USD)": [0.00, 0.00, 0.00],
        }),
        use_container_width=True,
    )
    st.caption(
        "In production, usage_logs table in Supabase tracks all API calls per tenant_id."
    )
