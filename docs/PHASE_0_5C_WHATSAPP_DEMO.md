# PHASE 0.5C — Fake WhatsApp CRM Demo

**Status:** Complete  
**Branch:** `feature/whatsapp-demo-ui`  
**File:** `apps/streamlit_demo/pages/whatsapp_demo.py`

---

## Overview

Phase 0.5C adds a WhatsApp-style chat interface as a **demo layer** on top of the existing CRM AI backend. This is a fake UI for client presentations — no real WhatsApp API is used.

---

## What Was Built

### New Files
| File | Purpose |
|---|---|
| `apps/streamlit_demo/pages/whatsapp_demo.py` | WhatsApp demo page |
| `docs/PHASE_0_5C_WHATSAPP_DEMO.md` | This document |

### Unchanged Files
All existing CRM logic is untouched:
- `apps/streamlit_demo/app.py` — main CRM app
- `core/agents/provider_router.py` — AI routing
- `core/rag/retriever.py` — RAG retrieval
- `core/rag/embedder.py`, `vector_store.py`, `loader.py`, `chunker.py`

---

## Architecture

```
pages/whatsapp_demo.py
│
├── UI Layer (Streamlit + inline CSS)
│   ├── WhatsApp header bar (dark green #075e54)
│   ├── Chat body (tan background #e5ddd5)
│   ├── Customer bubble (white, left-aligned)
│   ├── AI bubble (green #dcf8c6, right-aligned)
│   ├── Typing indicator (animated dots)
│   └── Input area (simulate + free text)
│
├── Shared Session State (read-only from main app)
│   ├── ai_provider_configs — AI provider settings
│   ├── ai_provider — selected provider
│   ├── rag_retriever — RAG retriever instance
│   └── rag_initialized — KB ready flag
│
└── Private Session State (wa_ namespace)
    ├── wa_chat_history — list of message dicts
    ├── wa_typing — bool typing indicator state
    ├── wa_selected_example — dropdown selection
    └── wa_input — text input value
```

---

## Chat Message Schema

Every message in `wa_chat_history` follows this structure:

```python
{
    "role": "customer" | "ai",
    "text": "...",
    "timestamp": "HH:MM",
    "source": "OpenAI API" | "System" | "",
    "kb_used": True | False,
    "confidence": "HIGH" | "MEDIUM" | "LOW" | "N/A",
    "conflict_warning": "..." | None,  # AI messages only
}
```

---

## Backend Reuse (No Duplication)

| Feature | Source |
|---|---|
| AI reply generation | `core.agents.provider_router.call_ai_reply` |
| KB search / RAG retrieval | `core.rag.retriever.RAGRetriever.search` |
| Confidence scoring | `RAGRetriever.calculate_confidence` |
| Conflict detection | `RAGRetriever.detect_conflicts` |
| Anti-hallucination prompt | Same `CRM_SYSTEM_PROMPT_WITH_KB` pattern as main CRM |
| Error masking | `core.agents.provider_router.mask_sensitive_text` |

---

## Graceful Degradation

| Scenario | Behaviour |
|---|---|
| AI not configured | Warning banner shown, Send button disabled |
| AI configured but not connected | Same as above |
| KB not initialized | Info banner shown, AI replies without KB context |
| KB search fails | Non-fatal, continues with plain AI reply |
| AI call fails | Error message displayed as AI bubble, no crash |

---

## Fake Incoming Messages

Four pre-loaded example messages for demo:

| Message | Topic |
|---|---|
| "What is your MOQ?" | Minimum order quantity |
| "What are your shipping terms?" | Shipping conditions |
| "Can I order 200 units?" | Order quantity check |
| "Do you offer FOB or EXW?" | Incoterms |

---

## UI Features

- **Mobile-first** — max-width 520px, centered on desktop, full-width on mobile
- **WhatsApp dark green header** — `#075e54` with avatar, name, status
- **Customer bubbles** — white, left-aligned, rounded top-right corners
- **AI bubbles** — `#dcf8c6` green, right-aligned, rounded top-left corners
- **Typing indicator** — animated bouncing dots while AI processes
- **Confidence badge** — 🟢 HIGH / 🟡 MEDIUM / 🔴 LOW per AI bubble
- **KB badge** — KB ✓ or No KB per AI bubble
- **Source badge** — AI provider name per AI bubble
- **Conflict warning** — shown below chat if KB conflict detected
- **Simulate button** — inject fake customer messages from dropdown
- **Clear chat** — reset conversation history

---

## How to Use

1. Start the Streamlit app:
   ```bash
   cd buildway-ai-core
   streamlit run apps/streamlit_demo/app.py
   ```

2. Navigate to **AI Model Setup** → configure and test connection

3. (Optional) Navigate to **Knowledge Base** → upload KB documents

4. Navigate to **WhatsApp CRM Demo** in the sidebar

5. Use the **Simulate** button or type a message to start chatting

---

## Strictly Excluded

- ❌ WhatsApp Business API
- ❌ Meta Webhook
- ❌ WebSocket / realtime sync
- ❌ Login / authentication
- ❌ Database writes
- ❌ External HTTP calls (beyond AI provider API)

---

## Next Steps (Phase 0.6+)

- Real WhatsApp Business API integration (webhook receiver)
- Multi-tenant conversation history
- Human takeover toggle
- Message queue / async processing
- Read receipts and delivery status
