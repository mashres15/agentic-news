"""
Generates concise summaries using OpenAI or local model.
"""
import os
import openai
from typing import Any

openai.api_key = os.getenv('OPENAI_API_KEY')


class Summarizer:
    @staticmethod
    def summarize(text: str, max_tokens: int = 150) -> str:
        response = openai.Completion.create(
            model='text-davinci-003',
            prompt=f"Summarize the following in <=150 words:
{text}",
            max_tokens=max_tokens,
            temperature=0.3
        )
        return response.choices[0].text.strip()