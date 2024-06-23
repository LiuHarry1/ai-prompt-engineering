import prompts.react_agent.react_prompt as react_prompt
from service.LLMFactory import *
from function_calling import *


def get_action_and_action_input(bot_response):
    try:
        if "Thought:" in bot_response and "Action:" in bot_response:
            thought_index = bot_response.index("Thought:")
            action_index = bot_response.index("Action:")
            if thought_index != None:
                thought_start = bot_response.index("Thought:") + 9
                thought = bot_response[thought_start:action_index].strip()
                bot_response= bot_response.replace(bot_response[:action_index],"")
        elif "Thought:" in bot_response and "\n" in bot_response :
            thought_index = bot_response.index("Thought:")
            if thought_index != None:
                thought_start = bot_response.index("Thought:") + 9
                thought_end = bot_response.index("\n", thought_start)
                thought = bot_response[thought_start:thought_end].strip()
                bot_response= bot_response.replace(bot_response[:thought_end],"")
        elif ("Action:" in bot_response):
            action_index = bot_response.index("Action:")
            thought = bot_response[:action_index].strip()
            bot_response = bot_response.replace(bot_response[:action_index], "")
        else:
            thought = bot_response
            return thought, None, None
    except Exception as e:
        logger.exception(e)

    try:
        if "Action:" in bot_response and "Action Input:" in bot_response:
            action_index = bot_response.index("Action:")
            if action_index != None:
                action_start = bot_response.index("Action:") + 8
                action_input_start = bot_response.index("Action Input:")
                action = bot_response[action_start:action_input_start].strip()
                input_ = bot_response.replace(bot_response[:action_input_start], "")
                if action == "None" or action == "none":
                    return thought, None, None
            else:
                return thought, None, None
    except Exception as e:
        # logger.exception(e)
        action = None
        input_ = None

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
        if index != None:
            bot_response = bot_response[index:].strip()
            if bot_response:
                return bot_response
    except Exception as e:
        return bot_response


def get_bot_response(conversation):

    llm_name = "llama3"
    bot_response = ''
    executed_tool = []
    tool_and_description = tools.get_tool_name_and_descpritions()
    tool_names = tools.get_tool_names()

    inital_prompt = react_prompt.get_inital_react_prompt(tool_and_description, tool_names, conversation)

    for i in range(3):
        # print(f"bot_response: {bot_response}")

        prompt = react_prompt.get_react_prompt_by_new_thought(inital_prompt, bot_response)
        print("====== Following is prompt ====", )
        print(prompt)
        print("====== End of prompt ====", )

        print("calling llm at "+ str(i)+ " times")
        new_bot_response = LLMFactory.create_llm(llm_name).completion(prompt, temperature=0.3, stop=["<|eot_id|>","Observation:"])
        final_answer = get_final_answer(new_bot_response)
        if final_answer:
            print("Final Answer:", final_answer)
            return final_answer, executed_tool

        thought , action, action_input = get_action_and_action_input(new_bot_response)
        if (action and action_input and (len(action)!=0) and (len(action_input) != 0)):
            new_bot_response = remove_words_before_thought(new_bot_response)
            executed_result, url, input_data = tools.call_tool(action, action_input)
            executed_tool.append({"url":url, "input_data": input_data})

            bot_response = new_bot_response + "\nObservation:" + executed_result + "\nThought:"
            # bot_response = new_bot_response + "\nObservation:" + executed_result
        elif (thought):
            # no action required to be executed. just normal chat.
            return thought, executed_tool
        else:
            return new_bot_response, executed_tool


    return bot_response.strip(), executed_tool

if __name__ == '__main__':
    # user_question = "how many pods does announcement component have? "
    # user_question = "please start announcement component. "
    # user_question = "please shut down announcement component. "
    # user_question = "please stop announcement component."
    user_question = "please scale up announcement to 2. "

    # user_question = "hi you, "

    # conversation = [{"type": "bot", "text": "hello, I am robot" } ,{"type": "user", "text": "hello" },
    #                 {"type": "bot", "text": "I'm happy to help you. What's on your mind?"},{"type": "user", "text": "please start announcement component" },
    #                 {"type": "bot", "text": "Now that the announcement component is started, what would you like to do next?"},
    #                 {"type": "user", "text": "how many pods does announcement component have?"},
    #                 {"type": "bot","text": "The announcement component has 3 pods."},
    #                 {"type": "user", "text": "can you help me scale announcement component?"},
    #                 {"type": "bot", "text": "I'm waiting for the number of pods to scale the announcement component. Please provide the number of pods you want to scale it to."},
    #                 {"type": "user", "text": "4 pods"},
    #                 ]
    #
    # response, executed_tool  = get_bot_response(conversation)
    # print(response)
    # print(executed_tool)

    response = """Thought: I should respond with a friendly greeting.
Action: None
Action Input: None"""
    print(get_action_and_action_input(response))



