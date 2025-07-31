from openai import OpenAI
# import os
from src.config import settings
# from llama_index.llms.openai import OpenAI
# from llama_index.llms.core import SQLDatabase


client = OpenAI(api_key=settings.openai_api_key)


def get_response(message: str, filters: dict):
    response = client.chat.completions.create(
        model=settings.model_base,
        messages=[{"role": "user", "content": message}],
        temperature=0.1
    )
    return response.choices[0].message.content
