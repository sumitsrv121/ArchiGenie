import logging
import re
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain_community.cache import SQLiteCache
from backend.config import settings
import langchain

# Use SQLiteCache from langchain_community to cache responses.
langchain.llm_cache = SQLiteCache(database_path="./.demo_cache.db")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

PROMPT_VERSION = "v2.3-technical-arch"
MARKER = "<<<ARCHITECTURE_START>>>"

class ArchitectureGenerator:
    def __init__(self, provider: str = None):
        self.provider = (provider or settings.ai_provider).lower().strip()
        logger.debug("Using provider: %s", self.provider)
        if self.provider not in ("openai", "huggingface"):
            raise ValueError("Unsupported provider. Use 'openai' or 'huggingface'.")
        self.llm = self._init_llm()
        logger.debug("ArchitectureGenerator initialized with provider: %s", self.provider)
        # Update prompt template to include a unique marker.
        if "falcon" in settings.model_name.lower():
            template = (
                f"[{PROMPT_VERSION}] Generate a detailed production-ready architecture specification for the following requirement:\n"
                "{raw_requirement}\n\n"
                f"Your response must start with the marker {MARKER} and then include only the final architecture details. Do not echo any prompt instructions.\n"
                f"{MARKER}"
            )
        else:
            template = (
                f"[{PROMPT_VERSION}] Generate a comprehensive production-ready architecture plan for the following requirement:\n"
                "{raw_requirement}\n\n"
                f"Your response must start with the marker {MARKER} and then include only the final architecture details (with headings, sub-headings, etc.). Do not include any of the above instructions or prompt text.\n"
                f"{MARKER}"
            )
        self.architecture_template = PromptTemplate(
            input_variables=["raw_requirement"],
            template=template
        )

    def _init_llm(self):
        if self.provider == "huggingface":
            from langchain_community.llms import HuggingFaceHub
            try:
                return HuggingFaceHub(
                    repo_id=settings.model_name,  # e.g., "tiiuae/falcon-7b-instruct" or "google/flan-t5-xl"
                    model_kwargs={"temperature": 0.4, "max_length": 2048},
                    huggingfacehub_api_token=settings.huggingfacehub_api_token
                )
            except Exception as e:
                logger.error(f"Model loading failed: {str(e)}")
                raise ValueError(f"Failed to load model: {str(e)}")
        elif self.provider == "openai":
            logger.info("Initializing OpenAI Chat model with GPT-4")
            return ChatOpenAI(
                model_name="gpt-4",
                temperature=0.3,
                max_retries=3,
                request_timeout=30,
                openai_api_key=settings.openai_api_key,
                max_tokens=2048,
                frequency_penalty=0.7
            )
        else:
            raise ValueError("Unsupported provider. Use 'openai' or 'huggingface'.")

    def _sanitize_output(self, text: str) -> str:
        # Remove extraneous artifacts.
        cleaned = text.replace("--- Begin Detailed Architecture Plan ---", "").replace("Answer:", "")
        cleaned = re.sub(r'^#+\s*', '', cleaned, flags=re.MULTILINE)
        cleaned = cleaned.strip()
        # Extract only the text after the marker.
        if MARKER in cleaned:
            parts = cleaned.split(MARKER, 1)
            return parts[1].strip()
        return cleaned

    def _is_valid_output(self, text: str) -> bool:
        return (
            len(text) > 500 and 
            "scalability" in text.lower() and 
            "security" in text.lower() and 
            "technology" in text.lower()
        )

    def _generate(self, raw_requirement: str) -> str:
        from langchain.schema import HumanMessage
        prompt_text = self.architecture_template.format(raw_requirement=raw_requirement)
        result = self.llm.predict_messages([HumanMessage(content=prompt_text)]).content
        return result.strip()

    def generate_architecture(self, raw_requirement: str) -> str:
        logger.info("Generating architecture details...")
        for attempt in range(3):
            result = self._generate(raw_requirement)
            sanitized = self._sanitize_output(result)
            if self._is_valid_output(sanitized):
                logger.info("Valid output generated on attempt %d", attempt + 1)
                return sanitized
            else:
                logger.warning("Output not valid on attempt %d; retrying...", attempt + 1)
                logger.debug("Attempt %d output: %s", attempt + 1, sanitized)
        logger.error("Failed to generate valid output after 3 attempts")
        return sanitized

def generate_architecture_details(prompt: str, provider: str = None) -> str:
    generator = ArchitectureGenerator(provider=provider)
    return generator.generate_architecture(prompt)

def generate_prompt(mode: str, inputs: dict) -> str:
    if mode == "functional":
        raw_requirement = (
            f"FUNCTIONAL REQUIREMENT: {inputs.get('functional_requirement', '')}\n\n"
            "Provide a clear and detailed production-ready architecture plan."
        )
    else:
        raw_requirement = (
            f"Core Architecture Pattern: {inputs.get('architecture', '')}\n"
            f"Business Services: {', '.join(inputs.get('services', []))}\n"
            f"Integration Strategy: {', '.join(inputs.get('integration', []))}\n"
            f"Data Storage: {', '.join(inputs.get('data_storage', []))}\n"
            f"Security Measures: {', '.join(inputs.get('security', []))}\n"
            f"Deployment Environment: {inputs.get('deployment', '')}\n"
            f"Scaling Strategies: {', '.join(inputs.get('scaling', []))}\n"
            f"Performance Targets: Expected Concurrency: {inputs.get('expected_concurrency', 'N/A')}, "
            f"Latency: {inputs.get('latency', 'N/A')}ms, Throughput: {inputs.get('throughput', 'N/A')} req/sec\n"
            f"Advanced Features: {', '.join(inputs.get('advanced_features', []))}\n\n"
            "Provide a clear and detailed production-ready architecture plan."
        )
    return generate_architecture_details(raw_requirement, provider=settings.ai_provider)
