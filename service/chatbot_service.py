from prompts import *
from service.LLMFactory import *

def get_bot_message(conversations):
    prompt = chatbot_prompt.get_chabot_prompt(conversations)
    if prompt is None:
        return None
    llm_name = 'llama3'
    bot_response = LLMFactory.create_llm(llm_name).completion(prompt)

    return bot_response.strip()