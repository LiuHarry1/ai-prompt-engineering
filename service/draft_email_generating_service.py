from prompts import *
from service.LLMFactory import *

def generate_draft_email(conversations: [], user_query:''):
    draft_email_prompt = draft_email_generating_prompt.get_draft_email_prompt(conversations, user_query)
    if draft_email_prompt is None:
        return None
    llm_name = 'llama3'
    generated_draft_email = LLMFactory.create_llm(llm_name).completion(draft_email_prompt)
    # Q: there is line break character at the beginning and end of generated_draft_email. how to remove it ?
    #
    return generated_draft_email.strip()