from core.channels.whatsapp_adapter import (
    build_reply_payload,
    parse_incoming_message,
    send_reply,
)


def test_whatsapp_adapter_placeholder_flow():
    incoming = parse_incoming_message(
        {
            "provider": "Meta Cloud API",
            "id": "wamid-1",
            "from": "+85212345678",
            "message": {"body": "What is the MOQ?"},
        }
    )

    assert incoming["channel"] == "whatsapp"
    assert incoming["customer_ref"] == "+85212345678"
    assert incoming["customer_message"] == "What is the MOQ?"

    reply_payload = build_reply_payload(
        {
            "tenant_id": "demo_tenant",
            "customer_ref": incoming["customer_ref"],
            "draft_reply": "Please confirm the product model.",
        }
    )

    result = send_reply(reply_payload)
    assert result["sent"] is False
    assert result["status"] == "placeholder_only"
