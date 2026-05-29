from pathlib import Path

from core.memory.customer_memory import list_customer_history, save_customer_interaction
from core.memory.tenant_memory import load_tenant_profile, save_tenant_profile


def test_tenant_profile_save_load(tmp_path: Path):
    profile_path = tmp_path / "demo_tenant.json"

    saved = save_tenant_profile(
        {
            "tenant_id": "demo_tenant",
            "company_name": "Buildway Demo",
            "industry": "CRM",
            "human_review_threshold": 0.7,
        },
        path=profile_path,
    )
    loaded = load_tenant_profile(path=profile_path)

    assert saved["company_name"] == "Buildway Demo"
    assert loaded["tenant_id"] == "demo_tenant"
    assert loaded["human_review_threshold"] == 0.7


def test_crm_generate_memory_write(tmp_path: Path):
    record = save_customer_interaction(
        tenant_id="demo_tenant",
        customer_ref="CUST-001",
        customer_message="What is the MOQ?",
        ai_reply="Please confirm the product model first.",
        confidence="LOW",
        kb_used=False,
        provider="OpenAI",
        base_dir=tmp_path,
    )

    history = list_customer_history("demo_tenant", "CUST-001", base_dir=tmp_path)

    assert record["interaction_id"].startswith("INT-")
    assert len(history) == 1
    assert history[0]["customer_message"] == "What is the MOQ?"
    assert history[0]["provider"] == "OpenAI"
