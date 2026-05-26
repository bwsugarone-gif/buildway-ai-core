# -*- coding: utf-8 -*-
"""
pages/whatsapp_demo.py
Buildway AI Core — PHASE 0.5C (Hotfix: Chinese UI + nav buttons)
Fake WhatsApp-style CRM chat UI (demo only, no real WhatsApp API).

Design:
- Reuses existing RAG retriever and AI provider from session state
- No webhook / websocket / login / realtime sync
- Mobile-first, WhatsApp-style chat bubbles
- Session state keys: wa_chat_history, wa_typing, wa_selected_example, wa_input
- UI language: Traditional Chinese
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
    DEFAULT_OPENAI_COMPATIBLE_ENDPOINT_PATH,
    STATUS_CONNECTED,
    call_ai_reply,
    get_default_model,
    mask_sensitive_text,
    PROVIDER_OPENAI,
)

# ──────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="WhatsApp CRM 示範 — Buildway",
    page_icon="💬",
    layout="centered",
)

# ──────────────────────────────────────────────
# Hide Streamlit chrome (toolbar, header, footer, deploy/fork)
# Sidebar navigation is NOT affected.
# ──────────────────────────────────────────────
st.markdown(
    """
<style>
[data-testid="stToolbar"] { visibility: hidden; height: 0%; position: fixed; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stHeader"] { display: none !important; }
.stDeployButton { display: none !important; }
button[kind="header"] { display: none !important; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
</style>
""",
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────
FAKE_MESSAGES = [
    "MOQ 幾多？",
    "Shipping terms 係點？",
    "200 件可唔可以落單？",
    "FOB 定 EXW？",
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
.wa-container {
    max-width: 520px;
    margin: 0 auto;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
}
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
.wa-body {
    background: #e5ddd5;
    background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23c4b9ad' fill-opacity='0.15'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    padding: 12px 10px;
    min-height: 340px;
    border-left: 1px solid #ccc;
    border-right: 1px solid #ccc;
}
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
.wa-bubble-time { font-size: 10px; color: #888; text-align: right; margin-top: 3px; }
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
.wa-typing {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 8px 12px;
    margin: 2px 0 6px 0;
}
.wa-typing-dots { display: flex; gap: 3px; }
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
@media (max-width: 600px) {
    .wa-container { max-width: 100%; }
    .wa-bubble-customer, .wa-bubble-ai { max-width: 90%; }
}
</style>
"""

# ──────────────────────────────────────────────
# Helper functions
# ──────────────────────────────────────────────

def _get_ai_config():
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


def _generate_ai_reply(customer_msg: str, ai_cfg: dict) -> dict:
    """Generate AI reply using existing CRM backend logic."""
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
                try:
                    confidence = (
                        retriever.calculate_confidence(results)
                        if hasattr(retriever, "calculate_confidence")
                        else _calculate_confidence(results)
                    )
                except Exception:
                    confidence = _calculate_confidence(results)
                try:
                    if hasattr(retriever, "detect_conflicts"):
                        conflict_warning = retriever.detect_conflicts(results, customer_msg)
                except Exception:
                    conflict_warning = None
                context_parts = [f"[Context {i}]\n{r['text']}" for i, r in enumerate(results, 1)]
                kb_context = "\n\n".join(context_parts)
        except Exception:
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
        confidence = msg.get("confidence", "N/A")
        kb_used = msg.get("kb_used", False)
        source = msg.get("source", "AI")
        conf_emoji = CONFIDENCE_EMOJI.get(confidence, "⚪")
        kb_badge = "KB ✓" if kb_used else "無 KB"
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
    <span class="wa-typing-label">AI 正在輸入...</span>
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
# Top row: title + quick nav buttons
# ──────────────────────────────────────────────
st.markdown(WA_CSS, unsafe_allow_html=True)

title_col, nav_col1, nav_col2 = st.columns([3, 1, 1])
with title_col:
    st.markdown("## 💬 WhatsApp CRM 示範")
with nav_col1:
    st.page_link("app.py", label="返回主頁 / CRM", icon="🏠")
with nav_col2:
    st.page_link("app.py", label="返回主頁 / Knowledge Base", icon="📚")

# ──────────────────────────────────────────────
# Status banners
# ──────────────────────────────────────────────
if not ai_ready:
    st.warning("⚠️ 請先設定 AI Model（前往 AI Model 設定頁面配置並測試連線）。", icon="🤖")
if not rag_ready:
    st.info("ℹ️ Knowledge Base 尚未初始化，AI 將不使用公司資料回覆。請先到 Knowledge Base 上載文件。", icon="📚")

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
      <div class="wa-header-name">示範客戶</div>
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
        '💬 請在下方開始對話</div>'
    )
else:
    for msg in st.session_state["wa_chat_history"]:
        chat_html_parts.append(_render_chat_bubble(msg))

if st.session_state["wa_typing"]:
    chat_html_parts.append(_render_typing_indicator())

chat_html_parts.append('</div></div>')
st.markdown("".join(chat_html_parts), unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Conflict warning
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

with st.container():
    st.caption("📨 模擬客戶訊息")
    sim_col1, sim_col2 = st.columns([4, 1])
    with sim_col1:
        selected_example = st.selectbox(
            "選擇訊息",
            FAKE_MESSAGES,
            key="wa_selected_example",
            label_visibility="collapsed",
        )
    with sim_col2:
        simulate_clicked = st.button(
            "模擬",
            use_container_width=True,
            help="以此訊息模擬客戶來訊",
            disabled=not ai_ready,
        )

st.caption("✏️ 或輸入自訂訊息")
input_col1, input_col2 = st.columns([5, 1])
with input_col1:
    user_input = st.text_input(
        "訊息",
        key="wa_input",
        placeholder="輸入訊息...",
        label_visibility="collapsed",
    )
with input_col2:
    send_clicked = st.button(
        "發送",
        type="primary",
        use_container_width=True,
        disabled=not ai_ready,
    )

clear_col1, clear_col2 = st.columns([5, 1])
with clear_col2:
    if st.button("清空對話", use_container_width=True):
        st.session_state["wa_chat_history"] = []
        st.session_state["wa_typing"] = False
        st.rerun()

# ──────────────────────────────────────────────
# Message processing
# ──────────────────────────────────────────────
def _process_message(customer_text: str) -> None:
    customer_text = customer_text.strip()
    if not customer_text:
        return
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
    ai_cfg_local = _get_ai_config()
    if not ai_cfg_local:
        st.session_state["wa_typing"] = False
        st.session_state["wa_chat_history"].append({
            "role": "ai",
            "text": "⚠️ AI 未連線，請先設定 AI Model。",
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
            "text": result["text"] or "（空回覆）",
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
            "text": f"❌ 錯誤：{err_msg}",
            "timestamp": _format_timestamp(),
            "source": "System",
            "kb_used": False,
            "confidence": "N/A",
            "conflict_warning": None,
        })
    finally:
        st.session_state["wa_typing"] = False


# Handle typing state
if st.session_state.get("wa_typing"):
    last_customer = next(
        (m["text"] for m in reversed(st.session_state["wa_chat_history"]) if m["role"] == "customer"),
        "",
    )
    if last_customer:
        with st.spinner("AI 正在生成回覆..."):
            _finalize_ai_reply(last_customer)
        st.rerun()
    else:
        st.session_state["wa_typing"] = False

# Handle simulate
if simulate_clicked and ai_ready:
    _process_message(selected_example)

# Handle send
if send_clicked and user_input.strip():
    if not ai_ready:
        st.warning("請先設定 AI Model。")
    else:
        _process_message(user_input)
        st.session_state["wa_input"] = ""

# ──────────────────────────────────────────────
# Footer
# ──────────────────────────────────────────────
st.markdown("---")
with st.expander("ℹ️ 關於此示範"):
    st.markdown("""
**WhatsApp CRM 示範 — PHASE 0.5C**

此為**示範介面**，用於展示 CRM AI 工作流程的 WhatsApp 風格 UI。

**真實功能：**
- AI 回覆使用已配置的 AI Provider（OpenAI / Claude / Gemini / DeepSeek）
- KB 檢索使用與 CRM 頁面相同的 RAG 系統
- 信心評分和衝突偵測功能完整

**示範模擬：**
- 不使用真實 WhatsApp API
- 無 Webhook、WebSocket 或即時同步
- 無登入或認證
- 客戶訊息為模擬輸入

**AI 氣泡標籤：**
- 🟢 HIGH / 🟡 MEDIUM / 🔴 LOW — 信心評分
- KB ✓ / 無 KB — 是否使用了 Knowledge Base
- Source — 使用的 AI Provider

> 請先在對應頁面設定 AI Model 及上載 Knowledge Base 文件。
""")
