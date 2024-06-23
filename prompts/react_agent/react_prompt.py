import util.logging_utils as logging_utils

logger = logging_utils.setup_logger('draft_email_generating_prompt')

react_agent_prompt_template_1 = """
<|begin_of_text|><|start_header_id|>user<|end_header_id|>
You are an assistant to give people the answer of questions.
Human may provide new question to you with a description and you should use tools to get the answer, rather than directly reply from the description.

you have access to the following tools:
[{tool_name_and_description}]


user the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action

..(this Thought/Action/Action Input/Observation can repeat N times)

Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {question}
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""

react_prompt_test1= """<|begin_of_text|><|start_header_id|>user<|end_header_id|>
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible. Keep the answer short and concise.

only If the user demands answer but you are unsure, execute the thought/action/action input/observation sequence.

if you have required information on Observation, then provide final answer directly. No double-check required, No confirm required.

you have access to the following tools:
[{tool_name_and_description}]

To use a tool, please use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action

..(this Thought/Action/Action Input/Observation can repeat N times)

Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {question}
"""

react_prompt_test2= """<|begin_of_text|><|start_header_id|>user<|end_header_id|>
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible. Keep the answer short and concise.

only If the user demands answer but you are unsure, execute the thought/action/action input/observation sequence.

if you have required information on Observation, then provide final answer directly. No double-check required, No confirm required.

you have access to the following tools:
{tool_name_and_description}

before using those tool, if you want to request user to provide input data which you don't know. please don't output action and action input.

To use a tool, please use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of {tool_names}
Action Input: the input to the action
Observation: the result of the action

..(this Thought/Action/Action Input/Observation can repeat N times)

Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""

react_prompt_llama2= """
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible.

only If the user demands a final answer but you are unsure, execute the thought/action/action input/observation sequence .

if you have required information on Observation, then provide final answer directly. No double-check required, No confirm required.

you have access to the following tools:
[{tool_name_and_description}]

To use a tool, please use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
..(this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!
"""

react_agent_prompt_template = """
<|begin_of_text|><|start_header_id|>user<|end_header_id|>
Answer the following questions as best you can.

If the user demands a final answer but you are unsure, execute the thought/action/action input/observation sequence.
if you have required information on Observation, then provide final answer directly. No double-check required, No confirm required.

you have access to the following tools:
[{tool_name_and_description}]

To use a tool, please use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action

..(this Thought/Action/Action Input/Observation can repeat N times)

Thought: I now know the final answer
Final Answer: the final answer to the original input question.

Begin!

Question: {question}
"""

def get_inital_react_prompt(tool_name_and_description, tool_names, conversations,  prompt = react_prompt_test2):
    try:
        prompt = prompt.format(tool_name_and_description=tool_name_and_description,
                                                       tool_names=tool_names)

        conversation_prompt = ""
        if conversations:
            for index , message in enumerate(conversations):
                message_type = message['type']
                message_content = message['text']
                if message_type == 'bot':
                    conversation_prompt = conversation_prompt + f"""{message_content}<|eot_id|><|start_header_id|>user<|end_header_id|>"""
                if message_type == 'user':
                    if index == (len(conversations)-1):
                        conversation_prompt = conversation_prompt +  "\nQuestion: {question}\n".format(question = message_content)
                    else:
                        conversation_prompt = conversation_prompt + f"""{message_content}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

            prompt = prompt + conversation_prompt
            logger.info(conversation_prompt)
            return prompt.strip()
    except Exception as e:
        logger.exception(e)
        return None

    return prompt

def get_react_prompt_by_new_thought(prompt,  bot_response= ''):
    try:

        if bot_response and len(bot_response) !=0:
            prompt = prompt + bot_response
        prompt = prompt + "<|eot_id|><|start_header_id|>assistant<|end_header_id|>"

        return prompt.strip()
    except Exception as e:
        logger.exception(e)
        return None

    return prompt

def get_react_prompt(tool_name_and_description, tool_names, conversations, user_input,  prompt = react_prompt_test2):
    inital_prompt = get_inital_react_prompt(tool_name_and_description, tool_names,conversations,  user_input, prompt)
    prompt = get_react_prompt_by_new_thought(inital_prompt)
    return prompt