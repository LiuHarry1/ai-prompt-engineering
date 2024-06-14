import util.logging_utils as logging_utils

logger = logging_utils.setup_logger('chatbot_prompt')


prompt_template = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
you are a chatbot. Always answer as helpfully as possible.
Keep the answer short and concise.
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""

def get_chabot_prompt(conversations, prompt = prompt_template ):
    try:
        conversation_prompt = ""
        if conversations:
            for message in conversations:
                message_type=  message['type']
                message_content = message['text']
                if message_type == 'bot':
                    conversation_prompt = conversation_prompt + f"""{message_content}<|eot_id|><|start_header_id|>user<|end_header_id|>"""
                if message_type == 'user':
                    conversation_prompt = conversation_prompt + f"""{message_content}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

            prompt = prompt+ conversation_prompt
            logger.info(conversation_prompt)
            return prompt.strip()
    except Exception as e:
        logger.exception(e)
        return None

    return prompt