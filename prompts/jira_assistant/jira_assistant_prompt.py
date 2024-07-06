import util.logging_utils as logging_utils

logger = logging_utils.setup_logger('jira_assistant_prompt')


prompt_template = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
you are a rebot to help people generate summary, description, acceptance criteria, development required with the description of user story user input in JIRA.

if this user story involve code change then DevelopmentRequired would be true. otherwise, it is false.  only investigation or research doesn't require code change.

provide them in json format with below keys:
summary, description, acceptanceCriteria, DevelopmentRequired
<|eot_id|><|start_header_id|>user<|end_header_id|>
user story: {user_input}
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""

def get_jira_assistant_prompt(user_input, prompt = prompt_template ):
    try:
        if user_input:
            prompt = prompt.format(user_input=user_input)
            logger.info(prompt)
            return prompt.strip()
    except Exception as e:
        logger.exception(e)
        return None

    return prompt