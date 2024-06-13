from prompts import *
from service.LLMFactory import *
def order_food(last_prompt, user_query, conversations):

    order_food_prompt = order_chatbot_prompt.get_order_food_prompt(last_prompt, conversations, user_query)
    if order_food_prompt is None:
        return None
    llm_name = 'llama3'
    bot_response = LLMFactory.create_llm(llm_name).completion(order_food_prompt)
    # Q: there is line break character at the beginning and end of generated_draft_email. how to remove it ?
    #
    return bot_response, last_prompt