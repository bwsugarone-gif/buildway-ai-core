from pathlib import Path

from core.approval.queue import enqueue_approval_item, list_approval_queue, needs_human_review


def test_low_confidence_enters_approval_queue(tmp_path: Path):
    needs_review, reasons = needs_human_review(
        customer_message="What is the price?",
        confidence="LOW",
        kb_used=False,
        conflict_warning=None,
    )

    assert needs_review is True
    assert "Confidence LOW" in reasons
    assert "out-of-KB" in reasons
    assert "price missing" in reasons

    item = enqueue_approval_item(
        tenant_id="demo_tenant",
        customer_ref="CUST-001",
        customer_message="What is the price?",
        draft_reply="Please confirm the product model.",
        confidence="LOW",
        reason=reasons,
        provider="OpenAI",
        queue_dir=tmp_path,
    )

    queue = list_approval_queue(queue_dir=tmp_path)
    assert item["status"] == "Needs Human Review"
    assert len(queue) == 1
    assert queue[0]["customer_message"] == "What is the price?"
