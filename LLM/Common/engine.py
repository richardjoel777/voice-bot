# This is a common class for LLM engines

class LLMEngine:
    def __init__(self, api_key, system_prompt = "") -> None:
        self.__api_key = api_key
        self.system_prompt = system_prompt
    
    async def generate_response(self, user_input):
        pass