# WhatsApp API Integration Plan

Phase 0.9 只建立 webhook-ready 架構，不連接真 WhatsApp API，不發送任何真訊息。

## Current Placeholder

- Adapter: `core/channels/whatsapp_adapter.py`
- `parse_incoming_message(payload)`：把 webhook payload normalize 成 CRM 可用格式。
- `build_reply_payload(message)`：建立 provider-neutral 的文字回覆 payload。
- `send_reply(payload)`：placeholder，不會呼叫外部 API。

## Future Providers

| Provider | Future Use | Notes |
|---|---|---|
| YCloud | WhatsApp Business API gateway | 適合快速接入與多渠道管理 |
| Twilio | WhatsApp messaging API | 適合已有 Twilio 帳戶客戶 |
| 360dialog | WhatsApp Business API partner | 適合專注 WhatsApp BSP 的部署 |
| Meta Cloud API | 官方直連 | 需要 Meta App、Webhook、Phone Number ID、Token 管理 |

## Future Flow

1. Provider webhook receives WhatsApp message.
2. Buildway endpoint validates signature/token.
3. Adapter parses message into tenant-aware CRM format.
4. CRM RAG + AI generates draft reply.
5. Human approval queue checks low confidence, conflicts, out-of-KB, price/shipping missing.
6. Approved reply is sent through selected provider adapter.
7. Interaction is stored in persistent customer memory.

## Safety Rules

- 不在 Phase 0.9 儲存真 WhatsApp token。
- 不在 Phase 0.9 發送真 WhatsApp message。
- 不繞過 Human Approval Queue。
- 不改現有 WhatsApp demo flow。
