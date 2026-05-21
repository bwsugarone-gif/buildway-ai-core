# -*- coding: utf-8 -*-
"""
apps/streamlit_demo/app.py
Buildway AI Core — SaaS Onboarding Demo (Phase 0.3B)

Multi-page Streamlit demo with sidebar navigation.
No real API connections — placeholder UI only.
API keys are never stored or committed.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st

st.set_page_config(
    page_title="Buildway AI Core",
    page_icon="🤖",
    layout="wide",
)

# ──────────────────────────────────────────────
# Sidebar — Logo + Navigation
# ──────────────────────────────────────────────
LOGO_PATH = Path(__file__).parent.parent.parent / "assets" / "logo.png"

with st.sidebar:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=120)
    else:
        st.markdown("### 🏗️")
    st.markdown("**Buildway Tech (HK) Limited**")
    st.caption("AI Core SaaS Platform")
    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "🏢 Tenant Setup",
            "🤖 AI Model Setup",
            "🗄️ Database Setup",
            "📚 Knowledge Base",
            "💬 CRM Demo",
            "📊 Usage Logs",
        ],
        label_visibility="collapsed",
    )

# ──────────────────────────────────────────────
# Page: Home
# ──────────────────────────────────────────────
if page == "🏠 Home":
    st.title("🤖 Buildway AI Core")
    st.caption("Multi-industry AI workflow framework — SaaS Platform")

    st.info(
        "**Phase 0.3B Demo** — UI skeleton only. "
        "No real API connections. No data is stored or transmitted."
    )

    st.subheader("📦 Core Modules")
    st.markdown("""
| Module | Path | Description |
|---|---|---|
| Session Memory | `core/memory/base.py` | Tenant-isolated session storage |
| RAG Manager | `core/rag/base.py` | Knowledge base retrieval |
| Tenant Context | `core/tenant/context.py` | Multi-tenant isolation |
| Config Loader | `core/config.py` | Env-based config (no hardcoded keys) |
| Agent Router | `core/agents/` | Generic agent routing framework |
| Action Manager | `core/actions/` | Action item tracking |
| Report Generator | `core/reports/` | Output generation |
| Workflow Tracker | `core/workflow/` | Workflow step tracking |
""")

    st.subheader("🗂️ Verticals")
    st.markdown("""
| Vertical | Path | Status |
|---|---|---|
| CRM | `verticals/crm/` | ✅ Active Demo |
| Construction | `verticals/construction/` | Existing vertical |
| Document AI | `verticals/document_ai/` | Placeholder |
| ERP | `verticals/erp/` | Placeholder |
""")

    st.divider()
    st.subheader("🔐 Login System")
    st.warning("**Coming Soon** — Login system is not yet implemented.")
    st.markdown("""
- Admin login
- Staff login
- Tenant isolation
- Role-based permission
""")

# ──────────────────────────────────────────────
# Page: Tenant Setup
# ──────────────────────────────────────────────
elif page == "🏢 Tenant Setup":
    st.title("🏢 Tenant Setup")
    st.caption("Configure your company profile for this SaaS tenant.")

    with st.form("tenant_form"):
        company_name = st.text_input("Company Name", value="Demo Trading Company")
        industry = st.text_input("Industry", value="Foreign Trade")
        contact_email = st.text_input("Contact Email", value="admin@example.com")
        default_channel = st.selectbox(
            "Default Channel", ["WhatsApp", "Email", "Web Chat"], index=0
        )
        save_tenant = st.form_submit_button("Save Tenant Profile")

    if save_tenant:
        st.success(
            f"Tenant profile saved (demo): **{company_name}** | {industry} | {default_channel}"
        )
        st.caption("In production, this will be stored in the tenants table with a unique tenant_id.")

# ──────────────────────────────────────────────
# Page: AI Model Setup
# ──────────────────────────────────────────────
elif page == "🤖 AI Model Setup":
    st.title("🤖 AI Model Setup")
    st.caption("Configure your AI provider. You bring your own API key.")

    st.warning(
        "🔒 **Security Notice:** API keys are not stored in this demo version. "
        "Production version will store encrypted keys in a secure backend."
    )

    provider = st.selectbox(
        "AI Provider",
        ["OpenAI", "Claude / Anthropic", "DeepSeek", "Gemini", "Custom OpenAI-Compatible API"],
    )

    with st.form("ai_model_form"):
        model_name = st.text_input(
            "Model Name",
            value={
                "OpenAI": "gpt-4o",
                "Claude / Anthropic": "claude-3-5-sonnet-20241022",
                "DeepSeek": "deepseek-chat",
                "Gemini": "gemini-1.5-pro",
                "Custom OpenAI-Compatible API": "your-model-name",
            }.get(provider, ""),
        )
        api_key = st.text_input(
            f"{provider} API Key",
            type="password",
            placeholder="sk-... (never stored or committed)",
        )
        if provider == "Custom OpenAI-Compatible API":
            base_url = st.text_input(
                "Base URL",
                placeholder="https://your-api-endpoint.com/v1",
            )
        save_ai = st.form_submit_button("Save AI Model Config")

    if save_ai:
        if api_key:
            st.success(f"✅ **{provider}** configured — model: `{model_name}`")
            st.caption("Key accepted (demo only — not stored anywhere).")
        else:
            st.error("API Key is required.")

    st.divider()
    st.subheader("Current Status")
    status_col1, status_col2 = st.columns(2)
    with status_col1:
        st.metric("AI Provider", provider)
    with status_col2:
        st.metric("Status", "Not configured" if not st.session_state.get("ai_configured") else "Configured")

# ──────────────────────────────────────────────
# Page: Database Setup
# ──────────────────────────────────────────────
elif page == "🗄️ Database Setup":
    st.title("🗄️ Database Setup")
    st.caption("Configure your database and vector store connections.")

    st.warning(
        "🔒 **Security Notice:** API keys are not stored in this demo version. "
        "Production version will store encrypted keys in a secure backend."
    )

    st.subheader("Relational Database")
    db_provider = st.selectbox(
        "Database Provider",
        ["Supabase", "PostgreSQL", "Firebase", "Custom REST API", "None / Buildway Hosted"],
    )

    with st.form("db_form"):
        db_url = st.text_input(
            "Database URL",
            placeholder="https://xxxx.supabase.co or postgresql://...",
        )
        db_service_key = st.text_input(
            "API Key / Service Key",
            type="password",
            placeholder="(never stored or committed)",
        )
        db_readonly_endpoint = st.text_input(
            "Read-only API Endpoint (optional)",
            placeholder="https://xxxx.supabase.co/rest/v1",
        )
        db_notes = st.text_area("Notes", placeholder="e.g. project name, region, etc.", height=60)

        st.divider()
        st.markdown("**Vector Database (Qdrant)**")
        qdrant_url = st.text_input(
            "Qdrant URL",
            placeholder="https://your-qdrant-instance.com or http://localhost:6333",
        )
        qdrant_api_key = st.text_input(
            "Qdrant API Key",
            type="password",
            placeholder="(never stored or committed)",
        )
        collection_name = st.text_input(
            "Collection Name",
            value="crm_knowledge_base",
        )

        save_db = st.form_submit_button("Save Database Config")

    if save_db:
        if db_url or qdrant_url:
            st.success("Database config saved (demo — not stored anywhere).")
            if db_url:
                st.info(f"DB: `{db_provider}` — URL configured")
            if qdrant_url:
                st.info(f"Qdrant: collection `{collection_name}` — URL configured")
        else:
            st.warning("No database URL provided. Using placeholder mode.")

# ──────────────────────────────────────────────
# Page: Knowledge Base
# ──────────────────────────────────────────────
elif page == "📚 Knowledge Base":
    st.title("📚 Knowledge Base")
    st.caption("Upload and manage your tenant knowledge base.")

    kb_col1, kb_col2, kb_col3 = st.columns(3)
    with kb_col1:
        st.metric("FAQ uploaded", "Not connected")
    with kb_col2:
        st.metric("Product catalog", "Not connected")
    with kb_col3:
        st.metric("Reply templates", "Not connected")

    st.caption("Connect a real knowledge base via Qdrant in Phase 1.")
    st.divider()

    st.subheader("Upload Documents (Demo)")
    uploaded = st.file_uploader(
        "Upload FAQ / Product Catalog / Templates",
        type=["pdf", "txt", "docx", "csv"],
        accept_multiple_files=True,
    )
    if uploaded:
        for f in uploaded:
            st.info(f"📄 `{f.name}` — received (demo: not processed or stored)")
        st.caption("In Phase 1, files will be chunked and indexed into Qdrant per tenant_id.")

# ──────────────────────────────────────────────
# Page: CRM Demo
# ──────────────────────────────────────────────
elif page == "💬 CRM Demo":
    st.title("💬 CRM AI Assist Demo")
    st.caption("Foreign trade WhatsApp customer service — AI draft reply placeholder.")

    # Tenant context reminder
    st.info("Tenant: **Demo Trading Company** | Industry: Foreign Trade | Channel: WhatsApp")

    st.subheader("Customer Message")
    demo_message = st.text_area(
        "Customer Message",
        value="Hi, what is your MOQ and delivery time?",
        height=80,
        label_visibility="collapsed",
    )

    if st.button("Generate AI Draft Reply (Demo)"):
        with st.spinner("Generating draft reply..."):
            draft_reply = (
                "Thank you for your enquiry. Our MOQ and delivery time depend on the "
                "product model. Please allow us to check the details and provide you "
                "with an accurate quotation shortly."
            )
        st.success("AI Draft Reply (placeholder):")
        st.info(draft_reply)
        st.caption(
            "⚠️ Static placeholder. Real AI reply requires OpenAI/Claude API key configured in AI Model Setup."
        )

    st.divider()
    st.subheader("🧠 Customer Memory")
    mem_col1, mem_col2, mem_col3 = st.columns(3)
    with mem_col1:
        st.text_area("Customer Summary", value="(Not connected)", height=80, disabled=True)
    with mem_col2:
        st.text_area("Last Inquiry", value="(Not connected)", height=80, disabled=True)
    with mem_col3:
        st.text_area("Follow-up Status", value="(Not connected)", height=80, disabled=True)
    st.caption("Customer memory will be stored per tenant_id in Supabase in Phase 1.")

    st.divider()
    st.subheader("💾 Save Customer Session")
    with st.form("session_form"):
        customer_ref = st.text_input("Customer Ref", value="CUST-001")
        customer_message = st.text_input("Customer Message", value="What is your MOQ?")
        submitted = st.form_submit_button("Save Customer Session")

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
                question=customer_message,
            )
            st.success(f"Session saved: `{sid}`")
            sessions = load_sessions(project_ref=customer_ref)
            st.write(f"Total sessions for `{customer_ref}`: {len(sessions)}")
            if sessions:
                st.json(sessions[0])
        except Exception as e:
            st.warning(f"Session memory not connected (expected in skeleton): {e}")
            st.info(f"Would save: customer_ref=`{customer_ref}`, message=`{customer_message}`")

# ──────────────────────────────────────────────
# Page: Usage Logs
# ──────────────────────────────────────────────
elif page == "📊 Usage Logs":
    st.title("📊 Usage Logs")
    st.caption("Token usage and cost tracking per tenant.")

    st.info("Usage logs will be populated once AI Model is connected.")

    import pandas as pd
    placeholder_data = {
        "Date": ["—", "—", "—"],
        "Tenant": ["Demo Trading Company", "—", "—"],
        "Provider": ["OpenAI", "—", "—"],
        "Tokens Used": [0, 0, 0],
        "Estimated Cost (USD)": [0.00, 0.00, 0.00],
    }
    st.dataframe(pd.DataFrame(placeholder_data), use_container_width=True)
    st.caption("In production, usage_logs table in Supabase will track all API calls per tenant_id.")
