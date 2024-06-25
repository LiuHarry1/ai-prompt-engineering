from service.llama2_server import *
from service.llama3_server import *
import service.draft_email_generating_service as draft_email_generating_service
import service.order_food_service as order_food_service
import service.chatbot_service as chat_service
import service.jira_assistant_service as jira_assistant_service
import service.react_service as react_service
import service.function_calling_service as function_calling_service

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
