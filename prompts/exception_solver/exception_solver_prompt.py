import util.logging_utils as logging_utils

logger = logging_utils.setup_logger('jira_assistant_prompt')


prompt_template = """<|begin_of_text|><|start_header_id|>user<|end_header_id|>
your target is to help user find solution based on the following information user provided.
request you provide corrected code if there is issue code as well.
Keep the answer short and concise.

{issue_description}
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""

def get_exception_solver_prompt(data, prompt = prompt_template ):

    try:
        issue_description  = ""
        problemDescription = data["problemDescription"]
        if problemDescription:
            issue_description = issue_description + "problem description: ```" + problemDescription + "```\n"

        environmentInformation = data["environmentInformation"]
        if environmentInformation:
            issue_description = issue_description + "environment information: ```" + environmentInformation + "```\n"
        exceptionStack = data["exceptionStack"]
        if exceptionStack:
            issue_description = issue_description + "exception stack: ```" + exceptionStack + "```\n"
        code_snippets_array = data["codeSnippets"]
        if code_snippets_array:
            code_snippets = ""
            for code_snippet_item in code_snippets_array:
                if code_snippet_item["description"] and code_snippet_item["code"]:
                    code_snippets = code_snippets + "file name: " + code_snippet_item["description"] + "\nissue code: ```" + \
                                    code_snippet_item["code"] + "```\n"
            if code_snippets:
                issue_description = issue_description + code_snippets

        prompt = prompt.format(issue_description=issue_description)
        logger.info(prompt)
        return prompt.strip()
    except Exception as e:
        logger.exception(e)
        return None

    return prompt