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

react_prompt_test1= """
<|begin_of_text|><|start_header_id|>user<|end_header_id|>
You are an assistant to give people the answer of questions.

only If the user demands a final answer but you are unsure, execute the thought/action/action input/observation sequence,
otherwise , you can answer it directly.


you have access to the following tools:
[Search: search the latest information you needs on the internet, Calculator: use it while calculating something ]


To use a tool, please use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [Search, Calculator]
Action Input: the input to the action
Observation: the result of the action
..(this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: Hi, how are you?
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""

react_agent_prompt_template = """
<|begin_of_text|><|start_header_id|>user<|end_header_id|>
Answer the following questions as best you can.

If the user demands a final answer but you are unsure, execute the thought/action/action input/observation sequence.

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
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""


def get_react_prompt(tool_name_and_description, tool_names,  question: ''):
    try:

        draft_email_promp = react_agent_prompt_template.format(tool_name_and_description = tool_name_and_description,
                                                               tool_names = tool_names,
                                                               question = question)

        return draft_email_promp.strip()
    except Exception as e:
        logger.exception(e)
        return None

    return None