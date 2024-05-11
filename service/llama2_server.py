from service.LLM_server import *
import requests
import util.logging_utils as logging_utils

logger = logging_utils.setup_logger('llama2_server')

import certifi
print(certifi.where())

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


requests.packages.urllib3.disable_warnings()

import time
class Llama2Server(LLM):
    def __init__(self):
        super().__init__("Llama2")

    def completion(self, prompt, temperature=0, top_p=0.5, top_k=5, n_predict=600, presence_penalty=0, frequency_penalty=0, history=""):
        start = time.time()
        session = requests.session()
        # fix 407 error while connecting llama3
        session.trust_env = False

        resp = session.post(
            url="http://127.0.0.1:9999/completion",
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
This is a conversation between User and Llama, a friendly chatbot. Llama is helpful, kind, honest, good at writing, and never fails to answer any requests immediately and with precision. 

User: hi you
Llama:"""
    llama2Server = Llama2Server()
    print(llama2Server.name)
    result = Llama2Server().completion(prompt)
    print("---")
    print(result)
