# -*- coding: utf-8 -*-
"""
apps/streamlit_demo/app.py
Buildway AI Core — Streamlit Demo App

A minimal demo showing how to use the core modules.
"""

import sys
from pathlib import Path

# Add project root to path so core/ and verticals/ are importable
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st

st.set_page_config(
    page_title="Buildway AI Core Demo",
    page_icon="🏗️",
    layout="wide",
)

st.title("🏗️ Buildway AI Core")
st.caption("Multi-industry AI workflow framework")

st.markdown("""
## Available Modules

| Module | Path | Description |
|---|---|---|
| Session Memory | `core/memory/session_memory.py` | Lightweight JSON session storage |
| RAG Manager | `core/rag/rag_manager.py` | Local document retrieval |
| OCR Engine | `core/ocr/ocr_engine.py` | PDF & image text extraction |
| File Loader | `core/document_processing/file_loader.py` | Multi-format file loading |
| Agent Router | `core/agents/agent_router.py` | Generic agent routing framework |
| Evidence Confidence | `core/agents/evidence_confidence.py` | Evidence quality scoring |
| Conflict Resolver | `core/agents/conflict_resolver.py` | Multi-agent conflict detection |
| Action Manager | `core/actions/action_manager.py` | Action item tracking |
| Report Generator | `core/reports/report_generator.py` | PDF report generation |
| Progress Tracker | `core/workflow/progress_tracker.py` | Workflow step tracking |
| Repeated Issue Detector | `core/workflow/repeated_issue_detector.py` | Cross-session issue detection |

## Verticals

| Vertical | Path | Status |
|---|---|---|
| Construction | `verticals/construction/` | Active (HK-AICOS) |
| CRM | `verticals/crm/` | Placeholder |
| Document AI | `verticals/document_ai/` | Placeholder |
""")

st.divider()
st.subheader("Quick Test: Session Memory")

with st.form("session_form"):
    project_ref = st.text_input("Project Ref", value="DEMO-001")
    question = st.text_input("Question", value="What are the key issues?")
    submitted = st.form_submit_button("Save Session")

if submitted:
    try:
        from core.memory.session_memory import save_session, load_sessions
        sid = save_session(
            project_ref=project_ref,
            file_names=["demo.pdf"],
            file_types=["pdf"],
            selected_agents=["demo_agent"],
            risk_level="low",
            analysis_summary="Demo session from Streamlit app.",
            question=question,
        )
        st.success(f"Session saved: `{sid}`")

        sessions = load_sessions(project_ref=project_ref)
        st.write(f"Total sessions for `{project_ref}`: {len(sessions)}")
        if sessions:
            st.json(sessions[0])
    except Exception as e:
        st.error(f"Error: {e}")
