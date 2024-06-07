from service.LLM_server import *
import requests
import util.logging_utils as logging_utils

logger = logging_utils.setup_logger('llama3_server')

import certifi
print(certifi.where())

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


requests.packages.urllib3.disable_warnings()

import time
class Llama3Server(LLM):
    def __init__(self):
        super().__init__("Llama3")

    def completion(self, prompt, temperature=0, top_p=0.5, top_k=5, n_predict=600, presence_penalty=0, frequency_penalty=0, history=""):
        start = time.time()
        session = requests.session()
        # fix 407 error while connecting llama3
        session.trust_env = False

        resp = session.post(
            url="http://127.0.0.1:8080/completion",
            json={"prompt": prompt,
                  "temperature": float(temperature),
                  "top_p": float(top_p),
                  "top_k": int(top_k),
                  "n_predict": int(n_predict),
                   "presence_penalty": float(presence_penalty),
                  "frequency_penalty": float(frequency_penalty),
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
        print(content)

        return content

if __name__ == '__main__':
    # prompt = "please translate the following text into English, no notes and no explanation. text:'你很坏', result: "

#     prompt = """System: You are a helpful, respectful and honest assistant. Always answer as helpfully as possible.
# User: I want to use spring security in my web project , please provide me how to add it in my web project.
# Assistant:
#     """
    prompt = """
Tool Descriptions:

1. Calculator Tool: Performs basic arithmetic operations such as addition, subtraction, multiplication, and division. Parameters: Operation, Number 1, Number 2
2. Weather Tool: Provides current weather information and forecasts based on location input. Parameters: Location, Date
3. Translation Tool: Translates text from one language to another. Parameters: Source Language, Target Language, Text
4. Dictionary Tool: Provides definitions, synonyms, antonyms, and examples of word usage. Parameters: Word

User Query:

"What will the weather be like in New York tomorrow?"

Task:

Based on the user's query and the descriptions of the available tools, decide which tool is most suitable for addressing the query. If a suitable tool is found, also provide the necessary parameters. If none of the tools are appropriate for the query, output "NA".
the template of response would be [tool name:xxx, parameters:xxx] .
Response:
"""
    llama2Server = Llama3Server()
    print(llama2Server.name)
    result = Llama3Server().completion(prompt)
    print("---")
    print(result)
