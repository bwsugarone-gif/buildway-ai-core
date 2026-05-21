import sys
import types

from core.ai.provider_router import (
    AIProviderConfig,
    COMING_SOON_MESSAGE,
    CONNECTION_REQUIRED_MESSAGE,
    CRM_PROVIDER_UNAVAILABLE_MESSAGE,
    PROVIDER_CLAUDE,
    PROVIDER_GEMINI,
    PROVIDER_OPENAI,
    PROVIDER_OPENAI_COMPATIBLE,
    STATUS_CONFIGURED,
    STATUS_COMING_SOON,
    STATUS_CONNECTED,
    STATUS_NOT_CONFIGURED,
    STATUS_NOT_SUPPORTED,
    SUPPORTED_PROVIDERS,
    generate_reply,
    is_provider_integrated,
    provider_requires_base_url,
    test_connection,
)


class _FakeMessage:
    content = "OK"


class _FakeChoice:
    message = _FakeMessage()


class _FakeResponse:
    choices = [_FakeChoice()]


class _FakeCompletions:
    def create(self, **kwargs):
        return _FakeResponse()


class _FakeChat:
    completions = _FakeCompletions()


class _FakeOpenAI:
    calls = []

    def __init__(self, **kwargs):
        self.__class__.calls.append(kwargs)
        self.chat = _FakeChat()


def _install_fake_openai():
    fake_openai = types.SimpleNamespace(OpenAI=_FakeOpenAI)
    sys.modules["openai"] = fake_openai
    _FakeOpenAI.calls = []


def test_supported_provider_architecture():
    assert SUPPORTED_PROVIDERS == [
        "OpenAI",
        "OpenAI-Compatible",
        "Claude",
        "Gemini",
        "DeepSeek",
    ]
    assert is_provider_integrated(PROVIDER_OPENAI) is True
    assert is_provider_integrated(PROVIDER_CLAUDE) is False
    assert is_provider_integrated(PROVIDER_GEMINI) is False
    assert provider_requires_base_url(PROVIDER_OPENAI_COMPATIBLE) is True


def test_openai_compatible_requires_base_url_to_be_configured():
    missing_base_url = AIProviderConfig(
        provider=PROVIDER_OPENAI_COMPATIBLE,
        model="custom-openai-compatible-model",
        api_key="test-key",
        base_url="",
    )
    configured = AIProviderConfig(
        provider=PROVIDER_OPENAI_COMPATIBLE,
        model="custom-openai-compatible-model",
        api_key="test-key",
        base_url="https://api.example.com/v1",
    )

    assert missing_base_url.configured is False
    assert configured.configured is True


def test_non_openai_connection_returns_coming_soon_without_sdk_call():
    config = AIProviderConfig(
        provider=PROVIDER_CLAUDE,
        model="claude-haiku-4.5",
        api_key="test-key",
        connection_status=STATUS_CONFIGURED,
    )

    result = test_connection(config)

    assert result.status == STATUS_COMING_SOON
    assert result.message == COMING_SOON_MESSAGE


def test_non_openai_generation_returns_demo_unavailable_message():
    config = AIProviderConfig(
        provider=PROVIDER_CLAUDE,
        model="claude-haiku-4.5",
        api_key="test-key",
        connection_status=STATUS_COMING_SOON,
    )

    try:
        generate_reply(config, "system", "hello")
    except NotImplementedError as exc:
        assert str(exc) == CRM_PROVIDER_UNAVAILABLE_MESSAGE
    else:
        raise AssertionError("Expected coming-soon provider to be unavailable")


def test_generation_requires_connected_status():
    config = AIProviderConfig(
        provider=PROVIDER_OPENAI,
        model="gpt-4o-mini",
        api_key="test-key",
        connection_status=STATUS_CONFIGURED,
    )

    try:
        generate_reply(config, "system", "hello")
    except RuntimeError as exc:
        assert str(exc) == CONNECTION_REQUIRED_MESSAGE
    else:
        raise AssertionError("Expected generation to require Connected status")


def test_missing_openai_compatible_base_url_is_friendly_error():
    config = AIProviderConfig(
        provider=PROVIDER_OPENAI_COMPATIBLE,
        model="custom-openai-compatible-model",
        api_key="test-key",
        base_url="",
        connection_status=STATUS_CONFIGURED,
    )

    result = test_connection(config)

    assert result.status == STATUS_NOT_CONFIGURED
    assert result.message == "Missing Base URL"


def test_openai_test_connection_success_uses_real_route():
    _install_fake_openai()
    config = AIProviderConfig(
        provider=PROVIDER_OPENAI,
        model="gpt-4o-mini",
        api_key="test-key",
        connection_status=STATUS_CONFIGURED,
    )

    result = test_connection(config)

    assert result.status == STATUS_CONNECTED
    assert _FakeOpenAI.calls[-1] == {"api_key": "test-key", "timeout": 30}


def test_openai_compatible_test_connection_success_uses_base_url():
    _install_fake_openai()
    config = AIProviderConfig(
        provider=PROVIDER_OPENAI_COMPATIBLE,
        model="custom-openai-compatible-model",
        api_key="test-key",
        base_url="https://api.example.com/v1",
        connection_status=STATUS_CONFIGURED,
    )

    result = test_connection(config)

    assert result.status == STATUS_CONNECTED
    assert _FakeOpenAI.calls[-1] == {
        "api_key": "test-key",
        "timeout": 30,
        "base_url": "https://api.example.com/v1",
    }
