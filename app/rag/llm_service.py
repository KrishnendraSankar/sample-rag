from openai import OpenAI

from app.config.settings import settings


class LLMService:

    def __init__(self):

        self.client = OpenAI(

            api_key=settings.OPENAI_API_KEY.get_secret_value(),

            base_url=settings.OPENAI_BASE_URL

        )

    def ask(
        self,
        prompt: str,
    ) -> str:

        response = self.client.chat.completions.create(

            model=settings.OPENAI_MODEL,

            messages=[

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0

        )

        return response.choices[0].message.content or ""