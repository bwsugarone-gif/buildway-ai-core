from pathlib import Path


APP_PATH = Path(__file__).resolve().parents[1] / "apps" / "streamlit_demo" / "app.py"


def test_crm_blocks_without_api_key_and_has_no_template_fallback():
    source = APP_PATH.read_text(encoding="utf-8")

    assert "No AI model configured. Please complete AI Model Setup first." in source
    assert "_generate_template_reply" not in source
    assert "Template (no API key)" not in source
    assert "Template reply will be used as fallback." not in source


def test_crm_uses_openai_api_source_and_persists_configured_status():
    source = APP_PATH.read_text(encoding="utf-8")

    assert 'st.session_state["ai_provider"] = provider' in source
    assert 'st.session_state["ai_model"] = model_name' in source
    assert 'st.session_state["ai_api_key"] = api_key_input' in source
    assert 'st.session_state["ai_configured"] = True' in source
    assert 'st.session_state["crm_reply_source"] = "OpenAI API"' in source
