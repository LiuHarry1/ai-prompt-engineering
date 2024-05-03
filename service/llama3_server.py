from service.LLM_server import *
import requests

import certifi
print(certifi.where())

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class Llama3Server(LLM):
    def __init__(self):
        super().__init__("Llama3")

    def completion(self, prompt, history=""):
        resp = requests.post(
            url="http://127.0.0.1:8080/completion",
            # url="http://127.0.0.1:8080/chat/completion",
            # url="https://lgtcmtaspn1d.nam.nsroot.net:8088/completion",
            json={"prompt": prompt,
                  "temperature": 0.7,
                  "top_p": 0.5,
                  "top_k": 40,
                  "n_predict": 400
                  },
            # json={"prompt": prompt, "history": history},
            # data = '{"prompt": "Building a website can be done in 10 simple steps:","n_predict": 128}',
            headers={"Content-Type": "application/json;charset=utf-8"},
            # verify=False

        )
        print(resp.json())
        # print(resp.json()["content"])
        return resp.json()["content"]

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
    llama2Server = Llama3Server()
    print(llama2Server.name)
    result = Llama3Server().completion(prompt)
    print("---")
    print(result)
