from service.LLM_server import *
import requests
import util.logging_utils as logging_utils
import prompts.order_chatbot.order_chatbot_prompt as order_chatbot

logger = logging_utils.setup_logger('llama3_1_server')
from function_calling.tools import *

import certifi
print(certifi.where())

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


requests.packages.urllib3.disable_warnings()

import time
class Llama3_1Server(LLM):
    def __init__(self):
        super().__init__("Llama3_1")

    def completion(self, prompt, temperature=0, top_p=0.5, top_k=5, n_predict=600, presence_penalty=0, frequency_penalty=0, stop = ["<|eot_id|>", "Observation"], history=""):
        start = time.time()
        session = requests.session()
        # fix 407 error while connecting llama3
        session.trust_env = False

        try:
            resp = session.post(
                url="http://127.0.0.1:8080/completion",
                json={"prompt": prompt,
                      "temperature": float(temperature),
                      "top_p": float(top_p),
                      "top_k": int(top_k),
                      "n_predict": int(n_predict),
                      "presence_penalty": float(presence_penalty),
                      "frequency_penalty": float(frequency_penalty),
                      "stop": stop,
                      "history": history
                      },
                headers={"Content-Type": "application/json;charset=utf-8"},
                verify=False

            )
            print(resp)
            content = resp.json()["content"]
            if content:
                total_time = time.time() - start
                token_size = len(content)
                print(f'Total time: {total_time}, Token size: {token_size} Time per token : {total_time / token_size}')
            print("========Following is llama3 response =========")
            print(content)
            print("========End of Llama3 response =========")

            return content
        except Exception as e:
            logger.exception(e)
            return ""

import json
if __name__ == '__main__':

    user_question= "I am very sad";
    prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are an intelligent chatbot designed to assist users in managing various components using the following tools. 


Use the function  '{tools_new[0]["name"]}' to: '{tools_new[0]["description"]}',
'{tools_new[1]["name"]}' to: '{tools_new[1]["description"]}'
'{tools_new[2]["name"]}' to: '{tools_new[2]["description"]}'
 '{tools_new[3]["name"]}' to: '{tools_new[3]["description"]}'

{tools_new}

If a you choose to call a function ONLY reply in the following format:

<function=example_function_name>{{\"example_name\": \"example_value\"}}</function>

Reminder:
- Function calls MUST follow the specified format, start with <function= and end with </function>
- Required parameters MUST be specified
- Only call one function at a time
- Put the entire function call reply on one line

If the input is a general chat or question, respond appropriately.
Keep the answer short and concise.

don't output any function if required parameters are not specified.

<|eot_id|><|start_header_id|>user<|end_header_id|>

{user_question}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

"""
#     prompt = prompt + """
# <function=spotify_trending_songs>{"n": "5"}</function><|eom_id|><|start_header_id|>ipython<|end_header_id|>
# ["1. BIRDS OF A FEATHER by Billie Eilish", "2. Espresso by Sabrina Carpenter", "3. Please Please Please by Sabrina Carpenter", "4. Not Like Us by Kendrick Lamar", "5. Gata Only by FloyyMenor, Cris Mj"]<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

    print(prompt)
    # print(json.dumps(tools_new[0]))
    result = Llama3_1Server().completion(prompt)


    # print(result)
