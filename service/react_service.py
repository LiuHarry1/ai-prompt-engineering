import prompts.react_agent.react_prompt as react_prompt
from service.LLMFactory import *

tool_and_description = """{[{tool_name: "shut_down_component", required_parameters: "component name", description: "a tool to shut down a certain component. " },
{tool_name: "start_up_component", required_parameters: "component name", description: "a tool to start up or roll out a certain component. " },
{tool_name: "scale_component", required_parameters: "component name", description: "a tool to scale up or down pods." },
{tool_name: "select_pod_count", required_parameters: "component name", description: "a tool to select the number of pods for a certain component. " }
]}
"""

tool_names = "shut_down_component, start_up_component, scale_component, select_pod_count"

def get_action_and_action_input(bot_response):
    try:
        thought_index = bot_response.index("Thought:")
        if thought_index:
            thought_start = bot_response.index("Thought:") + 9
            thought_end = bot_response.index("\n", thought_start)
            thought = bot_response[thought_start:thought_end].strip()

        action_index = bot_response.index("Action:")
        if action_index:
            action_start = bot_response.index("Action:") + 8
            action_end = bot_response.index("\n", action_start)
            action = bot_response[action_start:action_end].strip()

            if action == "None":
                return thought, None, None
        action_input_index = bot_response.index("Action Input:")
        if (action_input_index):
            input_start = bot_response.index("Action Input:") + 13
            input_end = bot_response.find("\n", input_start)
            input_ = bot_response[input_start:input_end].strip()

        print(f"Action: {action}")
        print(f"Action Input: {input_}")
    except Exception as e:
        return None, None, None

    return thought, action, input_

def get_final_answer(bot_response):
    try:
        index = bot_response.index("Final Answer:")
        if index:
            index = bot_response.index("Final Answer:") + 13
            final_answer = bot_response[index:].strip()
            if final_answer:
                return final_answer
    except Exception as e:
        return None

def remove_words_before_thought(bot_response):
    try:
        index = bot_response.index("Thought:")
        if index:
            bot_response = bot_response[index:].strip()
            if bot_response:
                return bot_response
    except Exception as e:
        return bot_response


def execute_tool(tool_name, inputs):
    print(f"calling {tool_name} with input: {inputs}")

    if tool_name == "select_pod_count":
        return "The number of announcement pods is 3."
    if tool_name == "shut_down_component":
        return "The announcement component is now down. "
    if tool_name == "start_up_component":
        return "The announcement component is now started and ready for use."
    if tool_name == "scale_component":
        return "The number of announcement pods is 2."

    return ""

def get_bot_response(user_input):

    llm_name = "llama3"
    bot_response = ''

    for i in range(3):
        # print(f"bot_response: {bot_response}")
        prompt = react_prompt.get_react_prompt(tool_and_description, tool_names, user_input, bot_response)
        print("====== Following is prompt ====", )
        print(prompt)
        print("====== End of prompt ====", )

        print("calling llm at "+ str(i)+ " times")
        new_bot_response = LLMFactory.create_llm(llm_name).completion(prompt, temperature=0.3, stop=["<|eot_id|>","Observation:"])
        final_answer = get_final_answer(new_bot_response)
        if final_answer:
            print("Final Answer:", final_answer)
            return final_answer

        thought , action, action_input = get_action_and_action_input(new_bot_response)
        if (action and action_input and (len(action)!=0) and (len(action_input) != 0)):
            new_bot_response = remove_words_before_thought(new_bot_response)
            executed_result =execute_tool(action, action_input)

            bot_response = new_bot_response + "\nObservation:" + executed_result + "\nThought:"
            # bot_response = new_bot_response + "\nObservation:" + executed_result
        elif (thought):
            # no action required to be executed. just normal chat.
            return thought
        else:
            return new_bot_response


    return bot_response.strip()

if __name__ == '__main__':
    # user_question = "how many pods does announcement component have? "
    # user_question = "please start announcement component. "
    # user_question = "please shut down announcement component. "
    # user_question = "please stop announcement component."
    # user_question = "please scale up announcement to 2. "

    user_question = "hi you, "
    response = get_bot_response(user_question)
    print(response)


