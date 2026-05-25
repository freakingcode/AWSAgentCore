from openai import AsyncOpenAI
from dotenv import load_dotenv

import os

load_dotenv()


class OpenAIModel:

    stateful = False

    def __init__(self):

        self.client = AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        self.model_name = "gpt-4.1-mini"

    async def stream(self, messages, *args, **kwargs):
        formatted_messages = []

        for msg in messages:
            content = msg.get("content", "")

            # Convert Strands content format
            if isinstance(content, list):
                text_parts = []
                for item in content:
                    if isinstance(item, dict):
                        if "text" in item:
                            text_parts.append(item["text"])
                content = " ".join(text_parts)
            formatted_messages.append({
                "role": msg["role"],
                "content": content
            })

        response = await self.client.chat.completions.create(
            model=self.model_name,
            messages=formatted_messages
        )

        yield {
            "data": response.choices[0].message.content
        }