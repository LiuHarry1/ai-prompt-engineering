from prompts import *
from service.LLMFactory import *
import re
import json

pattern = re.compile(r"```(.*?)```", re.DOTALL)
pattern2 = re.compile(r"{(.*?)}", re.DOTALL)

summary_patten = r'"summary":\s*"([^"]+)"'
description_patten = '"description":\s*"([^"]+)"'
acceptance_criteria_patten = r'"acceptanceCriteria":\s*\[(.*?)\]'
acceptance_criteria_patten2 = r'"acceptanceCriteria":\s*"([^"]+)"'
development_required_pattern = r'"developmentRequired":\s*(true|false)'
story_point_pattern = r'"storyPoint":\s*(\d+)'

def extract_acceptance_criteria(bot_response: str):
    if "acceptanceCriteria" in bot_response :
        acceptance_criteria_match = re.search(acceptance_criteria_patten2, bot_response, re.DOTALL)
        acceptance_criteria = acceptance_criteria_match.group(1) if acceptance_criteria_match else "Not Provided"

        if "[" in acceptance_criteria and "]" in acceptance_criteria:
            acceptance_criteria = re.findall(r'"([^"]+)"', acceptance_criteria)

        if "Not Provided" == acceptance_criteria:
            acceptance_criteria_match = re.search(acceptance_criteria_patten, bot_response, re.DOTALL)
            acceptance_criteria = acceptance_criteria_match.group(1) if acceptance_criteria_match else "Not Provided"

            if "Not Provided" != acceptance_criteria:
                acceptance_criteria = re.findall(r'"([^"]+)"', acceptance_criteria)

        return acceptance_criteria

    else:
        return "Not Provided"


def extract_jira_info_with_re (bot_response: str):
    if "summary" in bot_response and "description" in bot_response and "acceptanceCriteria" in bot_response:
        summary_match = re.search(summary_patten, bot_response)
        description_match = re.search(description_patten, bot_response, re. DOTALL)
        development_required_match = re.search(development_required_pattern, bot_response, re. DOTALL)

        story_point_match = re.search(story_point_pattern, bot_response , re. DOTALL)
        summary = summary_match.group(1) if summary_match else "Not Provided"
        description = description_match.group(1) if description_match else "Not Provided"
        development_required = development_required_match.group(1) if description_match else "true"

        story_point = story_point_match.group(1) if story_point_match else "3"

        acceptance_criteria = extract_acceptance_criteria(bot_response)
        return {"summary": summary, "description": description, "acceptanceCriteria": acceptance_criteria, "developmentRequired": development_required, "storyPoint": story_point}
    else:
        return None

def extract_jira_information(bot_response: str):
    match = pattern.search(bot_response)
    match2 = pattern2.search(bot_response)

    if match:
        json_string = match.group(1).strip()
        try:
            data = json.loads(json_string)
            print("Extracted Json data", data)
            return data
        except json.JSONDecodeError as e:
            print('Invalid Json', e)
            return extract_jira_info_with_re(bot_response)
    if match2:
        json_string = match2.group(1).strip()
        try:
            data = json.loads("{ "+json_string + " }")
            print("Extracted Json data", data)
            return data
        except json.JSONDecodeError as e:
            print('Invalid Json', e)
            return extract_jira_info_with_re(bot_response)
    else:
        print("No Json Found in tripple quotes. ")
        return extract_jira_info_with_re(bot_response)

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
"summary": "Replace Tibico Queue with Kafka for Position Component",
"description": "As a developer, I want to replace Tibico queue with Kafka for position component to improve scalability and reliability. This change will allow us to handle a larger volume of data and reduce the risk of data loss.",
"acceptanceCriteria": [
"The system should be able to process a minimum of 1000 requests per minute without any noticeable performance degradation."
],
"developmentRequired": true,
"storyPoint": 5
}

Note: I assumed that this user story requires code changes, as it involves replacing Tibico queue with Kafka. Therefore, developmentRequired is set to true. The acceptance criteria are also provided based on the description of the user story. Finally, I estimated the story point to be 5, which is a moderate complexity task.
    """
    data = extract_jira_info_with_re(bot_response)
    print(data['developmentRequired'])
    print(data['acceptanceCriteria'])
    print(data['storyPoint'])
