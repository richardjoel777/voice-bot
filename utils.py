import pyaudio
import asyncio
from Audio import (
    InputStream,
    OutputStream,
    PyAudioInputStream,
    PyAudioOutputStream
)
from LLM import LLMEngine, OpenAI as OpenAILLM
from STT import STTEngine, Deepgram
from TTS import TTSEngine, OpenAI as OpenAITTS

def create_input_stream(
    *,
    sample_rate: int = 16_000,
    chunk_size: int = 8000
) -> InputStream:

    audio_queue = asyncio.Queue()

    def callback(input_data, frame_count, time_info, status_flag):
        audio_queue.put_nowait(input_data)

        return (input_data, pyaudio.paContinue)

    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk_size,
        stream_callback=callback
    )

    return PyAudioInputStream(stream, audio_queue)

def create_output_stream(
    *,
    sample_rate: int = 24_000,
    chunk_size: int = 1024
) -> OutputStream: 
    audio = pyaudio.PyAudio()
    stream = audio.open(
            format=8,
            channels=1,
            rate=sample_rate,
            output=True,
            frames_per_buffer=chunk_size
        )
    
    return PyAudioOutputStream(stream)

def create_stt_engine(
    *,
    name : str,
    api_key: str
) -> STTEngine:
    if name == "deepgram":
        return Deepgram(api_key)
    raise ValueError("Unsupported Engine")

def create_llm_engine(
    *,
    name : str,
    api_key: str,
    system_prompt: str
) -> LLMEngine:
    if name == "openai":
        return OpenAILLM(api_key, system_prompt)
    raise ValueError("Unsupported Engine")

def create_tts_engine(
    *,
    name : str,
    api_key: str
) -> TTSEngine:
    if name == "openai":
        return OpenAITTS(api_key)
    raise ValueError("Unsupported Engine")
    