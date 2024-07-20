import util.logging_utils as logging_utils

logger = logging_utils.setup_logger('jira_assistant_prompt')


prompt_template = """<|begin_of_text|><|start_header_id|>user<|end_header_id|>
you are a rebot to help me correct issue code and find the root cause given that exception stack and relevant code snippets.
every code snippet includes code description and code.
No Note or explanation required.

exception stack: ```{exception_stack}```
{code_snippets}```

please correct the issue code . don't add unnecessary code.
provide me corrected code and root cause only in json format with below two keys:
root_cause, corrected_code

<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""

def get_exception_solver_prompt(exception_stack, code_snippets_array, prompt = prompt_template ):

    try:
        code_snippets = ""
        if exception_stack and code_snippets_array:
            for code_snippet_item in code_snippets_array:
                code_snippets = code_snippets + "file name: " + code_snippet_item["description"]+ " \n issue code: ```" + code_snippet_item["code"] + "```"

            prompt = prompt.format(exception_stack=exception_stack, code_snippets= code_snippets)
            logger.info(prompt)
            return prompt.strip()
    except Exception as e:
        logger.exception(e)
        return None

    return prompt