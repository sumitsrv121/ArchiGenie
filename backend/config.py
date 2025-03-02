from pydantic_settings import BaseSettings  # For Pydantic v2
import openai

# Updated import for OpenAI errors (for openai>=1.0.0)
from openai import (
    APIError,
    APIConnectionError,
    RateLimitError,
    APITimeoutError
)
from openai import OpenAI  # For modern OpenAI client initialization
client = OpenAI(api_key="")  # Placeholder; will be set via settings

class Settings(BaseSettings):
    openai_api_key: str
    huggingfacehub_api_token: str
    ai_provider: str = "huggingface"  # Options: "openai" or "huggingface"
    app_env: str
    allowed_origins: str  # Comma-separated list of allowed origins
    model_name: str = "google/flan-t5-xl"  # Change this in .env to a smaller model (e.g., tiiuae/falcon-7b-instruct)
    redis_host: str = "localhost"
    redis_port: int = 6379
    rate_limit_per_minute: int = 30
    backend_url: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

if settings.openai_api_key:
    openai.api_key = settings.openai_api_key
    client = OpenAI(api_key=settings.openai_api_key)

def validate_settings():
    provider = settings.ai_provider.lower().strip()
    if provider not in ("openai", "huggingface"):
        raise ValueError("Unsupported provider in environment. Use 'openai' or 'huggingface'.")
    if provider == "openai" and not settings.openai_api_key:
        raise ValueError("OpenAI API key is required when using the OpenAI provider.")
    if provider == "huggingface" and not settings.huggingfacehub_api_token:
        raise ValueError("HuggingFace Hub token is required when using the HuggingFace provider.")
    if provider == "huggingface" and "gpt" in settings.model_name.lower():
        raise ValueError("GPT models require the OpenAI provider.")

validate_settings()
