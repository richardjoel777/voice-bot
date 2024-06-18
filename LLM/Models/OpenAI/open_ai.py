from openai import AsyncOpenAI
from LLM.Common.engine import LLMEngine
import json
import time

class OpenAI(LLMEngine):
    def __init__(self, api_key, system_prompt):
        self.__api_key = api_key
        self.system_prompt = system_prompt
        self.engine = "OpenAI"

    async def generate_response(self, user_input : str) -> str:
        message = ""
        openAI = AsyncOpenAI(api_key=self.__api_key)
        first_response = None

        async with openAI.chat.completions.with_streaming_response.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input},
            ]
        ) as response:
        
            async for chunk in response.iter_lines():
                if not first_response:
                    first_response = time.perf_counter()
                message += chunk
            last_response = time.perf_counter()

        return {
            'result': json.loads(message)["choices"][0]["message"]['content'],
            'first_response_time': first_response,
            'last_response_time': last_response
        }