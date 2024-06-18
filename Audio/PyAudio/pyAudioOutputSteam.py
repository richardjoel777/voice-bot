from Audio.Common.outputStream import OutputStream

class PyAudioOutputStream(OutputStream):
    def __init__(self, stream):
        super().__init__(stream)

    async def write(self, chunks):
        self.stream.write(chunks)

    async def start(self):
        self.stream.start_stream()

    async def stop(self):
        self.stream.stop_stream()
        self.stream.close()