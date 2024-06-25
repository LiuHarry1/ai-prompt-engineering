from prompts import *
from service.LLMFactory import *
from function_calling.tools import *
import json

def get_bot_message(conversations):
    prompt = function_call_prompt.get_function_call_prompt(conversations)
    if prompt is None:
        return None
    llm_name = 'llama3'
    bot_response = LLMFactory.create_llm(llm_name).completion(prompt, temperature=0.3)

    tool_name, inputs = extract_tool_name_and_inputs(bot_response)
    if tool_name and inputs:
        executed_result, url, input_data = call_tool(tool_name, inputs)
        return executed_result

    return bot_response.strip()


def extract_tool_name_and_inputs(bot_response):
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

    tool_name = json_object["tool_name"]
    inputs = json_object["inputs"]
    return tool_name, inputs

if __name__ == '__main__':
    print(extract_tool_name_and_inputs("""{"tool_name": "scale_component", "inputs": ["announcement", 3]}"""))
