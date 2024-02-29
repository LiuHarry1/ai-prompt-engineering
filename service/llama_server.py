import requests

import certifi
print(certifi.where())

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def completion(prompt, history=""):
    return ""
    resp = requests.post(
        # url="http://lgtcmtaspn1d.nam.nsroot.net:9999/completion",
        url="https://lgtcmtaspn1d.nam.nsroot.net:8088/completion",
        json={"prompt": prompt,
              "temperature": 0.1,
              "top_p": 0.5,
               "top_k": 5,
              "n_predict": 600
              },
        # json={"prompt": prompt, "history": history},
        # data = '{"prompt": "Building a website can be done in 10 simple steps:","n_predict": 128}',
        headers={"Content-Type": "application/json;charset=utf-8"},
        verify=False

    )
    print(resp)
    print(resp.json()["content"])
    return resp.json()["content"]

if __name__ == '__main__':
    prompt = "hi you"
    result = completion(prompt)
    print(result)
