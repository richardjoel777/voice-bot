from utils import create_input_stream, create_output_stream, create_stt_engine, create_llm_engine, create_tts_engine
from bot import VoiceBot
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')
OPEN_AI_API_KEY = os.getenv('OPEN_AI_API_KEY')

stt_engine = create_stt_engine(api_key=DEEPGRAM_API_KEY, name="deepgram")
llm_engine = create_llm_engine(api_key=OPEN_AI_API_KEY, name="openai", system_prompt="You are a chatbot like OK Google. So Respond like how it will do for user queries but don't take more than 50 words")
tts_engine = create_tts_engine(api_key=OPEN_AI_API_KEY, name="openai")

async def printInterimResult():
    while True:
        data = await stt_engine.stream()
        if data is None:
            print()
            return
        print(data,end=' ')

async def main():
    input("Press Any Key to Speak : ")
    input_stream = create_input_stream()
    output_stream = create_output_stream()
    bot = VoiceBot(input_stream=input_stream, output_stream=output_stream, stt_engine=stt_engine, llm_engine=llm_engine, tts_engine=tts_engine)
    await asyncio.gather(printInterimResult(), bot.run())

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())