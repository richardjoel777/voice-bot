# common class for text to speech engine

class TTSEngine:
    def __init__(self, api_key : str) -> None:
        self.__api_key = api_key
        self.engine = None
    
    async def convert(self, text : str, stream):
        pass