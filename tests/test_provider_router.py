from core.ai.provider_router import (
    AIProviderConfig,
    COMING_SOON_MESSAGE,
    PROVIDER_CLAUDE,
    PROVIDER_GEMINI,
    PROVIDER_OPENAI,
    PROVIDER_OPENAI_COMPATIBLE,
    SUPPORTED_PROVIDERS,
    generate_reply,
    is_provider_integrated,
    provider_requires_base_url,
)


def test_supported_provider_architecture():
    assert SUPPORTED_PROVIDERS == [
        "OpenAI",
        "Claude",
        "Gemini",
        "DeepSeek",
        "OpenAI-Compatible",
    ]
    assert is_provider_integrated(PROVIDER_OPENAI) is True
    assert is_provider_integrated(PROVIDER_CLAUDE) is False
    assert is_provider_integrated(PROVIDER_GEMINI) is False
    assert provider_requires_base_url(PROVIDER_OPENAI_COMPATIBLE) is True


def test_openai_compatible_requires_base_url_to_be_configured():
    missing_base_url = AIProviderConfig(
        provider=PROVIDER_OPENAI_COMPATIBLE,
        model="custom-model",
        api_key="test-key",
        base_url="",
    )
    configured = AIProviderConfig(
        provider=PROVIDER_OPENAI_COMPATIBLE,
        model="custom-model",
        api_key="test-key",
        base_url="https://api.example.com/v1",
    )

    assert missing_base_url.configured is False
    assert configured.configured is True


def test_non_openai_generation_returns_coming_soon_without_sdk_call():
    config = AIProviderConfig(
        provider=PROVIDER_CLAUDE,
        model="claude-3-5-haiku-20241022",
        api_key="test-key",
    )

    try:
        generate_reply(config, "system", "hello")
    except NotImplementedError as exc:
        assert str(exc) == COMING_SOON_MESSAGE
    else:
        raise AssertionError("Expected non-OpenAI provider to be blocked")

