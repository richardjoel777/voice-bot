# common class for speech to text engine
from Audio.Common.inputStream import InputStream

class STTEngine:
    def __init__(self, api_key : str) -> None:
        self.__api_key = api_key
        self.engine = None

    async def transcribe(self, stream : InputStream) -> str:
        pass

    async def stream(self):
        pass