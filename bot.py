from Audio.Common.inputStream import InputStream
from Audio.Common.outputStream import OutputStream
from STT.Common.engine import STTEngine
from LLM.Common.engine import LLMEngine
from TTS.Common.engine import TTSEngine
import asyncio
import time

class VoiceBot:
    def __init__(self, *, input_stream: InputStream, output_stream: OutputStream, stt_engine: STTEngine, llm_engine: LLMEngine, tts_engine: TTSEngine):
        self.input_stream = input_stream
        self.output_stream = output_stream
        self.stt_engine = stt_engine
        self.llm_engine = llm_engine
        self.tts_engine = tts_engine

    async def run(self):
        results = await asyncio.gather(self.input_stream.start(), self.stt_engine.transcribe(self.input_stream))

        user_input = results[1]['result']
        user_stopped_time = results[1]['stopped_time']
        stt_end_time = results[1]['end_time']

        if not user_input:
            user_input = "How can I use this bot?"
        
        llm_result = await self.llm_engine.generate_response(user_input)

        # print(llm_result)

        results = await asyncio.gather(self.output_stream.start(), self.tts_engine.convert(llm_result['result'], self.output_stream))

        first_speech_time = results[1]

        print(f"Total Time for STT post user stopped speaking {stt_end_time - user_stopped_time:.2f}s")

        # Assuming the timings since user stopped speaking
        print(f"Time for First Token from LLM {llm_result['first_response_time'] - user_stopped_time:.2f}s")
        print(f"Time for Complete Response From LLM {llm_result['last_response_time'] - user_stopped_time:.2f}s")
        
        print(f"Total time from when user stopped speaking and TTS generated first speech {first_speech_time - user_stopped_time:.2f}s")
