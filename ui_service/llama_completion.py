from flask import Blueprint, jsonify, request, jsonify, send_file
import os
import service.llama_server as llama

llama_completion = Blueprint("llama_completion", __name__)



@llama_completion.route('/llama/completion', methods=['POST'])
def completion():
    print("completion....")

    data = request.json

    if data is None:
        return jsonify({"message": "Invalid JSON data in the request body."}), 400

    prompt = data.get('prompt')
    if prompt:
        result_completion = llama.completion(prompt)
        return result_completion

    return ""


