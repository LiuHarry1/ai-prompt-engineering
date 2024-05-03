from flask import Blueprint, jsonify, request, jsonify, send_file
import os
from service import *

llama_completion = Blueprint("llama_completion", __name__)



@llama_completion.route('/llama/completion', methods=['POST'])
def completion():
    print("completion....")

    data = request.json

    if data is None:
        return jsonify({"message": "Invalid JSON data in the request body."}), 400

    prompt = data.get('prompt')
    llm_name = data.get('llm_name')
    print('llm name', llm_name)
    if prompt:
        result_completion = LLMFactory.create_llm(llm_name).completion(prompt)
        return jsonify({'completion': result_completion})

    return ""


