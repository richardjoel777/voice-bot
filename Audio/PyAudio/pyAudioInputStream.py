from Audio.Common.inputStream import InputStream
import asyncio

class PyAudioInputStream(InputStream):
    def __init__(self, stream, queue):
        super().__init__(stream)
        self.queue = queue

    async def read(self):
        data = await self.queue.get()
        return data

    async def start(self):
        self.stream.start_stream()
    
    async def stop(self):
        await self.queue.put(None)
        self.stream.stop_stream()
        self.stream.close()
    