# Buildway AI Core — Roadmap

## Phase 1 (Current) — Architecture Foundation

- [x] Core module extraction from HK-AICOS
- [x] Generic agent routing framework
- [x] Session memory (JSON)
- [x] RAG lite (local JSON index)
- [x] OCR engine (Tesseract)
- [x] Document processing (PDF, DOCX, XLSX)
- [x] Evidence confidence scoring
- [x] Conflict resolver
- [x] Action manager
- [x] PDF report generator
- [x] Progress tracker
- [x] Repeated issue detector
- [x] Construction vertical (agent definitions)
- [x] CRM vertical (placeholder)
- [x] Document AI vertical (placeholder)
- [x] Streamlit demo app

## Phase 2 — Production Hardening

- [ ] REST API server (FastAPI)
- [ ] Security layer (API key auth, rate limiting, input sanitisation)
- [ ] Vector embeddings for RAG (replace keyword search)
- [ ] Multi-tenant support
- [ ] Audit logging
- [ ] CRM vertical — full implementation
- [ ] Document AI vertical — full implementation

## Phase 3 — SaaS Preparation

- [ ] User authentication (OAuth2 / JWT)
- [ ] Cloud storage integration (S3 / GCS)
- [ ] Webhook support
- [ ] Dashboard UI
- [ ] Usage analytics
- [ ] Multi-language support (beyond CJK)

## Vertical Roadmap

| Vertical | Phase 1 | Phase 2 | Phase 3 |
|---|---|---|---|
| Construction | ✅ Active | Enhance | SaaS |
| CRM | 🔲 Placeholder | Build | SaaS |
| Document AI | 🔲 Placeholder | Build | SaaS |
| Legal | — | Plan | Build |
| Finance | — | Plan | Build |
