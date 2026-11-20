from openai import OpenAI

from app.core.config import settings
from app.services.personas import get_system_prompt


class ChatService:
    def reply(self, figure: str, history: list[dict[str, str]], message: str) -> str:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured. Add it to your .env file.")

        client = OpenAI(api_key=settings.openai_api_key)
        completion = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": get_system_prompt(figure)},
                *history,
                {"role": "user", "content": message},
            ],
            temperature=0.4,
        )
        return completion.choices[0].message.content or "I am unable to answer that right now."


chat_service = ChatService()
