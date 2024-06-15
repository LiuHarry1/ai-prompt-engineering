from prompts import *
from service.LLMFactory import *
import re
import json

pattern = re.compile(r"```(.*?)```", re.DOTALL)

def extract_jira_information(bot_response: str):
    match = pattern.search(bot_response)

    if match:
        json_string = match.group(1).strip()
        try:
            data = json.loads(json_string)
            print("Extracted Json data", data)
            return data
        except json.JSONDecodeError as e:
            print('Invalid Json', e)
            return None
    else:
        print("No Json Found in tripple quotes. ")
        return None

def get_jira_message(user_input):
    prompt = jira_assistant_prompt.get_jira_assistant_prompt(user_input)
    if prompt is None:
        return None
    llm_name = 'llama3'
    bot_response = LLMFactory.create_llm(llm_name).completion(prompt)
    jira_information = extract_jira_information(bot_response)
    print(jira_information)
    if jira_information and isinstance(jira_information['acceptanceCriteria'], list):
        acceptanceCriteria_str = ""
        for index, acceptanceCriteria in enumerate(jira_information['acceptanceCriteria']):
            acceptanceCriteria_str =acceptanceCriteria_str + str(index+1) + ":" + acceptanceCriteria + "\n\n"

        jira_information['acceptanceCriteria'] = acceptanceCriteria_str

    return jira_information


