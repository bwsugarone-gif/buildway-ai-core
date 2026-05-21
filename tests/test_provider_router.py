import sys
import types
from io import BytesIO
from urllib import error

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
    normalize_openai_compatible_base_url,
    provider_requires_base_url,
    request,
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


class _FakeHTTPResponse:
    def __init__(self, body=b'{"choices":[{"message":{"content":"OK"}}]}'):
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self):
        return self.body


def _install_fake_urlopen(status_body=b'{"choices":[{"message":{"content":"OK"}}]}'):
    calls = []
    original_urlopen = request.urlopen

    def fake_urlopen(req, timeout):
        calls.append(
            {
                "url": req.full_url,
                "method": req.get_method(),
                "headers": dict(req.header_items()),
                "body": req.data.decode("utf-8"),
                "timeout": timeout,
            }
        )
        return _FakeHTTPResponse(status_body)

    request.urlopen = fake_urlopen
    return calls, original_urlopen


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


def test_openai_compatible_base_url_normalization():
    assert (
        normalize_openai_compatible_base_url(" http://pro.mmw.ink/v1 ")
        == "http://pro.mmw.ink/v1"
    )
    assert (
        normalize_openai_compatible_base_url("http://pro.mmw.ink/v1/")
        == "http://pro.mmw.ink/v1"
    )
    assert (
        normalize_openai_compatible_base_url("http://pro.mmw.ink")
        == "http://pro.mmw.ink/v1"
    )
    assert (
        normalize_openai_compatible_base_url("https://host/api/v1/")
        == "https://host/api/v1"
    )


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
    calls, original_urlopen = _install_fake_urlopen()
    config = AIProviderConfig(
        provider=PROVIDER_OPENAI_COMPATIBLE,
        model="custom-openai-compatible-model",
        api_key="test-key",
        base_url="https://api.example.com/v1",
        connection_status=STATUS_CONFIGURED,
    )

    try:
        result = test_connection(config)
    finally:
        request.urlopen = original_urlopen

    assert result.status == STATUS_CONNECTED
    assert calls[-1]["url"] == "https://api.example.com/v1/chat/completions"
    assert calls[-1]["method"] == "POST"
    assert '"model": "custom-openai-compatible-model"' in calls[-1]["body"]


def test_openai_compatible_test_connection_appends_v1_and_posts():
    calls, original_urlopen = _install_fake_urlopen()
    config = AIProviderConfig(
        provider=PROVIDER_OPENAI_COMPATIBLE,
        model="custom-openai-compatible-model",
        api_key="test-key",
        base_url="http://pro.mmw.ink",
        connection_status=STATUS_CONFIGURED,
    )

    try:
        result = test_connection(config)
    finally:
        request.urlopen = original_urlopen

    assert result.status == STATUS_CONNECTED
    assert calls[-1]["url"] == "http://pro.mmw.ink/v1/chat/completions"
    assert calls[-1]["method"] == "POST"


def test_openai_compatible_generate_uses_same_normalized_post_path():
    calls, original_urlopen = _install_fake_urlopen(
        b'{"choices":[{"message":{"content":"Draft reply"}}]}'
    )
    config = AIProviderConfig(
        provider=PROVIDER_OPENAI_COMPATIBLE,
        model="custom-openai-compatible-model",
        api_key="test-key",
        base_url="http://pro.mmw.ink/v1/",
        connection_status=STATUS_CONNECTED,
    )

    try:
        reply = generate_reply(config, "system", "customer message")
    finally:
        request.urlopen = original_urlopen

    assert reply == "Draft reply"
    assert calls[-1]["url"] == "http://pro.mmw.ink/v1/chat/completions"
    assert calls[-1]["method"] == "POST"


def test_openai_compatible_invalid_key_error_masks_key_and_shows_endpoint():
    original_urlopen = request.urlopen

    def fake_urlopen(req, timeout):
        raise error.HTTPError(
            req.full_url,
            401,
            "Unauthorized sk-test-secret-key",
            {},
            BytesIO(b'{"error":"bad key sk-test-secret-key"}'),
        )

    request.urlopen = fake_urlopen
    config = AIProviderConfig(
        provider=PROVIDER_OPENAI_COMPATIBLE,
        model="custom-openai-compatible-model",
        api_key="sk-test-secret-key",
        base_url="http://pro.mmw.ink",
        connection_status=STATUS_CONFIGURED,
    )

    try:
        result = test_connection(config)
    finally:
        request.urlopen = original_urlopen

    assert result.status == "Invalid Key"
    assert "http://pro.mmw.ink/v1/chat/completions" in result.message
    assert "sk-test-secret-key" not in result.message
