from streamlit.testing.v1 import AppTest


def test_ai_setup_dynamic_provider_ui_and_crm_placeholder():
    at = AppTest.from_file("apps/streamlit_demo/app.py")
    at.run(timeout=10)

    at.selectbox[0].set_value("English")
    at.run(timeout=10)
    at.radio[0].set_value("AI Model Setup")
    at.run(timeout=10)

    assert at.exception == []
    assert at.selectbox[0].options == [
        "OpenAI",
        "Claude",
        "Gemini",
        "DeepSeek",
        "OpenAI-Compatible",
    ]

    at.selectbox[0].set_value("OpenAI-Compatible")
    at.run(timeout=10)

    assert [field.label for field in at.text_input] == [
        "Custom Model Name",
        "Base URL",
        "API Key",
    ]

    at.selectbox[0].set_value("Claude")
    at.run(timeout=10)
    at.text_input[0].set_value("test-key")
    at.button[0].click()
    at.run(timeout=10)

    assert ("AI Provider", "Claude") in [(metric.label, metric.value) for metric in at.metric]
    assert ("Connection Status", "Configured") in [
        (metric.label, metric.value) for metric in at.metric
    ]

    at.radio[0].set_value("CRM Demo")
    at.run(timeout=10)

    assert ("Provider", "Claude") in [(metric.label, metric.value) for metric in at.metric]
    assert ("Connection Status", "Configured") in [
        (metric.label, metric.value) for metric in at.metric
    ]
    assert at.button[0].disabled is True


def test_provider_switch_resets_active_config():
    at = AppTest.from_file("apps/streamlit_demo/app.py")
    at.run(timeout=10)

    at.selectbox[0].set_value("English")
    at.run(timeout=10)
    at.radio[0].set_value("AI Model Setup")
    at.run(timeout=10)

    at.text_input[0].set_value("test-openai-key")
    at.button[0].click()
    at.run(timeout=10)

    assert ("Connection Status", "Configured") in [
        (metric.label, metric.value) for metric in at.metric
    ]

    at.selectbox[0].set_value("Gemini")
    at.run(timeout=10)

    assert ("AI Provider", "Gemini") in [(metric.label, metric.value) for metric in at.metric]
    assert ("Connection Status", "Not configured") in [
        (metric.label, metric.value) for metric in at.metric
    ]
    assert ("Model Name", "gemini-3-pro-preview") in [
        (metric.label, metric.value) for metric in at.metric
    ]

    at.selectbox[0].set_value("OpenAI")
    at.run(timeout=10)

    assert ("Connection Status", "Not configured") in [
        (metric.label, metric.value) for metric in at.metric
    ]
    assert at.text_input[0].value == ""
