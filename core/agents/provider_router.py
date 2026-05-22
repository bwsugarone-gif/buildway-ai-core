"""
core.agents.provider_router
---------------------------
Provider routing and connection checks for Buildway AI Core.

Phase 0.4C supports real OpenAI and OpenAI-compatible connection tests. Other
providers keep their config surface but intentionally return a not-supported
status until their SDK integrations are implemented.
"""

from dataclasses import dataclass
import json
import re
from urllib import error, request


PROVIDER_OPENAI = "OpenAI"
PROVIDER_CLAUDE = "Claude"
PROVIDER_GEMINI = "Gemini"
PROVIDER_DEEPSEEK = "DeepSeek"
PROVIDER_OPENAI_COMPATIBLE = "OpenAI-Compatible"

SUPPORTED_PROVIDERS = [
    PROVIDER_OPENAI,
    PROVIDER_OPENAI_COMPATIBLE,
    PROVIDER_CLAUDE,
    PROVIDER_GEMINI,
    PROVIDER_DEEPSEEK,
]
AVAILABLE_PROVIDERS = [PROVIDER_OPENAI, PROVIDER_OPENAI_COMPATIBLE]
COMING_SOON_PROVIDERS = [PROVIDER_CLAUDE, PROVIDER_GEMINI, PROVIDER_DEEPSEEK]

STATUS_NOT_CONFIGURED = "Not configured"
STATUS_CONFIGURED = "Configured"
STATUS_CONNECTED = "Connected"
STATUS_FAILED = "Failed"
STATUS_INVALID_KEY = "Invalid Key"
STATUS_TIMEOUT = "Timeout"
STATUS_NOT_SUPPORTED = "Not supported yet"
STATUS_COMING_SOON = "Coming Soon"

PROVIDER_MODELS = {
    PROVIDER_OPENAI: [
        "gpt-5.5",
        "gpt-5.4",
        "gpt-5.3",
        "gpt-5.3-instant",
        "gpt-4.1",
        "gpt-4.1-mini",
        "gpt-4o",
        "gpt-4o-mini",
        "custom",
    ],
    PROVIDER_CLAUDE: [
        "claude-opus-4.7",
        "claude-opus-4.6",
        "claude-sonnet-4.6",
        "claude-opus-4.5",
        "claude-sonnet-4.5",
        "claude-haiku-4.5",
        "custom",
    ],
    PROVIDER_GEMINI: [
        "gemini-3-pro-preview",
        "gemini-3.5-flash",
        "gemini-2.5-pro",
        "gemini-2.5-flash",
        "custom",
    ],
    PROVIDER_DEEPSEEK: [
        "deepseek-v4-flash",
        "deepseek-v4-pro",
        "custom",
    ],
    PROVIDER_OPENAI_COMPATIBLE: ["custom"],
}

PROVIDER_KEY_LABELS = {
    PROVIDER_OPENAI: "API Key",
    PROVIDER_CLAUDE: "Anthropic API Key",
    PROVIDER_GEMINI: "Google AI API Key",
    PROVIDER_DEEPSEEK: "API Key",
    PROVIDER_OPENAI_COMPATIBLE: "API Key",
}

PROVIDER_KEY_PLACEHOLDERS = {
    PROVIDER_OPENAI: "sk-... (session only, never stored)",
    PROVIDER_CLAUDE: "sk-ant-... (session only, never stored)",
    PROVIDER_GEMINI: "AIza... (session only, never stored)",
    PROVIDER_DEEPSEEK: "sk-... (session only, never stored)",
    PROVIDER_OPENAI_COMPATIBLE: "Provider API key (session only, never stored)",
}

COMING_SOON_MESSAGE = "This provider is listed for future support and cannot be used in CRM yet."
CRM_PROVIDER_UNAVAILABLE_MESSAGE = (
    "This provider is not available in this demo. Please use OpenAI or OpenAI-Compatible."
)
CONNECTION_REQUIRED_MESSAGE = "AI Provider is not connected. Please run Test Connection first."


@dataclass
class AIProviderConfig:
    provider: str
    model: str
    api_key: str = ""
    base_url: str = ""
    connection_status: str = STATUS_NOT_CONFIGURED

    @property
    def configured(self) -> bool:
        if not self.api_key:
            return False
        if self.provider == PROVIDER_OPENAI_COMPATIBLE and not self.base_url:
            return False
        return bool(self.model)


@dataclass
class ConnectionResult:
    status: str
    message: str


@dataclass
class AIRequestDebug:
    function_name: str
    method: str
    final_endpoint: str
    provider: str
    model: str
    base_url: str


@dataclass
class AIReplyResult:
    content: str
    debug: AIRequestDebug


class OpenAICompatibleRequestError(RuntimeError):
    def __init__(self, result: ConnectionResult):
        super().__init__(result.message)
        self.result = result


def get_default_model(provider: str) -> str:
    return PROVIDER_MODELS.get(provider, ["custom"])[0]


def provider_requires_base_url(provider: str) -> bool:
    return provider == PROVIDER_OPENAI_COMPATIBLE


def normalize_openai_compatible_base_url(base_url: str) -> str:
    normalized = base_url.strip().rstrip("/")
    if normalized.endswith("/v1"):
        return normalized
    return f"{normalized}/v1"


def build_ai_request_debug(provider: str, model: str, base_url: str = "") -> AIRequestDebug:
    if provider == PROVIDER_OPENAI_COMPATIBLE:
        normalized_base_url = normalize_openai_compatible_base_url(base_url)
        final_endpoint = f"{normalized_base_url}/chat/completions"
        debug_base_url = normalized_base_url
    else:
        final_endpoint = "OpenAI SDK chat.completions.create"
        debug_base_url = ""
    return AIRequestDebug(
        function_name="call_ai_reply",
        method="POST",
        final_endpoint=final_endpoint,
        provider=provider,
        model=model,
        base_url=debug_base_url,
    )


def is_provider_integrated(provider: str) -> bool:
    return provider in {PROVIDER_OPENAI, PROVIDER_OPENAI_COMPATIBLE}


def is_provider_available(provider: str) -> bool:
    return provider in AVAILABLE_PROVIDERS


def resolve_model(model: str, custom_model: str = "") -> str:
    if model == "custom":
        return custom_model.strip()
    return model.strip()


def mask_sensitive_text(text: str) -> str:
    if not text:
        return text
    masked = re.sub(r"(sk-[A-Za-z0-9_\-]{4})[A-Za-z0-9_\-]+", r"\1...", text)
    masked = re.sub(r"(sk-ant-[A-Za-z0-9_\-]{4})[A-Za-z0-9_\-]+", r"\1...", masked)
    masked = re.sub(r"(AIza[A-Za-z0-9_\-]{4})[A-Za-z0-9_\-]+", r"\1...", masked)
    return masked


def classify_error(exc: Exception) -> ConnectionResult:
    raw = mask_sensitive_text(str(exc))
    err = raw.lower()
    exc_name = exc.__class__.__name__.lower()
    if "auth" in err or "api_key" in err or "api key" in err or "401" in err:
        return ConnectionResult(STATUS_INVALID_KEY, f"Invalid API key: {raw}")
    if "timeout" in err or "timed out" in err or "timeout" in exc_name:
        return ConnectionResult(STATUS_TIMEOUT, f"Timeout: {raw}")
    return ConnectionResult(STATUS_FAILED, f"Connection failed: {raw}")


def _classify_openai_compatible_error(exc: Exception, endpoint: str) -> ConnectionResult:
    post_endpoint = f"POST {endpoint}"
    if isinstance(exc, TimeoutError):
        return ConnectionResult(STATUS_TIMEOUT, f"Timeout calling {post_endpoint}")
    if isinstance(exc, error.HTTPError):
        body = mask_sensitive_text(exc.read().decode("utf-8", errors="replace"))
        if exc.code in {401, 403}:
            return ConnectionResult(STATUS_INVALID_KEY, f"Invalid API key calling {post_endpoint}: {body}")
        return ConnectionResult(
            STATUS_FAILED,
            f"Connection failed calling {post_endpoint}: HTTP {exc.code} {body}",
        )
    message = mask_sensitive_text(str(exc))
    err = message.lower()
    if "timeout" in err or "timed out" in err:
        return ConnectionResult(STATUS_TIMEOUT, f"Timeout calling {post_endpoint}: {message}")
    if "auth" in err or "api key" in err or "api_key" in err or "401" in err:
        return ConnectionResult(STATUS_INVALID_KEY, f"Invalid API key calling {post_endpoint}: {message}")
    return ConnectionResult(STATUS_FAILED, f"Connection failed calling {post_endpoint}: {message}")


def call_openai_compatible_chat(
    *,
    base_url: str,
    api_key: str,
    model: str,
    messages: list[dict[str, str]],
    temperature: float,
    max_tokens: int | None = None,
) -> AIReplyResult:
    debug = build_ai_request_debug(PROVIDER_OPENAI_COMPATIBLE, model, base_url)
    normalized_base_url = normalize_openai_compatible_base_url(base_url)
    endpoint = f"{normalized_base_url}/chat/completions"
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }
    if max_tokens is not None:
        payload["max_tokens"] = max_tokens

    req = request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=30) as response:
            raw_body = response.read().decode("utf-8")
    except Exception as exc:
        raise OpenAICompatibleRequestError(
            _classify_openai_compatible_error(exc, endpoint)
        ) from exc

    parsed = json.loads(raw_body)
    choices = parsed.get("choices", [])
    if not choices:
        return AIReplyResult("", debug)
    message = choices[0].get("message", {})
    return AIReplyResult(message.get("content", "") or "", debug)


def validate_config(config: AIProviderConfig) -> ConnectionResult | None:
    if not config.api_key:
        return ConnectionResult(STATUS_NOT_CONFIGURED, "Missing API key")
    if provider_requires_base_url(config.provider) and not config.base_url:
        return ConnectionResult(STATUS_NOT_CONFIGURED, "Missing Base URL")
    if not config.model:
        return ConnectionResult(STATUS_NOT_CONFIGURED, "Missing Model Name")
    return None


def call_ai_reply(
    *,
    provider: str,
    message: str,
    api_key: str,
    model: str,
    base_url: str = "",
    system_prompt: str = "",
    test_mode: bool = False,
) -> AIReplyResult:
    if not is_provider_available(provider):
        raise NotImplementedError(CRM_PROVIDER_UNAVAILABLE_MESSAGE)
    if provider == PROVIDER_OPENAI_COMPATIBLE:
        return call_openai_compatible_chat(
            base_url=base_url,
            api_key=api_key,
            model=model,
            messages=[
                *([{"role": "system", "content": system_prompt}] if system_prompt and not test_mode else []),
                {"role": "user", "content": message},
            ],
            temperature=0 if test_mode else 0.7,
            max_tokens=8 if test_mode else None,
        )

    from openai import OpenAI

    client_kwargs = {"api_key": api_key, "timeout": 30}
    client = OpenAI(**client_kwargs)
    request_kwargs = {
        "model": model,
        "messages": [
            *([{"role": "system", "content": system_prompt}] if system_prompt and not test_mode else []),
            {"role": "user", "content": message},
        ],
        "temperature": 0 if test_mode else 0.7,
        "presence_penalty": 0 if test_mode else 0.2,
    }
    if test_mode:
        request_kwargs["max_tokens"] = 8
    response = client.chat.completions.create(**request_kwargs)
    return AIReplyResult(
        response.choices[0].message.content or "",
        build_ai_request_debug(provider, model, base_url),
    )


def generate_reply(config: AIProviderConfig, system_prompt: str, user_message: str) -> str:
    if not is_provider_available(config.provider):
        raise NotImplementedError(CRM_PROVIDER_UNAVAILABLE_MESSAGE)
    if config.connection_status != STATUS_CONNECTED:
        raise RuntimeError(CONNECTION_REQUIRED_MESSAGE)
    return call_ai_reply(
        provider=config.provider,
        message=user_message,
        api_key=config.api_key,
        model=config.model,
        base_url=config.base_url,
        system_prompt=system_prompt,
    ).content
