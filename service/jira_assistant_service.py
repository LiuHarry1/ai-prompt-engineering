from prompts import *
from service.LLMFactory import *
import re
import json

pattern = re.compile(r"```(.*?)```", re.DOTALL)

summary_patten = r'"summary":\s*"([^"]+)"'
description_patten = '"description":\s*"([^"]+)"'
acceptance_criteria_patten = r'"acceptanceCriteria":\s*\[(.*?)\]'
development_required_pattern = r'"developmentRequired":\s*(true|false)'
def extract_jira_info_with_re (bot_response: str):
    if "summary" in bot_response and "description" in bot_response and "acceptanceCriteria" in bot_response:
        summary_match = re.search(summary_patten, bot_response)
        description_match = re.search(description_patten, bot_response, re. DOTALL)
        development_required_match = re.search(development_required_pattern, bot_response, re. DOTALL)
        acceptance_criteria_match = re.search(acceptance_criteria_patten, bot_response, re.DOTALL)
        summary = summary_match.group(1) if summary_match else "Not Provided"
        description = description_match.group(1) if description_match else "Not Provided"
        development_required = development_required_match.group(1) if description_match else "true"
        acceptance_criteria = acceptance_criteria_match.group(1) if acceptance_criteria_match else "Not Provided"
        if acceptance_criteria != "Not Provided":
            acceptance_criteria = re.findall(r'"([^"]+)"', acceptance_criteria)

        return {"summary": summary, "description": description, "acceptance_criteria": acceptance_criteria, "development_required": development_required}
    else:
        return None

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
            return extract_jira_info_with_re(bot_response)
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


if __name__ == '__main__':
    bot_response = """
Here is the output in JSON format:

{
"summary": "Migrate Position Component to Spring Boot 3.2.4",
"description": "Migrate the existing position component to use Spring Boot 3.2.4, ensuring compatibility and functionality remain unchanged.",
"acceptanceCriteria": [
"Migrated position component should be compatible with Spring Boot 3.2.4",
"No changes in functionality or behavior of the position component"
],
"developmentRequired": true
}

Let me know if you have any further questions!
    """
    data = extract_jira_info_with_re(bot_response)
    print(data['development_required'])
    print(data['acceptance_criteria'])
