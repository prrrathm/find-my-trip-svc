# AsyncOpenAI → Ollama, swappable by base_url

from openai import AsyncOpenAI
from internal.core.config import settings

client = AsyncOpenAI(
    base_url=settings.agent_url,
    api_key=settings.agent_api_key,
)
