# Client Onboarding Guide

This guide covers what a new tenant needs to prepare before going live on Buildway AI Core.

---

## What the Client Needs to Prepare

### 1. WhatsApp Business API
- A verified WhatsApp Business account
- Access to the WhatsApp Business API (via Meta or an approved BSP)
- Phone number registered and approved for messaging
- Webhook URL will be provided by Buildway after tenant setup

### 2. AI API Key
- **OpenAI** — API key from https://platform.openai.com
- **Anthropic (Claude)** — API key from https://console.anthropic.com
- At least one provider is required. Both can be configured for fallback.
- The client is responsible for billing on their own API account.

### 3. FAQ Document
- A list of common customer questions and standard answers
- Format: plain text, Word, or PDF
- Used to build the tenant's RAG knowledge base
- Minimum recommended: 20–50 Q&A pairs

### 4. Product Catalog
- Full product or service listing
- Include: product name, description, SKU/code, price range
- Format: Excel, CSV, or PDF
- Used for AI product lookup and recommendation

### 5. MOQ / Shipping / Payment Terms
- Minimum order quantities per product (if applicable)
- Shipping zones, lead times, and courier options
- Accepted payment methods and terms (e.g., T/T 30 days, PayPal)
- This information is loaded into the knowledge base for AI reference

### 6. Reply Templates
- Standard reply templates for common scenarios:
  - Order confirmation
  - Shipping update
  - Out-of-stock notice
  - Escalation to human agent
  - After-hours auto-reply
- Format: plain text or Word document
- Templates are used in Phase 1 (AI Assist) and Phase 2 (Auto Mode)

---

## Onboarding Steps

1. **Tenant Registration** — Buildway creates the tenant account and provides login credentials
2. **API Key Setup** — Client submits WhatsApp API and AI API keys via the admin portal (encrypted at rest)
3. **Knowledge Base Upload** — Client uploads FAQ, product catalog, and terms documents
4. **Template Configuration** — Reply templates are loaded and reviewed
5. **Test Run** — Buildway runs a test conversation to verify AI responses
6. **Go Live** — WhatsApp webhook is activated; AI Assist Mode is enabled

---

## Phase 1 Go-Live Checklist

- [ ] WhatsApp Business API credentials submitted
- [ ] AI API key submitted (OpenAI or Anthropic)
- [ ] FAQ document uploaded (min. 20 Q&A)
- [ ] Product catalog uploaded
- [ ] MOQ / shipping / payment terms provided
- [ ] Reply templates provided (min. 5 scenarios)
- [ ] Test conversation completed and approved
- [ ] Staff trained on AI Assist dashboard

---

## Support

For onboarding support, contact your Buildway account manager.
