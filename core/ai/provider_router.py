"""
core.ai.provider_router
-----------------------
Provider routing foundation for Buildway AI Core.

Phase 0.4B.1 intentionally executes only the native OpenAI route. Other
providers are represented in config so the UI and workflow can evolve without
adding SDK dependencies before their integration phase.
"""

from dataclasses import dataclass


PROVIDER_OPENAI = "OpenAI"
PROVIDER_CLAUDE = "Claude"
PROVIDER_GEMINI = "Gemini"
PROVIDER_DEEPSEEK = "DeepSeek"
PROVIDER_OPENAI_COMPATIBLE = "OpenAI-Compatible"

SUPPORTED_PROVIDERS = [
    PROVIDER_OPENAI,
    PROVIDER_CLAUDE,
    PROVIDER_GEMINI,
    PROVIDER_DEEPSEEK,
    PROVIDER_OPENAI_COMPATIBLE,
]

PROVIDER_MODELS = {
    PROVIDER_OPENAI: ["gpt-4o-mini", "gpt-4.1-mini"],
    PROVIDER_CLAUDE: ["claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022"],
    PROVIDER_GEMINI: ["gemini-1.5-flash", "gemini-1.5-pro"],
    PROVIDER_DEEPSEEK: ["deepseek-chat", "deepseek-reasoner"],
    PROVIDER_OPENAI_COMPATIBLE: ["gpt-4o-mini", "custom-model"],
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

COMING_SOON_MESSAGE = "Provider integration coming in next phase."


@dataclass
class AIProviderConfig:
    provider: str
    model: str
    api_key: str = ""
    base_url: str = ""

    @property
    def configured(self) -> bool:
        if self.provider == PROVIDER_OPENAI_COMPATIBLE:
            return bool(self.api_key and self.base_url)
        return bool(self.api_key)


def get_default_model(provider: str) -> str:
    return PROVIDER_MODELS.get(provider, [""])[0]


def provider_requires_base_url(provider: str) -> bool:
    return provider == PROVIDER_OPENAI_COMPATIBLE


def is_provider_integrated(provider: str) -> bool:
    return provider == PROVIDER_OPENAI


def generate_reply(config: AIProviderConfig, system_prompt: str, user_message: str) -> str:
    if not is_provider_integrated(config.provider):
        raise NotImplementedError(COMING_SOON_MESSAGE)
    if not config.api_key:
        raise ValueError("No AI model configured. Please complete AI Model Setup first.")

    from openai import OpenAI

    client = OpenAI(api_key=config.api_key)
    response = client.chat.completions.create(
        model=config.model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0.7,
        presence_penalty=0.2,
        timeout=30,
    )
    return response.choices[0].message.content or ""

