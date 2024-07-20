from prompts import *
from service.LLMFactory import *
import json
import re

pattern = re.compile(r"```json(.*?)```", re.DOTALL)
pattern2 = re.compile(r"{(.*?)}", re.DOTALL)

def get_fixedcode_and_rootcause(exception_stack, code_snippets):
    prompt = exception_solver_prompt.get_exception_solver_prompt(exception_stack, code_snippets)
    if prompt is None:
        return None
    llm_name = 'llama3'
    bot_response = LLMFactory.create_llm(llm_name).completion(prompt, temperature=0.3)
    # bot_response = "```json" + bot_response
    return bot_response
    # bot_response = extract_json(bot_response)
    # fixed_code, root_cause = extract_fixedcode_and_rootcause(bot_response)

    # return fixed_code, root_cause

def extract_json(bot_response: str):
    match = pattern.search(bot_response)
    match2 = pattern2.search(bot_response)

    if match:
        json_string = match.group(1).strip()
        return json_string
    if match2:
        json_string = match2.group(1).strip()
        return "{ "+json_string + " }"

    else:
        print("No Json Found in tripple quotes. ")
        return bot_response


corrected_code_pattern = re.compile(r'"corrected_code": "(.*?)"')
root_cause_pattern = re.compile(r'"root_cause": "(.*?)",')

def extract_fixedcode_and_rootcause(bot_response):
    try:
        # Try to parse the string to a JSON object
        json_object = json.loads(bot_response)
        # print("The string is a valid JSON.")
    except json.JSONDecodeError as e:
        # If parsing fails, it is not a valid JSON
        # print("The string is not a valid JSON.")
        # print(f"Error: {e}")
        corrected_code_match = corrected_code_pattern.search(bot_response)
        root_cause_match = root_cause_pattern.search(bot_response)

        # Extract the matched groups
        corrected_code = corrected_code_match.group(1).strip() if corrected_code_match else None
        root_cause = root_cause_match.group(1).strip() if root_cause_match else None

        return corrected_code, root_cause

    # Output the result
    if json_object is not None:
        print("JSON object:", json_object)

    fixed_code = json_object["corrected_code"]
    root_cause = json_object["root_cause"]
    return fixed_code, root_cause

if __name__ == '__main__':
    # extract_fixedcode_and_rootcause({"fixed_code": "hahah", "root_cause": "this is root cause"})

    exception_stack = """Failed to load resource: the server responded with a status of 404 ()
"""
    code = """
    @RequestMapping(value = "/test/", method = RequestMethod.GET)
    public String test() {
    """
    code_snippets = [{"description": "java code", "code": code}]
    result = get_fixedcode_and_rootcause(exception_stack, code_snippets)
    print(result)

#     test = """
# {
#   "corrected_code": \"""
#      @RequestMapping(value = "/test", method = RequestMethod.GET)
#     public String test() {
#         // Your code here
#     }
# \"""
#   "root_cause": "Typo in the URL, missing trailing slash"
# }
#     """
#     json_object = extract_fixedcode_and_rootcause(test)
#     print(json_object)
