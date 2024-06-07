from service.llama2_server import *
from service.llama3_server import *


llama2Server = Llama2Server()
llama3Server = Llama3Server()
class LLMFactory:
    @staticmethod
    def create_llm(name):
        if name.lower().startswith("llama2"):
            return llama2Server
        elif name.lower().startswith("llama3"):
            return llama3Server
        else:
            return llama2Server
            # raise ValueError("Unknown LLM type")