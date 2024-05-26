from prompts import *
from  service import *
def generate_draft_email(conversations: []):
    draft_email_prompt = draft_email_generating_prompt.get_draft_email_prompt(conversations)
    llm_name = 'llama3'
    generated_draft_email = LLMFactory.create_llm(llm_name).completion(draft_email_prompt)
    return generated_draft_email