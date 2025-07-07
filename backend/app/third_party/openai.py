from dotenv import load_dotenv
import os
from typing import List
from openai import AsyncOpenAI, OpenAIError

load_dotenv()

# Expect an environment variable named OPENAI_API_KEY (not DEEPSEEK_API_KEY anymore)
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise EnvironmentError("OPENAI_API_KEY not found in environment variables.")

# Create a single asynchronous client that will be re‑used for every request
_openai_client = AsyncOpenAI(api_key=openai_api_key)


class OpenAI:
    """Wraps common Chat Completions use‑cases used in our project."""

    def __init__(self, *, model: str = "gpt-4o-mini", temperature: float = 0.7):
        self.model = model
        self.temperature = temperature

    async def _chat_completion(self, prompt: str):
        """Private helper that sends the prompt to the Chat Completions API."""
        try:
            response = await _openai_client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
            )
            return response
        except OpenAIError as exc:
            # Wrap and re‑raise so callers do not need to import OpenAIError
            raise RuntimeError(f"OpenAI API error: {exc}") from exc

    async def generate_subtitles(self, prompt: str) -> List[str]:
        """Splits the assistant response into clean subtitle‑sized chunks."""
        data = await self._chat_completion(prompt)
        content = data.choices[0].message.content

        # Break at blank lines, strip white‑space, and remove leading * if present
        raw_sections = [section.strip() for section in content.split("\n\n") if section.strip()]
        cleaned_sections = [section.replace("*", "").strip() for section in raw_sections]
        return cleaned_sections

    async def generate_prompt_for_image_generator(self, prompt: str) -> str:
        """Returns a single string prompt suitable for an image generation model."""
        data = await self._chat_completion(prompt)
        return data.choices[0].message.content.strip()
