from TTS.Common.engine import TTSEngine
from Audio.Common.outputStream import OutputStream
from openai import AsyncOpenAI
import time

class OpenAI(TTSEngine):
    def __init__(self, api_key: str) -> None:
        self.__api_key = api_key
        self.engine = "OpenAI"
    
    async def convert(self, user_input: str, stream: OutputStream):
        client = AsyncOpenAI(api_key=self.__api_key)
        first_speech = None

        async with client.audio.speech.with_streaming_response.create(
            input=user_input,
            model="tts-1",
            voice="alloy",
            response_format="pcm"
        ) as response:
            async for chunk in response.iter_bytes(1024):
                if first_speech is None:
                    first_speech = time.perf_counter()
                await stream.write(chunk)
        
        await stream.stop()
        return first_speech
        