# -*- coding: utf-8 -*-
"""
pages/whatsapp_demo.py
Buildway AI Core — PHASE 0.5C
Fake WhatsApp-style CRM chat UI (demo only, no real WhatsApp API).

Design:
- Reuses existing RAG retriever and AI provider from session state
- No webhook / websocket / login / realtime sync
- Mobile-first, WhatsApp-style chat bubbles
- Session state keys: wa_chat_history, wa_typing, wa_selected_example, wa_input
"""

import os
import sys
from pathlib import Path
from datetime import datetime

os.environ.setdefault("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "python")

# Allow imports from project root
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import streamlit as st

from core.agents.provider_router import (
    AIProviderConfig,
    DEFAULT_OPENAI_COMPATIBLE_ENDPOINT_PATH,
    STATUS_CONNECTED,
    call_ai_reply,
    get_default_model,
    mask_sensitive_text,
    PROVIDER_OPENAI,
    SUPPORTED_PROVIDERS,
)

# ──────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="WhatsApp CRM Demo — Buildway",
    page_icon="💬",
    layout="centered",
)

# ──────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────
FAKE_MESSAGES = [
    "What is your MOQ?",
    "What are your shipping terms?",
    "Can I order 200 units?",
    "Do you offer FOB or EXW?",
]

CRM_SYSTEM_PROMPT_BASE = (
    "You are a professional foreign trade sales assistant. "
    "Generate concise and professional English customer replies. "
    "Avoid hallucination. "
    "If information is missing, ask politely for clarification. "
    "Keep replies business-friendly."
)

CRM_SYSTEM_PROMPT_WITH_KB = """\
You are a professional foreign trade sales assistant.

STRICT RULES:
- NEVER invent pricing information
- NEVER invent shipping fees or delivery times
- NEVER invent MOQ (Minimum Order Quantity)
- NEVER make up product specifications
- ONLY use information from the provided Knowledge Base context
- If information is missing: politely ask follow-up questions
- If confidence is low: explicitly state uncertainty
- If KB has conflicting data: explain the conflict instead of choosing randomly

CONTEXT (from Knowledge Base):
{kb_context}

Generate a professional reply based ONLY on the customer message and context above.
If the answer is not in the knowledge base, say so and ask for clarification."""

CONFIDENCE_EMOJI = {"HIGH": "🟢", "MEDIUM": "🟡", "LOW": "🔴"}

# ──────────────────────────────────────────────
# WhatsApp CSS
# ──────────────────────────────────────────────
WA_CSS = """
<style>
/* Chat container */
.wa-container {
    max-width: 520px;
    margin: 0 auto;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
}

/* Header bar */
.wa-header {
    background: #075e54;
    color: white;
    padding: 12px 16px;
    border-radius: 12px 12px 0 0;
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 0;
}
.wa-header-avatar {
    width: 38px;
    height: 38px;
    background: #25d366;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}
.wa-header-info { flex: 1; }
.wa-header-name { font-weight: 600; font-size: 15px; }
.wa-header-sub { font-size: 11px; opacity: 0.8; }

/* Chat body */
.wa-body {
    background: #e5ddd5;
    background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23c4b9ad' fill-opacity='0.15'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    padding: 12px 10px;
    min-height: 340px;
    border-radius: 0;
    border-left: 1px solid #ccc;
    border-right: 1px solid #ccc;
}

/* Bubbles */
.wa-bubble-row-customer {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 6px;
}
.wa-bubble-row-ai {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 6px;
}
.wa-bubble-customer {
    background: #ffffff;
    color: #111;
    padding: 8px 12px 6px 12px;
    border-radius: 0 8px 8px 8px;
    max-width: 78%;
    box-shadow: 0 1px 2px rgba(0,0,0,0.18);
    word-wrap: break-word;
}
.wa-bubble-ai {
    background: #dcf8c6;
    color: #111;
    padding: 8px 12px 6px 12px;
    border-radius: 8px 0 8px 8px;
    max-width: 78%;
    box-shadow: 0 1px 2px rgba(0,0,0,0.18);
    word-wrap: break-word;
}
.wa-bubble-text { font-size: 14px; line-height: 1.5; }
.wa-bubble-time {
    font-size: 10px;
    color: #888;
    text-align: right;
    margin-top: 3px;
}
.wa-bubble-meta {
    font-size: 10px;
    color: #666;
    margin-top: 3px;
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    justify-content: flex-end;
}
.wa-badge {
    background: rgba(0,0,0,0.06);
    border-radius: 8px;
    padding: 1px 5px;
    font-size: 10px;
}

/* Typing indicator */
.wa-typing {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 12px;
    margin: 2px 0 6px 0;
}
.wa-typing-dots {
    display: flex;
    gap: 3px;
}
.wa-typing-dot {
    width: 7px;
    height: 7px;
    background: #888;
    border-radius: 50%;
    animation: wa-bounce 1.2s infinite;
}
.wa-typing-dot:nth-child(2) { animation-delay: 0.2s; }
.wa-typing-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes wa-bounce {
    0%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-5px); }
}
.wa-typing-label { font-size: 11px; color: #555; font-style: italic; }

/* Input area */
.wa-input-area {
    background: #f0f0f0;
    padding: 8px 10px;
    border-radius: 0 0 12px 12px;
    border: 1px solid #ccc;
    border-top: none;
}

/* Responsive */
@media (max-width: 600px) {
    .wa-container { max-width: 100%; }
    .wa-bubble-customer, .wa-bubble-ai { max-width: 90%; }
}
</style>
"""

# ──────────────────────────────────────────────
# Helper functions
# ──────────────────────────────────────────────

def _get_ai_config() -> dict | None:
    """Read AI config from shared session state. Returns None if not connected."""
    configs = st.session_state.get("ai_provider_configs", {})
    provider = st.session_state.get("ai_provider", PROVIDER_OPENAI)
    if not configs or provider not in configs:
        return None
    cfg = configs[provider]
    if cfg.get("connection_status") != STATUS_CONNECTED:
        return None
    return cfg


def _get_rag_retriever():
    """Return RAG retriever if initialized, else None."""
    if not st.session_state.get("rag_initialized", False):
        return None
    return st.session_state.get("rag_retriever", None)


def _calculate_confidence(results: list) -> str:
    """Calculate confidence from search results."""
    if not results:
        return "LOW"
    similarity = results[0].get("similarity")
    if similarity is None:
        distance = results[0].get("distance", 1.0)
        similarity = 1.0 - (distance / 2.0)
    if similarity >= 0.85:
        return "HIGH"
    elif similarity >= 0.65:
        return "MEDIUM"
    return "LOW"


def _generate_ai_reply(
    customer_msg: str,
    ai_cfg: dict,
) -> dict:
    """
    Generate AI reply using existing CRM backend logic.
    Returns dict: {text, source, kb_used, confidence, conflict_warning}
    """
    kb_context = ""
    kb_used = False
    confidence = "N/A"
    conflict_warning = None
    source = f"{ai_cfg.get('provider', 'AI')} API"

    retriever = _get_rag_retriever()
    if retriever:
        try:
            results = retriever.search(customer_msg, top_k=5)
            if results:
                kb_used = True
                # confidence
                try:
                    if hasattr(retriever, "calculate_confidence"):
                        confidence = retriever.calculate_confidence(results)
                    else:
                        confidence = _calculate_confidence(results)
                except Exception:
                    confidence = _calculate_confidence(results)
                # conflict detection
                try:
                    if hasattr(retriever, "detect_conflicts"):
                        conflict_warning = retriever.detect_conflicts(results, customer_msg)
                except Exception:
                    conflict_warning = None
                # build context
                context_parts = [f"[Context {i}]\n{r['text']}" for i, r in enumerate(results, 1)]
                kb_context = "\n\n".join(context_parts)
        except Exception as kb_err:
            # Non-fatal: continue without KB
            kb_used = False

    system_prompt = (
        CRM_SYSTEM_PROMPT_WITH_KB.format(kb_context=kb_context)
        if kb_context
        else CRM_SYSTEM_PROMPT_BASE
    )

    provider = ai_cfg.get("provider", PROVIDER_OPENAI)
    model = ai_cfg.get("resolved_model") or ai_cfg.get("model", get_default_model(provider))
    api_key = ai_cfg.get("api_key", "")
    base_url = ai_cfg.get("base_url", "")
    endpoint_path = ai_cfg.get("endpoint_path", DEFAULT_OPENAI_COMPATIBLE_ENDPOINT_PATH)

    ai_result = call_ai_reply(
        provider=provider,
        message=customer_msg,
        api_key=api_key,
        model=model,
        base_url=base_url,
        endpoint_path=endpoint_path,
        system_prompt=system_prompt,
    )

    return {
        "text": ai_result.content,
        "source": source,
        "kb_used": kb_used,
        "confidence": confidence,
        "conflict_warning": conflict_warning,
    }


def _format_timestamp() -> str:
    return datetime.now().strftime("%H:%M")


def _render_chat_bubble(msg: dict) -> str:
    """Render a single chat bubble as HTML string."""
    role = msg["role"]
    text_escaped = (
        msg["text"]
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br>")
    )
    ts = msg.get("timestamp", "")

    if role == "customer":
        return f"""
<div class="wa-bubble-row-customer">
  <div class="wa-bubble-customer">
    <div class="wa-bubble-text">{text_escaped}</div>
    <div class="wa-bubble-time">{ts}</div>
  </div>
</div>"""
    else:
        # AI bubble
        confidence = msg.get("confidence", "N/A")
        kb_used = msg.get("kb_used", False)
        source = msg.get("source", "AI")
        conf_emoji = CONFIDENCE_EMOJI.get(confidence, "⚪")
        kb_badge = "KB ✓" if kb_used else "No KB"

        meta_html = f"""
    <div class="wa-bubble-meta">
      <span class="wa-badge">{conf_emoji} {confidence}</span>
      <span class="wa-badge">{kb_badge}</span>
      <span class="wa-badge">{source}</span>
    </div>"""

        return f"""
<div class="wa-bubble-row-ai">
  <div class="wa-bubble-ai">
    <div class="wa-bubble-text">{text_escaped}</div>
    <div class="wa-bubble-time">{ts}</div>
    {meta_html}
  </div>
</div>"""


def _render_typing_indicator() -> str:
    return """
<div class="wa-bubble-row-ai">
  <div class="wa-typing">
    <div class="wa-typing-dots">
      <div class="wa-typing-dot"></div>
      <div class="wa-typing-dot"></div>
      <div class="wa-typing-dot"></div>
    </div>
    <span class="wa-typing-label">AI is typing...</span>
  </div>
</div>"""


# ──────────────────────────────────────────────
# Session state init (wa_ namespace only)
# ──────────────────────────────────────────────
if "wa_chat_history" not in st.session_state:
    st.session_state["wa_chat_history"] = []
if "wa_typing" not in st.session_state:
    st.session_state["wa_typing"] = False
if "wa_selected_example" not in st.session_state:
    st.session_state["wa_selected_example"] = FAKE_MESSAGES[0]
if "wa_input" not in st.session_state:
    st.session_state["wa_input"] = ""

# ──────────────────────────────────────────────
# Status checks
# ──────────────────────────────────────────────
ai_cfg = _get_ai_config()
ai_ready = ai_cfg is not None
rag_ready = _get_rag_retriever() is not None

# ──────────────────────────────────────────────
# Page header
# ──────────────────────────────────────────────
st.markdown(WA_CSS, unsafe_allow_html=True)

# Status banners (outside chat container)
if not ai_ready:
    st.warning("⚠️ Please configure and connect an AI Model first (AI Model Setup page).", icon="🤖")
if not rag_ready:
    st.info("ℹ️ Knowledge Base not initialized. AI will reply without KB context. Upload KB in the Knowledge Base page.", icon="📚")

# ──────────────────────────────────────────────
# WhatsApp header bar
# ──────────────────────────────────────────────
provider_label = st.session_state.get("ai_provider", "AI")
ai_status_dot = "🟢" if ai_ready else "🔴"
kb_status_dot = "🟢" if rag_ready else "⚪"

st.markdown(f"""
<div class="wa-container">
  <div class="wa-header">
    <div class="wa-header-avatar">👤</div>
    <div class="wa-header-info">
      <div class="wa-header-name">Demo Customer</div>
      <div class="wa-header-sub">AI: {ai_status_dot} {provider_label} &nbsp;|&nbsp; KB: {kb_status_dot}</div>
    </div>
    <div style="font-size:22px;">💬</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Chat body
# ──────────────────────────────────────────────
chat_html_parts = ['<div class="wa-container"><div class="wa-body">']

if not st.session_state["wa_chat_history"]:
    chat_html_parts.append(
        '<div style="text-align:center;color:#888;font-size:12px;padding:20px 0;">'
        '💬 Start a conversation below</div>'
    )
else:
    for msg in st.session_state["wa_chat_history"]:
        chat_html_parts.append(_render_chat_bubble(msg))

if st.session_state["wa_typing"]:
    chat_html_parts.append(_render_typing_indicator())

chat_html_parts.append('</div></div>')
st.markdown("".join(chat_html_parts), unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Conflict warning (outside chat, more visible)
# ──────────────────────────────────────────────
if st.session_state["wa_chat_history"]:
    last_ai = next(
        (m for m in reversed(st.session_state["wa_chat_history"]) if m["role"] == "ai"),
        None,
    )
    if last_ai and last_ai.get("conflict_warning"):
        st.warning(last_ai["conflict_warning"])

# ──────────────────────────────────────────────
# Input area
# ──────────────────────────────────────────────
st.markdown("---")

# Example messages simulator
with st.container():
    st.caption("📨 Simulate Incoming Message")
    sim_col1, sim_col2 = st.columns([4, 1])
    with sim_col1:
        selected_example = st.selectbox(
            "Select example",
            FAKE_MESSAGES,
            key="wa_selected_example",
            label_visibility="collapsed",
        )
    with sim_col2:
        simulate_clicked = st.button(
            "Simulate",
            use_container_width=True,
            help="Inject this as a customer message",
        )

st.caption("✏️ Or type your own message")
input_col1, input_col2 = st.columns([5, 1])
with input_col1:
    user_input = st.text_input(
        "Message",
        key="wa_input",
        placeholder="Type a message...",
        label_visibility="collapsed",
    )
with input_col2:
    send_clicked = st.button(
        "Send",
        type="primary",
        use_container_width=True,
        disabled=not ai_ready,
    )

clear_col1, clear_col2 = st.columns([5, 1])
with clear_col2:
    if st.button("Clear chat", use_container_width=True):
        st.session_state["wa_chat_history"] = []
        st.session_state["wa_typing"] = False
        st.rerun()

# ──────────────────────────────────────────────
# Message processing
# ──────────────────────────────────────────────
def _process_message(customer_text: str) -> None:
    """Add customer message, call AI, append AI reply."""
    customer_text = customer_text.strip()
    if not customer_text:
        return

    # Append customer bubble
    st.session_state["wa_chat_history"].append({
        "role": "customer",
        "text": customer_text,
        "timestamp": _format_timestamp(),
        "source": "",
        "kb_used": False,
        "confidence": "N/A",
    })
    st.session_state["wa_typing"] = True
    st.rerun()


def _finalize_ai_reply(customer_text: str) -> None:
    """Called when wa_typing is True — execute AI call and append result."""
    ai_cfg_local = _get_ai_config()
    if not ai_cfg_local:
        st.session_state["wa_typing"] = False
        st.session_state["wa_chat_history"].append({
            "role": "ai",
            "text": "⚠️ AI provider not connected. Please configure AI Model first.",
            "timestamp": _format_timestamp(),
            "source": "System",
            "kb_used": False,
            "confidence": "N/A",
            "conflict_warning": None,
        })
        return

    try:
        result = _generate_ai_reply(customer_text, ai_cfg_local)
        st.session_state["wa_chat_history"].append({
            "role": "ai",
            "text": result["text"] or "(empty response)",
            "timestamp": _format_timestamp(),
            "source": result["source"],
            "kb_used": result["kb_used"],
            "confidence": result["confidence"],
            "conflict_warning": result.get("conflict_warning"),
        })
    except Exception as e:
        err_msg = mask_sensitive_text(str(e))
        st.session_state["wa_chat_history"].append({
            "role": "ai",
            "text": f"❌ Error: {err_msg}",
            "timestamp": _format_timestamp(),
            "source": "System",
            "kb_used": False,
            "confidence": "N/A",
            "conflict_warning": None,
        })
    finally:
        st.session_state["wa_typing"] = False


# Handle "typing" state — finalize pending AI reply
if st.session_state.get("wa_typing"):
    # Find last customer message to reply to
    last_customer = next(
        (m["text"] for m in reversed(st.session_state["wa_chat_history"]) if m["role"] == "customer"),
        "",
    )
    if last_customer:
        with st.spinner("AI is generating reply..."):
            _finalize_ai_reply(last_customer)
        st.rerun()
    else:
        st.session_state["wa_typing"] = False

# Handle simulate button
if simulate_clicked and ai_ready:
    _process_message(selected_example)

# Handle send button or Enter
if send_clicked and user_input.strip():
    if not ai_ready:
        st.warning("Please configure and connect an AI Model first.")
    else:
        _process_message(user_input)
        # Clear input by resetting key
        st.session_state["wa_input"] = ""

# ──────────────────────────────────────────────
# Footer info
# ──────────────────────────────────────────────
st.markdown("---")
with st.expander("ℹ️ About this demo"):
    st.markdown("""
**WhatsApp CRM Demo — PHASE 0.5C**

This is a **fake demo UI** for showcasing the CRM AI workflow in a WhatsApp-style interface.

**What's real:**
- AI replies use your configured AI provider (OpenAI / Claude / Gemini / DeepSeek)
- KB retrieval uses the same RAG system as the CRM page
- Confidence scoring and conflict detection are fully functional

**What's fake:**
- No real WhatsApp API
- No webhook, websocket, or realtime sync
- No login or authentication
- Customer messages are simulated

**Chat bubble badges:**
- 🟢 HIGH / 🟡 MEDIUM / 🔴 LOW — confidence score
- KB ✓ / No KB — whether Knowledge Base was used
- Source — AI provider used

> Configure AI Model and Knowledge Base on their respective pages before using this demo.
""")
