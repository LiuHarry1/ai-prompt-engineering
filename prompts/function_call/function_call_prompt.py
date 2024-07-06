import util.logging_utils as logging_utils
from function_calling.tools import get_all_tool_descriptions

logger = logging_utils.setup_logger('jira_assistant_prompt')


prompt_template = """<|begin_of_text|><|start_header_id|>user<|end_header_id|>
You are a smart assistant capable of using various web REST APIs to answer questions. Before providing a response, always think through the following steps:

1. Understand the User's Query: Clearly understand what the user is asking.
2. Reason through Possible Tools: Think about which API tools you have and which one is best suited for the query.
3. Act: Call the appropriate API with the necessary parameters.
4. Respond: Provide the user with a clear and concise answer based on the API response.

Available API tools:
- Weather API: Provides current weather information.
- **News API**: Provides the latest news headlines.
- **Joke API**: Provides a random joke.
- **Stock API**: Provides the latest stock prices.

Here is an example to guide your reasoning and acting process:

User: "What's the weather like today?"
Thought: The user is asking about the weather. I should use the Weather API.
Action: Call Weather API.
Response: "The current weather is sunny with a temperature of 75°F."

User: "Tell me a joke."
Thought: The user wants to hear a joke. I should use the Joke API.
Action: Call Joke API.
Response: "Why don't scientists trust atoms? Because they make up everything!"

Follow this reasoning process for each user query.

---

User: [user_input]

Thought:

<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""

prompt_template2= """<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are an intelligent chatbot designed to assist users in managing various components using specific tools. 
You can also engage in general chat and answer questions. Here are the tools you can use:
{all_tool_descriptions}
When a user provides an input, understand their request, and if it pertains to any of the tools, 
prompt them for necessary details and execute the corresponding tool. 

if you want to execute a tool, only output in json format with below keys:
tool_name, inputs

If the input is a general chat or question, respond appropriately.
Keep the answer short and concise.

<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

def get_function_calling_template( prompt = prompt_template2):
    all_tool_descriptions = get_all_tool_descriptions()

    prompt = prompt.format(all_tool_descriptions = all_tool_descriptions)

    return prompt




def get_function_call_prompt(conversations, prompt = prompt_template2 ):
    prompt =  get_function_calling_template(prompt)

    try:
        conversation_prompt = ""
        if conversations:
            for message in conversations:
                message_type=  message['type']
                message_content = message['text']
                if message_type == 'bot':
                    conversation_prompt = conversation_prompt + f"""{message_content}<|eot_id|><|start_header_id|>user<|end_header_id|>"""
                if message_type == 'user':
                    conversation_prompt = conversation_prompt + f"""{message_content}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

            prompt = prompt+ conversation_prompt
            logger.info(conversation_prompt)
            return prompt.strip()
    except Exception as e:
        logger.exception(e)
        return None

    return prompt


