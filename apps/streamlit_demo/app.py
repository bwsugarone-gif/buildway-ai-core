# -*- coding: utf-8 -*-
"""
apps/streamlit_demo/app.py
Buildway AI Core — Streamlit CRM Demo App (Phase 0.3A)

CRM AI Assist demo for foreign trade WhatsApp customer service vertical.
No real API connections — placeholder flow only.
"""

import sys
from pathlib import Path

# Add project root to path so core/ and verticals/ are importable
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st

st.set_page_config(
    page_title="Buildway AI Core — CRM Demo",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Buildway AI Core")
st.caption("Multi-industry AI workflow framework — CRM AI Assist Demo")

# ──────────────────────────────────────────────
# Tenant Info
# ──────────────────────────────────────────────
st.subheader("🏢 Tenant")

col1, col2, col3 = st.columns(3)
with col1:
    tenant_name = st.text_input("Tenant Name", value="Demo Trading Company")
with col2:
    industry = st.text_input("Industry", value="Foreign Trade")
with col3:
    channel = st.selectbox("Channel", ["WhatsApp", "Email", "Web Chat"], index=0)

st.divider()

# ──────────────────────────────────────────────
# Core Modules Table
# ──────────────────────────────────────────────
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

# ──────────────────────────────────────────────
# Verticals Table
# ──────────────────────────────────────────────
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

# ──────────────────────────────────────────────
# Knowledge Base Status
# ──────────────────────────────────────────────
st.subheader("📚 Knowledge Base")

kb_col1, kb_col2, kb_col3 = st.columns(3)
with kb_col1:
    st.metric("FAQ uploaded", "Not connected")
with kb_col2:
    st.metric("Product catalog", "Not connected")
with kb_col3:
    st.metric("Reply templates", "Not connected")

st.caption("Connect a real knowledge base via Qdrant in Phase 1.")

st.divider()

# ──────────────────────────────────────────────
# CRM Demo Flow
# ──────────────────────────────────────────────
st.subheader("💬 CRM Demo Flow")

demo_message = st.text_area(
    "Customer Message",
    value="Hi, what is your MOQ and delivery time?",
    height=80,
)

if st.button("Generate AI Draft Reply (Demo)"):
    with st.spinner("Generating draft reply..."):
        # Placeholder — no real LLM call
        draft_reply = (
            "Thank you for your enquiry. Our MOQ and delivery time depend on the "
            "product model. Please allow us to check the details and provide you "
            "with an accurate quotation shortly."
        )
    st.success("AI Draft Reply (placeholder):")
    st.info(draft_reply)
    st.caption("⚠️ This is a static placeholder. Real AI reply requires OpenAI/Claude API key in .env.")

st.divider()

# ──────────────────────────────────────────────
# Customer Memory Placeholder
# ──────────────────────────────────────────────
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

# ──────────────────────────────────────────────
# Session Save (Quick Test)
# ──────────────────────────────────────────────
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
