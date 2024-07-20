from prompts import *
from service.LLMFactory import *
import json

def get_fixedcode_and_rootcause(exception_stack, code_snippets):
    prompt = exception_solver_prompt.get_exception_solver_prompt(exception_stack, code_snippets)
    if prompt is None:
        return None
    llm_name = 'llama3'
    bot_response = LLMFactory.create_llm(llm_name).completion(prompt, temperature=0.3)

    fixed_code, root_cause = extract_fixedcode_and_rootcause(bot_response)

    return fixed_code, root_cause


def extract_fixedcode_and_rootcause(bot_response):
    try:
        # Try to parse the string to a JSON object
        json_object = json.loads(bot_response)
        # print("The string is a valid JSON.")
    except json.JSONDecodeError as e:
        # If parsing fails, it is not a valid JSON
        # print("The string is not a valid JSON.")
        # print(f"Error: {e}")
        return None, None

    # Output the result
    if json_object is not None:
        print("JSON object:", json_object)

    fixed_code = json_object["fixed_code"]
    root_cause = json_object["root_cause"]
    return fixed_code, root_cause

if __name__ == '__main__':
    pass
