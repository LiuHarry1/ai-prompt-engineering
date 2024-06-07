import util.logging_utils as logging_utils

logger = logging_utils.setup_logger('draft_email_generating_prompt')

draft_email_prompt_template_old = """Please review the following conversation between user and ps (production support). 

conversation: 

{conversation}

Based on this conversation, please draft a email for the following new user query to help user sort it out.

new user query: "we have inital notification sent , please find the resason behind of that "

no answer and explanation required. only an email is required. don't say any other things."""

draft_email_prompt_template_old1 = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are a product support who only reply email to resolve user problem or query. 

<|eot_id|><|start_header_id|>user<|end_header_id|>

please go through following conversation extracted from email chain and summarize the user problem and solution among it.

email conversation: \"\"\"{conversation}\"\"\"

here is a new user problem: \"\"\"{user_query}\"\"\"

Based on your understanding in previous email conversation, please only outputs email content to address this new user problem. If you don't know how to resolve it , just say you can't resolve it. No Note required. no answer and explanation required.

email body:<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""


draft_email_prompt_template = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are a product support (ps) for replying email to resolve new user problem or query. <|eot_id|><|start_header_id|>user<|end_header_id|>

please review following conversation extracted from similar user query email in history. Based on your understanding in this email conversation, please only outputs email content to address this new user problem. If you don't know how to resolve it , just say you can't resolve it. No Note required. no answer and explanation required.

Email  conversation: \"\"\"{conversation}\"\"\"

New user problem: \"\"\"{user_query}\"\"\"

email content: 
<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""


def get_draft_email_prompt(conversations: [], user_query: ''):
    try:
        if conversations:
            conversation = conversations[0]
            draft_email_promp = draft_email_prompt_template.format(conversation=conversation, user_query =user_query)

            return draft_email_promp.strip()
    except Exception as e:
        logger.exception(e)
        return None

    return None