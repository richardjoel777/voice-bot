from STT.Common.engine import STTEngine
import websockets
import asyncio
from Audio.Common.inputStream import InputStream
import ssl
import certifi
import json
import time

class Deepgram(STTEngine):
    def __init__(self, api_key : str) -> None:
        self.__api_key = api_key
        self.engine = "Deepgram"
        self.__interim_result = asyncio.Queue()
        self.__result = ""
        self.__stopped_time = None

    async def transcribe(self, stream : InputStream) -> str:
        extra_headers = {
            "Authorization": 'token ' + self.__api_key
        }

        async with websockets.connect('wss://api.deepgram.com/v1/listen?encoding=linear16&sample_rate=16000&channels=1', extra_headers=extra_headers, ssl=ssl.create_default_context(cafile=certifi.where())) as ws:
            async def sender(ws):
                try:
                    while True:
                        data = await stream.read()
                        # print(data)
                        if data is None:
                            return
                        await ws.send(data)
                except Exception as e:
                    print("Error while sending", str(e))
                    raise
            
            async def receiver(ws):
                async for msg in ws:
                    msg = json.loads(msg)
                    if msg['type'] == 'Metadata':
                        continue
                    # print(msg['speech_final'])
                    transcript = msg['channel']['alternatives'][0]['transcript']

                    if transcript:
                        await self.__interim_result.put(transcript)
                        self.__result += transcript
                    
                    if msg['speech_final']:
                        self.__stopped_time = time.perf_counter()
                        await self.__interim_result.put(None)
                        await stream.stop()
                        return

            await asyncio.gather(sender(ws), receiver(ws))

            return {
                'result': self.__result,
                'stopped_time': self.__stopped_time,
                'end_time': time.perf_counter()
            }
    
    async def stream(self):
        data = await self.__interim_result.get()
        return data