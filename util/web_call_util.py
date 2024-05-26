import requests
import util.logging_utils as logging_utils
import time
logger = logging_utils.setup_logger('web_call_util')


import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

requests.packages.urllib3.disable_warnings()

def call(url, json_data, headers={"Content-Type": "application/json;charset=utf-8"}):
    start = time.time()
    session = requests.session()
    session.trust_env = False

    resp = session.post(
        url=url,
        json=json_data,
        headers=headers,
        verify=False

    )
    print(resp)
    return resp.json()